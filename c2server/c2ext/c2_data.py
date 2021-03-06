import requests
import collections
import c2ext.schema as schema
from lxml import etree
from io import StringIO
from c2gui.models import Pinor
from c2gui.views import save_new_pinor
from decimal import Decimal
from io import BytesIO


def get_updates_from_ext_c2s(url, clear_table=False):
    """
    Queries all servers from in url_list for data, updates db with new information
    :param url: remote server
    :param clear_table: clear the pinor table before updating
    :return: list of new pinors
    """
    xml_bytes = _request_data(url)
    if not xml_bytes:
        return
    try:
        xml = schema.parse(BytesIO(xml_bytes), True)
    except etree.XMLSyntaxError as err:
        print("XMLSyntaxError from url " + url + " : {0}".format(err))
        return
    pinor_list = _get_pinors_from_xml(xml)
    if clear_table:
        Pinor.objects.all().delete()
    _update_db(pinor_list)
    return pinor_list


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
    :return: xml bytes
    """
    try:
        resp = requests.get(url)
    except requests.exceptions.InvalidSchema:
        return
    except requests.exceptions.ConnectionError:
        return
    if not resp.status_code == 200:
        print("received response " + resp.status_code + " from URL " + url)
        return

    return resp.content


def _get_pinors_from_xml(xml):
    pinor = collections.namedtuple("pinor", ["lat", "lon", "timestamp"])
    pinor_list = []
    for gis in xml.get_gisposition():
        if gis.get_value().get_extensiontype_() == "strandedPerson" \
                and gis.get_position().get_extensiontype_() == "point":
            time_stamp = gis.get_timestamp().get_date()
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
        date_time = schema.timestamp(pinor.get("timestamp"))
        gis = schema.gisPosition(point, date_time, schema.strandedPerson())
        root.add_gisposition(gis)
    return root


def _update_db(pinor_list):
    for pinor in pinor_list:
        save_new_pinor(pinor.lat, pinor.lon, pinor.timestamp)
