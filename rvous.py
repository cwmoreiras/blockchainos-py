import sys
import socket 
import threading
import peer

# get the desired port number from command line args
def process_args():
    argc = len(sys.argv)
    argv = sys.argv
    if argc > 2:
        raise TypeError("Malformed arguments")
    return int(argv[1])

def get_socket(port=60000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("localhost", port)
    print("Server starting at localhost:", port)
    sock.bind(server_address)
    return sock

def extract_data():
    pass

def main():
    try:
        print("hello world" )
        peer = []
        port = process_args()
        sock = get_socket(port)

        while True:
            data, address = sock.recvfrom(port)
            

    except KeyboardInterrupt:
        sys.exit()
    else:
        sys.exit(0)

if __name__=="__main__":
    main()