import sys
import socket 
import threading
import os
import re
import random
from itertools import repeat
sys.path.append(os.getcwd())
from comm import *

DEFAULT_RVOUS_PORT = 60000

# get the desired port number from command line args
def process_args():
    argc = len(sys.argv)
    argv = sys.argv
    if argc == 1:
        return DEFAULT_RVOUS_PORT
    if argc == 2:
        return int(argv[1])
    if argc > 2:
        raise TypeError("Malformed arguments")



# looking - the waiting index of the node for which we'd like to find peers
# active - the list of active nodes
# waiting - the list of waiting nodes
# n_wanted - the number of peers wanted for this node
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
    
    # now we've connected waiting peers
    # lets make up the difference with active peers

    return peers

def main():
    try:
        waiting = []
        active = []

        port = process_args()
        sock = get_udp_socket(port)

        while True:
            data = sock.recv(port)
            print("*** Received Peer Matching Request")
            recvd = extract_data(data)
            recvd.print_info()

            waiting.append(recvd)
            looking = len(waiting)-1 # index of newest waiting peer

            # select up to n peers from the active peer list to send to the client
            # or as many as we have
            print("*** Selecting Peers for this host")
            print(len(waiting)-1, "waiting peers to choose from")
            print(len(active), "active peers to choose from")
            peers = select_peers(looking=looking, active=active, waiting=waiting, n_wanted=5)
            print("Found", len(peers), "peers")
            for peer in peers:
                peer.print_info()
                
            if peers:
                print("Sending list to node")
                packet = construct_packet(peers=peers, npeers=len(peers))
                sock.sendto(packet, (recvd.hostname, recvd.port))
            
    except KeyboardInterrupt:
        sys.exit()
    else:
        sys.exit(0)

if __name__=="__main__":
    main()