import time
import requests
import collections
import dateutil.parser
import c2ext.schema as schema
from lxml import etree
from io import StringIO
from c2gui.models import Pinor
from c2gui.views import save_new_pinor
from decimal import Decimal, getcontext


def get_updates_from_ext_c2s(url_list):
    """
    Queries all servers from in url_list for data, updates db with new information
    :param url_list: list of urls
    :return: nothing
    """
    for url in url_list:
        xml_str = _request_data(url)
        if not xml_str:
            continue
        try:
            xml = schema.parseString(xml_str, True)
        except etree.XMLSyntaxError as err:
            print("XMLSyntaxError from url " + url + " : {0}".format(err))
            return
        pinors = _get_pinors_from_xml(xml)
        _update_db(pinors)


def create_xml_for_ext_c2():
    """
    :return: xml data in string format
    """
    pinor_list = Pinor.objects.all().values("lat", "lon", "timestamp")
    xml = _create_xml(pinor_list)
    out = StringIO()
    xml.export(out, 0)
    xml_str = out.getvalue()
    return xml_str


def _request_data(url):
    """
    :param url: url of external c2 server
    :return: xml in string form
    """
    resp = requests.get(url)
    if not resp.status_code == 200:
        print("received response " + resp.status_code + "from URL " + url)
        return

    if not resp.headers == "application/xml":
        print("received incorrect header " + resp.headers + "from URL " + url)
        return

    return resp.text


def _get_pinors_from_xml(xml):
    pinor = collections.namedtuple("pinor", ["lat", "lon", "timestamp"])
    pinor_list = []
    for gis in xml.get_gisposition():
        if gis.get_value().get_extensiontype_() == "strandedPerson" \
                and gis.get_position().get_extensiontype_() == "point":
            time_stamp_iso = gis.get_timestamp()
            time_stamp = dateutil.parser.parser(time_stamp_iso)
            pinor_list.append(pinor(
                Decimal(gis.get_position().get_position().get_latitude()).quantize(Decimal("1.000000")),
                Decimal(gis.get_position().get_position().get_longitude()).quantize(Decimal("1.000000")), time_stamp))
    return pinor_list


def _create_xml(pinor_list):
    """
    :param pinor_list: list of dictionaries containing pinors
    :return: xml object of pinors
    """
    root = schema.gpigData()
    for pinor in pinor_list:
        coord = schema.coord(pinor.get("lat"), pinor.get("lon"))
        point = schema.point(coord)
        date_time = time.localtime(pinor.get("timestamp"))
        gis = schema.gisPosition(point, date_time, schema.strandedPerson())
        root.add_gisposition(gis)
    return root


def _update_db(pinor_list):
    for pinor in pinor_list:
        if not Pinor.objects.filter(lat=pinor.lat, lon=pinor.lon).exists():
            save_new_pinor(pinor.lat, pinor.lon, pinor.timestamp)
