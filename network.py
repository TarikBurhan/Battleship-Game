from battleships import *
import socket
import logging


class Network:
    """
    Class for TCP/IP protocol connection for server host and client join that have main functions.
    """
    def __init__(self, host, port, is_host):
        """
        :param host: Host ip address
        :param port: Port address
        :param is_host: Flag for whether player is a host or not
        """
        self.is_host = is_host
        self.sock = None
        self.conn = None

        # If player is a host, socket listens for connection from another socket.
        if self.is_host == True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((host, port))
            self.sock.listen()
            logging.debug("Server is listening on port.")
        # If player is not a host, socket connects to another socket which is a host.
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))

    def close(self):
        """
        Close socket and connection if there is
        """
        self.sock.close()
        if(self.conn != None):
            self.conn.close()

    def _server_send(self, packet):
        """
        Child send function for sending packet from host socket to connected socket.
        :param packet: Data needed to be send
        """
        self.conn.sendall(packet)
    
    def _client_send(self, packet):
        """
        Child send function for sending packet from socket to host socket.
        :param packet: Data needed to be send
        """
        self.sock.send(packet)

    def send(self, packet):
        """
        Parent send function for sending packet from one socket to another for both client and host.
        :param packet: Data needed to be send
        """
        if(self.is_host == True):
            return self._server_send(packet)
        else:
            return self._client_send(packet)

    def _server_receive(self):
        """
        Child receive function for getting a packet from socket that connected to host.
        """
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
        """
        Child receive function for getting a packet from socket which is a host.
        """
        data = self.sock.recv(16)
        return data

    def receive(self):
        """
        Parent receive function for getting a packet from one socket from another between host and client.
        """
        try:
            if(self.is_host == True):
                return self._server_receive()
            else:
                return self._client_receive()
        except Exception:
            self.close()
