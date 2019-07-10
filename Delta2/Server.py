import socket 
import sys
import select 
import sys 
from thread import *
import hashlib
import binascii
import os
import datetime

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

Users={
    "madhav": hash_password("madhav"),
    "kush": hash_password("kush"),
    "nivi": hash_password("nivi")
}

f=open("chats.txt","+w")
f.close()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
if len(sys.argv) != 4: 
    print "Correct usage: script, IP address, port number, username"
    exit() 
  
ipaddress = str(sys.argv[1]) 
  
Port = int(sys.argv[2])
user = str(sys.argv[3])

server.bind((ipaddress, Port)) 

server.listen(25) 
list_of_clients = []


def receive(conn, addr): 

    ftemp=open("yourtranscript.txt","w+")
    ftemp.close()
    conn.send("Welcome to this chatroom!: To exit enter exit") 
    while True: 
            try: 
                message = conn.recv(2048) 
                f = open("chats.txt","a+")
                datet=datetime.datetime.now()
                f.write(str(datet) + '\n')
                print "<" + user + "> " + message 
                message_to_send = "<" + user + "> " + message
                f.write(message_to_send + '\n')
                sendmessage(message_to_send, conn) 
                if message == "exit":
                    conn.send("Do you want chat backup? ")
                    s = conn.recv(2048) 
                    if s == "Y":
                        f1 = open("chats.txt","r+")
                        ftemp= open("yourtranscript.txt","a+")
                        flag=0
                        line=f1.readline()
                        while line:
                            if(user in line):
                                flag=1
                            if flag==1:
                                ftemp.write(line)
                            line=f1.readline()
                        f1.close()
                        ftemp.close()
                    removeclient(conn) 
            except: 
                continue

def sendmessage(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 

                removeclient(clients) 

def removeclient(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)
    print "Number of Clients Active are: " + str(len(list_of_clients)) 

flag = True
while flag: 
    conn, addr = server.accept()         
    conn.send("Enter your password:")
    passwd = conn.recv(2048)
    if verify_password(Users.get(user), passwd) == True:
        
        f1=open("yourtranscript.txt","w+")
        f1.close()
        
        list_of_clients.append(conn) 
    
        print "Number of Clients Active are: " + str(len(list_of_clients))

        print addr[0] + " connected"

        start_new_thread(receive,(conn,addr))   
    else:
        conn.send("You have entered an incorrect password")
        flag=False

conn.close()
server.close() 
