"""+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Project 1 of Computer networks and programming 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
SERVER CODE
+++++++++++++++++++++++++++++++++++++++++++++++++++++++
programmed by : Krupaben Dave and Akshata More 
access id  : gb9978 and 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Code runs 3 steps 
step 1 : 
step 2 :
step 3 :
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Heading End """

from socket import*
import datetime
import os
import time
#
serverPort = 9000                               # server port address 
computer_name = gethostname()                   # get computer name
ip_add = gethostbyname(computer_name)           # get computer ip address to make it as server ip address 

#
print ('\n ----------------starting server----------------')
print ('\n hostname is: ', computer_name)  
print (' hostname ip: ', ip_add)           
print ('\n Ready To Serve... ')
# binding sockects
serverSocket = socket(AF_INET, SOCK_STREAM)     # creating socket
serverSocket.bind((computer_name, serverPort))
serverSocket.listen(1)
#
while True:  
        #print ('\n Server running Ip:- '+ str(ip_add) + ' and Port:- ' + str(serverPort))
        connectionSocket, addr = serverSocket.accept()                   # to accept new clients 
        if connectionSocket:                                             #when there is a connection display the clint ip addess
                print ('\n server connected to client ip: '+ str(addr[0])+ ' and client port: '+ str(addr[1]))
        else:
                print("\n waiting for conection")
        try:
            # to receive data from client, devided in 1Mb
                message =  connectionSocket.recv(1024)
                print ('\n Message recieved is: ', message)              # recieve the request
                filename = message.decode().split()[1]                   # split the list from 0,1,..
                print ('\n File name is: ', filename)
                #
                f = open(filename[1:])                                  # removes slash and gets the name of file
                print('\n Type of file reqested is :',f.name)
                outputdata = f.read()                                   #open file 
                #
                print('\n Sending data :')
                print(outputdata)                                       #printing output data
                #
                connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')       # sending file found 
 
                for i in range(0, len(outputdata)):
                        connectionSocket.send(outputdata[i].encode())
                connectionSocket.close()
                #
                print ('\n data send Complete')
                print (' File data length : ', len(outputdata))
                file = os.getcwd()+ "\\"+ filename[1:]
                statbuf = os.stat(file)
                print(' file location: %s' % os.getcwd())                        #gettting current owrking directory
                print(' last modified: %s' % time.ctime(os.path.getmtime(file))) # getting modified time
                print(' file created : %s' % time.ctime(os.path.getctime(file))) # gettig curent time 
                val = datetime.datetime.now()
                print (" Current date and time :",val.strftime('%Y-%m-%d %H:%M:%S'))
                
        except IOError:
                connectionSocket.send(bytes("HTTP/1.1 404 file not found\r\n\r\n",'UTF-8'))  # if file not found
                connectionSocket.send(bytes(' 404 file not found\r\n','UTF-8')) # if file not found
                connectionSocket.close()
        print ('\n ----------------Restarting socket---------------')

serverSocket.close()  
"""
+++++++++++++++++++++++++++++++++++++END+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
