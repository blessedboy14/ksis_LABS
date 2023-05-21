import socket
import threading
import os
import csv
import shutil
from datetime import datetime
import random


class myThread(threading.Thread):
    def __init__(self, threadID, conSoc, dest):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conSoc = conSoc
        self.dest = dest
        self.user = ''
        self.portRange = [50000, 60000]
        self.password = ''
        self.open = True
        self.authorized = False
        self.dataSoc = None
        self.activeIP = None
        self.activePort = None
        self.passiveIP = None
        self.passivePort = None
        self.structure = 'File'
        self.type = ''
        self.file_to_rename = None
        self.credentials = None
        self.textExtensions = None
        self.currentPath = os.getcwd()
        self.corePath = self.currentPath
        self.transferMode = 'S'

    def run(self):
        self.runServer()

    def verifyUser(self):
        if (self.user, self.password) in self.credentials:
            self.authorized = True
        else:
            self.authorized = False

    def ReadCredentials(self):
        with open('logins.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.credentials = [('ADMIN', 'ADMIN'), ('anonymous', 'anonymous@example.com')]
            for row in csv_reader:
                self.credentials.append((row[0], row[1]))
        print(self.credentials)

    def ReadExtensions(self):
        with open('extensions.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.textExtensions = ['.txt']
            for extList in csv_reader:
                for ext in extList:
                    self.textExtensions.append(ext)

    def runServer(self):
        greeting = '200 Welcome\r\n'
        self.conSoc.sendall(greeting.encode('ascii'))

        self.ReadCredentials()
        self.ReadExtensions()
        while self.open:
            if not self.authorized:
                self.USER()

            if self.authorized:
                while 1 & self.open:
                    rec_data = self.conSoc.recv(1024)
                    decoded = rec_data.decode('ascii')
                    if not rec_data:
                        break

                    receivedData = self.parseCommand(decoded)
                    print("Received", receivedData)
                    if receivedData[0] == 'QUIT':
                        self.QUIT()
                    elif receivedData[0] == 'PORT':
                        self.PORT(receivedData[1])
                    elif receivedData[0] == 'RETR':
                        self.RETR(receivedData[1])
                    elif receivedData[0] == 'TYPE':
                        self.TYPE(receivedData[1])
                    elif receivedData[0] == 'STOR':
                        self.STOR(receivedData[1])
                    elif receivedData[0] == 'PWD':
                        self.PWD()
                    elif receivedData[0] == 'LIST':
                        self.LIST(receivedData[1])
                    elif receivedData[0] == 'PASV':
                        self.PASV()
                    elif receivedData[0] == 'CWD':
                        self.CWD(receivedData[1])
                    elif receivedData[0] == 'MKD':
                        self.MKD(receivedData[1])
                    elif receivedData[0] == 'RMD':
                        self.RMD(receivedData[1])
                    elif receivedData[0] == 'DELE':
                        self.DELE(receivedData[1])
                    elif receivedData[0] == 'RNFR':
                        self.RNFR(receivedData[1])
                    elif receivedData[0] == 'RNTO':
                        self.RNTO(receivedData[1])
                    else:
                        self.UNKNOWN()

    def UNKNOWN(self):
        message = '502 Command not implemented\r\n'
        self.conSoc.sendall(message.encode('ascii'))

    def parseCommand(self, recCommand):
        splitStr = recCommand[:-2]
        splitStr = splitStr.split(' ', 3)
        splitStr[0] = splitStr[0].upper()
        if len(splitStr) == 1:
            return [splitStr[0], '']
        return splitStr

    def CheckExtension(self, file):
        if self.type == 'b':
            return True
        name, ext = os.path.splitext(file)
        return ext in self.textExtensions

    def USER(self):  # gets username and stores in variable #This was written by Junaid Dawood 1094837
        rec_data = self.conSoc.recv(1024)
        print(rec_data)
        response = self.parseCommand(rec_data.decode('ascii'))
        print('C %s' % response)
        self.user = response[1]

        response = '331 Need Password\r\n'
        self.conSoc.sendall(response.encode('ascii'))

        self.PASS()

    def PASS(self):  # gets userpass for checking authentication #This was written by Junaid Dawood 1094837
        rec_data = self.conSoc.recv(1024)
        print(rec_data)
        # response = self.parseCommand(rec_data.decode('ascii'))
        response = self.parseCommand(rec_data.decode('ascii'))
        print('C ', response)
        if (response[0] != 'PASS'):
            response = '530 Not logged in\r\n'
            self.conSoc.sendall(response.encode('ascii'))
            return
        self.password = response[1]
        self.verifyUser()
        if self.authorized:
            response = '200 Success\r\n'
            self.conSoc.sendall(response.encode('ascii'))
            self.corePath = self.currentPath
        else:
            response = '430 Invalid login\r\n'
            self.conSoc.sendall(response.encode('ascii'))

    def QUIT(self):  # closes connection #This was written by Junaid Dawood 1094837
        response = '221 Service closing control connection\r\n'
        self.conSoc.sendall(response.encode('ascii'))
        self.open = False
        print('Server is shutting down for user %s' % self.user)

    def PASV(self):
        print('Initiating passive data port')
        self.passiveIP = host
        self.passivePort = random.randint(self.portRange[0], self.portRange[1])
        splitIP = host.split('.')
        port1 = int(self.passivePort) // 256
        port2 = int(self.passivePort) % 256
        sequence = ','.join(splitIP)
        sequence = sequence + ',' + str(port1) + ',' + str(port2)
        print(sequence)
        self.dataSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataSoc.bind((self.passiveIP, self.passivePort))
        message = '227 Entering Passive Mode' + '\r\n'

        self.conSoc.sendall(message.encode('ascii'))

    def TYPE(self, newType):
        newType = newType.upper()
        types = ['A', 'I']
        if newType not in types:
            permitted = ['A', 'I', 'E', 'L']
            if newType in permitted:
                response = '504 Command not implemented for that parameter\r\n'
                self.conSoc.sendall(response.encode('ascii'))
                return
            else:
                response = '501 Invalid type given\r\n'
                self.conSoc.sendall(response.encode('ascii'))
                return
        if newType == 'A':
            self.type = ''
        else:
            self.type = 'b'

        response = '200 Type Altered\r\n'
        self.conSoc.sendall(response.encode('ascii'))  # sends appropriate response

    def STOR(self, filename):
        if not self.CheckExtension(filename):
            encodingError = '550 Incompatible type encoding.\r\n'
            self.conSoc.sendall(encodingError.encode('ascii'))
            return

        if self.activeIP is not None:
            try:
                newFile = open(self.currentPath + '\\' + filename,
                               "w" + self.type)
            except:
                errorMsg = '426 Connection closed (file error); transfer aborted.\r\n'
                self.conSoc.send(errorMsg.encode('ascii'))
                self.CloseDataSoc()
                self.activeIP = None
                self.activePort = None
                return

            transferAccept = '250 Accepted\r\n'
            self.conSoc.sendall(transferAccept.encode('ascii'))

            self.dataSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.dataSoc.connect((self.activeIP, self.activePort))

            newFile = open(self.currentPath + '\\' + filename, "w" + self.type)
            if self.transferMode == 'S':
                while 1:
                    data = self.dataSoc.recv(1024)
                    if not data:
                        break
                    if self.type == '':
                        data = data.decode('ascii')
                    newFile.write(data)
            newFile.close()
            self.CloseDataSoc()
            self.activeIP = None
            self.activePort = None
            return

        if self.dataSoc is not None:
            try:
                newFile = open(self.currentPath + '\\' + filename, "w" + self.type)
            except:
                errorMsg = '426 Connection closed; transfer aborted.\r\n'
                self.conSoc.send(errorMsg.encode('ascii'))
                self.CloseDataSoc()
                self.activeIP = None
                self.activePort = None
                return
            transferAccept = '250 Accepted\r\n'
            self.conSoc.sendall(transferAccept.encode('ascii'))

            self.dataSoc.listen()
            s1, addr = self.dataSoc.accept()

            newFile = open(self.currentPath + '\\' + filename, "w" + self.type)
            if self.transferMode == 'S':
                while 1:
                    data = s1.recv(1024)
                    if not data:
                        break
                    if self.type == '':
                        data = data.decode('ascii')
                    newFile.write(data)
            newFile.close()
            self.dataSoc.close()
            self.dataSoc = None
            self.passiveIP = None
            self.passivePort = None
            return

        noDataCon = '425 Data connection was never created\r\n'
        self.conSoc.sendall(noDataCon.encode('ascii'))

    def RETR(self, filename):
        if not self.CheckExtension(filename):
            encodingError = '550 Incompatible type encoding.\r\n'
            self.conSoc.sendall(encodingError.encode('ascii'))
            return

        filename = self.currentPath + '\\' + filename

        if not os.path.isfile(filename):
            fileNotFound = '550 is a directory, not a file.\r\n'
            self.conSoc.sendall(fileNotFound.encode('ascii'))
            return

        if self.activeIP is not None:
            transferAccept = '250 Accepted\r\n'
            self.conSoc.sendall(transferAccept.encode('ascii'))

            self.dataSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.dataSoc.connect((self.activeIP, self.activePort))
            with open(filename, "r" + self.type) as f:
                if self.transferMode == 'S':
                    toSend = f.read(1024)
                    while toSend:
                        if self.type == '':
                            toSend = toSend.encode('ascii')
                        self.dataSoc.send(toSend)
                        toSend = f.read(1024)
            self.CloseDataSoc()
            self.activeIP = None
            self.activePort = None

        if self.dataSoc is not None:
            transferAccept = '250 Accepted\r\n'
            self.conSoc.sendall(transferAccept.encode('ascii'))

            self.dataSoc.listen()
            s1, addr = self.dataSoc.accept()

            with open(filename, "r" + self.type) as f:
                if self.transferMode == 'S':
                    toSend = f.read(1024)
                    while toSend:
                        if self.type == '':
                            toSend = toSend.encode('ascii')
                        s1.send(toSend)
                        toSend = f.read(1024)
            self.dataSoc.close()
            self.dataSoc = None
            self.passiveIP = None
            self.passivePort = None
            return

        noDataCon = '425 Data connection was never created\r\n'
        self.conSoc.sendall(noDataCon.encode('ascii'))

    def PORT(self, args):
        splitArgs = args.split(',')
        if len(splitArgs) != 6:
            response = '501 Syntax error in parameters or arguments\r\n'
            self.conSoc.sendall(response.encode('ascii'))
        response = '200 Creating data socket\r\n'
        self.conSoc.sendall(response.encode('ascii'))
        ip = splitArgs[0] + '.' + splitArgs[1] + '.' + splitArgs[2] + '.' + splitArgs[3]
        port = int(splitArgs[4]) * 256 + int(splitArgs[5])
        self.activeIP = ip
        self.activePort = port

    def CloseDataSoc(self):
        self.dataSoc.shutdown(socket.SHUT_RDWR)
        self.dataSoc.close()
        self.dataSoc = None
        return

    def PWD(self):
        path = self.currentPath
        response = '257 ' + path + '\r\n'
        self.conSoc.sendall(response.encode('ascii'))
        return

    def LIST(self, args):

        if args == '':
            files = os.listdir(self.currentPath)
            print(files)
        else:
            if os.path.exists(args):
                files = os.listdir(args)
                print(files)
            else:
                response = '501 The directory does not exist \r\n'
                self.conSoc.sendall(response.encode('ascii'))
                return

        toSend = ''
        for file in files:
            if args == '':
                fullpath = self.currentPath + '\\' + file
            else:
                fullpath = args + '\\' + file
            fileInfo = os.stat(fullpath)
            prefix = ''
            if os.path.isdir(fullpath):
                prefix = 'drwxr-xr-x 1'
            else:
                prefix = '-rw-r--r-- 1'
            line = [prefix, 'def', 'def', str(fileInfo.st_size), '\t',
                    datetime.utcfromtimestamp(fileInfo.st_mtime).strftime('%b \t %d \t %H:%M'),
                    '\t', str(file), '\r\n'
                    ]

            lineStr = ' '.join(line)
            # print(lineStr)
            toSend += lineStr

        if self.activeIP is not None:
            print('List sent')
            transferAccept = '226 Accepted\r\n'
            self.conSoc.sendall(transferAccept.encode('ascii'))

            self.dataSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.dataSoc.connect((self.activeIP, self.activePort))

            self.dataSoc.sendall(toSend.encode('ascii'))

            self.CloseDataSoc()
            self.activeIP = None
            self.activePort = None
            return

        if self.dataSoc is not None:
            transferAccept = '250 Accepted\r\n'
            self.conSoc.sendall(transferAccept.encode('ascii'))

            self.dataSoc.listen()
            s1, addr = self.dataSoc.accept()
            s1.sendall(toSend.encode('ascii'))

            s1.shutdown(socket.SHUT_RDWR)
            s1.close()
            self.dataSoc.close()
            self.dataSoc = None
            self.passiveIP = None
            self.passivePort = None
            return

        noDataCon = '425 No data connection created\r\n'
        self.conSoc.sendall(noDataCon.encode('ascii'))
        return

    def CWD(self, newWd):
        if '\\' not in newWd:
            newWd = self.currentPath + '\\' + newWd

        if os.path.isdir(newWd):
            self.currentPath = newWd
            print('Newpath', self.currentPath)
            response = '200 directory changed to+' + newWd + '\r\n'
            self.conSoc.send(response.encode('ascii'))
            return
        else:
            response = '550 Requested action not taken\r\n'
            self.conSoc.send(response.encode('ascii'))
        return

    def RNTO(self, new_name):
        full_name = self.currentPath + '\\' + new_name
        try:
            os.rename(self.file_to_rename, full_name)
            response = '250 File ' + self.file_to_rename + ' renamed successfully to' + full_name + '\r\n'
            self.conSoc.sendall(response.encode('ascii'))
        except:
            response = '550 RNTO failed \r\n'
            self.conSoc.sendall(response.encode('ascii'))

    def RNFR(self, renameFile):
        try:
            self.file_to_rename = self.currentPath + '\\' + renameFile
            response = '350 File ' + self.file_to_rename + ' ready to be renamed\r\n'
            self.conSoc.sendall(response.encode('ascii'))
        except:
            response = '550 RNFR failed \r\n'
            self.conSoc.sendall(response.encode('ascii'))

    def DELE(self, delFile):
        delFile = self.currentPath + '\\' + delFile
        try:
            os.remove(delFile)
            response = '250 File ' + delFile + ' removed successfully\r\n'
            self.conSoc.sendall(response.encode('ascii'))
        except:
            response = '550 DELE failed \r\n'
            self.conSoc.sendall(response.encode('ascii'))

    def RMD(self, directory):
        directory = self.currentPath + '\\' + directory
        try:
            shutil.rmtree(directory)
            responce = '250 Dir ' + directory + ' removed successfully\r\n'
            self.conSoc.sendall(responce.encode('ascii'))
        except:
            response = '550 RMD failed \r\n'
            self.conSoc.sendall(response.encode('ascii'))

    def MKD(self, directory):
        directory = self.currentPath + '\\' + directory
        try:
            os.mkdir(directory)
            response = '257 Dir ' + directory + 'created\r\n'
            self.conSoc.sendall(response.encode('ascii'))
        except:
            response = '550 MKD failed \r\n'
            self.conSoc.sendall(response.encode('ascii'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    host = '127.0.0.1'
    port = 4500
    soc.bind((host, port))
    soc.listen(1)  # restricts number of attempts to create a connection at once

    # open new conenction socket
    while 1:  # loop to keep server listening
        s1, addr = soc.accept()
        print("New Client at: %s" % str(addr))
        threadi = myThread(0, s1, addr)
        threadi.start()
