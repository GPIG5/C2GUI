from __future__ import unicode_literals

from django.db import models
from rest_framework import serializers

class SearchArea(models.Model):
    STATUS_TYPES = (
        ('RE', 'Rescue Needed'),
        ('NRE', 'No Rescues Needed'),
        ('DD', 'Drones Dispatched'),
        ('NE', 'Not Explored'),
    )

    lat = models.DecimalField(max_digits=8, decimal_places=6, db_index=True)
    lon = models.DecimalField(max_digits=8, decimal_places=6, db_index=True)
    status = models.CharField(max_length=3, choices=STATUS_TYPES)

class Event(models.Model):
    EVENT_TYPES = (
        ('ST', 'Started the server'),
        ('IS', 'Initiated search'),
        ('POI', 'Found a point of interest'),
    )

    event_type = models.CharField(max_length=3, choices=EVENT_TYPES)
    headline = models.CharField(max_length=25)
    text = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    pinor = models.ForeignKey('Pinor', on_delete=models.CASCADE, blank=True, null=True)
    # whether the events have been seen by the operator
    is_new = models.BooleanField(default=True)

class Pinor(models.Model):
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    region = models.ForeignKey('SearchArea', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ('lat', 'lon',)

class Drone(models.Model):
    uid = models.CharField(max_length=36, primary_key=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    last_communication = models.DateTimeField(auto_now=True)

##### Custom Serializers #####

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchArea
        fields = ('pk', 'status', 'lat', 'lon')

class PinorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pinor
        fields = ('pk', 'lat', 'lon', 'region')
        depth = 1

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('event_type', 'headline', 'text', 'timestamp', 'pinor')
        depth = 2

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ('uid', 'lat', 'lon')
