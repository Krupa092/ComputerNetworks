import asyncio
import socket
import sys
import os
import time
import datetime
import threading # supports multithreding functions 
import itertools # for counting number of connection

#
count=0        # counting connecitons made 
results = ''
all_connections=[] # to store the connections arrays 
all_address=[]  # to store address 
#

loop =asyncio.get_event_loop() # Create the core of asynchronous tasks and callbacks

#**********************************************#Declaring Variables#**********************************************#
                    
timeArray=[] # to Calculate time
data_sz=[] # to calculate data
client_time=43200 #12*60*60

#**********************************************#Serevr connection#**********************************************#
async def getConnection(coreclient,addr,i):
    print('connections list: \n')
    for i,coreclient in enumerate(all_connections): # print connections base on size of it
        r1 = "= "+str(coreclient._closed)           # checking if the connection is close 
        r2 = " ("+ str(all_address[i][0]) + " , " + str(all_address[i][1]) +")"
        print("---- connection "+ str(i) +r2 + " closed ? " +r1)
    return


async def coreserver():
    host=socket.gethostbyname(socket.gethostname()) # To get Host name from user 
    port=9000   # Declaring Port Number
    print('Server IP is: ', str(host) + '\nPort Number is: ', str(port))
    coreserver=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating Socket
    coreserver.bind(('',9000)) # Binding Sockets 
    coreserver.listen(5)
    coreserver.setblocking(False) # To set non-blocking
    count = 0 
    while True:
        coreclient, addr= await loop.sock_accept(coreserver) # To accept new clients
        s=time.time() # starting timer for calculating each object execution time
        if coreclient:  # if there is a client creatoing hand shaking      
            count= count+1
            all_connections.append(coreclient) # append connection to print
            all_address.append(addr)
            print('Hand Shaking Connection....'.format(addr))
            await getConnection(all_connections,all_address,count) # await connection to get the list of connections 
            print ("\nconnected to client: "+ str(addr[0])+ " and client port: "+ str(addr[1]))
            loop.create_task(handler(coreclient,s))#Scheduling execution
            
#************************************************#Handling Client#*********************************************#
async def handler(coreclient,s):
    with coreclient:    
        while True:
            message = await loop.sock_recv(coreclient,1024) #To receive data
            try:
                print('Message is:\n ' + str(message.decode())) # To get response headers
                if message!="": # If there is Data in the message variable
                    filename = message.decode().split()[1] 
                    print('Filename :' + str(filename)) # split the list from 0,1,.. to get filename 
                    f = open(filename[1:])
                    await loop.sock_sendall(coreclient,b"HTTP/1.1 200 OK\r\n\n")#Wait until Http response completed 
                    with open(f.name,'rb') as fileData:    # open the file reqested in read binary format (rb)
                        d = fileData.readlines()            # read line by line
                        for a in d:              # auto iteration to send one by one instead of sending at a 
                            await loop.sock_sendall(coreclient,a) #Sending all the data 
                        coreclient.close() #closing Client
                print ('Data send Complete* = ',f.name)
                file = os.getcwd()+ "\\"+ filename[1:] 
                size=os.path.getsize(file) # getting file size
                print ('Object size  :', os.path.getsize(file))
                data_sz.append(size)
                print('Total Data size in kb : '+str(sum(data_sz)/1024))
                print("last modified: %s" % time.ctime(os.path.getmtime(file))) #getting modified time and date
                print("created: %s" % time.ctime(os.path.getctime(file)))
                now = datetime.datetime.now()
                print ("Current date and time using isoformat:",now.isoformat()) #Getting Current Time 
                
                exp1=time.gmtime(time.time()+client_time)
                expires=time.strftime("%a,%d-%b-%Y %T GMT"+str(exp1))
                print('Expires at: ',expires)
                e=time.time() # Ening the Timer counter for object 
                value = round(e- s, 3)
                timeArray.append(value)
                print('time taken by object = '+ str(value))
                print('\nOveral total Time ='+str(timeArray)+' = '+str(sum(timeArray)))
                letency=round((sum(timeArray)/len(timeArray)),3)
                print('latency is :'+str(letency))
                print('Data Transfer : '+str((sum(data_sz)/sum(timeArray))/(1048576)))
                return False
            except IOError: #comes here when the required file not found.
                await loop.sock_sendall(coreclient,b"HTTP/1.0 404 Not Found\r\n\n")# print as file notfound
                await loop.sock_sendall(coreclient,b"<html><head></head><body><h1>404NotFound</h1></body></html>\r\n\n")
                coreclient.close()
                return False


if __name__== '__main__':
    loop.create_task(coreserver())  # create task
    loop.run_forever() # run task


