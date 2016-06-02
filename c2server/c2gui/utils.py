import base64
import os
import aiofiles

from .communicator import Communicator
from .models import Image

def decode_file(file_data, filename, path):
    file_bytes = bytes(file_data, "utf-8")
    file_contents = base64.b64decode(file_bytes)
    file_data = open(path + "/" + filename, mode="wb")
    file_data.write(file_contents)
    file_data.close()


def decode_file_dictionary(f_dict, root_path):
    if not os.path.isdir(root_path):
        os.makedirs(root_path)
    for i in f_dict:
        if type(f_dict[i]) is str:
            decode_file(f_dict[i], i, root_path)
        elif type(f_dict[i]) is dict:
            decode_file_dictionary(f_dict[i], root_path + "/" + i + "/")


def get_ext_c2_data():
    from c2ext.c2_data import get_updates_from_ext_c2s
    with open("ext_c2_addr.txt", "r") as file:
        urls = file.read().splitlines()
    for url in urls:
        get_updates_from_ext_c2s(url)

def readfiles(path):
    op = {}
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            fl = yield from aiofiles.open(os.path.join(path, f), mode='rb')
            try:
                contents = yield from fl.read()
            finally:
                yield from fl.close()
            op[f] = base64.b64encode(contents).decode('utf-8')
        else:
            op[f] = yield from readfiles(os.path.join(path, f))
    return op
