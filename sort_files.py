#!/bin/python3.9

from protofuzz import protofuzz
from protofuzz import gen
import netmessages_pb2 as proto
from google.protobuf.any_pb2 import Any
import random
import sys
import os

def deinit():
	pass

protopaths = ["/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/netmessages.proto", "/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/network_connection.proto", "/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/engine_gcmessages.proto"]



#message_handlers = []
#for path in protopaths:
#	message_handlers += protofuzz.from_file(path)
message_handlers = protofuzz.from_file("/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/netmessages.proto")
'''

The messages we are interested in are these:

enum NET_Messages
{
	net_NOP = 0;
	net_Disconnect = 1;				// disconnect, last message in connection
	net_File = 2;					// file transmission message request/deny
	net_SplitScreenUser = 3;		// Changes split screen user, client and server must both provide handler
	net_Tick = 4; 					// s->c world tick, c->s ack world tick
	net_StringCmd = 5; 				// a string command
	net_SetConVar = 6;				// sends one/multiple convar/userinfo settings
	net_SignonState = 7;			// signals or acks current signon state
	// client clc messages and server svc messages use the range 8+
	net_PlayerAvatarData = 100;		// player avatar RGB data (client clc & server svc message blocks use 8..., so start a new range here @ 100+)
}

and then these:

enum SVC_Messages
{
	svc_ServerInfo 			= 8;		// first message from server about game; map etc
	svc_SendTable 			= 9;		// sends a sendtable description for a game class
	svc_ClassInfo 			= 10;		// Info about classes (first byte is a CLASSINFO_ define).							
	svc_SetPause 			= 11;		// tells client if server paused or unpaused
	svc_CreateStringTable 	= 12;		// inits shared string tables
	svc_UpdateStringTable 	= 13;		// updates a string table
	svc_VoiceInit 			= 14;		// inits used voice codecs & quality
	svc_VoiceData 			= 15;		// Voicestream data from the server
	svc_Print 				= 16;		// print text to console
	svc_Sounds 				= 17;		// starts playing sound
	svc_SetView 			= 18;		// sets entity as point of view
	svc_FixAngle 			= 19;		// sets/corrects players viewangle
	svc_CrosshairAngle 		= 20;		// adjusts crosshair in auto aim mode to lock on traget
	svc_BSPDecal 			= 21;		// add a static decal to the world BSP
	svc_SplitScreen 		= 22;		// split screen style message
	svc_UserMessage 		= 23;		// a game specific message 
	svc_EntityMessage 		= 24;		// a message for an entity
	svc_GameEvent 			= 25;		// global game event fired
	svc_PacketEntities 		= 26;		// non-delta compressed entities
	svc_TempEntities 		= 27;		// non-reliable event object
	svc_Prefetch 			= 28;		// only sound indices for now
	svc_Menu 				= 29;		// display a menu from a plugin
	svc_GameEventList 		= 30;		// list of known games events and fields
	svc_GetCvarValue 		= 31;		// Server wants to know the value of a cvar on the client	
	svc_PaintmapData		= 33;		// Server paintmap data
	svc_CmdKeyValues		= 34;		// Server submits KeyValues command for the client
	svc_EncryptedData		= 35;		// Server submites encrypted data
	svc_HltvReplay			= 36;		// start or stop HLTV-fed replay
	svc_Broadcast_Command	= 38;		// broadcasting a user command
}


'''


all_messages = proto.SVC_Messages.items()+proto.NET_Messages.items() # these are all of the net messages we are interested in.

for i in range(len(all_messages)):
	all_messages[i] = list(all_messages[i])
	all_messages[i].reverse() # this actually works. thanks python

all_messages = dict(all_messages)

print(all_messages)


actual_shits = '''CSVCMsg_ServerInfo
CSVCMsg_ClassInfo
CSVCMsg_SendTable
CSVCMsg_Print
CSVCMsg_SetPause
CSVCMsg_SetView
CSVCMsg_CreateStringTable
CSVCMsg_UpdateStringTable
CSVCMsg_VoiceInit
CSVCMsg_VoiceData
CSVCMsg_FixAngle
CSVCMsg_CrosshairAngle
CSVCMsg_Prefetch
CSVCMsg_BSPDecal
CSVCMsg_SplitScreen
CSVCMsg_GetCvarValue
CSVCMsg_Menu
CSVCMsg_UserMessage
CSVCMsg_PaintmapData
CSVCMsg_GameEvent
CSVCMsg_GameEventList
CSVCMsg_TempEntities
CSVCMsg_PacketEntities
CSVCMsg_Sounds
CSVCMsg_EntityMsg
CSVCMsg_CmdKeyValues
CSVCMsg_EncryptedData
CSVCMsg_HltvReplay
CSVCMsg_Broadcast_Command
CNETMsg_Tick
CNETMsg_StringCmd
CNETMsg_SignonState
CNETMsg_SetConVar
CNETMsg_NOP
CNETMsg_Disconnect
CNETMsg_File
CNETMsg_SplitScreenUser
CNETMsg_PlayerAvatarData'''.split("\n")


