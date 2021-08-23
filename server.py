import socket
import getopt
import sys
import random
import time
import pickle #to manage data transfer between sockets
import lru_cache
from utils.db import *


recvsize=9999999

def server():
    # create a socket object
    s = socket.socket()

    #binding the host and the port to the socket
    s.bind(('', port))

    # put the socket into listening mode
    s.listen(5) #allow 5 connections
    print ("socket is listening in port {}".format(port))

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        # Establish connection with client.
        conn, addr = s.accept()
        print("connection received from {}".format(addr))

        # send a verified message to the client
        mssg = 'You are connected to the port ' + str(port)
        conn.send(pickle.dumps(mssg))

        wordSearched = pickle.loads(conn.recv(1024))

        cache.get(wordSearched)
        result = cache.get(wordSearched)

        valid = False
        if(result == -1):
            for key in dictWords:
                if (key == wordSearched):

                    cache.put(wordSearched,dictWords[wordSearched])

                    cache_items = cache.show_entries();
                    response = cache_items[key]
                    conn.send(pickle.dumps(response))
                    #conn.close()
                    valid = True
                    break

            if(valid == False):
                response = "there is no information"
                conn.send(pickle.dumps(response))

            print("LRU cache:")
            print(cache.show_entries())
        else:
            #if the word exists
            #--------------------------------------------------
            cache.put(wordSearched,result)

            cache_items = cache.show_entries();
            response = cache_items[wordSearched]
            conn.send(pickle.dumps(response))
            #print("here there are elements in the cache")

            print("LRU cache:")
            print(cache.show_entries())

        # Close the connection with the client
        conn.close()

def client(port):
    try:
        # creating a socket (AF_INET = ipv4, SOCK_STREAM = TCP)
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the server on local computer
        c.connect((socket.gethostname(), port))

        # receive data from the server
        #print (c.recv(1024))
        c.recv(1024)
        c.send(b'server')

        print(portinfo)
        portinfoEncoded = pickle.dumps(portinfo)
        c.send(portinfoEncoded)

        print(c.recv(recvsize))
        c.close()
    except socket.error:
        print("Unable to connect to port {}".format(port))

if __name__=='__main__':

    csize=3 #chace size
    timeout=10 #to expires (seconds)
    argv = sys.argv[1:] #here we take the port

    try:
        opts, args = getopt.getopt(argv, 'hp:t:c:')
    except getopt.GetoptError:
        print('Something went wrong with your command!')
        sys.exit(2)
    for op,ar in opts:
        #print(op,ar)
        if op=="-t":
            try:
                timeout=float(ar)
            except:
                print("The timeout value has to be a number")
                sys.exit()
        elif op=="-c":
            try:
                csize=int(ar)
            except:
                print("The cache size value has to be an integer")
                sys.exit()
        elif op=="-p":
            try:
                port = int(ar)
            except:
                print("The port value has to be an integer")
                sys.exit()
        elif op=="-h":
            print("Create a server with a LRU cache")
            print("-p        Indicate the port value of the server, it is a mandatory argument")
            print("-c        Indicate the size of the cache, the default value is 1024")
            print("-t        Indicate the timeout after which the cache expires, default value is 10s")
            sys.exit()

    #Random location of the server to simulate geo distribution
    coor=[random.uniform(-90,90),random.uniform(-180,180)]
    print("The server is located in {}, its port number is {}, its cache size {} and the cache timeout is {}".format(coor,port,csize,timeout))
    portinfo={port:coor}
    #print(portinfo)

    #Connect to the central server in port 20000
    client(20000)

    #create the server cache
    cache = lru_cache.SimpleLRUCache(csize) #lru cache

    #Ready to serve clients
    server()
