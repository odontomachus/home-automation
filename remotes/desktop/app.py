import bluetooth
import time
import socket

NAME="lls"
ADDRESS="20:13:07:26:03:86"
PORT = 1

class ConnectionError(Exception):
    pass

class App:
    def __init__(self):
        self._get_socket()

    def __enter__(self):
        return self

    def get_socket(self):
        """
        Try and make sure the bluetooth connection is open and alive.
        """
        num_tries = 4
        for i in range(num_tries):
            try:
                self.socket.send("?")
                self.socket.recv(1024)
                break
            except Exception as e:
                if i > 0:
                    time.sleep(1)
                if i < num_tries - 1:
                    self._get_socket()
                else:
                    raise ConnectionError("Could not connect to bluetooth.")

    def _get_socket(self):
        try:
            self.socket.close()
        except:
            pass

        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.settimeout(0.3)
        # This sometimes throws errors but still works
        try:
            self.socket.connect((ADDRESS, PORT))
        except:
            pass
        time.sleep(1)
        for i in range(10):
            try:
                self.socket.send("?")
                time.sleep(.5)
                self.socket.recv(1024)
                break
            except Exception as e:
                if i == 4:
                    raise
                time.sleep(2)

    def toggle(self):
        self.get_socket()
        self.socket.send("T")

    def status(self):
        self.get_socket()
        self.socket.send("?")
        b = self.socket.recv(1024)
        return b==b'1'

    def __exit__(self, type, value, traceback):
        self.socket.close()

