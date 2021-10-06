import socket
import logging
import threading
import protocol as p
from ClientConfig import clientconfig
from ClientCredentials import ClientCredentials
from Session import Session
from CliThread import ClientThread

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

class Client(object):

    def __init__(self):
        self.logger = logging.getLogger('SmartChatClient')
        self.request_cnt = 0
        self.cfg = clientconfig()
        self.clientthreadobj = ClientThread(self.cfg.server_ip, self.cfg.port, self.cfg.version)
        #connect to server
        self.clientthreadobj.connect()
        self.clientthreadobj.start()
        self.bLogged = False

    def login_toServer(self):
        self.bLogged = False
        username = ''
        password = ''
        while not self.bLogged:
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
            if self.clientthreadobj.waitforloginEvent() == False:
                    self.logger.warning("\nServer TimeOut Occurred!Retrying Login...")
                    username = ''
                    password = ''
            else:
                reponse_object = self.clientthreadobj.respdict.pop(request.req_id)
                if reponse_object.resp_code == p.RESPCODE_OK:
                    self.bLogged = True
                elif reponse_object.resp_code == p.RESPCODE_LOGIN_INVALIDPASSWD:
                    password = ''
                else:
                    username = ''
                    password = ''
                

    def run(self): 
        self.request_cnt += 1
        request = p.request(p.CMD_CONN, self.request_cnt, '')
        self.clientthreadobj.send(request.to_Json())
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