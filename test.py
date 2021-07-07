import socket
import threading

RECV_LEN = 10

def reader():
    HOST = 'localhost'
    PORT = 5555
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            print(s.recv(RECV_LEN))
            s.sendall(b'0')

def writer():
    HOST = 'localhost'
    PORT = 6666
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            s.sendall(RECV_LEN * b'a')
            s.recv(1)

th1 = threading.Thread(target=reader, daemon=True)
th2 = threading.Thread(target=writer, daemon=True)

th1.start()
th2.start()

th1.join()
th2.join()
