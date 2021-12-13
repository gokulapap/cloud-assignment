import socket
import pickle
import time
import threading

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = "127.0.0.1"
header = 20
port = 5000
bind = (ip, port)
Format = "utf-8"
client.connect(bind)
print(socket.gethostbyname(socket.gethostname()))

def receive_msg():
    msg_len = client.recv(header).decode(Format)
    msg = client.recv(int(msg_len)).decode(Format)
    print(msg)
    print("data received")
    receive_msg()

def send_msg():
    data = str(input())
    data_len = str(len(data))
    data_len = data_len.encode(Format)
    data_len += b' '*(header-len(data_len))
    client.send(data_len)
    data=data.encode(Format)
    client.send(data)
    print(f"The data was sent to : {ip}")
    send_msg()

print("connected")

if __name__=="__main__":
    try:
        thread_send_data = threading.Thread(target=send_msg)
        thread_rec_data = threading.Thread(target=receive_msg)
        thread_send_data.start()
        thread_rec_data.start()
    except:
        print("some error occured")