for thing in all_messages.keys():
	poopoostring = all_messages[thing]
	poopoostring = poopoostring[poopoostring.index("_")+1:]
	#print(poopoostring)
	for thing2 in actual_shits:
		if poopoostring in thing2:
			#print(thing)
			all_messages[thing] = thing2





def init(seed):
	random.seed(seed) # initialize randomness with seed
    #pass





'''


class bf_read:
	def __init__(self, bytes_stuff):
		print("bytes_stuff == "+str(bytes_stuff))
		self.bytes = bytes_stuff
		self.counter = 0

	def ReadByte(self):

		result = self.bytes[self.counter]
		self.counter += 1
		return result



	def ReadVarInt32(self):
		result = 0
		count = 0
		b = 0x80

		while (b & 0x80):
			b = self.ReadByte()
			result |= (b & 0x7f) << (7* count)
			count += 1
		return result


def to_bytes(hex_string):
	return bytearray.fromhex(hex_string)

if __name__=="__main__":
	hex_string = str(input("Please input hex_string: "))
	reader = bf_read(to_bytes(hex_string))
	print(hex(reader.ReadVarInt32()))

'''


class bf_read:
	def __init__(self, bytes_stuff):
		#print("bytes_stuff == "+str(bytes_stuff))
		self.bytes = bytes_stuff
		self.counter = 0

	def ReadByte(self):

		result = self.bytes[self.counter]
		self.counter += 1
		return result



	def ReadVarInt32(self):
		result = 0
		count = 0
		b = 0x80

		while (b & 0x80):
			b = self.ReadByte()
			result |= (b & 0x7f) << (7* count)
			count += 1
		return result


def to_bytes(hex_string):
	return bytearray.fromhex(hex_string)


def parse_type(buffer):

	reader = bf_read(buffer)

	# this function parses the message type from the packet itself

	command_id = reader.ReadVarInt32()

	return command_id, reader.counter

def parse_length(buffer):

	reader = bf_read(buffer)

	# this function parses the message type from the packet itself

	command_id = reader.ReadVarInt32()

	return command_id, reader.counter


def get_length_bytes(length_integer):
	
	# this converts to the other format
	result = 0x00
	count = 0
	result_list = []
	while length_integer > 0x7f:
		result_list.append(((length_integer & 0x7f)|0x80))
		count += 1
		length_integer >>= 7
		#print("length_integer: "+str(length_integer))

	
	result_list.append(((length_integer & 0x7f)))
	#print(result_list)
	return bytes(result_list)



def mutate_message(message, msg_type):

	'''
	>>> from protofuzz import protofuzz
>>> message_fuzzers = protofuzz.from_description_string("""
...     message Address {
...      required int32 house = 1;
...      required string street = 2;
...     }
... """)
>>> for obj in message_fuzzers['Address'].permute():
...     print("Generated object: {}".format(obj))
	'''

	#for thing in message_handlers[msg_type].permute():
	#	print(thing)
		#thing.permute()
	#print("tick before:")

	#print(message_handlers[msg_type].tick)

	#message_handlers[msg_type].permute()

	#print("after")

	#print(message_handlers[msg_type].tick)

	res = [field for field in message.DESCRIPTOR.fields]
	#print(protofuzz._prototype_to_generator(res[0], None))

	#print(list(protofuzz._prototype_to_generator(res[0], None)))

	#print("all fields:")
	#print(res)

	#print("Length of res: "+str(len(res)))
	if len(res) != 0:

		random_field = random.choice(res)


	#print("protofuzz._prototype_to_generator(random_field.name, None) == "+str(protofuzz._prototype_to_generator(random_field, None)))
	#print("random_field: "+str(random_field))
	#print("poopoo: " + str(protofuzz._prototype_to_generator(random_field, gen.Product)))
	#print("Now trying the thing:")
	#print("List thing: "+str(list(protofuzz._prototype_to_generator(random_field, gen.Product))))
	#print("Done")
	#setattr(message, random_field.name, random.choice(list(protofuzz._prototype_to_generator(random_field, None))))

	thing = protofuzz.from_protobuf_class(message)
	fuzzed_stuff = thing.permute(limit=100)
	for thing in fuzzed_stuff:
		return thing
	#return list(fuzzed_stuff)[0]


	#return message

