import socket
from generator import generate
from random import randint

# net data
HEADER = 64
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

# packets data
SERVICE_MSG_SIZE = 24
packet_count = 1
packet_size = 409600
# init_value = randint(0, 65536)
init_value = 100
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

# connection stuff
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send_intro():
    intro = bytearray(SERVICE_MSG_SIZE)

    tick = SERVICE_MSG_SIZE // 3
    intro[:tick] = packet_size.to_bytes(tick, byteorder='little')
    intro[tick:2 * tick] = packet_count.to_bytes(tick, byteorder='little')
    intro[2 * tick:] = init_value.to_bytes(tick, byteorder='little')

    client.send(intro)
    response = client.recv(SERVICE_MSG_SIZE)
    if response == intro:
        print(f'Intro is already returned and all is ok')
    else:
        print("Intro is already returned, but doesn't match sent one")


rep_num = 100 * 1024


def send_data():
    # for pack in generate(packet_count, init_value):
    #     request = int.to_bytes(pack, packet_size, byteorder='little')
    #
    #     client.send(request)
    #     response = client.recv(packet_size)
    request = bytes()
    for i in generate(rep_num, init_value):
        request += int.to_bytes(i, 4, byteorder='little')

    client.send(request)
    response = client.recv(packet_size)


def receive_results():
    result_size = client.recv(SERVICE_MSG_SIZE)
    result_size = int.from_bytes(result_size, byteorder='little')
    # print(result_size)

    result = client.recv(result_size)
    result = result.decode('utf-8')

    return result


# send(str(datetime.now()))
send_intro()
send_data()
print(receive_results())
