from django.core.management.base import BaseCommand
from c2gui.models import SearchArea
from c2gui.map_settings import MIN_LAT, MIN_LON, MAX_LAT, MAX_LON, REG_NUM_X, REG_NUM_Y, REG_WIDTH, REG_HEIGHT

class Command(BaseCommand):
    help = 'Fills the database with initial data'

    def handle(self, *args, **options):
        counter = 0
        for i in range(0, REG_NUM_Y):
            for j in range(0, REG_NUM_X):
                counter = counter + 1
                sa = SearchArea(id = counter, lat = MAX_LAT - (REG_HEIGHT*i), lon = MAX_LON - (REG_WIDTH*j), status='NE')
                sa.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully initialised the database.'))
