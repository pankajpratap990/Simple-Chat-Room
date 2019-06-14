import socket
import select
import sys

class ChatServer(object):


    def __init__(self,port):
        self.port = port
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = socket.gethostname()
        self.srvsock.bind((host, port))
        self.srvsock.listen(5)

        self.descriptors = [self.srvsock]
        print('ChatServer started on port %s' % port)


    def run(self):
        while 1:
            try:
                (sread, swrite, sexec) = select.select(self.descriptors, [], [])
                for sock in sread:
                    if sock == self.srvsock:
                        self.accept_new_connection()
                    else:
                        s = sock.recv(4096)
                        s = str(s.decode('utf-8'))
                        host, port = sock.getpeername()
                        if not s:
                            s = 'Client left %s:%s\r\n' % (host, port)
                            self.broadcast_string(s, sock)
                            sock.close
                            self.descriptors.remove(sock)
                        else:
                            ns = '[%s:%s] %s' % (host, port, s)
                            self.broadcast_string(ns, sock)
            except KeyboardInterrupt:
                for sock in sread:
                    if sock == self.srvsock:
                      continue
                    else:
                        sock.close()
                self.srvsock.close()
                sys.exit(1)


    def broadcast_string(self, strin, omit_sock):
        print(strin,end='')
        for sock in self.descriptors:
            if sock != self.srvsock and sock != omit_sock:
                try:
                    sock.send(strin.encode('utf-8'))
                except:
                    sock.close()
                    self.descriptors.remove(sock)


    def accept_new_connection( self ):
        newsock, (remhost, remport) = self.srvsock.accept()
        self.descriptors.append(newsock)
        s = "You are connected to %s:%s " % (socket.gethostbyname(socket.gethostname()), self.port)
        newsock.send(s.encode())
        st = 'Client joined %s:%s \n' %(remhost, remport)
        self.broadcast_string(st, newsock)



myserver = ChatServer( 2626 ).run()



