import math
import socket
import threading
from datetime import datetime


def get_julian_datetime(date):
    if not isinstance(date, datetime):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julian_datetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0) + int(
        (275 * date.month) / 9.0) + date.day + 1721013.5 + (
                              date.hour + date.minute / 60.0 + date.second / math.pow(60,
                                                                                      2)) / 24.0 - 0.5 * math.copysign(
        1, 100 * date.year + date.month - 190002.5) + 0.5

    return julian_datetime


class DTServer:
    def __init__(self):
        PORT = 5051
        self.SERVICE_MSG_SIZE = 24
        SERVER = '127.0.0.1'
        ADDR = (SERVER, PORT)

        # server binding
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            l_koef = 0
            tt = 61
            health = 0  # seems good
            sub_str = " UTC(NIST) * "
            time = datetime.utcnow()
            added_time = datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, time.microsecond
                                  + 50)
            res = "\n" + str(math.floor(get_julian_datetime(datetime.now()) - 2400000.5)) + \
                  " " + str(added_time)[2:-7] + " " + str(tt) + " " + str(l_koef) + " " + str(health) + " " + \
                  str(50.0) + sub_str
            conn.send(res.encode())
            connected = False

    def run(self):
        self.server.listen()
        print("[LISTENING]")
        while True:
            conn, addr = self.server.accept()
            self.handle_client(conn, addr)
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


myServer = DTServer()
myServer.run()
