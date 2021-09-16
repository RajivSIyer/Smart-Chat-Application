import threading
import select

class clientthread(threading.Thread):
    def __init__(self, Serv, socket, ip_addr):
        threading.Thread.__init__(self)
        self.serv = Serv
        self.socket = socket
        self.name = ''
        self.ip_addr = ip_addr

    def run(self):
        client_socket_list = [self.socket]
        while True:
            try:
                ready_to_read,ready_to_write,in_error = select.select(client_socket_list,[],[],0)
                for sock in ready_to_read:
                    
                    data = sock.recv(2048)
                    data = data.decode('utf-8')
                    self.serv.logger.info("Recieved Message from " + self.name + ":" + str(data))
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
                        '''if sock in socket_to_client_threads:
                            from_user_t = socket_to_client_threads[sock]'''
                        to_user_t = self.serv.getUserThread(to_username)

                        if to_user_t:
                            message = data[data.index(':')+1:]
                            to_user_t.socket.send((str(self.name)+" says: "+message).encode('utf-8'))
                            self.serv.logger.info(str(self.name)+" said to "+to_user_t.name+':- '+message)
                        else:
                            sock.send(("User " + to_username + " is Unavailable.").encode('utf-8'))

                    else:
                        self.serv.logger.info(self.name+" send Invalid Command! "+data)
                        sock.send(("Invalid Command! "+data).encode('utf-8'))

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