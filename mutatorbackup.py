
from protofuzz import protofuzz
import netmessages_pb2 as proto
from google.protobuf.any_pb2 import Any

protopaths = ["/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/netmessages.proto", "/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/network_connection.proto", "/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/engine_gcmessages.proto"]



def init(seed):
    pass

def fuzz_count(buf):
    return cnt





def fuzz(buf, add_buf, max_size):

	message = proto.CNETMsg_Tick()
	message.ParseFromString(buf)
	print(message.tick)
	#message.descriptor()
	#thing = message.Is(proto._CNETMSG_TICK)
	#stuff = message.messageid
	#print(stuff)


	#return mutated_out

'''
def fuzz(buf, add_buf, max_size):

	message = Any()
	message.Pack(buf)
	thing = message.Is(proto._CNETMSG_TICK)
	print(thing)


	#return mutated_out
'''
def describe(max_description_length):
    return "description_of_current_mutation"

def post_process(buf):
    return out_buf

def init_trim(buf):
    return cnt

def trim():
    return out_buf

def post_trim(success):
    return next_index

def havoc_mutation(buf, max_size):
    return mutated_out

def havoc_mutation_probability():
    return probability # int in [0, 100]

def queue_get(filename):
    return True

def queue_new_entry(filename_new_queue, filename_orig_queue):
    return False

def introspection():
    return string

def deinit():  # optional for Python
    pass


def initialize_stuff():
	message_handlers = []
	for path in protopaths:
		message_handlers += protofuzz.from_file(path)
	#print(message_handlers)


def load_from_file(filename):
	fh = open(filename, "rb")
	buffer = fh.read()
	fh.close()
	return buffer

import sys

if __name__=="__main__":
	
	if "--file" not in sys.argv:
		print("Pass file with --file FILE .")
		exit(1)
	file = sys.argv[sys.argv.index("--file")+1]
	
	initialize_stuff()
	bytes_buffer = load_from_file(file)

	fuzz(bytes_buffer, 0, 0)

	# def fuzz(buf, add_buf, max_size):




