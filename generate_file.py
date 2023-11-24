from protofuzz import protofuzz
from protofuzz import gen
import netmessages_pb2 as proto
from google.protobuf.any_pb2 import Any
import random
import sys
import os
import data_thing
def deinit():
	pass

protopaths = ["/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/netmessages.proto", "/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/network_connection.proto", "/home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/engine_gcmessages.proto"]
import binascii


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

'''
for thing in all_messages.keys():
	poopoostring = all_messages[thing]
	poopoostring = poopoostring[poopoostring.index("_")+1:]
	#print(poopoostring)
	for thing2 in actual_shits:
		if poopoostring in thing2:
			#print(thing)
			all_messages[thing] = thing2
'''


for thing in all_messages.keys():
	poopoostring = all_messages[thing]
	poopoostring = poopoostring[poopoostring.index("_")+1:]
	#print(poopoostring)
	for thing2 in actual_shits:
		if poopoostring in thing2:
			#print(thing)
			#print("thing2 == "+str(thing2))
			all_messages[thing] = thing2

all_messages[24] = "CSVCMsg_EntityMsg"

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




TYPE_BOOL = 8
TYPE_BYTES = 12
TYPE_DOUBLE = 1
TYPE_ENUM = 14
TYPE_FIXED32 = 7
TYPE_FIXED64 = 6
TYPE_FLOAT = 2
TYPE_GROUP = 10
TYPE_INT32 = 5
TYPE_INT64 = 3
TYPE_MESSAGE = 11
TYPE_SFIXED32 = 15
TYPE_SFIXED64 = 16
TYPE_SINT32 = 17
TYPE_SINT64 = 18
TYPE_STRING = 9
TYPE_UINT32 = 13
TYPE_UINT64 = 4


oooo = '''TYPE_BOOL = 8
TYPE_BYTES = 12
TYPE_DOUBLE = 1
TYPE_ENUM = 14
TYPE_FIXED32 = 7
TYPE_FIXED64 = 6
TYPE_FLOAT = 2
TYPE_GROUP = 10
TYPE_INT32 = 5
TYPE_INT64 = 3
TYPE_MESSAGE = 11
TYPE_SFIXED32 = 15
TYPE_SFIXED64 = 16
TYPE_SINT32 = 17
TYPE_SINT64 = 18
TYPE_STRING = 9
TYPE_UINT32 = 13
TYPE_UINT64 = 4'''

types = {}

line_stuff = oooo.split("\n")
for line in line_stuff:
	tokens = line.split(" ")
	types[int(tokens[-1])] = tokens[0]
print("Types: "+str(types))




integers = [TYPE_UINT64, TYPE_UINT32, TYPE_INT32, TYPE_INT64, TYPE_SINT64, TYPE_SINT32]


def hex_to_bytes(hex_str: str):
	return bytes.fromhex(hex_str)

def gen_packet():

	# print version string
	#print("Python version in the fuzz function: "+str(sys.version))

	# this function assumes that the buf has the message_id first and then the length of the buffer


	#original_message = buf


	#message_id, read_bytes = parse_type(buf)

	#buf = buf[read_bytes:] # just skip over the id stuff

	#length, read_bytes = parse_length(buf)

	#buf = buf[read_bytes:]




	


	print("What kind of message would you like?")
	print("Available messages: "+str(all_messages))
	print("Which one? : ")
	#message_type = all_messages[message_id]
	message_type = str(input("> "))

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

	stuff = data_thing.stuff
	function = getattr(proto, message_type)
	print("shitoof:")
	print("message_type =="+str(message_type))
	#print("message_type: "+str(message_type))
	print("proto.message_type == "+str(proto.svc_EntityMessage)) # svc_EntityMessage
	message = function()
	#message.ParseFromString(buf)

	print("=============================")
	#print(message)
	#print(message.type)
	print("2222222222222222222222222")
	#print(binascii.hexlify(bytearray(message.string_data)))
	#print("len(stuff) == "+str(len(stuff)))
	#print(binascii.hexlify(bytearray(message.string_data.toByteArray())))

	#message.string_data = bytes.fromhex(stuff)


	while True:
		print("Which element of the message would you like to modify? (type \"DONE\" to get your message to a file.)")
		field_list = [field.name for field in message.DESCRIPTOR.fields]

		print(field_list)
		field = str(input("> "))
		
		if field == "DONE":
			break

		if field not in field_list:
			print("Field not in message!")
			continue
		else:

			#print("oof == "+str(getattr(message, field)))
			index = field_list.index(field)
			#print("getattr(message.DESCRIPTOR.fields, field) == "+str(getattr(message.DESCRIPTOR, field)))

			type_thing = message.DESCRIPTOR.fields[index].type
			
			type_as_str = types[type_thing]

			#print("type_thing == "+str(type_thing))

			inputthing = str(input("Please enter your input (must be of type "+str(type_thing)+" aka "+str(type_as_str)+") "))

			if type_thing == TYPE_STRING:
				print("Casting to string")
				inputthing = str(inputthing)
			elif type_thing in integers:
				print("Casting to integer.")
				inputthing = int(inputthing)
			elif type_thing == TYPE_BOOL:
				print("Casting to bool")
				print("type_thing == "+str(inputthing))
				inputthing = bool(int(inputthing))
				print("Boolean value is this: "+str(inputthing))
			elif type_thing == TYPE_BYTES:
				if "0x" in inputthing:
					inputthing = hex_to_bytes(inputthing[2:])
				else:
					inputthing = bytes(inputthing, encoding="ascii")

			setattr(message, field, inputthing)

	#return message.SerializeToString()




	#print(binascii.hexlify(bytearray(message.string_data)))


	stuffa = message.SerializeToString()
	print(stuffa)

	# mutate the protobuf buffer:


	#print("poopoo")
	#print(message)


	#message = mutate_message(message, message_type)

	#if message == None or message == 0:
	#	print("Fuck!")
	#	exit(1)

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
	#type_bytes = get_length_bytes(all_messages.index(message_type)) # the message_id ( which is also VarInt32 )
	
	type_bytes = get_length_bytes(list(all_messages.keys())[list(all_messages.values()).index(message_type)])

	print("type bytes: "+str(type_bytes))
	#if len(bytes(type_bytes)+bytes(len_bytes)+mut_msg_bytes) > max_size:
	#	return bytearray(original_message)
	#else:
	#	return bytearray(bytes(type_bytes)+bytes(len_bytes)+mut_msg_bytes)  # return the packet



	return bytearray(bytes(type_bytes)+bytes(len_bytes)+mut_msg_bytes)



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
	
	#test_files = os.listdir("tests/") # hardcoded dir

	initialize_stuff()
	#for file in test_files:

	#output_file = "poopoo"
	#filename = sys.argv[-1]
	#print("Running file: "+str(filename))
		
		
	#bytes_buffer = load_from_file(filename)
	stuff = gen_packet()
	#stuff = fuzz(bytes_buffer, 0, 0)
	#print("type of final stuff: "+str(type(stuff)))
	sys.stdout.buffer.write(bytes(stuff))


	# def fuzz(buf, add_buf, max_size):

	outfile = str(input("Which file do you want to save the packet to? : "))

	fh = open(outfile, "wb")
	fh.write(stuff)
	fh.close()
	print("[+] Done")
	exit(0)










