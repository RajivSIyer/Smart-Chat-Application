import select
import threading
from serversocket import serversocket
from clientthread import clientthread
from SmartChatConfig import smart_chat_config
import logging

class Server(object):
    def __init__(self):
        #Logging Setup
        #logging.basicConfig(filename='smartchat.log', encoding='utf-8', level=logging.DEBUG)
        self.logger = logging.getLogger('SmartChatServer')
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('smartchat.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(thread)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.info("Logger Created")
        #Server Initialization & Variables
        self.client_thread_list = []
        self.users_to_client_thread = {}
        self.socket_to_client_threads = {}
        self.server_socket = serversocket(cfg.server_ip, cfg.port)
        self.server_socket.initialize()
        self.server_socket.listen()

    def getUserThread(self, username):
        if username in self.users_to_client_thread:
            return self.users_to_client_thread[username]
        else:
            return None

    def getSocketThread(self, sock):
        if sock in self.socket_to_client_threads:
            return self.socket_to_client_threads[sock]
        else:
            return None

    def registerUser(self, name, client_thread):
        if name in self.users_to_client_thread:
            return False
        else:
            self.users_to_client_thread[name] = client_thread
            return True

    def removeinvalidclientthread(self, sock):
        client_thread =  self.getSocketThread(sock)
        if client_thread:
            client_name = client_thread.name
            self.socket_to_client_threads.pop(sock, None)
            self.users_to_client_thread.pop(client_name, None)


def listening_thread_func():
    global serv
    server_socket_list = []
    server_socket_list.append(serv.server_socket.socket)
    while True:
        ready_to_read,ready_to_write,in_error = select.select(server_socket_list,[],[],0)
        for sock in ready_to_read:
            client_sock, addr = sock.accept()
            serv.logger.info("New Client Connected. Client Thread created. : " + str(addr))
            client_t = clientthread(serv, client_sock, addr)
            serv.socket_to_client_threads[client_sock] = client_t
            serv.client_thread_list.append(client_t)
            client_sock.send(("You are connected from:" + str(addr[1])).encode('utf-8'))
            client_t.start()
try:
    cfg = smart_chat_config()
    serv = Server()
    serv.logger.info("Server Chat started Successfully. Version= "+str(cfg.version))
except Exception as e:
    serv.logger.critical("Fatal Error Occured! Couldn't start the server.\nException: ",e)
    exit(0)
t = threading.Thread(target= listening_thread_func)
t.start()
t.join()
serv.logger.info("Smart Chat Shutdown Successfully.")
server_socket.close()
