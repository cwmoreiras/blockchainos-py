import sys
import socket 
import threading
import os
import re

DEFAULT_PORT = 60000

class Peer():
    def __init__(self, topology="", hostname="", port=0):
        self.topology=topology
        self.hostname=hostname 
        self.port=port

    def print_info(self):
        print("NAT Topology: ", self.topology)
        print("IP Address  : ", self.hostname)
        print("Port Number : ", self.port)

# get the desired port number from command line args
def process_args():
    argc = len(sys.argv)
    argv = sys.argv
    if argc == 1:
        return DEFAULT_PORT
    if argc == 2:
        return int(argv[1])
    if argc > 2:
        raise TypeError("Malformed arguments")
    

def get_socket(port=60000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("", port)
    print("Server starting at localhost:", port)
    sock.bind(server_address)
    return sock

def extract_data():
    pass

def main():
    try:
        waiting_peer = []
        inactive_peer = []

        port = process_args()
        sock = get_socket(port)

        while True:
            data = sock.recv(port)
            print("*** Received Message")
            top,host,cport = re.split(':', data.decode())
            recvd_peer = Peer(topology=top, hostname=host, port=int(cport))
            recvd_peer.print_info()
            waiting_peer.append(recvd_peer)

    except KeyboardInterrupt:
        sys.exit()
    else:
        sys.exit(0)

if __name__=="__main__":
    main()