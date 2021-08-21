import socket
import getopt
import sys
import random
import time
import operator
import pickle
from math import sin, cos, sqrt, atan2, radians

def distance(a,b):
    '''Calculate the distance between two coordinates in earth'''
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(a[0])
    lon1 = radians(a[1])
    lat2 = radians(b[0])
    lon2 = radians(b[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    p = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(p), sqrt(1 - p))

    return R * c


def get_server(por):
    #Connect to the central server to get the list of the available servers and their locations
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the server on local computer
        s.connect((socket.gethostname(), por))

        # receive data from the server
        resp = s.recv(1024)
        print(resp)

        #send client to tell the central server that it is a client and not a server
        s.send(b'client')

        serverListRec = pickle.loads(s.recv(1024))
        #print("getting servers from server")
        #print(serverListRec)

        # close the connection
        s.close()
        return serverListRec
    except socket.error:
        print("Unable to connect to port {}".format(por))
        por+=1
        if por<num_central_server:
            print("Trying to connect to port {}".format(por))
            client(por)
        else:
            print("The location of this server cannot be delivered to central servers")
            sys.exit()


if __name__=='__main__':
    #get random coordinates of the client to simulate geo distribution
    coor=[random.uniform(-90,90),random.uniform(-180,180)]
    port=20000
    recvsize=9999999


    #get a dictionary of the ports of the servers and their locations
    list_server=get_server(port)
    if list_server=={}:
        print("No server is available, try later")
    #server_num=len(list_server)
    #print("list_server")
    #print(list_server)

    closestServer = 1000000.0
    keyClosestServer = 0
    for key in list_server:
        arrayServers = []
        arrayServers.append(list_server[key][0])
        arrayServers.append(list_server[key][1])

        distanceBetweenServers = distance(coor,arrayServers)
        if (distanceBetweenServers < closestServer):
            closestServer = distanceBetweenServers
            keyClosestServer = key

    #print("keyClosestServer")
    #print(keyClosestServer)

    # Create a second socket object to connect to the server
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server on local computer
    s2.connect((socket.gethostname(), keyClosestServer))

    mssgFromServer = pickle.loads(s2.recv(1024))
    #print(mssgFromServer)

    #here we will do a request
    print("Text the word you want to search")
    word = input()

    wordToSend = pickle.dumps(word)
    s2.send(wordToSend)

    responseFromServer = pickle.loads(s2.recv(1024))
    #print("responseFromServer")
    print(responseFromServer)

    s2.close()
