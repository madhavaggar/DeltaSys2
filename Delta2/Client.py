import socket 
import select 
import sys 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

if len(sys.argv) != 4: 
    print "Correct usage: script, IP address, port number, username"
    exit() 
   
ipaddress = str(sys.argv[1]) 
  
Port = int(sys.argv[2]) 
user = str(sys.argv[3])
server.connect((ipaddress, Port)) 

while True: 
    sockets_list = [sys.stdin, server] 

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print message 
        else:
            message = raw_input() 
            server.send(message) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message + '\n') 
            sys.stdout.flush() 
server.close() 
