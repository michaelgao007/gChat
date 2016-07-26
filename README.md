# **Overview**

This project creates a client-server based online chat application. The client is called gChat and the server is named msgRouter.

The client connects to and registers with the server and then from the sent message is routed by the server to the specified destination. This is the reason why the server is given the name 'msgRouter'.

# **Test Environment**

The client and server processes are running on the following platforms:

**1. Client**

- System Version:	OS X 10.11.1 (15B42)
- Kernel Version:	Darwin 15.0.0

**2. Server**

- System Version: CentOS release 6.4 (Final)
- Kernel Version: 2.6.32-358.el6.x86_64

# **Deployment**

The python version and modules requirements

**1. Client**

1) Python Version: Python 3.5.1 (lower version will not work)

2) Python Modules:

- socket
- tkinter
- sys
- time
- threading
- clntConfig (self-defined)

**2. Server**

1) Python Version: Python 2.6.6 (tested with) or higher

2) Python Modules:

- socket
- time
- threading
- sys
- logging
- config (self-defined)

# **Start the program**

**1. Server**

  1) Config the configuration file, config.py, to set the necessary parameters as required

  2) Check iptables or firewall and make sure it allows incoming TCP connections on port 21567 (default)

  3) Run msgRouter.py to start the server process. The eventlog will be automatically created and is named to evntlog

  4) `tail -f evntlog` to check the activities on the server

**2. Client**

  1) Config the configuration file, clntConfig.py, to set necessary parameters as required

  2) Make sure the server process is running before launching the client process, gChat.py

  3) Enter a nickname and press 'Connect'. The status will change from 'Not Connected' to 'Connected' once the connection is accepted by the server

  4) Type in the text area in the 'Control Panel' and send a Message by either of the way as below

    1) select a recipient from the 'Send Message To' drop-down menu and press 'Send' button to send the message to the remote recipient

    2) broadcast the message to all online users by pressing the 'Broadcast' button.

  5) Press 'Disconnect' to terminate the session at the server. The status will change from 'Connected' to 'Disconnected' once the connection is terminated from the server

# **Message Types and Formats**

**1. Client**

  **i) Log-on Message:**

This message is sent to the server upon the connection establishment with the server and thus, the user is registered on the server.

*Format: 'From'-Empty String-'log on'*

`logOnMsg=nickName.get()+'-'+''+'-'+'log on'`

  **ii) Regular Message:**

This is the regular message (non-broadcast) sent to the specified recipient.

*Format: 'From'-'To'-'Message body'*

`sendMsg=nickName.get()+'-'+toUser+'-'+sendText.get('1.0',tk.END)`

  **iii) Broadcast Message:**

This message is broadcasted to all online users.

*Format: 'From'-'To'-'BROADCAST: Message body'*

`sendMsg=nickName.get()+'-'+''+'-'+'BROADCAST: '+sendText.get('1.0',tk.END)`

  **iv) Exit Message:**

This message is sent to the server to terminate the connection.

*Format: 'from'-Empty String-'exit'*

`sendMsg=nickName.get()+'-'+''+'-'+'exit'`

**2. Server**

  **i) Broadcast Message (regular):**

This regular message is broadcasted to all online users.

*Format: 'From'-Empty String-'Message body'*

`broadcastMsg=ids+'-'+''+'-'+msg`

  **ii) Regular Message:**

This is the regular message (non-broadcast) routed to the specified recipient.

*Format: 'From'-'To'-'Message body'*

`outbndMsg=userInfo[0]+'-'+userInfo[1]+'-'+userInfo[2]`

  **iii) Exit Message:**

This is the message sent back to the exiting user in response to his/her exit request

*Format: 'urout'*

`outMsg='urout'`

  **iv) Broadcast Messages (Online user list)**

This is a special broadcast message sent to all online users once a new user logs in or an existing user logs out. Thus, all online users will get the most up-to-date contact list in their 'Send Message To' drop-down menu

*Format: 'From'-Empty String-'Message body'*

`broadcastMsg=ids+'-'+''+'-'+msg`
