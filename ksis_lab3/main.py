import socket

# net data
HEADER = 64
# PORT = 13
PORT = 5051
# SERVER = '132.163.96.3'
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

# connection stuff
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print(client.recv(2048).decode())
