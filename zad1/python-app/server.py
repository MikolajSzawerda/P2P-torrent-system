import socket
import sys

HOST = '127.0.0.1'
BUFSIZE = 1024

INFO_MSG = "You have sent proper message"
ERROR_MSG = "Your message does not obey contract!"

try:
    port = int(sys.argv[1])
except:
    print("Error in port number")
    sys.exit(1)

print("Will listen on port ", port)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, port))
    i = 1
    while True:
        data_address = s.recvfrom(BUFSIZE)
        data = data_address[0]
        address = data_address[1]
        print("Message from Client:{}".format(data))

        if not data:
            print("Error in datagram?")
            break

        s.sendto(INFO_MSG.encode(), address)
        print('sending dgram #', i)
        i += 1
