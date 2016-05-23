import simplejson
import socket
import struct

from .messages import DeployMesh

HOST = '144.32.178.57'
PORT = 5556

class Communicator:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))
        print("connected to environment")

    def send(self, message):
        encoded_message = simplejson.dumps(message.to_json()).encode('UTF-8')
        print(encoded_message)
        self.sock.send(struct.pack("!L", len(encoded_message)))
        self.sock.send(encoded_message)

    def close(self):
        self.sock.close()
