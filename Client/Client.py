import socket
import logging
import threading
import protocol as p
from ClientConfig import clientconfig
import ClientCredentials
import Session

def setupLogger():
        #Logging Setup
        #logging.basicConfig(filename='smartchat.log', encoding='utf-8', level=logging.DEBUG)
        logger = logging.getLogger('SmartChatClient')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('SmartChatClient.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(thread)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        #logger.addHandler(ch)
        logger.info("Logger Created")

class ClientThread(threading.Thread):

    def __init__(self, server_ip, port, version):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger('SmartChatClient')
        self.server_ip = server_ip
        self.port = port
        self.version = version
        self.client_socket = ''
        self.sesh = None
        self.bLogged = False
        self.bRetry = True

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
                self.bLogged = True
                self.bRetry = False
                self.logger.info(server_response.msg)
            elif server_response.resp_code == p.RESPCODE_LOGIN_INVALIDUSER:
                self.bLogged = False
                self.bRetry = True
                self.logger.info(server_response.msg)
            elif server_response.resp_code == p.RESPCODE_LOGIN_INVALIDPASSWD:
                self.bLogged = False
                self.bRetry = True
                self.logger.info(server_response.msg)
            else:
                self.bLogged = False
                self.bRetry = True
                self.logger.info(server_response.msg)

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

class Client(object):

    def __init__(self):
        self.logger = logging.getLogger('SmartChatClient')
        self.request_cnt = 0
        self.cfg = clientconfig()
        self.clientthreadobj = ClientThread(self.cfg.server_ip, self.cfg.port, self.cfg.version)
        #connect to server
        self.clientthreadobj.connect()
        self.clientthreadobj.start()

    def login_toServer(self):
        username = ''
        password = ''
        while username == '':
            username = input("Enter your Username: ")
            username = username.strip()
        while password == '':
            password = input("Enter your Password: ")
            password = password.strip()
        cred = ClientCredentials(username, password)
        self.request_cnt += 1
        request = p.request(p.CMD_LOGIN, self.request_cnt, cred.to_Json())
        request_JsonStr = request.to_Json()
        self.logger.info("Sending Login request to Server:\n"+request_JsonStr)
        self.clientthreadobj.send(request_JsonStr)
        self.logger.info("Logging In...")

    def run(self): 
        self.request_cnt += 1
        request = p.request(p.CMD_CONN, self.request_cnt, '')
        self.clientthreadobj.send(request.to_Json())
        while self.clientthreadobj.bRetry:
            self.login_toServer()
        while True:
            send_msg = input("Send your message in format [@user:message] ")
            if str(send_msg) == 'exit':
                bool_exit = True
                self.clientthreadobj.join()
                break
            else:
                self.clientthreadobj.send(send_msg)

        self.clientthreadobj.cleanUp()

if __name__ == '__main__':
    try:
        setupLogger()
        c = Client()
        c.run()
    except Exception as e:
        print("Exception Occurred. Fatal Error! : ",str(e))