"""+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Project 2 of Computer networks and programming 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
SERVER CODE
+++++++++++++++++++++++++++++++++++++++++++++++++++++++
programmed by : Krupaben Dave and Akshata More 
access id  : gb9978 and 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Code runs 3 steps 
step 1 : just double click
loads 3 objects pdf, image and text
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Heading End """


import socket  
import datetime
import os
import time
import threading # supports multithreding functions 

################################################################################
class coreServer(object): # main class    
    def __init__(self):   #create socket initiate function
        self.hostip = socket.gethostbyname(socket.gethostname()) # to get host ip address 
        self.port = 9000 #port number
        #Socket connection 
        self.coreserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.coreserverSocket.bind((self.hostip, self.port))
        # printing sever ip address and server port
        print ('\n\n ----------------starting server----------------')
        print ('\n Server ip: '+ str(self.hostip)+ ' and Server Port: '+ str(self.port)) 

    def coreServer_Listen(self):  #listen to request
        self.coreserverSocket.listen(5)  # listen to request 
        self.i = 0 # thread counter
        while True:
            newconnected_client, addr = self.coreserverSocket.accept()
            threading.Thread(target = self.listenToClient,args = (newconnected_client,addr)).start() #creating thread for every connection accepted
           
            
    def listenToClient(self,newconnected_client,addr):  #called by thread
        while True:
            
            try:
                
                message = newconnected_client.recv(1024)
                if message:                     
                    # Set the response to echo back the recieved data  
                    print ('\n--------Connection created -------')
                    self.th =  threading.current_thread()
                    self.thr = self.th.name
                    #threading.activeCount()
                    print ('\n-------- '+ str(self.thr)+ ' status = ', self.th.is_alive())
                    self.respondToClient(message,newconnected_client,addr)
                    newconnected_client.close()
                    print ('\n-------- '+ str(self.thr) + ' status = complete')
                   # print ('\n Main thread status  ============', threading.main_thread().is_alive())
                   
                    self.i = self.i+1  # after complete thread count 
                    print(str(i))
                    print('Total threads created is =  ',self.i)
                    print('Client socked closed , server waiting for new request......' )
                    #print ('\nserver connected to client ip: '+ str(addr[0])+ ' and client port: '+ str(addr[1]))
                    #returns here from responseToClient function to close the socket
                else:
                    raise error('Client not connected anymore') # if client disconnects before response 
            except:
                newconnected_client.close()        # force close socket after catching error
                return False                    # if this errors out return false so that thread is closed 
    
    def respondToClient(self,message,newconnected_client,addr):
        try:
            filename = message.decode.split()[1] 
            print('message:',message.decode())                  # split the list from 0,1,..
            time.sleep(3)
            f = open(filename[1:])
            
            print ('-------- File name is: ',str(f.name) )
            if f.name : # if there is a name present in the request
                with open(f.name,'rb') as fileData:    # open the file reqested in read binary format (rb)
                    d = fileData.readlines()# read line by line
                    newconnected_client.send(b'HTTP/1.1 200 OK\r\n\r\n')
                    for a in d:              # auto iteration to send one by one instead of sending at a time 
                        newconnected_client.send(a) 
                    print ('-------- Data send Complete')
            file=os.getcwd()+"\\"+filename[1:]
            statbuf = os.stat(file)
            print(' file location: %s' % os.getcwd())                        #gettting current owrking directory
            print(' last modified: %s' % time.ctime(os.path.getmtime(file))) # getting modified time
            print(' file created : %s' % time.ctime(os.path.getctime(file))) # gettig curent time 
            val = datetime.datetime.now()
            print (" Current date and time :",val.strftime('%Y-%m-%d %H:%M:%S')) 
        except IOError:
            newconnected_client.send(bytes("HTTP/1.1) 404 file not found\r\n\r\n",'UTF-8'))  # if file not found
            newconnected_client.send(bytes(' 404 file not found\r\n','UTF-8')) # if file not found
if __name__ == "__main__":
    coreServer().coreServer_Listen()  # auto execute server at start 
