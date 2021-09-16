import socket
import threading

bool_exit = False

def recvmsgthread():
    client_socket.settimeout(2)
    while True:
        if bool_exit:
            break
        try:
            recv_msg = client_socket.recv(1024)
            if len(recv_msg) > 0:
                recv_msg = recv_msg.decode('utf-8')
                print("\n")
                print(recv_msg)
        except socket.timeout:
            continue
        except Exception as e:
            print(e)
            continue

client_socket = socket.socket()
port = 12345
client_socket.connect(('192.168.1.107',port))
#recieve connection message from server
recv_msg = client_socket.recv(1024)
recv_msg = recv_msg.decode('utf-8')
print(recv_msg)
#send user details to server
send_msg = input("Enter your user name(prefix with #):")
client_socket.send(send_msg.encode('utf-8'))
#receive and send message from/to different user/s
recv_msg = client_socket.recv(1024)
recv_msg = recv_msg.decode('utf-8')
print(recv_msg)
t = threading.Thread(target = recvmsgthread)
#t.setDaemon(True)
t.start()

while True:
    send_msg = input("Send your message in format [@user:message] ")
    if str(send_msg) == 'exit':
        bool_exit = True
        t.join()
        break
    else:
        client_socket.send(send_msg.encode('utf-8'))

client_socket.close()