import socket
import threading
from datetime import datetime
from generator import generate


class TCPServer:
    def __init__(self):
        # net data
        PORT = 5050
        self.SERVICE_MSG_SIZE = 24
        SERVER = '127.0.0.1'
        ADDR = (SERVER, PORT)

        # server binding
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.rep_num = 100 * 1024

        # measure
        self.packet_size = None
        self.packets_count = None
        self.init_value = None
        self.total_time = None
        self.total_received = None

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            self.receive_intro(conn)
            self.measure(conn)
            self.send_result(conn)
            connected = False

    def receive_intro(self, conn):
        intro = conn.recv(self.SERVICE_MSG_SIZE)

        tick = self.SERVICE_MSG_SIZE // 3
        self.packet_size = int.from_bytes(intro[:tick], byteorder='little')
        self.packets_count = int.from_bytes(intro[tick:2 * tick], byteorder='little')
        self.init_value = int.from_bytes(intro[2 * tick:], byteorder='little')

        print("Intro:")
        print("s: {} bytes".format(self.packet_size))
        print("c: " + str(self.packets_count))
        print("i: " + str(self.init_value))
        print("-" * 10)
        conn.send(intro)

    def measure(self, conn):
        self.total_time = 0
        self.total_received = 0
        start_time = last_time = datetime.now()

        # for check in generate(self.packets_count, self.init_value):
        #     req = conn.recv(self.packet_size)
        #     conn.send(req)
        #
        #     last_time = datetime.now()
        #
        #     req = int.from_bytes(req, byteorder='little')
        #     if req == check:
        #         self.total_received += 1
        #
        # self.total_time = last_time - start_time
        req = conn.recv(self.packet_size)
        conn.send(req)
        last_time = datetime.now()
        request = int.from_bytes(req, byteorder='little')
        check = bytes()
        for i in generate(self.rep_num, self.init_value):
            check += int.to_bytes(i, 4, byteorder="little")
        check = int.from_bytes(check, byteorder="little")
        if request == check:
            self.total_received += 1

        self.total_time = last_time - start_time

    def send_result(self, conn):
        self.total_time = self.total_time.seconds * 10 ** 6 + self.total_time.microseconds
        self.total_time = 1 if self.total_time == 0 else self.total_time
        result = "Packets received:\t{}/{}\n".format(self.total_received, self.packets_count)
        result += "Packets lost:\t{}\n".format(self.packets_count - self.total_received)

        full_size = self.packet_size * self.packets_count
        result += "Overall size:\t{} bytes\n".format(full_size)
        result += "Overall time:\t{} mcsec\n".format(self.total_time)

        speed = ((full_size // 1024) / self.total_time) * 10 ** 6  # in KB/sec
        result += "Speed:\t~{0:.2f} KB/sec\n".format(speed)

        print(result)

        result = bytearray(result, encoding='utf-8')

        msg = len(result).to_bytes(self.SERVICE_MSG_SIZE, byteorder='little')
        conn.send(msg)
        conn.send(result)

    def start(self):
        self.server.listen()
        print("[LISTENING]")
        while True:
            conn, addr = self.server.accept()
            self.handle_client(conn, addr)
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("Starting...")
myServer = TCPServer()
myServer.start()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
