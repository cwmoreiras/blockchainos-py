'''
programmer: Carlos Williams-Moreiras
Date: 10/23/2019
Description: Implements some networking utilities used 
  on both the p2p node, as well as the rendezvous server
'''

import socket
import re
from enum import Enum

DEFAULT_RVOUS_PORT = 60000
DEFAULT_SOURCE_PORT = 54320

'''
Description 
  All packets that go between peers or between a peer and the rendezvous server
  have a standard structure. The first byte in the packet indicates what type of 
  packet it is.
  RVOUS_MSG - a message from an rvous server to a peer
  PEER_MSG - a message from a peer to a peer
  CLIENT_MSG - a message from a peer to an rvous server
'''
class PacketType(Enum):
    INVALID = ''
    RVOUS_MSG = 'r'
    PEER_MSG = 'p'
    CLIENT_MSG = 'c'

'''
Description 
  Encapsulates attributes associated with peers on the network,
  including NAT topology, hostname and port
'''
class Peer():
    def __init__(self, topology="", hostname="", port=0):
        self.topology=topology
        self.hostname=hostname 
        self.port=port

    '''
    Func: encode the peer data as a string
    Args: None
    Retn: A string representing the peer's info
    '''
    def encode(self):
        return self.topology + ';' + self.hostname + ';' + str(self.port)

    '''
    Func: print the peer's info'
    Args: None
    Retn: None
    '''
    def print_info(self):
        print("NAT Topology: ", self.topology)
        print("IP Address  : ", self.hostname)
        print("Port Number : ", self.port)

'''
Func: Initializes a udp socket bound to a port on the local host
Args: source_port - the port at which to bind the socket
Retn: The bound udp socket
'''
def get_udp_socket(source_port=DEFAULT_SOURCE_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", source_port))
    return sock

'''
Func: Decodes a packet received from a host on this network
      Packet must have the specified structure
Args: packet - a packet to decode
Retn: A tuple containing the packet type, number of peers,
      and a list of peers
'''
def decode_packet(packet=None):  
    pack_split = re.split(';', packet.decode('utf-8'))
    pack_type = PacketType(pack_split[0]) # first is the packet type
    npeers = int(pack_split[1]) # next is the number of peers
    p_info = pack_split[2:3*npeers+2] # next is the list of peers
    
    peers = []
    for i in range(npeers): # construct the list of peers
        peers.append(Peer(p_info[i*3], p_info[i*3+1], int(p_info[i*3+2])))

    return pack_type,npeers,peers

'''
Func: Encodes a packet of the specified type
Args: pack_type - the type of packet
      peers - the list of peers 
      npeers - the number of peers in the list
Retn: the encoded packet in bytes
'''
def encode_packet(pack_type=PacketType.INVALID, peers=None, npeers=0):
    packet = str(pack_type.value) + ';'
    packet += str(npeers) 
    for peer in peers:
        packet += ";" + peer.encode()

    return bytes(packet, 'utf-8')