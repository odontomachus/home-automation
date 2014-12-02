import bluetooth
import time
import socket


class ConnectionError(Exception):
    pass

class App:
    self.port = 1

    def __init__(self):
        self._get_socket()

    def __enter__(self):
        return self

    def get_socket(self):
        """
        Try and make sure the bluetooth connection is open and alive.
        """
        num_tries = 6
        # Try and access the socket a few times, then try and get a
        # new socket if that fails
        for i in range(num_tries):
            try:
                self.socket.send("?")
                self.socket.recv(1024)
                break
            except Exception as e:
                # wait, it might just be busy
                if i > 0:
                    time.sleep(1)
                # Try and get a new socket
                if (i > 3) and (i < num_tries - 1):
                    self._get_socket()
                # fail
                elif i == num_tries - 1:
                    raise ConnectionError("Could not connect to bluetooth.")

    def _get_socket(self):
        """
        Try and get a new socket.
        """
        try:
            self.socket.close()
        except:
            pass

        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.settimeout(0.3)
        # This sometimes throws errors but still works
        try:
            self.socket.connect((self.address, self.port))
        except:
            pass
        time.sleep(1)
        # Give the socket a bit of time to come online. Bluetooth is fickle.
        num_tries = 10
        for i in range(num_tries):
            try:
                self.socket.send("?")
                time.sleep(.5)
                self.socket.recv(1024)
                break
            except Exception as e:
                if i == num_tries - 1:
                    raise
                time.sleep(2)

    def __exit__(self, type, value, traceback):
        print("Closing socket")
        self.socket.close()

class LivingRoomSwitch(App):
    self.address="20:13:07:26:03:86"

    def toggle(self):
        self.get_socket()
        self.socket.send("T")

    def status(self):
        self.get_socket()
        self.socket.send("?")
        b = self.socket.recv(1024)
        return b==b'1'

class BedRoomSwitch(App):
    self.address="30:14:07:03:07:80"

    def on(self):
        self.get_socket()
        self.socket.send("f")

    def off(self):
        self.get_socket()
        self.socket.send("h")

    def side(self, side, val):
        try:
            assert(side in ['l', 'r'])
            val = int(val)
            val = min(val, 255)
            val = max(val, 0)
        except:
            return False
        self.get_socket()
        self.socket.send(side)
        self.socket.send(val)

    def status(self):
        self.get_socket()
        self.socket.send("q")
        b = self.socket.recv(1024)
        try:
            res = (ord(b[0]), ord(b[1]))
        except:
            res = (0,0)
        return res
