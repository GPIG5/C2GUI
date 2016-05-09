from .communicator import Communicator
import asyncio

@asyncio.coroutine
def connect_and_send(host, data):
    c = Communicator.Communicator()
    yield from c.connect(host)
    print("connected")
    yield from c.send(data)
    print("sent")
