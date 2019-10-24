class Peer():
    def __init__(self, topology="", hostname="", port=0):
        self.topology=topology
        self.hostname=hostname 
        self.port=port

    def print_info(self):
        print("NAT Topology: ", self.topology)
        print("IP Address  : ", self.hostname)
        print("Port Number : ", self.port)