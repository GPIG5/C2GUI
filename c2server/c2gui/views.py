import base64
import binascii
import io
import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseRedirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.urlresolvers import reverse

from . import utils
from .communicator import Communicator
from .utils import *
from .models import SearchArea, Event, Pinor, Drone, Image, EventSerializer, DroneSerializer, PinorSerializer, RegionSerializer
from .map_settings import REG_WIDTH, REG_HEIGHT
from .messages import DeployMesh, PinorMesh, MeshMessage, Message, StatusMesh, CompleteMesh, UploadDirect
from .point import Point, Space

from decimal import *
import codecs
import simplejson
import json
import geopy
import geopy.distance
import logging
import datetime
import pytz
import tarfile
logging.basicConfig(filename='access.log', level=logging.DEBUG)

def index(request):
    events = Event.objects.all()
    return render(request, 'c2gui/index.html', {"event_list": events})

def send_search_coord(request):
    bottomleftlat = Decimal(request.POST['bottomleftlat'])
    bottomleftlon = Decimal(request.POST['bottomleftlon'])
    toprightlat = Decimal(request.POST['toprightlat'])
    toprightlon = Decimal(request.POST['toprightlon'])

    areasToSearch = SearchArea.objects.exclude(
        Q(lat__gt=toprightlat) | Q(lat__lt=bottomleftlat - REG_HEIGHT)
    ).exclude(Q(lon__gt=toprightlon) | Q(lon__lt=bottomleftlon - REG_WIDTH)
              )
    for sa in areasToSearch:
        sa.status = 'DD'
        sa.save()

    region_serializer = RegionSerializer(areasToSearch, many=True)
    coordinates = {"bottomleft": {"latitude": bottomleftlat, "longitude": bottomleftlon},
                   "topright": {"latitude": toprightlat, "longitude": toprightlon}
                   }
    new_event = Event(event_type='IS', headline="Initiated search",
                      text="Iniated search for the area (%f N, %f W):(%f N, %f W)" % (
                      bottomleftlat, -bottomleftlon, toprightlat, -toprightlon), is_new=False)
    new_event.save()
    new_event.regions.add(*list(areasToSearch))
    bottomleft = Point(latitude=bottomleftlat, longitude=bottomleftlon, altitude=0)
    topright = Point(latitude=toprightlat, longitude=toprightlon, altitude=0)
    mes = DeployMesh("c2", "c2", Space(bottomleft, topright))
    c = Communicator()
    c.send(mes)
    return HttpResponse(simplejson.dumps({"regions": region_serializer.data, "headline": new_event.headline, "text": new_event.text,
                                          "timestamp": {"year": new_event.timestamp.year,
                                                        "month": new_event.timestamp.month,
                                                        "day": new_event.timestamp.day,
                                                        "hour": new_event.timestamp.hour,
                                                        "minute": new_event.timestamp.minute,
                                                        "second": new_event.timestamp.second}
                                          }), content_type='application/json')

def get_all_regions_status(request):
    Event.objects.update(is_new=False)
    data = list(SearchArea.objects.values('id', 'status', 'lat', 'lon'))
    pinors = Pinor.objects.all()
    pinor_serializer = PinorSerializer(pinors, many=True)
   
    return HttpResponse(simplejson.dumps({"statuses": data, "pinors": pinor_serializer.data, "width": REG_WIDTH, "height": REG_HEIGHT}), content_type='application/json')

