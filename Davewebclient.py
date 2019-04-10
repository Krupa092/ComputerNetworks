# To run the code : " python client.py serverip portnumber filename " in command promt 

import socket # importing socket
import argparse # for passing arguements 
import sys # to get the inputs passed in commmand prompt 
bufferVar = ' ' # predefining buffer 
# Defining arguements passsed 

passed_arg = argparse.ArgumentParser()
passed_arg.add_argument('ip',nargs = 1) #  1st arguement 
passed_arg.add_argument('port',type = int,nargs = 1)# 2nd
passed_arg.add_argument('Filename',nargs = 1) #3rd 
args = passed_arg.parse_args() # parsing arguement as list
#print(args.ip[0]) we can extract arguements from list array
#
# server conneciton 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('\n connecting to server :- '+ str(args.ip[0]) + ' and Port:- ' + str(args.port[0]))
client_socket.connect((args.ip[0],int(args.port[0])))
#
#making it look like get request so that server can respond as web request
http_getRequest = 'GET '+ '/' +str(args.Filename[0])
# send file name 
client_socket.send(bytes(http_getRequest,'UTF-8')) # converting to bytes as request
# while connection is true
while True:
    try:
        recData = client_socket.recv(1024)
        recData = recData.decode()     # decode recieved  data 
        bufferVar += str(recData)  # concatinate revieved raw data one by one
       
        if not recData:                 # to break the loop after completing recieved data 
            break
           
    except Exception as e:
        print(e)
        client_socket.close() # error close socket
                
print ("\n Raw data recieved:-")
print(bufferVar[16:]) # print after recieving all raw data 
client_socket.close()
print ('\n Data recieve compelete closing socket')
