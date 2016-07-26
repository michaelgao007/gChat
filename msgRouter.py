#!/usr/bin/env python3

from socket import *
from time import ctime
import config
import threading as trd
import sys
import logging

#--------------Server Configurations Parameters--------------#
HOST=config.HOST
PORT=config.PORT
BUFSIZ=config.BUFFER
ADDR=config.ADDR
#--------------End of Server Configurations Parameters--------------#

sock=socket(AF_INET,SOCK_STREAM)

#--------------Server Logger Configurations--------------#
logging.basicConfig(filename='evntlog',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
#--------------End of Server Logger Configurations--------------#

userList={}

#--------------Message Parser--------------#
def msgParser(msg,addr):
	msgParsed=[]
	fromUser=msg.split('-')[0]
	msgParsed.append(fromUser)
	toUser=msg.split('-')[1]
	msgParsed.append(toUser)
	msgBody=msg.split('-')[2]
	msgParsed.append(msgBody)
	logMsg='Received msg from '+fromUser+' '+str(addr[0])+':'+str(addr[1])+' '+msgBody
	logging.info(logMsg.strip())
	return msgParsed
#--------------End of Message Parser--------------#

#--------------Check for current  Online Users--------------#
def chkUsers():
	onlineUsrList=''
	for user in userList.keys():
		onlineUsrList=onlineUsrList+user+' '
	return onlineUsrList
#--------------End of Check for current Online Users List--------------#

#--------------Broadcast Message to All Online Users--------------#
def broadcast(ids,msg):
	if len(userList) != 0:
		for user in userList.keys():
			broadcastMsg=ids+'-'+''+'-'+msg
			userList[user].send(broadcastMsg.encode())
		logging.info('broadcast: '+broadcastMsg.strip())
#--------------End of Broadcast Message to All Online Users--------------#

def clientThread(conn,addr):
	logOnMsg=conn.recv(BUFSIZ).decode()
	loginInfo=msgParser(logOnMsg,addr)
	userList[loginInfo[0]]=conn
	broadcast('server',chkUsers())
	while True:
		#--------------User Info Parser--------------#
		recvMsg=conn.recv(BUFSIZ).decode()
		logging.info(recvMsg.strip())
		recvTime=ctime().split()[3]
		userInfo=msgParser(recvMsg,addr)
		userList[userInfo[0]]=conn
		#--------------End of User Info Parser--------------#

		#--------------User Exit--------------#
		if userInfo[2] == 'exit':
			logging.info(userInfo[0]+' logged out')
			logging.info('Client connection terminated: '+userInfo[0]+' '+str(addr[0])+':'+str(addr[1]))
			outMsg='urout'
			conn.send(outMsg.encode())
			logging.info('Msg sent: '+userInfo[0]+' '+outMsg.strip())
			del userList[userInfo[0]]
			broadcast('server',chkUsers())
			break
		#--------------End of User Exit--------------#

		#--------------Broadcast message--------------#
		elif userInfo[2].startswith('BROADCAST'):
			broadcast(userInfo[0],userInfo[2])
		#--------------End of broadcast message--------------#

		#--------------Normal user message--------------#
		else:
			outbndMsg=userInfo[0]+'-'+userInfo[1]+'-'+userInfo[2]
			userList[userInfo[1]].send(outbndMsg.encode())
			logging.info('Msg sent: '+outbndMsg.strip())
		#--------------End of Normal user message--------------#

try:
	sock.bind(ADDR)
except (socket.error) as sockError:
	logging.critical('Socket bind failed. Error: '+str(sockError[0])+'\nMessage: '+str(sockError[1]))
	sys.exit()
sock.listen(8)
logging.info('***** MsgRouter Started. *****\tNow is %s'%(ctime()))
logging.info('Waiting for incoming connections .....')

while True:
	conn,addr=sock.accept()
	logging.info('Connected from '+str(addr[0])+':'+str(addr[1]))
	trd.Thread(target=clientThread,args=(conn,addr)).start()

sock.close()
