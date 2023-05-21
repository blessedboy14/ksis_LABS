import socket
from datetime import datetime
from generator import generate


class UDPServer:
    def __init__(self):
        PORT = 5051
        self.SERVICE_MSG_SIZE = 24
        # SERVER = socket.gethostbyname(socket.gethostname())
        SERVER = '192.168.43.76'
        ADDR = (SERVER, PORT)

        # server binding
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(ADDR)

        # packets data
        self.packet_size = None
        self.packets_count = None
        self.init_value = None
        self.rep_num = 100

        # time stuff
        self.total_time = None
        self.total_received = 0

    def receive_intro(self):
        intro, address = self.server.recvfrom(self.SERVICE_MSG_SIZE)

        tick = self.SERVICE_MSG_SIZE // 3
        self.packet_size = int.from_bytes(intro[:tick], byteorder='little')
        self.packets_count = int.from_bytes(intro[tick:2 * tick], byteorder='little')
        self.init_value = int.from_bytes(intro[2 * tick:], byteorder='little')

        print("Intro:")
        print("s: {} bytes".format(self.packet_size))
        print("c: " + str(self.packets_count))
        print("i: " + str(self.init_value))
        print("-" * 15)
        self.server.sendto(intro, address)

    def measure(self):
        self.total_time = 0
        self.total_received = 0
        start_time = last_time = datetime.now()
        address = None
        # for check in generate(self.packets_count, self.init_value):
        #     req, address = self.server.recvfrom(self.packet_size)
        #     self.server.sendto(req, address)
        #
        #     last_time = datetime.now()
        #
        #     req = int.from_bytes(req, byteorder='little')
        #     if req == check:
        #         self.total_received += 1
        for pack_num in range(self.packets_count):
            req, address = self.server.recvfrom(self.packet_size)
            self.server.sendto(req, address)
            last_time = datetime.now()
            request = int.from_bytes(req, byteorder='little')
            check = bytes()
            for i in generate(self.rep_num, self.init_value):
                check += int.to_bytes(i, 4, byteorder="little")
            check = int.from_bytes(check, byteorder="little")
            if request == check:
                self.total_received += 1

        self.total_time = last_time - start_time
        return address

    def send_result(self, addr):
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
        self.server.sendto(msg, addr)
        self.server.sendto(result, addr)

    def run(self):
        while True:
            self.receive_intro()
            addr = self.measure()
            if addr:
                self.send_result(addr)
            else:
                print("Error with measure and address!")


myServer = UDPServer()
myServer.run()
