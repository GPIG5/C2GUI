from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .communicator import Communicator
from .utils import *
from .models import SearchArea, Event, Pinor
from .map_settings import REG_WIDTH, REG_HEIGHT
from .tasks import send_search_area_coord
from .messages import DeployMesh, PinorMesh
from .point import Point, Space

from decimal import Decimal
import simplejson
import geopy
import geopy.distance

def index(request):
    events = Event.objects.all()
    print(events)
    return render(request, 'c2gui/index.html', {"event_list": events})

def send_search_coord(request):
    bottomleftlat = Decimal(request.POST['bottomleftlat'])
    bottomleftlon = Decimal(request.POST['bottomleftlon'])
    toprightlat = Decimal(request.POST['toprightlat'])
    toprightlon = Decimal(request.POST['toprightlon'])
    print("started the search in the database")
    areasToSearch = SearchArea.objects.exclude(
        Q(lat__gt=toprightlat+REG_HEIGHT) | Q(lat__lt=bottomleftlat-REG_HEIGHT)
    ).exclude(Q(lon__gt=toprightlon+REG_WIDTH) | Q(lon__lt=bottomleftlon-REG_WIDTH)
    )
    for sa in areasToSearch:
        sa.status = 'DD'
        sa.save()
    print("finished saving areas")
    
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
    send_search_area_coord.delay(coordinates)
    return HttpResponse(simplejson.dumps({"ids": ids, "headline": new_event.headline, "text": new_event.text, "timestamp": {"year": new_event.timestamp.year,
                              "month": new_event.timestamp.month,
                              "day": new_event.timestamp.day,
                              "hour": new_event.timestamp.hour,
                              "minute": new_event.timestamp.minute}
    }), content_type='application/json')

def get_all_regions_status(request):
    data = list(SearchArea.objects.values('id', 'status'))
    return HttpResponse(simplejson.dumps({"statuses": data}), content_type='application/json')

@csrf_exempt
def send_drone_data(request):
    print(request.body)
    #rec_message = request.POST["message"]
    #datatype = rec_message["data"]["datatype"]
    #if datatype == "pinor":
    #    decoded_message = PinorMesh.from_json(rec_message)
    #    for pinor in decoded_message.pinor:
    #        new_pinor = Pinor(lat=pinor.latitude, lon=pinor.longitude)
    #        new_pinor.save()
    #    print(decoded_message)

    return HttpResponse("received data")
