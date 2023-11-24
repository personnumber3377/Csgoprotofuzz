#!/bin/python3.9

from protofuzz import protofuzz
from protofuzz import gen
import netmessages_pb2 as proto
import cstrike15_usermessages_pb2 as usermessages
from google.protobuf.any_pb2 import Any
import random
import sys
import os
import copy
# import google.protobuf.internal.containers
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
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



# message, mutated = mutate_field_thing(message, message_type, random_field)

'''

common/protocol.h:#define INSTANCE_BASELINE_TABLENAME	"instancebaseline"
common/protocol.h:#define LIGHT_STYLES_TABLENAME		"lightstyles"
common/protocol.h:#define USER_INFO_TABLENAME			"userinfo"
common/protocol.h:#define SERVER_STARTUP_DATA_TABLENAME	"server_query_info"	// the name is a remnant...
common/protocol.h:#define DYNAMIC_MODEL_TABLENAME		"dynamicmodel"
engine/cl_demo.cpp:		if ( V_strcasecmp( demoTable->GetTableName(), USER_INFO_TABLENAME ) == 0 )
engine/precache.h:#define MODEL_PRECACHE_TABLENAME	"modelprecache"
engine/precache.h:#define GENERIC_PRECACHE_TABLENAME	"genericprecache"
engine/precache.h:#define SOUND_PRECACHE_TABLENAME	"soundprecache"
engine/precache.h:#define DECAL_PRECACHE_TABLENAME	"decalprecache"


#define DOWNLOADABLE_FILE_TABLENAME	"downloadables"
'''



INSTANCE_BASELINE_TABLENAME ="instancebaseline"
LIGHT_STYLES_TABLENAME ="lightstyles"
USER_INFO_TABLENAME ="userinfo"
SERVER_STARTUP_DATA_TABLENAME="server_query_info"
DYNAMIC_MODEL_TABLENAME ="dynamicmodel"
MODEL_PRECACHE_TABLENAME ="modelprecache"
GENERIC_PRECACHE_TABLENAME ="genericprecache"
SOUND_PRECACHE_TABLENAME ="soundprecache"
DECAL_PRECACHE_TABLENAME ="decalprecache"
DOWNLOADABLE_FILE_TABLENAME = "downloadables"


tablenames = [INSTANCE_BASELINE_TABLENAME,
LIGHT_STYLES_TABLENAME,
USER_INFO_TABLENAME,
SERVER_STARTUP_DATA_TABLENAME,
DYNAMIC_MODEL_TABLENAME,
MODEL_PRECACHE_TABLENAME,
GENERIC_PRECACHE_TABLENAME,
SOUND_PRECACHE_TABLENAME,
DECAL_PRECACHE_TABLENAME,
DOWNLOADABLE_FILE_TABLENAME]



STRINGTABLE_NAME_CHANCE= 0.9

OWN_MUTATOR_CHANCE = 0.3

BYTES_MUTATION_CHANCE = 0.9
STRING_MUTATION_CHANCE = 0.9

import string
alphabet = string.ascii_letters

def rand_str(len):
	return "".join(random.choice(alphabet) for _ in range(len))

def rand_bytes(len):
	return bytes([random.randrange(0,256) for _ in range(len)])

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

UINT_32_MAX = 4_294_967_295

def int_thing(message, field, selected_name):

	if field.name == selected_name:
		# set the thing
		#print("field.name: "+str(field.name))
		#for _ in range(1000000):

		#random_shit = random.randrange(-1*((4_294_967_295-1)//2), (4_294_967_295-1)//2)
		print("Modifying field "+str(field.name))
		random_shit = int(input("Please enter a integer. "))
		#random_shit = -1*((4_294_967_295-1)//2)
		#random_shit = (4_294_967_295-1)//2
		#random_shit = -2645071550+1
		#print(random_shit)
		setattr(message, field.name, random_shit)

		return message, True
	return message, False


def set_int(message, field):

	

	#random_shit = random.randrange(-1*((4_294_967_295-1)//2), (4_294_967_295-1)//2)
	print("Modifying field "+str(field.name))
	random_shit = int(input("Please enter a integer. "))
	#random_shit = -1*((4_294_967_295-1)//2)
	#random_shit = (4_294_967_295-1)//2
	#random_shit = -2645071550+1
	#print(random_shit)
	setattr(message, field.name, random_shit)

	return message, True
	#return message, False