@csrf_exempt
def send_drone_data(request):
    unicode_message = request.body.decode("utf-8")
    # print(unicode_message)
    json_message = json.loads(unicode_message)
    #logging.debug(json_message)
    if json_message["data"]["datatype"] == "pinor":
        decoded_message = PinorMesh.from_json(json_message)
        for pinor in decoded_message.pinor:
            getcontext().prec = 6
            lat = Decimal(pinor.latitude) + Decimal(0)
            lon = Decimal(pinor.longitude) + Decimal(0)
            time_stamp = datetime.datetime.utcfromtimestamp(decoded_message.timestamp).replace(tzinfo=pytz.utc)
            save_new_pinor(lat, lon, time_stamp)
    elif json_message["data"]["datatype"] == "status":
        decoded_message = StatusMesh.from_json(json_message)
        drone, created = Drone.objects.update_or_create(uid=decoded_message.uuid,
                                                        defaults={"lat": decoded_message.location.latitude,
                                                                  "lon": decoded_message.location.longitude})
    elif json_message["data"]["datatype"] == "complete":
        decoded_message = CompleteMesh.from_json(json_message)
        bottomleftlat = Decimal(decoded_message.space.bottom_left["lat"])
        bottomleftlon = Decimal(decoded_message.space.bottom_left["lon"])
        toprightlat = Decimal(decoded_message.space.top_right["lat"])
        toprightlon = Decimal(decoded_message.space.top_right["lon"])
        areasComplete = SearchArea.objects.exclude(
            Q(lat__gt=toprightlat) | Q(lat__lt=bottomleftlat - REG_HEIGHT)
        ).exclude(Q(lon__gt=toprightlon) | Q(lon__lt=bottomleftlon - REG_WIDTH)
                  )
        areasComplete.update(status='NRE')
        new_event = Event(event_type='CS', headline="Completed search",
                          text="Completed search at the area (%f N, %f W):(%f N, %f W)" % (
                          bottomleftlat, -bottomleftlon, toprightlat, -toprightlon,))
        new_event.save()
        new_event.regions.add(*list(areasComplete))

    elif json_message["data"]["datatype"] == "upload":
        decoded_message = UploadDirect.from_json(json_message)
        uuid = decoded_message.uuid
        #logging.debug(decoded_message.images)
        utils.decode_file_dictionary(decoded_message.images, "/tmp/" + uuid + "/")
        with open('/tmp/' + uuid + '/locations.csv') as csvfile:
            location_reader = csv.DictReader(csvfile)
            for row in location_reader:
                getcontext().prec = 6
                lat = Decimal(row["lat"]) + Decimal(0)
                lon = Decimal(row["lon"]) + Decimal(0)
                obj, created = Image.objects.get_or_create(lat=lat, lon=lon, defaults={"photo": "/tmp/images/" + row["img"]}) 
                obj.save()

        with open('/tmp/' + uuid + '/pinor.csv') as csvfile:
            pinor_reader = csv.DictReader(csvfile)
            for row in pinor_reader:
                lat = Decimal(row["lat"]) + Decimal(0)
                lon = Decimal(row["lon"]) + Decimal(0)
                img = Image.objects.get(lat=lat, lon=lon)
                pinor = Pinor.objects.get(lat=lat, lon=lon)
                img.pinor = pinor
                img.save()

    return HttpResponse("received data")


def save_new_pinor(lat, lon, timestamp):
    region = SearchArea.objects.filter(lat__lte=lat)\
        .filter(lat__gte=lat - REG_HEIGHT)\
        .filter(lon__gte=lon - REG_WIDTH)\
        .filter(lon__lte=lon)\
        .first()

    if not region:
        return

    region.status = "RE"

    new_pinor, created = Pinor.objects.get_or_create(lat=lat, lon=lon, defaults={"region": region,
                                                                                 "timestamp": timestamp})
    if created:
        region.save()
        new_pinor.save()
        new_event = Event(event_type='POI', headline="Found a stranded person",
                      text="Found a stranded person at %f N %f W" % (lat, -lon),
                      pinor=new_pinor)
        new_event.save()

def retrieve_new_data(request):
    new_events = Event.objects.filter(is_new=True)
    event_serializer = EventSerializer(new_events, many=True)
    new_event_list = event_serializer.data
    new_events.update(is_new=False)

    # remove old drones from the database
    min_date = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(minutes=15)
    old_drones = Drone.objects.exclude(last_communication__range=[min_date, datetime.datetime.now(tz=pytz.utc)])
    old_drones.delete()
    drones_list = []
    return HttpResponse(simplejson.dumps({"new_events": new_event_list, "drones": drones_list, "height": REG_HEIGHT, "width": REG_WIDTH}), content_type='application/json')

def send_c2_data(request):
    from c2ext.c2_data import create_xml_for_ext_c2
    print("received c2 data request")
    data_str = create_xml_for_ext_c2()

    if not data_str:
        print("error in creating xml")
        return HttpResponseServerError()
    else:
        print("sent xml data")
        return HttpResponse(data_str, content_type='application/xml')

def clear_data(request):
    Image.objects.all().delete()
    Event.objects.all().delete()
    Pinor.objects.all().delete()
    SearchArea.objects.all().update(status='NE')
    events = Event.objects.all()
    return HttpResponseRedirect("/c2gui/")

def get_ext_c2_data(request):
    from c2ext.c2_data import get_updates_from_ext_c2s
    with open("ext_c2_addr.txt", "r") as file:
        urls = file.read().splitlines()
    pinor_list = []
    for url in urls:
        pinors = get_updates_from_ext_c2s(url)
        if pinors:
            pinor_list += pinors
    return HttpResponse(pinor_list)

def test_data_fill(request):
    from c2ext.c2_data import _get_pinors_from_xml, _update_db
    import c2ext.schema as schema
    xml = schema.parse("test_gpig_xml.xml", True)
    pinors = _get_pinors_from_xml(xml)
    _update_db(pinors)
    return HttpResponse("ok")

