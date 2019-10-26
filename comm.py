import socket
import re
from enum import Enum

DEFAULT_RVOUS_PORT = 60000
DEFAULT_SOURCE_PORT = 54320

class PacketType(Enum):
    INVALID = ''
    RVOUS_MSG = 'r'
    PEER_MSG = 'p'
    CLIENT_MSG = 'c'

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

def get_udp_socket(source_port=DEFAULT_SOURCE_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", source_port))
    return sock

def decode_packet(packet=None):  
    pack_split = re.split(';', packet.decode('utf-8'))
    pack_type = PacketType(pack_split[0])
    npeers = int(pack_split[1])
    p_info = pack_split[2:3*npeers+2]
    
    peers = []
    for i in range(npeers):
        peers.append(Peer(p_info[i*3], p_info[i*3+1], int(p_info[i*3+2])))

    return pack_type,npeers,peers

def encode_packet(pack_type=PacketType.INVALID, peers=None, npeers=0):
    packet = str(pack_type.value) + ';'
    packet += str(npeers) 
    for peer in peers:
        packet += ";" + peer.encode()

    return bytes(packet, 'utf-8')