'''
def small_int_thing(message, field, selected_name):

	if field.name == selected_name:
		# set the thing
		#print("field.name: "+str(field.name))
		#for _ in range(1000000):

		random_shit = random.randrange(-1*((10)), 10)
		#random_shit = -1*((4_294_967_295-1)//2)
		#random_shit = (4_294_967_295-1)//2
		#random_shit = -2645071550+1
		#print(random_shit)
		setattr(message, field.name, random_shit)

		return message, True
	return message, False
'''


def small_int_thing(message, field, selected_name):

	if field.name == selected_name:
		# set the thing
		#print("field.name: "+str(field.name))
		#for _ in range(1000000):

		#random_shit = random.randrange(-1*((10)), 10)
		print("Modifying field "+str(field.name))

		random_shit = int(input("Please enter a small integer: "))

		#random_shit = -1*((4_294_967_295-1)//2)
		#random_shit = (4_294_967_295-1)//2
		#random_shit = -2645071550+1
		#print(random_shit)
		setattr(message, field.name, random_shit)

		return message, True
	return message, False


def replace_random_char(string):

	if len(string) == 0:
		return string
	else:

		random_index = random.randrange(len(string))
	return string[:random_index-1]+random.choice(alphabet)+string[random_index:]

def delete_char(string):
	if len(string) == 0:
		return string
	else:

		random_index = random.randrange(len(string))
	return string[:random_index-1]+string[random_index:]

def add_char(string):
	if len(string) == 0:
		return string
	else:

		random_index = random.randrange(len(string))
	#print("string[:random_index] == "+str(string[:random_index]))
	#print("string[random_index:] == "+str(string[random_index:]))
	return string[:random_index]+random.choice(alphabet)+string[random_index:]


def replace_random_char_byt(string):

	if len(string) == 0:
		return string
	else:

		random_index = random.randrange(len(string))
	#print("string[:random_index-1] == "+str(string[:random_index-1]))
	#print("string[random_index:] == "+str(string[random_index:]))
	return string[:random_index-1]+bytes(random.choice(alphabet), encoding="ascii")+string[random_index:]

def delete_char_byt(string):
	if len(string) == 0:
		return string
	else:

		random_index = random.randrange(len(string))
	return string[:random_index-1]+string[random_index:]

def add_char_byt(string):
	if len(string) == 0:
		return string
	else:

		random_index = random.randrange(len(string))
	return string[:random_index]+bytes(random.choice(alphabet),encoding="ascii")+string[random_index:]


def flip_random_bit(string):
	if len(string) == 0:
		return string
	random_byte = random.randrange(len(string))
	rand_bit = random.randrange(8)
	oof = list(string)
	oof[random_byte] ^= 1<<rand_bit
	return_val = bytes(oof)
	return return_val


def mutate_string(string):

	if isinstance(string, bytes):
		string = str(string)

	print("Trying to mutate a string.")
	print("Current string: "+str(string))
	new_str = str(input("Please enter the new string: "))
	return new_str

	mutation = random.randrange(3)
	if mutation == 0:
		return add_char(string)
	elif mutation == 1:
		return delete_char(string)
	else:
		return replace_random_char(string)
	#print("Error!")
	exit(1)


def mutate_bytes(string):
	if isinstance(string, str):
		string = bytes(string, encoding="ascii")

	#print("string == "+str(string))
	mutation = random.randrange(4)
	if mutation == 0:
		return add_char_byt(string)
	elif mutation == 1:
		return delete_char_byt(string)
	elif mutation == 2:
		return replace_random_char_byt(string)
	else:
		return flip_random_bit(string)
	#print("Error!")
	exit(1)



