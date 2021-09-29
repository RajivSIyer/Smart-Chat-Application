import socket
class serversocket(object):
    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port
        self.socket = None

    def initialize(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip_addr,self.port))

    def listen(self):
        try:
            if self.socket != None:
                self.socket.listen(5)
            else:
                raise Exception("Server socket Uninitialized! Cannot listen!")
        except Exception as e:
            print(e)
            raise e
