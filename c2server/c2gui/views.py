from django.shortcuts import render
from django.http import HttpResponse
from .communicator import Communicator
from .utils import *
import asyncio

def index(request):
    return render(request, 'c2gui/index.html', {})

def send_search_coord(request):
    topleftx = request.POST['topleftx']
    toplefty = request.POST['toplefty']
    width = request.POST['width']
    height = request.POST['height']
    c = Communicator.Communicator()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_and_send())
    return HttpResponse("submitted")