def bytes_thing(message, field, selected_name):

	if field.name == selected_name:
		# set the thing
		#print("field.name: "+str(field.name))
		#for _ in range(1000000):

		#random_shit = random.randrange(-1*((4_294_967_295-1)//2), (4_294_967_295-1)//2)
		#random_shit = -1*((4_294_967_295-1)//2)
		#random_shit = (4_294_967_295-1)//2
		#random_shit = -2645071550+1
		#print(random_shit)
		#if random.random() < BYTES_MUTATION_CHANCE:
		original_string = getattr(message, field.name)
		#new_string = mutate_bytes(original_string)
		if field.name != "string_data":

			print("Modifying bytes.")
			print("Original bytes: "+str(original_string))
			new_string = str(input("Please enter new string: > "))
		else:
			new_string = original_string[:300]
		if isinstance(new_string, str):

			setattr(message, field.name, bytes(new_string,encoding="ascii"))
		else:
			setattr(message, field.name, new_string)
		#else:
		#	setattr(message, field.name, rand_bytes(random.randrange(10000))) # just create random bytes

		return message, True
	return message, False

def bool_thing(message, field, selected_name):

	if field.name == selected_name:
		# set the thing
		#print("field.name: "+str(field.name))
		#for _ in range(1000000):

		#random_shit = random.randrange(-1*((4_294_967_295-1)//2), (4_294_967_295-1)//2)
		#random_shit = -1*((4_294_967_295-1)//2)
		#random_shit = (4_294_967_295-1)//2
		#random_shit = -2645071550+1
		#print(random_shit)
		setattr(message, field.name, bool(random.randrange(2))) # false or true

		return message, True
	return message, False

def set_bool(message, field):
	# set the thing
	#print("field.name: "+str(field.name))
	#for _ in range(1000000):

	#random_shit = random.randrange(-1*((4_294_967_295-1)//2), (4_294_967_295-1)//2)
	#random_shit = -1*((4_294_967_295-1)//2)
	#random_shit = (4_294_967_295-1)//2
	#random_shit = -2645071550+1
	#print(random_shit)
	setattr(message, field.name, bool(random.randrange(2))) # false or true

	return message, True



def string_thing(message, field, selected_name):
	if field.name == selected_name:

		#setattr(message, field.name, str(rand_str(random.randrange(1,100)))) # false or true


		if random.random() < BYTES_MUTATION_CHANCE:
			original_string = getattr(message, field.name)
			new_string = mutate_string(original_string)
			setattr(message, field.name, str(new_string))
		else:
			setattr(message, field.name, rand_str(random.randrange(10000))) # just create random bytes

		return message, True
	return message, False




def stuff_thing(msg, field, list_oof):

	# listoof is a list of lists and each of these sublists have first the field name and then the type aka [["ent_index", "int"], []]
	'''
		if msg_type == "CSVCMsg_EntityMsg":

		msg, thing = int_thing(msg, field, "ent_index")
		if thing:
			return msg, True

		msg, thing = int_thing(msg, field, "class_id")
		if thing:
			return msg, True

		msg, thing = bytes_thing(msg, field, "ent_data")
		if thing:
			return msg, True

	'''

	for thing in list_oof:
		
		field_string = thing[0]
		field_type = thing[1]

		if field_type == "bool":
			msg, thing = bool_thing(msg, field, field_string)
			if thing:
				return msg, True
		elif field_type == "int":
			msg, thing = int_thing(msg, field, field_string)
			if thing:
				return msg, True
		elif field_type == "bytes":
			msg, thing = bytes_thing(msg, field, field_string)
			if thing:
				return msg, True
		elif field_type == "string":
			msg, thing = string_thing(msg, field, field_string)
			if thing:
				return msg, True
		else:
			print("Invalid field type for this mutator: field_type == "+str(field_type))
			exit(1)

	return msg, False



