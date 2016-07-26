#!/usr/bin/env python3

from socket import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from time import ctime
import clntConfig as config
import threading as trd
import sys

#--------------Client Configurations Parameters--------------#
HOST=config.HOST
PORT=config.PORT
BUFSIZ=config.BUFFER
ADDR=config.ADDR
#--------------End of Client Configurations Parameters--------------#

try:
    sock=socket(AF_INET,SOCK_STREAM)
    print('Soket created')
except(socket.error) as sockError:
    print('Failed to create socket. Error: '+str(sockError[0])+'\nMessage: '+str(sockError[1]))
    sys.exit()

#--------------Connect to the Remote Server--------------#
def srvConnect():
    client.start()
#--------------Endo of Connect to the Remote Server--------------#

#--------------Send Msg to Server--------------#
def msgSend():
    toUser=activeCombo.get()
    if not toUser:
        infoLabel.configure(text='No Recipient Selected',foreground='red')
    else:
        infoLabel.configure(text='')
        sendMsg=nickName.get()+'-'+toUser+'-'+sendText.get('1.0',tk.END)
        sock.send(sendMsg.encode())
        sendTime=ctime().split()[3]
        msgText.insert(tk.END,'\n'+sendTime+'-You@'+toUser+'\n'+sendText.get('1.0',tk.END)+'\n')
        msgText.configure(foreground='blue')
        sendText.delete('1.0',tk.END)
#--------------End of Send Msg to Server--------------#

#--------------Message Broadcast--------------#
def broadcast():
    sendMsg=nickName.get()+'-'+''+'-'+'BROADCAST: '+sendText.get('1.0',tk.END)
    sendTime=ctime().split()[3]
    sock.send(sendMsg.encode())
    msgText.insert(tk.END,'\n'+sendTime+'-'+'You@All Users'+'\n'+sendText.get('1.0',tk.END)+'\n')
    msgText.configure(foreground='blue')
    sendText.delete('1.0',tk.END)

#--------------End of Message Broadcast--------------#

#--------------Update Online Users List--------------#
def chkUser(msg):
    onlineUsers=tuple(msg.split('-')[2].split())
    activeCombo['values']=onlineUsers
#--------------End of Update Online Users List--------------#

#--------------Message Parser--------------#
def msgParser(msg):
	msgParsed=[]
	fromUser=msg.split('-')[0]
	msgParsed.append(fromUser)
	toUser=msg.split('-')[1]
	msgParsed.append(toUser)
	msgBody=msg.split('-')[2]
	msgParsed.append(msgBody)
	#print(msgParsed)
	return msgParsed
#--------------End of Message Parser--------------#

#--------------Session Disconnect--------------#
def disconnect():
    sendMsg=nickName.get()+'-'+''+'-'+'exit'
    sock.send(sendMsg.encode())
#--------------End of Session Disconnet--------------#

#--------------Main Thread to Handle Incoming Msgs and Update Msg Windows--------------#
def clientThread():
    try:
        sock.connect(ADDR)
        logOnMsg=nickName.get()+'-'+''+'-'+'log on'
        sock.send(logOnMsg.encode())
        inButton.configure(state='disabled')
        statusLabel.configure(text='Connected',foreground='green')
        msgText.tag_config('msgReceived',foreground='purple',font='Arial')
        msgText.tag_config('broadcast',foreground='red',font='Arial')
    except:
        statusLabel.configure(text='Failed to connect to remote server')
        sys.exit()

    while True:
        recvMsg=sock.recv(BUFSIZ).decode()

        #--------------Wait for Server Response and Exit--------------#
        if recvMsg.endswith('urout'):
            sock.close()
            statusLabel.configure(text='Disconnected',foreground='red')
            infoLabel.configure(text='Session Terminated.\nPlease close the\ncurrent window.',foreground='red')
            break
        #--------------End of Wait for Server Response and Exit--------------#

        #--------------Current Online Users Checked From server--------------#
        else:
            recvInfo=msgParser(recvMsg)
            if recvInfo[0] == 'server':
                chkUser(recvMsg)
        #--------------End of Current Online Users Cheked From Server--------------#

            #--------------Broadcast Message Handling--------------#
            elif recvInfo[2].startswith('BROADCAST'):
                tag=('broadcast',)
                showMsg=ctime().split()[3]+'-'+recvInfo[0]+'\n'+recvInfo[2]+'\n'
                msgText.insert(tk.END,showMsg,tag)
            #--------------End of Broadcast Message Handling--------------#

            #--------------Regular Message Handling--------------#
            else:
                tags=('msgReceived',)
                showMsg=ctime().split()[3]+'-'+recvInfo[0]+'\n'+recvInfo[2]+'\n'
                msgText.insert(tk.END,showMsg,tags)
            #--------------End of Regular Message Handling--------------#

