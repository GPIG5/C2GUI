import time

from c2gui.models import Pinor
from c2ext.schemaSubs import gpigDataSub, gisPositionSub, coordSub, timestampSub, strandedPersonSub


def send_xml_data():
    """
    Responds to request for data
    :return: nothing
    """
    pinors = get_all_pinors()
    xml = create_xml(pinors)
    return


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
        date_time = time.localtime(pinor.get("timestamp"))
        time_stamp = timestampSub(time.strftime('%Y-%m-%dT%H:%M:%S', date_time))
        gis = gisPositionSub(coord, time_stamp, strandedPersonSub())
        root.add_gisposition(gis)
    return root