# mutate_field_thing(message, msg_type, random_field)
def mutate_field_thing(msg, msg_type, field):
	#if random.random() > OWN_MUTATOR_CHANCE:
	#	return msg, False
	# first check the obvious cases for example the string table thing
	original_msg = copy.deepcopy(msg)
	
	thing = False
	if msg_type == "CSVCMsg_CreateStringTable": # create some of the interesting tables
		if field.name == "name":
			#if random.random() < STRINGTABLE_NAME_CHANCE:
			#	string_table_name = random.choice(tablenames)
			#else:
			#	string_table_name = rand_str(3)
			print("Modifying table name. Current name: "+str(msg.name))

			string_table_name = input("Please give a table name: ")
			#setattr(msg, field.name, string_table_name)
			msg.name = string_table_name
			#print("poopooshitoof")
			#print(msg.fields)
			return msg, True
		integer_stuff = ["max_entries", "num_entries", "user_data_size", "user_data_size_bits", "flags"]
		for oof in integer_stuff:

			msg, thing = int_thing(msg, field, oof)
			if thing:
				#print("qqqqqqqqqqqqqqqq")
				return msg, True

		msg, thing = bytes_thing(msg, field, "string_data")
		#pri
		if thing:
			#print("qqqqqqqqqqqqqqqq")
			return msg, True

		msg, thing = bool_thing(msg, field, "user_data_fixed_size")
		if thing:
			#print("qqqqqqqqqqqqqqqq")
			return msg, True


	'''
message CSVCMsg_UpdateStringTable
{
	optional int32 table_id = 1;
	optional int32 num_changed_entries = 2;
	optional bytes string_data = 3;
}
	'''

	if msg_type == "CSVCMsg_UpdateStringTable":
		#print("Shitpoop")
		msg, thing = small_int_thing(msg, field, "table_id")
		if thing:
			#print("qqqqqqqqqqqqqqqq")
			return msg, True
		msg, thing = small_int_thing(msg, field, "num_changed_entries")
		if thing:
			#print("qqqqqqqqqqqqqqqq")
			return msg, True
		print("Bytes thing bullshit: ")
		msg, thing = bytes_thing(msg, field, "string_data")
		print("New string: "+str(msg.string_data))
		if thing:
			print("qqqqqqqqqqqqqqqq")
			return msg, True

	'''
	message CSVCMsg_GetCvarValue
{
	optional int32 cookie = 1;		// QueryCvarCookie_t
	optional string cvar_name = 2;
}
	'''

	if msg_type == "CSVCMsg_GetCvarValue":
		
		msg, thing = int_thing(msg, field, "cookie")
		if thing:
			#print("qqqqqqqqqqqqqqqq")
			return msg, True

		msg, thing = string_thing(msg, field, "cvar_name")
		if thing:
			return msg, True

	if msg_type == "CSVCMsg_PaintmapData":
		msg, thing = bytes_thing(msg, field, "paintmap")
		if thing:
			return msg, True
	if msg_type == "CSVCMsg_Sounds":
		msg, thing = bool_thing(msg, field, "reliable_sound")
		if thing:
			return msg, True

	if msg_type == "CSVCMsg_EntityMsg":
		

		msg, thing = int_thing(msg, field, "ent_index")
		if thing:
			return msg, True

		msg, thing = int_thing(msg, field, "class_id")
		if thing:
			return msg, True

		msg, thing = bytes_thing(msg, field, "ent_data")
		if thing:
			return msg, True

	if msg_type == "CSVCMsg_CmdKeyValues":
		# def stuff_thing(msg, field, list_oof):
		msg, thing = stuff_thing(msg, field, [["keyvalues", "bytes"]])


	'''
	message CSVCMsg_EncryptedData
{
	optional bytes encrypted = 1;
	optional int32 key_type = 2;
}


	'''



	if msg_type == "CSVCMsg_EncryptedData":
		# def stuff_thing(msg, field, list_oof):
		msg, thing = stuff_thing(msg, field, [["encrypted", "bytes"], ["key_type", "int"]])


	'''
	optional int32 msg_type = 1;
	optional bytes msg_data = 2;	
	optional int32 passthrough = 3
	'''

	if msg_type == "CSVCMsg_UserMessage":
		msg, thing = stuff_thing(msg, field, [["msg_type", "int"], ["msg_data", "bytes"], ["passthrough", "int"]])

	if msg_type == "CSVCMsg_Print":
		msg, thing = stuff_thing(msg, field, [["text", "string"]])

	if msg_type == "CNETMsg_StringCmd":
		msg, thing = stuff_thing(msg, field, [["command", "string"]])

	if msg_type == "CNETMsg_File":
		msg, thing = stuff_thing(msg, field, [["transfer_id", "int"],["file_name", "string"], ["is_replay_demo_file", "bool"], ["deny", "bool"]])


	'''
	optional int32 transfer_id = 1;
	optional string file_name = 2;
	optional bool is_replay_demo_file = 3;
	optional bool deny = 4;

	'''




	if thing:
		return msg, True

	return original_msg, False






