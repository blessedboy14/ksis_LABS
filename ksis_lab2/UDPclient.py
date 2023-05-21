import socket
from random import randint
from generator import generate

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# SERVER = socket.gethostbyname(socket.gethostname())\
SERVER = '192.168.43.76'
PORT = 5051
ADDR = (SERVER, PORT)

# packets data
SERVICE_MSG_SIZE = 24
packet_count = 8192
packet_size = 400
rep_num = 100
# init_value = randint(0, 65536)
init_value = 100
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


def send_intro():
    intro = bytearray(SERVICE_MSG_SIZE)

    tick = SERVICE_MSG_SIZE // 3
    intro[:tick] = packet_size.to_bytes(tick, byteorder='little')
    intro[tick:2 * tick] = packet_count.to_bytes(tick, byteorder='little')
    intro[2 * tick:] = init_value.to_bytes(tick, byteorder='little')

    client.sendto(intro, ADDR)
    response = client.recvfrom(SERVICE_MSG_SIZE)[0]

    if response == intro:
        print(f'Intro is already returned and all is ok')
    else:
        print("Intro is already returned, but doesn't match sent one")


def send_data():
    # for pack in generate(packet_count, init_value):
    #     request = int.to_bytes(pack, packet_size, byteorder='little')
    #
    #     client.sendto(request, ADDR)
    #     response, address = client.recvfrom(packet_size)
    for pack_num in range(packet_count):
        request = bytes()
        for i in generate(rep_num, init_value):
            request += int.to_bytes(i, 4, byteorder='little')

        client.sendto(request, ADDR)
        response, address = client.recvfrom(packet_size)


def receive_results():
    result_size = client.recvfrom(SERVICE_MSG_SIZE)[0]
    result_size = int.from_bytes(result_size, byteorder='little')
    # print(result_size)

    result = client.recvfrom(result_size)[0]
    result = result.decode('utf-8')

    return result


send_intro()
send_data()
print(receive_results())
