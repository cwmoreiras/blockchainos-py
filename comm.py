import socket
import re

DEFAULT_RVOUS_PORT = 60000
DEFAULT_SOURCE_PORT = 54320

class Peer():
    def __init__(self, topology="", hostname="", port=0):
        self.topology=topology
        self.hostname=hostname 
        self.port=port

    def encode(self):
        return self.topology + ';' + self.hostname + ';' + str(self.port)

    def print_info(self):
        print("NAT Topology: ", self.topology)
        print("IP Address  : ", self.hostname)
        print("Port Number : ", self.port)

def decode_rvous_msg(packet=None):
    peers = []
    npeers = int(re.split(';', packet.decode('utf-8'))[0])
    print("npeers: ", npeers)
    p_info = re.split(';', packet.decode('utf-8'))[1:3*npeers+1]
    
    for i in range(npeers):
        peers.append(Peer(p_info[i*3], p_info[i*3+1], p_info[i*3+2]))

    return npeers,peers

def get_udp_socket(source_port=DEFAULT_SOURCE_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", source_port))
    return sock

def extract_data(data=""):
    top,host,cport = re.split(';', data.decode())
    return Peer(topology=top, hostname=host, port=int(cport))

def construct_packet(peers=None, npeers=0):
    packet = str(npeers) 
    for peer in peers:
        packet += ";" + peer.encode()

    print("Packet: ", packet)
    return bytes(packet, 'utf-8')