def mutate_submessage(message, user_msg_type=None):
	# this crashes
	#print("ooffff : "+str(message.__dir__()))
	#print("type(message) == "+str(type(message)))
	if not isinstance(message, RepeatedCompositeFieldContainer):

		res = [field for field in message.DESCRIPTOR.fields]

	else:
		res = [field for field in message._message_descriptor.fields]
	#print("Options: "+str(message._message_descriptor.options))
	#print("message.DESCRIPTOR.options == "+str(message.DESCRIPTOR.options))
	print("message._message_descriptor.__dir__() == "+str(message._message_descriptor.__dir__()))
	print("message._message_descriptor.enum_types == "+str(message._message_descriptor.GetOptions()))
	shit = message._message_descriptor.GetOptions()
	print(type(shit))
	print(shit.__dir__())
	print(shit.Extensions)
	print(str(shit.Extensions))
	print(str(shit.Extensions.__dir__()))
	print(str(shit.Extensions._extended_message.__dir__()))
	

	print(str(shit.Extensions._extended_message._fields))

	print(str(shit.Extensions._extended_message.DESCRIPTOR.fields))
	print([field.name for field in shit.Extensions._extended_message.DESCRIPTOR.fields])

	print(str(shit.Extensions._extended_message.ListFields()))
	#print(shit.ListFields())
	#print(shit.fields)

	'''


	Mutating submessage.
message._message_descriptor.__dir__() == ['_options', '_options_class_name', '_serialized_options', 'has_options', 'name', 'full_name', 'file', 'containing_type', '_serialized_start', '_serialized_end', 'fields', 'fields_by_number', 'fields_by_name', '_fields_by_camelcase_name', 'nested_types', 'nested_types_by_name', 'enum_types', 'enum_types_by_name', 'enum_values_by_name', 'extensions', 'extensions_by_name', 'is_extendable', 'extension_ranges', 'oneofs', 'oneofs_by_name', 'syntax', '_concrete_class', '__module__', '__doc__', '__init__', 'fields_by_camelcase_name', 'EnumValueName', 'CopyToProto', '_SetOptions', 'GetOptions', '__dict__', '__weakref__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
message._message_descriptor.enum_types == 
<class 'google.protobuf.descriptor_pb2.MessageOptions'>
['DESCRIPTOR', '__module__', '__slots__', '_cached_byte_size', '_cached_byte_size_dirty', '_fields', '_is_present_in_parent', '_listener', '_listener_for_children', '_oneofs', '_unknown_fields', '__weakref__', '__doc__', '_decoders_by_tag', '__init__', 'MESSAGE_SET_WIRE_FORMAT_FIELD_NUMBER', 'message_set_wire_format', 'NO_STANDARD_DESCRIPTOR_ACCESSOR_FIELD_NUMBER', 'no_standard_descriptor_accessor', 'DEPRECATED_FIELD_NUMBER', 'deprecated', 'MAP_ENTRY_FIELD_NUMBER', 'map_entry', 'UNINTERPRETED_OPTION_FIELD_NUMBER', 'uninterpreted_option', 'Extensions', '_extensions_by_number', '_extensions_by_name', 'RegisterExtension', 'FromString', 'ListFields', 'HasField', 'ClearField', 'ClearExtension', 'HasExtension', '__eq__', '__str__', '__repr__', '__unicode__', 'ByteSize', 'SerializeToString', 'SerializePartialToString', '_InternalSerialize', 'MergeFromString', '_InternalParse', 'IsInitialized', 'FindInitializationErrors', 'MergeFrom', 'WhichOneof', '__reduce__', 'Clear', 'DiscardUnknownFields', '_SetListener', '_Modified', 'SetInParent', '_UpdateOneofState', '__deepcopy__', '__ne__', '__hash__', 'CopyFrom', 'ParseFromString', '__getstate__', '__setstate__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
<google.protobuf.internal.python_message._ExtensionDict object at 0x7ff026a0b490>
<google.protobuf.internal.python_message._ExtensionDict object at 0x7ff026a0b490>
['_extended_message', '__module__', '__doc__', '__init__', '__getitem__', '__eq__', '__ne__', '__hash__', '__setitem__', '_FindExtensionByName', '_FindExtensionByNumber', '__dict__', '__weakref__', '__repr__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
['DESCRIPTOR', '__module__', '__slots__', '_cached_byte_size', '_cached_byte_size_dirty', '_fields', '_is_present_in_parent', '_listener', '_listener_for_children', '_oneofs', '_unknown_fields', '__weakref__', '__doc__', '_decoders_by_tag', '__init__', 'MESSAGE_SET_WIRE_FORMAT_FIELD_NUMBER', 'message_set_wire_format', 'NO_STANDARD_DESCRIPTOR_ACCESSOR_FIELD_NUMBER', 'no_standard_descriptor_accessor', 'DEPRECATED_FIELD_NUMBER', 'deprecated', 'MAP_ENTRY_FIELD_NUMBER', 'map_entry', 'UNINTERPRETED_OPTION_FIELD_NUMBER', 'uninterpreted_option', 'Extensions', '_extensions_by_number', '_extensions_by_name', 'RegisterExtension', 'FromString', 'ListFields', 'HasField', 'ClearField', 'ClearExtension', 'HasExtension', '__eq__', '__str__', '__repr__', '__unicode__', 'ByteSize', 'SerializeToString', 'SerializePartialToString', '_InternalSerialize', 'MergeFromString', '_InternalParse', 'IsInitialized', 'FindInitializationErrors', 'MergeFrom', 'WhichOneof', '__reduce__', 'Clear', 'DiscardUnknownFields', '_SetListener', '_Modified', 'SetInParent', '_UpdateOneofState', '__deepcopy__', '__ne__', '__hash__', 'CopyFrom', 'ParseFromString', '__getstate__', '__setstate__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']


	
>>> shitoof = usermessages.CCSUsrMsg_ProcessSpottedEntityUpdate.SpottedEntityUpdate()
>>> shitoof.entity_idx
0
>>> shitoof.entity_idx = 1
>>> shitoof.entity_idx
1
>>> quit()




	'''







	
	# ListFields
	# DESCRIPTOR.fields

	#print([x.type for x in res])
	#input()
	#random_field = random.choice(res)

	random_field = prompt_for_field(res)


	# basically switch case for random_field
	field_type = random_field.type
	#print("field_type == "+str(field_type))


	# This won't work because for repeated submessages we need to do submessage.extend or stuff like that 

	# first pop the submessage, modify it, and then add it back.

	original_shit = copy.deepcopy(message)
	print("type(message) == "+str(type(message)))
	print("message == "+str(message))
	
	if len(message) > 0:

		message5 = message.pop()
	else:
		
		# need to create a new instance because the repeated field is empty

		print("Type of message: "+str(type(message)))
		print("Message fields: "+str(message.__dir__()))
		#print("Message fields: "+str(message.type))
		print("field_type == "+str(field_type))
		print("Random field: "+str(random_field))
		print("Random field: "+str(random_field.name))
		print("user_msg_type == "+str(user_msg_type))
		message.add()
		print("message == "+str(message))
		shitoof = message.pop()
		print("shitoof == "+str(shitoof))
		print(type(shitoof))
		#print(shitoof.name)
		print(shitoof.__dir__())
		print(shitoof.ListFields())
		message5 = shitoof
		# random_field.name is the name of the field which we would like to modify.
		'''
		['__module__', '__doc__', '__slots__', '__init__', 'add', 'extend', 'MergeFrom', 'remove', 'pop', '__getslice__', '__delitem__', '__delslice__', '__eq__', '_message_descriptor', '__hash__', '__slotnames__', '__getitem__', '__len__', '__ne__', '__repr__', 'sort', '_message_listener', '_values', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']


		['DESCRIPTOR', '__module__', '__slots__', '_cached_byte_size', '_cached_byte_size_dirty', '_fields', '_is_present_in_parent', '_listener', '_listener_for_children', '_oneofs', '_unknown_fields', '__weakref__', '__doc__', '_decoders_by_tag', '__init__', 'ENTITY_IDX_FIELD_NUMBER', 'entity_idx', 'CLASS_ID_FIELD_NUMBER', 'class_id', 'ORIGIN_X_FIELD_NUMBER', 'origin_x', 'ORIGIN_Y_FIELD_NUMBER', 'origin_y', 'ORIGIN_Z_FIELD_NUMBER', 'origin_z', 'ANGLE_Y_FIELD_NUMBER', 'angle_y', 'DEFUSER_FIELD_NUMBER', 'defuser', 'PLAYER_HAS_DEFUSER_FIELD_NUMBER', 'player_has_defuser', 'PLAYER_HAS_C4_FIELD_NUMBER', 'player_has_c4', '_extensions_by_number', '_extensions_by_name', 'RegisterExtension', 'FromString', 'ListFields', 'HasField', 'ClearField', '__eq__', '__str__', '__repr__', '__unicode__', 'ByteSize', 'SerializeToString', 'SerializePartialToString', '_InternalSerialize', 'MergeFromString', '_InternalParse', 'IsInitialized', 'FindInitializationErrors', 'MergeFrom', 'WhichOneof', '__reduce__', 'Clear', 'DiscardUnknownFields', '_SetListener', '_Modified', 'SetInParent', '_UpdateOneofState', '__deepcopy__', '__ne__', '__hash__', 'CopyFrom', 'ParseFromString', 'HasExtension', 'ClearExtension', '__getstate__', '__setstate__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']


		'''
	message = message5

	input()
		
	#print("Message popped: "+str(message5))

	#exit(1)



	
	if field_type == TYPE_STRING:

		original_string = getattr(message, random_field.name)
		new_string = mutate_string(original_string)
		setattr(message, random_field.name, str(new_string))
		return message, True
	if field_type == TYPE_BYTES:

		original_bytes= getattr(message, random_field.name)
		new_string = mutate_bytes(original_bytes)
		setattr(message, random_field.name, str(new_string))
		return message, True
	if field_type == TYPE_INT32:
		#print("rrrrrrrrrrrrrrrrrrrr")
		#original_integer = getattr(message, random_field.name)
		#message, _ = set_int(message, random_field)
		#print("Trying to mutate TYPE_INT32:")
		#print("Original message: ")
		#print(message)
		
		message, _ = set_int(message, random_field)
		#print("Succeeded. Now message is:")
		#print(message)
		return message, True
		
	if field_type == TYPE_MESSAGE:

		#print("Mutating submessage.")

		message2, result = mutate_submessage(getattr(message, random_field.name), user_msg_type=user_msg_type)
		message.random_field = message2
		return message, result
	
	


	#print("==============================================")
	#print(message)
	#print("==============================================")

	return message, False


