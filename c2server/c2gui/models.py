from __future__ import unicode_literals

from django.db import models

class SearchArea(models.Model):
    STATUS = (
        ('RE', 'Rescue Needed'),
        ('NRE', 'No Rescues Needed'),
        ('DD', 'Drones Dispatched'),
        ('NE', 'Not Explored'),
    )

    lat = models.DecimalField(max_digits=8, decimal_places=6, db_index=True)
    lon = models.DecimalField(max_digits=8, decimal_places=6, db_index=True)
    status = models.CharField(max_length=3, choices=STATUS)

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

class Pinor(models.Model):
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    
