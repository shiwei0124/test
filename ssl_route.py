#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, ssl, select
import time
import my_threadpool
import threading
import time
crtf="cert.pem"
keyf="key.pem"

locker = threading.Lock()
dest_src = ("172.7.3.130", 10021)

client_dict = {}
ssl_dict = {}
def recv_sock(newsocket):
    pass

if __name__ == "__main__":

    server_sc = socket.socket()
    server_sc.bind(('0.0.0.0', 8081))
    server_sc.setblocking(False)
    server_sc.listen(250)
    #thread_pool = my_threadpool.Thread_Pool(thread_count = 500, timeout = 10)
    inputs = [server_sc]
    
    while True:
        readable, writable, exceptional = select.select(inputs, inputs, inputs, 20)
        if not (readable or writable or exceptional): 
            pass
            #print "Time Out!"
            #break;
        for s in readable:
            if s == server_sc:
                connection, client_addr = s.accept()
                inputs.append(connection)
                
                print crtf
                print keyf
                ssl_conn = ssl.wrap_socket(connection, server_side = True, certfile = crtf, keyfile = keyf)
                connection.setblocking(False)
                ssl_dict[connection] = ssl_conn
                #ssl_dict[ssl_conn] = connection
                client_dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_dest.connect(dest_src)
                inputs.append(client_dest)
                client_dict[connection] = client_dest
                client_dict[client_dest] = connection
            else:
                if ssl_dict.has_key(s):
                    send_dest = client_dict[s]
                    recv_src = ssl_dict[s]
                    data = recv_src.read()
                    send_dest.send(data) 
                else:
                    send_dest = client_dict[s]
                    send_dest_ssl = ssl_dict[send_dest]
                    data = s.recv(1024)
                    send_dest_ssl.write(data)
                
