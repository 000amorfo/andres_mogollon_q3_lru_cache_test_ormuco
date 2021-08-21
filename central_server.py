import sys
import getopt
import socket
import pickle
from math import sin, cos, sqrt, atan2, radians

#from utils.server_setup import *

servers={}



def server(port):
    #creating a socket object
    s = socket.socket()
    print("socket successfully created in centrar server")

    #binding the host and the port to the socket
    s.bind(('', port))
    print("socket binded to {}".format(port))

    #putting the socket in listening mode
    #this just will allow 3 connections to keep the performance low
    s.listen(3)
    print("socket is listening right now")

    #infinite loop to accept connection with other sockets
    while True:
        conn, addr = s.accept()
        print("connection received from {}".format(addr))

        #sending a message to the client
        mssg = 'You are connected to the port ' + str(port)
        conn.send(mssg.encode())

        #here we are going to know who is connected to our socket
        typ=conn.recv(1024)
        #print(typ)

        if typ==b'server': #if its a server just update the available server list
            packRec = pickle.loads(conn.recv(1024))
            checker = False;
            for key in packRec:
                for port in servers: #if the port already exists just update coordinates
                    if port == key:
                        checker = True
                        servers[key] = packRec[key]
                        break
                    else:
                        checker = False

                if checker == False:
                    servers[key] = packRec[key]
                else:
                    checker = False

            print(servers)

        elif typ==b'client':
            serversEncoded = pickle.dumps(servers)
            #            conn.sendall(b'{}'.format(servers))
            conn.send(serversEncoded)
            #typeClient = pickle.loads(conn.recv(1024))

        #else:
            '''
            # here i get the coordinates
            coordinatesClient = pickle.loads(typ);
            #print(coordinatesClient)

            #print(servers)

            coorServer = {}
            #arrayServers = []
            closestServer = 1000000.0
            keyClosestServer = 0

            #tmpServer = 0
            for key in servers:
                arrayServers = []
                arrayServers.append(servers[key][0])
                arrayServers.append(servers[key][1])

                distanceBetweenServers = distance(coordinatesClient,arrayServers)
                if (distanceBetweenServers < closestServer):
                    closestServer = distanceBetweenServers
                    keyClosestServer = key

            #print("keyClosestServer")
            #print(keyClosestServer)

            chosenServer = pickle.dumps(servers[keyClosestServer])
            conn.send(chosenServer)
            '''


        #close the connection with the client
        conn.close()
        print("client connection closed")
        print(".------------------------------.")

if __name__=='__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 'p')
    except getopt.GetoptError:
        print('Something went wrong with your command!')
        sys.exit(2)
    try:
        port = int(args[0])
    except:
        print("The port value has to be an integer")
        sys.exit()

    #start the server
    server(port)