#--------------End of Main Thread to Handle Incoming Msgs and Update Msg Windows--------------#

root=tk.Tk()
root.geometry('590x550')
root.title('gChat v1.0')
root.resizable(0,0)

#--------------Status Panel--------------#
statusPane=tk.LabelFrame(root,text='Status Panel')
statusPane.pack(fill='both',padx=2)

nickLabel=tk.Label(statusPane,width=12,text='Nickname:',foreground='red')
nickLabel.grid(row=0,column=0,sticky='e')

nickName=tk.StringVar()
nickEntry=tk.Entry(statusPane,textvariable=nickName)
nickEntry.grid(row=0,column=1,sticky='we')
nickEntry.focus()

inButton=tk.Button(statusPane,text='Connect',command=srvConnect)
inButton.grid(row=0,column=2,sticky='e',padx=10)

statusLabel=tk.Label(statusPane,text='Not Connected',foreground='red')
statusLabel.grid(row=0,column=3,sticky='we',padx=10)

#--------------END of Status Panel--------------#

#--------------Message Panel--------------#
msgPane=tk.LabelFrame(root,text='Message Panel')
msgPane.pack(fill='both')

msgText=tk.scrolledtext.ScrolledText(msgPane,wrap='word',width=60)
msgText.grid(row=0,column=0,columnspan=4,sticky='we')

onlineFrame=tk.Frame(msgPane)
onlineFrame.grid(row=0,column=4,sticky='we')

onlineLabel=tk.Label(onlineFrame,text='Send Messages To: ',width=14)
onlineLabel.grid(row=1,column=0,sticky='wen',padx=2,pady=4)
onlineLabel.configure(foreground='blue')

remoteUser=tk.StringVar()
activeCombo=ttk.Combobox(onlineFrame,textvariable=remoteUser,width=14)
activeCombo['values']=()
activeCombo.grid(row=2,column=0,sticky='wen',padx=2)

broadcastButton=tk.Button(onlineFrame,text='Broadcast',command=broadcast)
broadcastButton.grid(row=3,column=0,sticky='wen',padx=2,pady=30)

reminderLabel=tk.Label(onlineFrame,width=12,text='System Reminder:',foreground='magenta')
reminderLabel.grid(row=4,column=0,sticky='wen',padx=2, pady=5)

infoLabel=tk.Label(onlineFrame,width=12,height=5,anchor='w',justify='left')
infoLabel.grid(row=5,column=0,sticky='wen',padx=2)

#--------------End of Message Panel--------------#

#--------------Control Panel--------------#
ctrlPane=tk.LabelFrame(root,text='Control Panel')
ctrlPane.pack(fill='both',padx=2)

sendText=tk.scrolledtext.ScrolledText(ctrlPane,wrap='word',height=5,width=50)
sendText.grid(row=0,column=0,sticky='we')

sendButton=tk.Button(ctrlPane,text='Send',width=6,command=msgSend)
sendButton.grid(row=0,column=1,sticky='we',padx=10)

exitButton=tk.Button(ctrlPane,text='Disconnect',command=disconnect)
exitButton.grid(row=0,column=3,sticky='we',padx=5)
#--------------End of Self Panel--------------#

client=trd.Thread(target=clientThread,args=())

root.mainloop()
