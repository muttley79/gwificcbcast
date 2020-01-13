import socket
import struct
import sys
import pickle
from datetime import datetime

class ObjectToPass:
    data = None
    address = None
    target = None
    targetPort = None
    def __init__(self, data,address,target,targetPort):
        self.data = data
        self.address = address
        self.target = target
        self.targetPort = targetPort


def sendToFinalTarget(data,returnAddress,targetAddress,targetPort):
    print(str(datetime.now()) + ' Sending data to ', targetAddress, targetPort)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(data, (targetAddress, targetPort))


HOST = '0.0.0.0'
PORT = 4545

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print(str(datetime.now()) + ' Listening')
s.listen()
while True:
    s.listen()

    conn, addr = s.accept()
    print(str(datetime.now()) + ' Connected from', addr)

    data = conn.recv(4096)
    data_variable = pickle.loads(data)
    conn.close()
    #print(data_variable.data, data_variable.address, data_variable.target, data_variable.targetPort)
    # Access the information by doing data_variable.process_id or data_variable.task_id etc..,
    sendToFinalTarget(data_variable.data, data_variable.address, data_variable.target, data_variable.targetPort)
    print(str(datetime.now()) + ' Data received from client and forwarwded')
