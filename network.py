from battleships import *
import socket
import logging


class Network:
    def __init__(self, host, port, is_host):
        self.is_host = is_host
        self.sock = None
        self.conn = None

        if self.is_host == True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((host, port))
            self.sock.listen()
            logging.debug("Server is listening on port.")
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))

    def close(self):
        self.sock.close()
        if(self.conn != None):
            self.conn.close()

    def _server_send(self, packet):
        self.conn.sendall(packet)
    
    def _client_send(self, packet):
        self.sock.send(packet)

    def send(self, packet):
        if(self.is_host == True):
            return self._server_send(packet)
        else:
            return self._client_send(packet)

    def _server_receive(self):
        if self.conn == None:
            while True:
                logging.debug("Waiting for an opponent to join.")
                self.conn, self.addr = self.sock.accept()
                break

        logging.debug("Waiting for an action from opponent.")
        while True:
            data = self.conn.recv(16)
            if not data:
                break
            return data
    
    def _client_receive(self):
        data = self.sock.recv(16)
        return data

    def receive(self):
        try:
            if(self.is_host == True):
                return self._server_receive()
            else:
                return self._client_receive()
        except Exception:
            self.close()

def prepare_move(x, y):
    return 1
def decode_data(data):
    return 0