def prompt_for_field(res):
	print("Please select a field by index.")
	print("Fields: "+str([thing.name for thing in res]))
	index = int(input("> "))
	return res[index]


def mutate_user_message(message, user_msg_type):
	print("Mutating user message.")
	#if random.random() > OWN_MUTATOR_CHANCE:
	#	return message, False

	res = [field for field in message.DESCRIPTOR.fields]

	#print([x.type for x in res])



	#random_field = random.choice(res)



	#while random_field.label == random_field.LABEL_REPEATED:
	#	random_field = random.choice(res)

	random_field = prompt_for_field(res)

	# basically switch case for random_field
	field_type = random_field.type
	#print("field_type == "+str(field_type))
	if field_type == TYPE_STRING:

		original_string = getattr(message, random_field.name)
		new_string = mutate_bytes(original_string)
		setattr(message, random_field.name, str(new_string))
		return message, True	
	if field_type == TYPE_BYTES:

		original_bytes= getattr(message, random_field.name)
		new_string = mutate_bytes(original_bytes)
		setattr(message, random_field.name, str(new_string))
		return message, True
	if field_type == TYPE_INT32:
		#print("rrrrrrrrrrrrrrrrrrrr")
		#original_integer = getattr(message, random_field.name)
		message, _ = set_int(message, random_field)
		#setattr(message, random_field.name, str(new_string))
		return message, True


	if field_type == TYPE_INT64:
		#print("rrrrrrrrrrrrrrrrrrrr")
		#original_integer = getattr(message, random_field.name)
		message, _ = set_int(message, random_field)
		#setattr(message, random_field.name, str(new_string))
		return message, True

	if field_type == TYPE_BOOL:

		message, _ = set_bool(message, random_field)

		return message, True
	
	if field_type == TYPE_MESSAGE:

		print("Mutating submessage.")

		message, result = mutate_submessage(getattr(message, random_field.name), user_msg_type=user_msg_type)
		return message, result
	


	'''
	if field_type == TYPE_MESSAGE:

		print("Mutating submessage.")

		message2, result = mutate_submessage(getattr(message, random_field.name))
		#message.random_field = message2

		print("random_field.name == "+str(random_field.name))

		try:
			setattr(message, random_field.name, message2)
			return message, result
		except:
			return message, False
	'''

	#print("==============================================")
	#print(message)
	#print("==============================================")

	return message, False
	

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



	if msg_type == "CSVCMsg_UserMessage":
		#print("Shitpoop:")
		#print(message.msg_type)
		#print(message.msg_data)

		# output the values of the user message bytes:




		#print("message.msg_type == "+str(message.msg_type))
		#function = getattr(usermessages, message.msg_type)

		if message.msg_type in usermessage_types:
			

			if not usermessage_types[message.msg_type] == "CCSUsrMsg_UpdateTeamMoney":
				#print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
				function = getattr(usermessages, usermessage_types[message.msg_type])
				#print("Type: "+str(usermessage_types[message.msg_type]))
				#print("message_type: "+str(message_type))
				message2 = function()
				skip = False
				try:

					message2.ParseFromString(message.msg_data)
				
				except:
					skip = True

				oof = True
				
				if not skip:

					message2, mutated = mutate_user_message(message2, usermessage_types[message.msg_type])
					
					#message.msg_data = message2.SerializeToString()
					if mutated:
						
						#print("Poopooshitoofoffffrferre")
						#print("len(message) == "+str(len(message)))

						message.msg_data = message2.SerializeToString()
						return message
				#if "AdjustMoney" in usermessage_types[message.msg_type]:

				#	print("Amount: "+str(message2.amount))

	res = [field for field in message.DESCRIPTOR.fields]
	#print(protofuzz._prototype_to_generator(res[0], None))

	#print(list(protofuzz._prototype_to_generator(res[0], None)))

	#print("all fields:")
	#print(res)

	#print("Length of res: "+str(len(res)))
	if len(res) != 0:

		#random_field = random.choice(res)
		
		# Get the selected field
		random_field = prompt_for_field(res)
		#print("Possible fields: "+str([thing.name for thing in res]))
		#print("Please give index of the field which you would like to modify:")
		#index = int(input("> "))
		#random_field = res[index]



	#print("protofuzz._prototype_to_generator(random_field.name, None) == "+str(protofuzz._prototype_to_generator(random_field, None)))
	#print("random_field: "+str(random_field))
	#print("poopoo: " + str(protofuzz._prototype_to_generator(random_field, gen.Product)))
	#print("Now trying the thing:")
	#print("List thing: "+str(list(protofuzz._prototype_to_generator(random_field, gen.Product))))
	#print("Done")
	#setattr(message, random_field.name, random.choice(list(protofuzz._prototype_to_generator(random_field, None))))
	mutated = False
	if len(res) != 0:

		message, mutated = mutate_field_thing(message, msg_type, random_field)


	if mutated:
		print(message)
		return message




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
	type_bytes = get_length_bytes(message_id) # the message_id ( which is also VarInt32 )
	#print("type bytes: "+str(type_bytes))
	if len(bytes(type_bytes)+bytes(len_bytes)+mut_msg_bytes) > max_size:
		#print("Returning this stuff:")
		#print("original_message: ")
		#print(original_message)
		print("Returning original message.")
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


'''

if __name__=="__main__":
	
	test_files = os.listdir("tests/") # hardcoded dir

	initialize_stuff()
	for _ in range(100):

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

	stuff = fuzz(bytes_buffer, 0, 10000)
	print("type of final stuff: "+str(type(stuff)))
	sys.stdout.buffer.write(bytes(stuff))
	# def fuzz(buf, add_buf, max_size):

	fh = open(output_file, "wb+")
	fh.write(stuff)
	fh.close()





