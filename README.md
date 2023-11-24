
# ProtoFuzz

This project is based on this: https://github.com/trailofbits/protofuzz

This is just a program which I quickly wrote to fuzz the protobuf messages sent between the server and the client in CS:GO . The generate_corpus.py file is used to generate a custom fuzzing corpus of your choice. There is a list of available message types and then you can filter out the ones that you want. For example if you only want to get the CSVCMsg_PacketEntities messages, then you should add everything else other than that type to the ban list.




