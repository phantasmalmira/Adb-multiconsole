import socket
import subprocess
import platform
import argparse
import time

class Sender(object):
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queue_send = []
        while True:
            try:
                self.sock.connect(('localhost', self.port))
                break
            except ConnectionRefusedError:
                pass

    def send(self, _msg):
        _msg = bytes(_msg, encoding='utf-8')
        self.queue_send.append(_msg)
        self.send_queue()

    def send_queue(self):
        try:
            while self.queue_send:
                self.sock.sendall(self.queue_send[0])
                self.queue_send.pop(0)
        except ConnectionResetError:
            # stop sending temporarily since it has lost connection to the console
            pass         

class Receiver(object):
    def __init__(self, port):
        if platform.system().lower() == 'windows':
            subprocess.call('', shell=True)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', self.port))
        try:
            self.sock.listen()
            self.conn, self.addrs = self.sock.accept()
            self.receive()
        except KeyboardInterrupt:
            pass
        
    def receive(self):
        while True:
            try:
                data = self.conn.recv(1024).decode('utf-8') 
                if data:
                    print(data)
            except KeyboardInterrupt:
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        metavar=('LISTENING_PORT'),
                        help='Specify PORT to listen to'
                        )
    args = parser.parse_args()
    if args:
        if args.port:
            Receiver(int(args.port))
        else:
            print('No port specified. Please run script with -p [PORT] or --port [PORT]')

if __name__ == '__main__':
    main()