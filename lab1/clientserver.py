"""
Client and server using classes
"""

import logging
import socket
import time

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    _database = {'annette': "1234",
                 'jack': "4098",
                 'peter': "5678",
                 'sape': "4139",
                 'björn' : "7392732937"
                 }

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped
                    connection.send(data + "*".encode('utf-8'))  # return sent data plus an "*"
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")
    
    def start_phone_book(self):
        """Start Server to send phone book records"""
        self.sock.listen(1)
        print("Listening for connection")
        while self._serving:
            try:
                (connection, address) = self.sock.accept()
                print("Connection established")
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8')
                    if message == "getAll" :
                        # task recieved to print out all records of database
                        message_out = ""
                        for k, v in self._database.items():
                            message_out += str(k) + ": " + str(v) + "\n"
                        print("Sending Data")
                        connection.send(message_out.encode("utf-8"))
                    else :
                        if message not in self._database:
                            # name not in the database
                            print("No Entries found")
                            connection.send("end".encode("utf-8"))
                        else:
                            # name in the database, ready to send
                            message_out = str(message) + ": " + str(self._database[message])
                            print("Sending Data")
                            connection.send(message_out.encode("utf-8"))
                print("Closing Connection")
                connection.close()
            except socket.timeout:
                pass
        self.sock.close()
        print("Server down.")


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        """ Call server """
        self.sock.send(msg_in.encode('utf-8'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('utf-8')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def get(self, name):
        """ Get a phone book record"""
        self.logger.info("Requesting Data")
        self.sock.send(name.encode('utf-8'))
        data = self.sock.recv(1024)
        result = data.decode('utf-8')
        if (result == "end"):
            print("Error404: Name not found")
        else:
            print(result)
        self.sock.close()
        return result
       
    def get_all(self):
        """ Get all phone book records"""
        name = "getAll"
        self.logger.info("Requesting Data")
        self.sock.send(name.encode('utf-8'))
        data = self.sock.recv(1024)
        result = data.decode('utf-8')
        print(result)
        self.sock.close()
        return result


    def close(self):
        """ Close socket """
        self.sock.close()