'''
programmer: Carlos Williams-Moreiras
Date: 10/23/2019
Description: The RVOUS server maintains lists of peers on the network 
  and provides clients with a list of peers which it can try to connect
  to. 
'''

import sys
import socket 
import threading
import os
import re
import random
from itertools import repeat
import comm

DEFAULT_RVOUS_PORT = 60000 # default port for the rendezvous service

'''
Func: Process command line arguments
Args: None
Retn: The port for this service
'''
def process_args():
    argc = len(sys.argv)
    argv = sys.argv
    if argc == 1:
        return DEFAULT_RVOUS_PORT
    if argc == 2:
        return int(argv[1])
    if argc > 2:
        raise TypeError("Malformed arguments")


'''
Func: Find peers for the client from the lists of peers
Args: looking - the waiting index of the node for which we'd like to find peers
      active - the list of active nodes
      waiting - the list of waiting nodes
      n_wanted - the number of peers wanted for this node 
Retn: a list of peers for the client to connect to
'''
def select_peers(looking=0, active=None, waiting=None, n_wanted=5):
    peers = []

    # choose as many peers as we can from the waiting list
    # if there is only one waiting, thats the one thats searching
    if len(waiting) > 1:
        n = min(len(waiting)-1, n_wanted)
        for _ in range(n): 
            index = random.randrange(0, len(waiting))
            while index == looking: # make sure not to select the looking node
                index = random.randrange(0, len(waiting))
            print("Selected waiting node:", index)
            peers.append(waiting[index])

    # make up the difference with active peers
    if len(active) > 0:
        for _ in range(len(waiting), n_wanted):
            index = random.randrange(0, len(active))
            print("Selected active node:", index)
            peers.append(active[index])

    return peers

'''
Func: Server waits for requests and then responds with a list of peers
Args: None
Retn: None
'''
def main():
    try:
        waiting = []
        active = []

        port = process_args()

        print("Starting server at port", port)
        sock = comm.get_udp_socket(port)

        # server loop
        while True:
            pack_type,npeers,peers = comm.decode_packet(sock.recv(port))
            print("*******************************************")
            print("Received request")
            print("PacketType:", pack_type.name)
            print("npeers:    ", npeers)
            for peer in peers:
                peer.print_info()

            # this machine should only receive client packets
            if pack_type == comm.PacketType.CLIENT_MSG:
                client = peers[0]
                waiting.append(client)
                looking = len(waiting)-1 # index of newest client
                peers = select_peers(looking=looking, active=active, waiting=waiting, n_wanted=5)
                    
                for peer in peers:
                    peer.print_info()

                if peers:
                    packet = comm.encode_packet(pack_type=comm.PacketType.RVOUS_MSG, peers=peers, npeers=len(peers))
                    print("Sending peer list to", client.hostname)
                    sock.sendto(packet, (client.hostname, client.port))
                else:
                    print("No available peers for this client")
            else:
                print("Received invalid request")              
            
    except KeyboardInterrupt:
        sys.exit()
    else:
        sys.exit(0)

if __name__=="__main__":
    main()