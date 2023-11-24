
#protoc -I /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/ --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/netmessages.proto


protoc -I /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/ --python_out=. /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/netmessages.proto
protoc -I /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/ -I . --python_out=. ./cstrike15_usermessages.proto
protoc -I /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/ -I . --python_out=. ./cstrike15_gcmessages.proto
protoc -I /home/cyberhacker/Fuzzingpackets/Kisak-Strike/common/ -I . --python_out=. ./steammessages.proto

protoc -I . --python_out=. ./engine_gcmessages.proto

cp *.py ..
