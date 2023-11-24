
#protoc -I /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/ --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/netmessages.proto


protoc -I /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/ -I . --python_out=. ./cstrike15_usermessages.proto
