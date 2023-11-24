#!/bin/python3.9

from protofuzz import protofuzz
from protofuzz import gen
import netmessages_pb2 as proto
import cstrike15_usermessages_pb2 as usermessages
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





usermessage_string = '''CS_UM_VGUIMenu = 1;
CS_UM_Geiger = 2;
CS_UM_Train = 3;
CS_UM_HudText = 4;
CS_UM_SayText = 5;
CS_UM_SayText2 = 6;
CS_UM_TextMsg = 7;
CS_UM_HudMsg = 8;
CS_UM_ResetHud = 9;
CS_UM_GameTitle = 10;
CS_UM_Shake = 12;
CS_UM_Fade = 13;
CS_UM_Rumble = 14;
CS_UM_CloseCaption = 15;
CS_UM_CloseCaptionDirect = 16;
CS_UM_SendAudio = 17;
CS_UM_RawAudio = 18;
CS_UM_VoiceMask = 19;
CS_UM_RequestState = 20;
CS_UM_Damage = 21;
CS_UM_RadioText = 22;
CS_UM_HintText = 23;
CS_UM_KeyHintText = 24;
CS_UM_ProcessSpottedEntityUpdate = 25;
CS_UM_ReloadEffect = 26;
CS_UM_AdjustMoney = 27;
CS_UM_UpdateTeamMoney = 28;
CS_UM_StopSpectatorMode = 29;
CS_UM_KillCam = 30;
CS_UM_DesiredTimescale = 31;
CS_UM_CurrentTimescale = 32;
CS_UM_AchievementEvent = 33;
CS_UM_MatchEndConditions = 34;
CS_UM_DisconnectToLobby = 35;
CS_UM_PlayerStatsUpdate = 36;
CS_UM_DisplayInventory = 37;
CS_UM_WarmupHasEnded = 38;
CS_UM_ClientInfo = 39;
CS_UM_XRankGet = 40;
CS_UM_XRankUpd = 41;
CS_UM_CallVoteFailed = 45;
CS_UM_VoteStart = 46;
CS_UM_VotePass = 47;
CS_UM_VoteFailed = 48;
CS_UM_VoteSetup = 49;
CS_UM_ServerRankRevealAll = 50;
CS_UM_SendLastKillerDamageToClient = 51;
CS_UM_ServerRankUpdate = 52;
CS_UM_ItemPickup = 53;
CS_UM_ShowMenu = 54;
CS_UM_BarTime = 55;
CS_UM_AmmoDenied = 56;
CS_UM_MarkAchievement = 57;
CS_UM_MatchStatsUpdate = 58;
CS_UM_ItemDrop = 59;
CS_UM_GlowPropTurnOff = 60;
CS_UM_SendPlayerItemDrops = 61;
CS_UM_RoundBackupFilenames = 62;
CS_UM_SendPlayerItemFound = 63;
CS_UM_ReportHit = 64;
CS_UM_XpUpdate = 65;
CS_UM_QuestProgress = 66;
CS_UM_ScoreLeaderboardData = 67;
CS_UM_PlayerDecalDigitalSignature = 68;
CS_UM_WeaponSound = 69;
CS_UM_UpdateScreenHealthBar = 70;
CS_UM_EntityOutlineHighlight = 71;
CS_UM_SSUI = 72;
CS_UM_SurvivalStats = 73;
CS_UM_DisconnectToLobby2 = 74;
CS_UM_EndOfMatchAllPlayersData = 75;'''




'''

{1: 'CCSUsrMsg_VGUIMenu', 2: 'CCSUsrMsg_Geiger', 3: 'CCSUsrMsg_Train', 4: 'CCSUsrMsg_HudText', 5: 'CCSUsrMsg_SayText', 6: 'CCSUsrMsg_SayText2', 7: 'CCSUsrMsg_TextMsg', 8: 'CCSUsrMsg_HudMsg', 9: 'CCSUsrMsg_ResetHud', 10: 'CCSUsrMsg_GameTitle', 11: 'CCSUsrMsg_Shake', 12: 'CCSUsrMsg_Fade', 13: 'CCSUsrMsg_Rumble', 14: 'CCSUsrMsg_CloseCaption', 15: 'CCSUsrMsg_CloseCaptionDirect', 16: 'CCSUsrMsg_SendAudio', 17: 'CCSUsrMsg_RawAudio', 18: 'CCSUsrMsg_VoiceMask', 19: 'CCSUsrMsg_RequestState', 20: 'CCSUsrMsg_Damage', 21: 'CCSUsrMsg_RadioText', 22: 'CCSUsrMsg_HintText', 23: 'CCSUsrMsg_KeyHintText', 24: 'CCSUsrMsg_ProcessSpottedEntityUpdate', 25: 'CCSUsrMsg_ReloadEffect', 26: 'CCSUsrMsg_AdjustMoney', 27: 'CCSUsrMsg_UpdateTeamMoney', 28: 'CCSUsrMsg_StopSpectatorMode', 29: 'CCSUsrMsg_KillCam', 30: 'CCSUsrMsg_DesiredTimescale', 31: 'CCSUsrMsg_CurrentTimescale', 32: 'CCSUsrMsg_AchievementEvent', 33: 'CCSUsrMsg_MatchEndConditions', 34: 'CCSUsrMsg_DisconnectToLobby', 35: 'CCSUsrMsg_PlayerStatsUpdate', 36: 'CCSUsrMsg_DisplayInventory', 37: 'CCSUsrMsg_WarmupHasEnded', 38: 'CCSUsrMsg_ClientInfo', 39: 'CCSUsrMsg_XRankGet', 40: 'CCSUsrMsg_XRankUpd', 41: 'CCSUsrMsg_CallVoteFailed', 42: 'CCSUsrMsg_VoteStart', 43: 'CCSUsrMsg_VotePass', 44: 'CCSUsrMsg_VoteFailed', 45: 'CCSUsrMsg_VoteSetup', 46: 'CCSUsrMsg_ServerRankRevealAll', 47: 'CCSUsrMsg_SendLastKillerDamageToClient', 48: 'CCSUsrMsg_ServerRankUpdate', 49: 'CCSUsrMsg_ItemPickup', 50: 'CCSUsrMsg_ShowMenu', 51: 'CCSUsrMsg_BarTime', 52: 'CCSUsrMsg_AmmoDenied', 53: 'CCSUsrMsg_MarkAchievement', 54: 'CCSUsrMsg_MatchStatsUpdate', 55: 'CCSUsrMsg_ItemDrop', 56: 'CCSUsrMsg_GlowPropTurnOff', 57: 'CCSUsrMsg_SendPlayerItemDrops', 58: 'CCSUsrMsg_RoundBackupFilenames', 59: 'CCSUsrMsg_SendPlayerItemFound', 60: 'CCSUsrMsg_ReportHit', 61: 'CCSUsrMsg_XpUpdate', 62: 'CCSUsrMsg_QuestProgress', 63: 'CCSUsrMsg_ScoreLeaderboardData', 64: 'CCSUsrMsg_PlayerDecalDigitalSignature', 65: 'CCSUsrMsg_WeaponSound', 66: 'CCSUsrMsg_UpdateScreenHealthBar', 67: 'CCSUsrMsg_EntityOutlineHighlight', 68: 'CCSUsrMsg_SSUI', 69: 'CCSUsrMsg_SurvivalStats', 70: 'CCSUsrMsg_DisconnectToLobby2', 71: 'CCSUsrMsg_EndOfMatchAllPlayersData'}

'''


