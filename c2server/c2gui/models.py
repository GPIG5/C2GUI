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
        ('IS', 'Initiated search'),
        ('POI', 'Found a point of interest'),
        ('CS', 'Completed search'),
    )

    event_type = models.CharField(max_length=3, choices=EVENT_TYPES)
    headline = models.CharField(max_length=25)
    text = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    pinor = models.ForeignKey('Pinor', on_delete=models.CASCADE, blank=True, null=True)
    # whether the events have been seen by the operator
    is_new = models.BooleanField(default=True)
    regions = models.ManyToManyField(SearchArea)

class Pinor(models.Model):
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    region = models.ForeignKey('SearchArea', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    origin = models.CharField(max_length=1, choices=(('M', 'My Team'), ('O', 'Other Team'), ), default='M')

    class Meta:
        unique_together = ('lat', 'lon')

class Drone(models.Model):
    uid = models.CharField(max_length=36, primary_key=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    last_communication = models.DateTimeField(auto_now=True)

class Image(models.Model):
    photo = models.ImageField(upload_to='drone-images')
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    pinor = models.ForeignKey('Pinor', on_delete=models.CASCADE, blank=True, null=True, related_name="images")

    class Meta:
        unique_together = ('lat', 'lon')

##### Custom Serializers #####
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchArea
        fields = ('pk', 'status', 'lat', 'lon')

class PinorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pinor
        fields = ('pk', 'lat', 'lon', 'timestamp', "images")
        depth = 1

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('event_type', 'headline', 'text', 'timestamp', 'pinor', 'regions')
        depth = 2

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ('uid', 'lat', 'lon')
