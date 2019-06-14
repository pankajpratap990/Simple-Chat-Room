import socket
import select
import sys



class client(object):
    def __init__(self,name):
        self.host = socket.gethostname()
        self.port = 2626
        self.clisock = None
        self.name = name
        self.connectToServer()


    def connectToServer(self):
        self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.clisock.connect((self.host, self.port))

        except:
            print('Unable to connect')
            sys.exit(-1)

        print('Connected to the chat room')
        rcv_msg = self.clisock.recv(1024).decode('utf-8')
        print(str(rcv_msg))
        sys.stdout.write(self.name + ' -> '); sys.stdout.flush()
        self.messageController()

    def messageController(self):
        flag=True
        while 1:
            try:
                socket_list = [sys.stdin, self.clisock]
                (cread, cwrite, cexec) = select.select(socket_list, [], [])
                for sock in cread:
                    if sock == self.clisock:
                        data = sock.recv(4096)
                        if not data:
                            print('\n Disconnected from chat server')
                            sys.exit()
                        else:
                            data = str(data.decode('utf-8'))
                            if flag:
                                flag = False
                                sys.stdout.write('\n'+data)
                                sys.stdout.flush()
                        #data = str(data.decode('utf-8'))
                            else:
                                sys.stdout.write(data)
                                sys.stdout.flush()
                    else:
                        msg = self.name + ' : '
                        msg = msg + sys.stdin.readline()
                        self.clisock.send(msg.encode('utf-8'))
                        sys.stdout.write(self.name + ' -> ')
                        sys.stdout.flush()
                        flag=True
            except KeyboardInterrupt:
                self.clisock.send(b'')
                self.clisock.close()
                sys.exit()

name = input("Enter User Name: ")
client( name )
