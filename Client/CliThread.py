import socket
import logging
import threading
import protocol as p
from ClientConfig import clientconfig
from ClientCredentials import ClientCredentials
from Session import Session

class ClientThread(threading.Thread):

    def __init__(self, server_ip, port, version):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger('SmartChatClient')
        self.server_ip = server_ip
        self.port = port
        self.version = version
        self.client_socket = ''
        self.sesh = None
        #self.bRetry = True
        self.login_event = threading.Event()
        self.creds = None
        self.respdict = {}

    def connect(self):
        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_ip,self.port))

    def handleserverdata(self, json_data):
        self.logger.info("Recieved Server Raw Message:\n" + str(json_data))
        server_response = p.response.from_Json(json_data)
    
        if str(server_response.cmd).upper() == p.CMD_CONN:
            self.logger.info("Received permit response to connect:\n"+server_response.cmd+"\nRequest Id: "+str(server_response.req_id))
        elif str(server_response.cmd).upper() == p.CMD_LOGIN:
            if server_response.resp_code == p.RESPCODE_OK:
                self.sesh = Session.from_Json(server_response.payload)
                
            self.logger.info(server_response.msg)
            self.respdict[server_response.req_id] = server_response
            print(server_response.msg)
            self.login_event.set()
            self.login_event.clear()

    def getSesh(self):
        return self.sesh

    def waitforloginEvent(self):
        return self.login_event.wait(10)

    def run(self):
        bool_exit = False
        self.client_socket.settimeout(2)
        while True:
            if bool_exit:
                break
            try:
                raw_recv_msg = self.client_socket.recv(1024)
                if len(raw_recv_msg) > 0:
                    raw_recv_msg = raw_recv_msg.decode('utf-8')
                    self.handleserverdata(raw_recv_msg)

            except socket.timeout:
                continue
            except Exception as e:
                print(e)
                continue

    def send(self, raw_data):
        self.client_socket.send(raw_data.encode('utf-8'))

    def cleanUp(self):
        self.client_socket.close()