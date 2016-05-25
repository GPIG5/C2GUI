from c2gui.models import Pinor

def


def get_all_pinors():
    """
    :return: list of pinors
    """
    pinors = Pinor.objects.all()
    return pinors.values('lat', 'lon')


def create_xml(pinor_list):
    """
    :param pinor_list: list of pinors
    :return: nothing
    """
    return

