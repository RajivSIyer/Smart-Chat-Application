import threading
import select
import protocol as p
import ClientCredentials
import User
import Session
import uuid
class clientthread(threading.Thread):
    def __init__(self, Serv, socket, ip_addr):
        threading.Thread.__init__(self)
        self.serv = Serv
        self.socket = socket
        self.name = ''
        self.ip_addr = ip_addr

    def handleclientrequest(self, json_data):
        self.serv.logger.info("Recieved Client Raw Message:\n" + str(json_data))
        client_request = p.request.from_Json(json_data)

        if str(client_request.cmd).upper() == p.CMD_CONN:
            response = p.response(p.CMD_CONN, p.RESPCODE_OK, client_request.req_id, "You are connected from:" + str(self.ip_addr), '')
            resp_to_json = response.to_Json()
            self.send(resp_to_json)
            self.serv.logger.info("Sent Message:\n"+resp_to_json)

        elif str(client_request.cmd) == p.CMD_LOGIN:
            clientcreds = ClientCredentials.from_Json(client_request.payload)
            self.handleloginrequest(client_request, clientcreds)

    def handleloginrequest(self, client_request, clientcreds: ClientCredentials):
        self.serv.logger.info("Username: "+clientcreds.username+"\nPassword: "+clientcreds.passwd)
        try:
            u = self.serv.db_obj.query_oneUser_byname(clientcreds.username)
            if u == None:
                self.serv.logger.info("Username "+clientcreds.username+" does not exist in database!")
                response = p.response(p.CMD_LOGIN, p.RESPCODE_LOGIN_INVALIDUSER, client_request.req_id, "User Not Found: " + str(clientcreds.username), '')
            else:
                if u.Passwd != clientcreds.passwd:
                    self.serv.logger.info("Incorrect Password entered by: "+clientcreds.username)
                    response = p.response(p.CMD_LOGIN, p.RESPCODE_LOGIN_INVALIDPASSWD, client_request.req_id, "Invalid Password", '')
                else:
                    sesh = Session(uuid.uuid1())
                    self.serv.logger.info("Successfully Logged In!")
                    response = p.response(p.CMD_LOGIN, p.RESPCODE_OK, client_request.req_id, "Successfully Logged In!", sesh.to_Json())
                    
        except Exception as e:
            self.serv.logger.info("Database Error!",str(e))
            response = p.response(p.CMD_LOGIN, p.RESPCODE_INTERNAL_SERVER_ERROR, client_request.req_id, 'Database Error!', '')
        response_JsonStr = response.to_Json()
        self.serv.logger.info("Login Response Sent:\n"+response_JsonStr)
        self.send(response_JsonStr)
        '''
        if data.startswith("#"):
            self.name = data[1:].lower()
            if self.serv.registerUser(self.name, self):
                #print("User " + data[1:] +" added.")
                self.serv.logger.info("User " + data[1:] +" added.")
                sock.send(("Your user detail saved as : "+str(data[1:])).encode('utf-8'))
            else:
                self.serv.logger.info("User " + data[1:] +" already exists. Registration Failed!")
                sock.send(("A User by the name "+ str(data[1:]) + " is already logged in. Choose another name.").encode('utf-8'))
        elif data.startswith("@"):
            to_username = data[1:data.index(':')].lower()
            #print(to_username)
            self.serv.logger.info("To User- " + to_username)
            #if sock in socket_to_client_threads:
                #from_user_t = socket_to_client_threads[sock]
            to_user_t = self.serv.getUserThread(to_username)

            if to_user_t:
                message = data[data.index(':')+1:]
                to_user_t.socket.send((str(self.name)+" says: "+message).encode('utf-8'))
                self.serv.logger.info(str(self.name)+" said to "+to_user_t.name+':- '+message)
            else:
                sock.send(("User " + to_username + " is Unavailable.").encode('utf-8'))

        else:
            self.serv.logger.info(self.name+" send Invalid Command! "+data)
            sock.send(("Invalid Command! "+data).encode('utf-8'))'''
            
    def send(self, raw_data):
        self.socket.send(raw_data.encode('utf-8'))   

    def run(self):
        client_socket_list = [self.socket]
        while True:
            try:
                ready_to_read,ready_to_write,in_error = select.select(client_socket_list,[],[],0)
                for sock in ready_to_read:
                    data = sock.recv(2048)
                    data = data.decode('utf-8')
                    self.handleclientrequest(data)

            except (ConnectionError, BrokenPipeError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError) as ce:
                self.serv.logger.error(str(ce))
                self.serv.logger.error(str(type(ce)))
                self.serv.logger.error("Muhammad-e-Akbar")
                self.serv.removeinvalidclientthread(self.socket)
                break

            except Exception as e:
                self.serv.logger.error(str(e))
                self.serv.logger.error(str(type(e)))
                self.serv.logger.error("Allah Hu Akbar")
                break
