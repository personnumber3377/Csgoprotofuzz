
from protofuzz import protofuzz
import netmessages_pb2 as proto
from google.protobuf.any_pb2 import Any


message = proto.CMsg_CVars()

cvar = message.cvars.add()
cvar.name = "thingoof"
cvar.value = "ferrgre"
cvar.dictionary_name = 123
for thing in message.cvars:
	print(thing)

