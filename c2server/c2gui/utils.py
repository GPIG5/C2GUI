import base64
import os

from .communicator import Communicator
import asyncio


@asyncio.coroutine
def connect_and_send(host, data):
    c = Communicator.Communicator()
    yield from c.connect(host)
    print("connected")
    yield from c.send(data)
    print("sent")


def decode_file(file_data, filename, path):
    file_bytes = bytes(file_data, "utf-8")
    file_contents = base64.b64decode(file_bytes)
    file_data = open(path + filename, mode="wb")
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
