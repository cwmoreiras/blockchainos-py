'''
programmer: Carlos Williams-Moreiras
Date: 10/23/2019
Description: This is a python port of the blockchain's data structure 
  from the github project I maintain at www.github.com/cwmoreiras/blockchainos
  If you like it, please contribute to the project with a pull request!
  TODO switch from lower level python sockets to WebSockets
'''
import pynat
import sys
import time
import struct
import hashlib
import socket
import os
sys.path.append(os.getcwd()) # TODO this is a hack
import comm
from multiprocessing.dummy import Pool as ThreadPool

'''
Description
  Definition of _Block, an implementation of a Blockchain block. This class can
  be used to store the data necessary for creation of a block. Only the blockchain
  should be interacting directly with objects of this class. 
  prevhash - the hash of the previous block
  hash - the current block's hash
  index - the index of this block
  timestamp - the timestamp (seconds since the epoch)
  record - a string given by the caller

'''
class _Block:
    prevhash = None  # the hash of the previous block
    hash = None      # the current block's hash
    index = None     # the index of this block
    timestamp = None # the timestamp (seconds since the epoch)
    record = None    # a string given by the caller

    '''
    Func: Constructs a block object from a string record. The chain handles 
          all the hashing and indexing. The end user will interact with the 
          chain as a whole, not individual blocks
    Args: prevhash - the hash of the previous block
          index - the index of this block
          record - a string record provided by the caller
    Retn: None
    '''
    def __init__(self, prevhash=None, index=None, record=None):
        if prevhash is None:
            raise TypeError
        if index is None:
            raise TypeError
        if record is None:
            raise TypeError

        self.prevhash = prevhash
        self.index = index
        self.record = record
        self.timestamp = int(time.time())

        self.hash = self.sha_hash()

    '''
    Func: Calculates the block hash
          TODO modify the hash algorithm so that the whole record 
          is beign hashed, along with the other data, not just adding 
          them up
    Args: None
    Retn: None
    '''
    # TODO need a more secure way of hashing
    # returns the hash so that we can test it from Blockchain object
    def sha_hash(self):
        r = list(self.record)
        r = sum(ord(c) for c in r)

        if self.index == 0: # the root block TODO
            ph = self.prevhash
        else:
            ph = int(self.prevhash.hexdigest(), 16)
            ph &= 0x7FFFFFFF # make it 4 bytes

        return hashlib.sha256(struct.pack("I", r + ph + self.index + self.timestamp))

'''
 Description
  Definition of the Blockchain, which uses a list to append blocks 
  as pushed by the caller
'''
class Blockchain:
    '''
    Func: Constructs the root block and adds it to the chain
    Args: None
    Retn: None
    '''
    def __init__(self):
        self.bc = []
        # root record is hardcoded
        record = "first record"
        self.bc.append(_Block(prevhash=0, index=0, record=record))

    # TODO
    # The longest chain replaces all other blockchains
    # once these are on the network
    def _blockchain_replace(self, new):
        raise NotImplementedError
    
    # return the most recent addition to the chain
    def peek(self):
        return self.bc[-1]
    
    # insert a new block at the end of the chain
    def append(self, record=None):
        if record is None:
            raise TypeError
        lastblock = self.bc[-1] # get the last block
        
        prevhash = lastblock.hash
        index = lastblock.index+1
        
        self.bc.append(_Block(prevhash=prevhash, index=index, record=record))
    
    '''
    Func: Verify a new block by checking its index, its hash, whether the 
          previous hash is correct, as well as all the data types. The most
          important feature of the chain is that a block contain the hash of the 
          previous block. This keeps the chain verifiable
          TODO instead of printing this all out here, use a debug mode
    Args: new_block - the block that is actually being verified
          old_block - the previous block.
    Retn: None
    '''
    def verify_block(self, new_block=None, old_block=None):
        if new_block is None:
            raise TypeError
        if old_block is None:
            raise TypeError

        rc = 0

        if old_block.index+1 != new_block.index:
            print("Block Verification Error 0: bad indices")
            rc = -1
        if old_block.hash != new_block.prevhash:
            print("Block Verification Error 1: stored hashes do not match")
            rc = -1
        if new_block.sha_hash().hexdigest() != new_block.hash.hexdigest():
            print("Block Verification Error 2: calculated hashes do not match")
            rc = -1
        if len(new_block.prevhash.hexdigest()) != 64: # TODO dont hardcode number
            print("Block Verification Error 3: malformed prevhash in new block")
            rc = -1
        if len(new_block.hash.hexdigest()) != 64:
            print("Block Verification Error 4: malformed hash in new block")
            rc = -1
        if type(new_block.index) != int:
            print("Block Verification Error 5: malformed index in new block")
            rc = -1
        if type(new_block.timestamp) != int:
            print("Block Verification Error 6: malformed timestamp in new block")
            rc = -1

        if rc is 0:
            print("Block Verification: Passed all tests")

        return rc

    '''
    Func: Validate the entire blockchain, by going through the whole thing and
          making sure each block hash points to the next block
    Args: None
    Retn: 0 if no errors, else -1
    '''
    def verify_chain(self):
        # TODO make blockchain iterable
        for i in range(len(self.bc), 0): # loop backwards
            print("test: " + i)
            new_block = self.bc[i]
            old_block = self.bc[i-1]
            if not self.verify_block(old_block=old_block, new_block=new_block):
                print("Blockchain Verification: Test failed")
                return 0
        print("Blockchain Verification: Passed all tests")
        return -1

