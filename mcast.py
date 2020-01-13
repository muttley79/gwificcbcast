import socket
import struct
import sys
import pickle
from datetime import datetime

# This is the google wifi ip. Assuming port 4545 (tcp) is forwarded to the target device with mcast_server.py running
target_nat_host = ('192.168.9.230','4545')

# This is the target host and port for broadcast (found via wireshark)
mdns_multicast_group = '224.0.0.251'
mdns_server_address = ('', 5353)

# This is the ethernet Chromecast IP address
origin_address = '192.168.9.107'

print('Listening for brodcast messages to ' + mdns_multicast_group + ' port ' + str(mdns_server_address[1]))
print('Coming from ip address ' + origin_address)
print('Messages will be forwarded to client at address ' + target_nat_host[0] + ' port ' + target_nat_host[1])

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

# Create the socket
mdns_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(str(datetime.now())+ ' Started')

# Bind to the server address
mdns_sock.bind(mdns_server_address)
# Tell the operating system to add the socket to the multicast group
# on all interfaces.
mdns_group = socket.inet_aton(mdns_multicast_group)
mdns_mreq = struct.pack('4sL', mdns_group, socket.INADDR_ANY)
mdns_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mdns_mreq)

def sendDataToNat(data,address,target,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print('connecting to ', target_nat_host[0], int(target_nat_host[1]))
    s.connect((target_nat_host[0], int(target_nat_host[1])))
    obj = ObjectToPass(data,address,target,port)
    data_string = pickle.dumps(obj)
    s.send(data_string)
    s.close()

# Receive/respond loop
while True:
    try:
        mdns_data, mdns_address = mdns_sock.recvfrom(1024)
        if (mdns_address[0] == origin_address):
            mdns_sock.sendto('ack'.encode(), mdns_address)
            sendDataToNat(mdns_data,mdns_address,mdns_multicast_group,mdns_server_address[1])
            print(str(datetime.now()) + ' Message from broadcast received and forwarded')
    except(ConnectionRefusedError):
        print(str(datetime.now()) + ' Error: Connection refused')
    except(KeyboardInterrupt):
        sys.exit()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
