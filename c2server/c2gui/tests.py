from django.test import TestCase
from c2ext.c2_data import _get_pinors_from_xml, _update_db, create_xml_for_ext_c2
from c2gui.models import Pinor, SearchArea
import c2ext.schema as schema
from lxml import etree

# Create your tests here.


class C2DataTestCase(TestCase):
    def setUp(self):
        Pinor.objects.all().delete()

    def test_c2_ext(self):
        region = SearchArea.objects.all()
        self.assertTrue(region)
"""        try:
            xml = schema.parse("test_gpig_xml.xml", True)
        except etree.XMLSyntaxError as err:
            print("XMLSyntaxError {0}".format(err))
            self.assertFalse(True)

        pinors = _get_pinors_from_xml(xml)
        _update_db(pinors)
        xml_str = create_xml_for_ext_c2()
        with open('test_gpig_xml.xml', 'r') as myfile:
            orig = myfile.read()
            self.assertEqual(orig, xml_str)"""





