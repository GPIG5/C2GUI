from django.contrib import admin

from .models import SearchArea, Event, Pinor, Drone, Image

admin.site.register(SearchArea)
admin.site.register(Event)
admin.site.register(Pinor)
admin.site.register(Image)

class DroneAdmin(admin.ModelAdmin):
    fields = ('uid', 'lat', 'lon', 'last_communication')
    readonly_fields = ('last_communication',)

admin.site.register(Drone, DroneAdmin)
