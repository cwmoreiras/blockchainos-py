import sys
import socket 
import threading
import os

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
        peer = []
        port = process_args()
        sock = get_socket(port)

        while True:
            data, address = sock.recvfrom(port)
            print("*** Received Message")
            print("Client: ", address)
            

    except KeyboardInterrupt:
        sys.exit()
    else:
        sys.exit(0)

if __name__=="__main__":
    main()