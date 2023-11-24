
from protofuzz import protofuzz
import netmessages_pb2 as proto
from google.protobuf.any_pb2 import Any


message = proto.CMsg_CVars

print(message.DESCRIPTOR.fields[0].cvars)

