import time
from io import StringIO

from c2gui.models import Pinor
from c2ext.schemaSubs import gpigDataSub, gisPositionSub, coordSub, timestampSub, strandedPersonSub, pointSub


def get_xml_string():
    """
    :return: xml data in string format
    """
    pinors = get_all_pinors()
    xml = create_xml(pinors)
    out = StringIO()
    xml.export(out, 0)
    xml_str = out.getvalue()
    return xml_str


def get_all_pinors():
    """
    :return: list of pinors
    """
    pinors = Pinor.objects.all()
    return pinors.values('lat', 'lon')


def create_xml(pinor_list):
    """
    :param pinor_list: list of pinors
    :return: xml object of pinors
    """
    root = gpigDataSub()
    for pinor in pinor_list:
        coord = coordSub(pinor.get("lat"), pinor.get("lon"))
        point = pointSub(coord)
        date_time = time.localtime(pinor.get("timestamp"))
        time_stamp = timestampSub(time.strftime('%Y-%m-%dT%H:%M:%S', date_time))
        gis = gisPositionSub(point, time_stamp, strandedPersonSub())
        root.add_gisposition(gis)
    return root