usermessage_types = {}

usermessage_stuff = usermessage_string.split("\n")

count = 1

for thing in usermessage_stuff:
	
	oof = thing.split(" =")[0]
	# at this point oof == CS_UM_WeaponSound  or oof == CS_UM_DisconnectToLobby2 etc etc .
	other_oof = oof.split("_")
	final_thing = other_oof[-1] # last element aka WeaponSound or DisconnectToLobby2 etc .

	#print("oof == "+str(oof))
	#print("oof[-1] == " +str(oof[-1]) )
	usermessage_types[int(thing.split(" =")[-1][:-1])] = "CCSUsrMsg_"+final_thing
	count += 1

print("=========================================")

print(usermessage_types)
print("=========================================")



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







def mutate_user_message(message):

	




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

	
	#print(protofuzz._prototype_to_generator(res[0], None))

	#print(list(protofuzz._prototype_to_generator(res[0], None)))

	#print("all fields:")
	#print(res)


	# 

	if msg_type == "CSVCMsg_UserMessage":
		print("Shitpoop:")
		print(message.msg_type)
		print(message.msg_data)

		# output the values of the user message bytes:




		print("message.msg_type == "+str(message.msg_type))
		#function = getattr(usermessages, message.msg_type)
		if not usermessage_types[message.msg_type] == "CCSUsrMsg_UpdateTeamMoney":

			function = getattr(usermessages, usermessage_types[message.msg_type])
			print("Type: "+str(usermessage_types[message.msg_type]))
			#print("message_type: "+str(message_type))
			message2 = function()
			message2.ParseFromString(message.msg_data)


			message2 = mutate_user_message(message2)

			message.msg_data = message2.SerializeToString()

			#if "AdjustMoney" in usermessage_types[message.msg_type]:

			#	print("Amount: "+str(message2.amount))




	res = [field for field in message.DESCRIPTOR.fields]


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
	#return fuzzed_stuff[random.randrange(len(list(fuzzed_stuff)))]

	random_integer = random.randrange(10)
	return_shit = None
	count = 0
	for thing in fuzzed_stuff:
		if count == random_integer:
			return thing
		else:
			return_shit = thing
		count += 1
	return return_shit

	#return list(fuzzed_stuff)[0]


	#return message




def fuzz(buf, add_buf, max_size):

	# print version string
	#print("Python version in the fuzz function: "+str(sys.version))

	# this function assumes that the buf has the message_id first and then the length of the buffer


	original_message = buf


	message_id, read_bytes = parse_type(buf)

	buf = buf[read_bytes:] # just skip over the id stuff

	length, read_bytes = parse_length(buf)

	buf = buf[read_bytes:]

	if len(buf) != length:
		print("Warning: Length of the protobuf packet does not match the length given in it.")
		print("Actual length: "+str(hex(len(buf))))
		print("Given length: "+str(hex(length)))
		return buf


	

	if message_id not in all_messages:
		print("Invalid message: "+str(message_id))
		return buf
		#exit(1)

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


	function = getattr(proto, message_type)
	#print("message_type: "+str(message_type))
	message = function()
	message.ParseFromString(buf)

	# mutate the protobuf buffer:


	#print("poopoo")
	#print(message)


	message = mutate_message(message, message_type)

	if message == None or message == 0:
		print("Fuck!")
		exit(1)

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
		return bytearray(original_message)
	else:
		return bytearray(bytes(type_bytes)+bytes(len_bytes)+mut_msg_bytes)  # return the packet




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
		#print("Running file: "+str(filename))
		
		
		bytes_buffer = load_from_file(filename)

		stuff = fuzz(bytes_buffer, 0, 0)
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



