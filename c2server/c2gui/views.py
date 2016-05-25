from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .communicator import Communicator
from .utils import *
from .models import SearchArea, Event, Pinor, EventSerializer
from .map_settings import REG_WIDTH, REG_HEIGHT
from .tasks import send_search_area_coord
from .messages import DeployMesh, PinorMesh, MeshMessage, Message
from .point import Point, Space

from decimal import Decimal
import codecs
import simplejson
import json
import geopy
import geopy.distance
import datetime
import pytz

def index(request):
    events = Event.objects.all()
    print(events)
    return render(request, 'c2gui/index.html', {"event_list": events})

def send_search_coord(request):
    bottomleftlat = Decimal(request.POST['bottomleftlat'])
    bottomleftlon = Decimal(request.POST['bottomleftlon'])
    toprightlat = Decimal(request.POST['toprightlat'])
    toprightlon = Decimal(request.POST['toprightlon'])

    areasToSearch = SearchArea.objects.exclude(
        Q(lat__gt=toprightlat) | Q(lat__lt=bottomleftlat-REG_HEIGHT)
    ).exclude(Q(lon__gt=toprightlon) | Q(lon__lt=bottomleftlon-REG_WIDTH)
    )
    for sa in areasToSearch:
        sa.status = 'DD'
        sa.save()
    
    ids = list(areasToSearch.values('id'))
    coordinates = {"bottomleft": {"latitude": bottomleftlat, "longitude": bottomleftlon},
                   "topright": {"latitude": toprightlat, "longitude": toprightlon}
    }
    new_event = Event(event_type='IS', headline="Initiated search", text = "Iniated search for the area (%f N, %f W):(%f N, %f W)" % (bottomleftlat, -bottomleftlon, toprightlat, -toprightlon))
    new_event.save()
    bottomleft = Point(latitude=bottomleftlat, longitude=bottomleftlon, altitude=0)
    topright = Point(latitude=toprightlat, longitude=toprightlon, altitude=0)
    mes = DeployMesh("c2", "c2", Space(bottomleft, topright))
    c = Communicator()
    c.send(mes)
    #send_search_area_coord.delay(coordinates)
    return HttpResponse(simplejson.dumps({"ids": ids, "headline": new_event.headline, "text": new_event.text, "timestamp": {"year": new_event.timestamp.year,
                              "month": new_event.timestamp.month,
                              "day": new_event.timestamp.day,
                              "hour": new_event.timestamp.hour,
                              "minute": new_event.timestamp.minute,
                              "second": new_event.timestamp.second}
    }), content_type='application/json')

def get_all_regions_status(request):
    Event.objects.update(is_new=False)
    data = list(SearchArea.objects.values('id', 'status'))
    return HttpResponse(simplejson.dumps({"statuses": data}), content_type='application/json')

@csrf_exempt
def send_drone_data(request):
    unicode_message = request.body.decode("utf-8")
    print(unicode_message)
    json_message = json.loads(unicode_message)
    if json_message["data"]["datatype"] == "pinor":
        decoded_message = PinorMesh.from_json(json_message)
        for pinor in decoded_message.pinor:
            lat = Decimal(pinor.latitude)
            lon = Decimal(pinor.longitude)
            region = SearchArea.objects.filter(lat__lte=lat
                                      ).filter(lat__gte=lat-REG_HEIGHT
                                      ).filter(lon__gte=lon-REG_WIDTH
                                      ).filter(lon__lte=lon
                                      ).first()
            region.status = "RE"
            region.save()
            new_pinor = Pinor(lat=pinor.latitude, lon=pinor.longitude,
                              timestamp=datetime.datetime.utcfromtimestamp(decoded_message.timestamp).replace(tzinfo=pytz.utc), region=region)
            new_pinor.save()
            new_event = Event(event_type='POI', headline="Found a stranded person", text="Found a stranded person at %f N %f W" % (pinor.latitude, -pinor.longitude), pinor=new_pinor)
            new_event.save()
        print(decoded_message)

    return HttpResponse("received data")

def retrieve_new_events(request):
    new_events = Event.objects.filter(is_new=True)
    event_serializer = EventSerializer(new_events, many=True)
    new_event_list = event_serializer.data
    new_events.update(is_new=False)
    return HttpResponse(simplejson.dumps({"new_events": new_event_list}), content_type='application/json')
