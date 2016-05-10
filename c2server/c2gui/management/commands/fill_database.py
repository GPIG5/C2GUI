from django.core.management.base import BaseCommand
from c2gui.models import SearchArea
from c2gui.map_settings import MIN_X, MIN_Z, MAX_X, MAX_Z, REG_NUM, REG_WIDTH, REG_HEIGHT

class Command(BaseCommand):
    help = 'Fills the database with initial data'

    def handle(self, *args, **options):
        counter = 0
        for i in range(0, REG_NUM):
            for j in range(0, REG_NUM):
                counter = counter + 1
                sa = SearchArea(id=counter, x_coord=MIN_X+(REG_WIDTH*j), z_coord=MIN_Z+(REG_HEIGHT*i), status='NE')
                sa.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully initialised the database.'))
