# Importing Modules
import socket
import threading
import logging
from dotenv import load_dotenv
from os import getenv


# Server processing class
class Process:
    def __init__(self):
        
        load_dotenv()

        # Server details
        self.HOST = "0.0.0.0"
        self.PORT = 1234
        
        # DB details
        self.DB_HOST = "localhost"
        self.DB = "rsa_pychat"
        self.DB_USER = "rsa_pychat"
        self.DB_PASS = getenv("DBPASS")

        self.connections = []
        self.client = None

    def broadcast(self, message):  # Broadcasts a message to all connected clients.
        for connection in self.connections:
            connection.send(message)

    def global_messaging(self):  # Handles message intended for all users.
        for connection in self.connections:
            if not connection.messages:
                for message in connection.messages:
                    self.broadcast(message)

    def main(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            server.bind((self.HOST, self.PORT))
            logging.info(f"Running on {self.HOST}:{self.PORT}")

        except socket.error as msg:
            logging.critical('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

        server.listen()

        while True:
            self.client, address = server.accept()
            logging.debug(f"Connected to {address}")

            self.connections.append(Client(self.client, address))
            self.connections[-1].start()
            logging.info(f"Active connections {len(self.connections)}")


class Client:
    def __init__(self, client, address):
        self.socket = client
        self.address = address
        self.messages = []
        self.name = ""

    def __rec(self):
        self.name = message = self.socket.recv(2048).decode("utf-8")
        while True:
            message = ""

            message = self.socket.recv(2048).decode("utf-8")
            while "`,#" not in message:
                message += self.socket.recv(2048).decode("utf-8")

            message = message.replace("`,#", "")

            self.messages.append(message)

    def send(self, message):
        message += "`,#"
        self.socket.sendall(message.encode("utf-8"))

    def start(self):
        thread = threading.Thread(target=self.__rec)
        thread.start()
        logging.debug(f"Started thread for {self.address}")


if __name__ == "__main__":
    m = Process()
    m.main()
