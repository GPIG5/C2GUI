from django.core.management.base import BaseCommand
from c2gui.views import save_new_pinor


class Command(BaseCommand):
    help = 'Fills the database with initial data'

    def handle(self, *args, **options):
        from c2ext.c2_data import _get_pinors_from_xml, _update_db
        import c2ext.schema as schema
        xml = schema.parse("test_gpig_xml.xml", True)
        pinors = _get_pinors_from_xml(xml)
        for pinor in pinors:
            save_new_pinor(pinor.lat, pinor.lon, pinor.timestamp)
        self.stdout.write(self.style.SUCCESS('Successfully initialised the database.'))