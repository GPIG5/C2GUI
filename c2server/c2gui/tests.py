import c2ext.schema as schema
from django.test import TestCase, Client
from c2ext.c2_data import _get_pinors_from_xml, _update_db, create_xml_for_ext_c2, get_updates_from_ext_c2s
from c2gui.models import Pinor, SearchArea
from lxml import etree

# Create your tests here.


class C2DataTestCase(TestCase):
    def setUp(self):
        Pinor.objects.all().delete()
        # db needs to be populated
        region = SearchArea.objects.all()
        self.assertTrue(region)

    def test_ext_c2_comms(self):
        # read in test data
        try:
            xml = schema.parse("test_gpig_xml.xml", True)
        except etree.XMLSyntaxError as err:
            print("XMLSyntaxError {0}".format(err))
            self.assertFalse(True)
        # update db
        pinors = _get_pinors_from_xml(xml)
        _update_db(pinors)

        # check output is the same as input
        xml_str = create_xml_for_ext_c2()
        with open("test_gpig_xml_out.xml", "w") as myfile:
            myfile.write(xml_str)
        with open("test_gpig_xml.xml", "r") as myfile:
            orig = myfile.read()
            self.assertEqual(orig, xml_str)

        # test requesting data by requesting from ourselves
        c = Client()
        resp = c.get("/c2gui/send_c2_data")

        if not resp.status_code == 200:
            print("received response " + resp.status_code)
            self.assertFalse(True)

        xml_str = resp.content.decode("utf-8")
        if not xml_str:
            return
        try:
            xml = schema.parseString(xml_str, True)
        except etree.XMLSyntaxError as err:
            print("XMLSyntaxError {0}".format(err))
            return
        pinors = _get_pinors_from_xml(xml)

        Pinor.objects.all().delete()
        _update_db(pinors)

        # check output is the same as input
        xml_str = create_xml_for_ext_c2()
        with open("test_gpig_xml_out.xml", "w") as myfile:
            myfile.write(xml_str)
        with open("test_gpig_xml.xml", "r") as myfile:
            orig = myfile.read()
            self.assertEqual(orig, xml_str)