processed_types = []


def fuzz(buf, add_buf, max_size):

	# print version string
	#print("Python version in the fuzz function: "+str(sys.version))

	# this function assumes that the buf has the message_id first and then the length of the buffer


	original_message = buf

	#buf = buf[10:]
	message_id, read_bytes = parse_type(buf)
	message_type = all_messages[message_id]
	print(message_type)
	buf = buf[read_bytes:] # just skip over the id stuff

	length, read_bytes = parse_length(buf)

	buf = buf[read_bytes:]

	if len(buf) != length:
		print("Warning: Length of the protobuf packet does not match the length given in it.")
		print("Actual length: "+str(hex(len(buf))))
		print("Given length: "+str(hex(length)))


	

	if message_id not in all_messages:
		print("Invalid message: "+str(message_id))
		#return buf
		exit(1)

	message_type = all_messages[message_id]


	'''
	message = proto.CNETMsg_Tick()
	message.ParseFromString(buf)
	print(message.tick)
	print(message.host_computationtime_std_deviation)

	'''



	'''
	obj = MyClass()
try:
    func = getattr(obj, "dostuff")
    func()

	'''
	marked_file = False

	function = getattr(proto, message_type)
	print("message_type: "+str(message_type))
	
	if message_type not in processed_types:
		marked_file = True
		processed_types.append(message_type)
	else:
		if random.randrange(1,300) == 2:
			marked_file = True

	message = function()
	#return
	message.ParseFromString(buf)

	# mutate the protobuf buffer:


	#print("poopoo")
	#print(message)


	message = mutate_message(message, message_type)
	#print("poopoo after")
	#print(message)

	# serialize the mutated message

	mut_msg_bytes = message.SerializeToString()


	#print("message_type : "+str(message_type))
	#print("Mutated stuff: ")
	#print(mut_msg_bytes)






	# Now we just need to pack everything back in. Shouldn't be that hard right? :)

	new_length = len(mut_msg_bytes) # get new length

	# get_length_bytes

	# get the length bytes (VarInt32)

	len_bytes = get_length_bytes(new_length)
	#print("message_id: " + str(message_id))
	type_bytes = get_length_bytes(message_id) # the message_id ( which is also VarInt32 )
	#print("type bytes: "+str(type_bytes))
	if len(bytes(type_bytes)+bytes(len_bytes)+mut_msg_bytes) > max_size:
		return bytearray(original_message), marked_file
	else:
		return bytearray(bytes(type_bytes)+bytes(len_bytes)+mut_msg_bytes), marked_file  # return the packet




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




if __name__=="__main__":
	
	test_files = os.listdir("tests/") # hardcoded dir

	initialize_stuff()
	for file in test_files:

		output_file = "poopoo"
		filename = "tests/"+file
		print("Running file: "+str(filename))
		
		
		bytes_buffer = load_from_file(filename)

		stuff, marked = fuzz(bytes_buffer, 0, 0)
		
		#if marked:
		#	os.system("cp "+str(filename)+" ./minified/")
		print("processed_types: " + str(processed_types))
		#print("type of final stuff: "+str(type(stuff)))
		#sys.stdout.buffer.write(bytes(stuff))


		# def fuzz(buf, add_buf, max_size):

	


'''

if __name__=="__main__":
	
	if "--file" not in sys.argv:
		print("Pass file with --file FILE .")
		exit(1)
	if "--outfile" not in sys.argv:
		print("Pass output file with --outfile FILE .")
		exit(1)
	output_file = sys.argv[sys.argv.index("--outfile")+1]
	file = sys.argv[sys.argv.index("--file")+1]
	
	initialize_stuff()
	bytes_buffer = load_from_file(file)

	stuff = fuzz(bytes_buffer, 0, 0)
	print("type of final stuff: "+str(type(stuff)))
	sys.stdout.buffer.write(bytes(stuff))
	# def fuzz(buf, add_buf, max_size):

	fh = open(output_file, "wb+")
	fh.write(stuff)
	fh.close()

'''



