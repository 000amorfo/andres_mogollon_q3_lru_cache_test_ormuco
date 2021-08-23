# andres_mogollon_q3_lru_cache_test_ormuco

#IT Arquitecture
1 Central server (CS)
2 Distributed servers (DS)
3 Client (Cl)

#How it works
1) Run the Central Server in port 20000

command: python central_server.py -p 20000

this Central Server register all the Distributed servers
when they get connected
* this implementation allows just 3 connections from distributed servers for this test. You can change this limit in central_server.py line 18


2) Run 2 Distributed Server (you can run as much as you want)
in the port you need

command: python server.py -p 3001
command: python server.py -p 3002

these servers are going to register their ip and port in the Central Server
* the Distributed Server will have a size cache (3 elements) for this test. You can change this limit in server.py line 114



3) Run the client

command: python client.py

the client asks to the Central Server the list of available servers and a word, then with the list of servers calculates the distance and access to the nearest server requesting data according to the word that client is looking for


4) When the distributed server receives the connection, it looks for the word in the cache and if not there, just looks for it in the dictionary util/db.py and then update the cache

# I used this repo as a reference
# https://github.com/samisajid/Geo-distributed-LRU-cache

# Considerations
# the test will be executed in localhost but different ports.



# whats done
1 - Simplicity. Integration needs to be dead simple.
2 - Resilient to network failures or crashes.
4 - Data consistency across regions
5 - Locality of reference, data should almost always be available from the closest region

# whats missing
3 - Near real time replication of data across Geolocation. Writes need to be in real time.
6 - Flexible Schema
7 - Cache can expire

if a server crashes the central server would have to update
the server list to get the performance better