'''
Func: parse command line arguments
      TODO use ArgumentParser
Args: None
Retn: None
'''
def parse_args():
    argc = len(sys.argv)
    argv = sys.argv 

    # TODO help menu for the user
    if argc == 1:
        raise TypeError("Malformed args: need RVOUS server hostname and source port")
    elif argc == 2:
        if argv[1] == "-h" or argv[1] == "--help":
            raise NotImplementedError("help flag")
        else:
            return argv[1].strip(),comm.DEFAULT_SOURCE_PORT

    elif argc == 3:
        return argv[1].strip(),int(argv[2].strip())
            
'''
Func: Creates a blockchain with two blocks, just as a minimal test
Args: None
Retn: The test blockchain
'''
def create_test_chain():
    print("Constructing blockchain")
    bc = Blockchain()

    print("Getting root hash")
    root_block = bc.peek()
    print(root_block.hash.hexdigest())

    print("Inserting new record")
    bc.append(record="hello world")
    print("Getting most recent hash")
    new_block = bc.peek()
    print(new_block.hash.hexdigest())

    bc.verify_block(old_block=root_block, new_block=new_block)
    bc.verify_chain()

    return bc

'''
Func: Use the PyNat package to find out the public IP of this host
Args: source_port: the port we're going to use for p2p communications
Retn: A tuple containing NAT type, external IP, and external port
      in that order
'''
def get_host_info(source_port=comm.DEFAULT_SOURCE_PORT):
    print("Running STUN test")
    return pynat.get_ip_info(source_port=source_port) # arbitrary public stun server


def udp_handshake(sock=0, node=None, peers=None, npeers=0):
    # TODO
    # udp handshake to verify addresses

    # once the handshake is complete, register this address as a known peer
    pass

'''
Func: Create a test blockchain, get the external IP address of this host,
      TODO connect to a remote host, address provided by rendezvous server
Args: argv[1] - the hostname of the rendezvous server
      arvg[2] - the port on which to attempt to connect
Retn: None
'''
def main():
    try:
        peer = []
        rvous_host,source_port = parse_args()
        print("RVOUS host: ", rvous_host)
        print("RVOUS port: ", comm.DEFAULT_RVOUS_PORT)
        print("source port: ", source_port)

        chain = create_test_chain()
        nat_top, extern_ip, extern_port = get_host_info(source_port=source_port) # why does this take so long?
        this_node = comm.Peer(nat_top, extern_ip, extern_port) # construct a peer object
        this_node.print_info()

        sock = comm.get_udp_socket(source_port=source_port) # construct a bound socket

        packet = comm.encode_packet(pack_type=comm.PacketType.CLIENT_MSG, peers=[this_node], npeers=1)

        # store the network data in Peer object
        print("Sending network info to rendezvous server")
        sock.sendto(packet, (rvous_host,comm.DEFAULT_RVOUS_PORT))

        print("Awaiting peer host info") # from either rvous or another peer
        packet = sock.recv(this_node.port)
        print(packet)

        pack_type,npeers,peers = comm.decode_packet(packet)
        print("Received packet of type", comm.PacketType(pack_type).name)
        print("Received address for", npeers, "peers")
        
        # one thread per peer
        # pool = ThreadPool(npeers)
        # results = pool.starmap(hole_punch, zip(itertools.repeat(sock), peers)


    except KeyboardInterrupt:
        sys.exit()
    else:
        sys.exit(0)

if __name__=="__main__":
    main()