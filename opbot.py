# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is an IRC bot.
#
# The Initial Developer of the Original Code is Tanner Filip.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
# Tanner Filip <tanner@techessentials.org>
# David Vo <aucg@geekbouncer.co.uk>
# DeltaQuad <deltaquad@live.ca>
# Ahmed El-Mahdawy <aa.mahdawy.10@gmail.com>
# Nic Matthew <nic.matthew@gmail.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

	#IMPORT REQUIRED MODULES
import socket
import random
import time
import re

	#CHANGE THESE SETTINGS
#Enter your name
owner = "NicHelps"
#Enter the name of your bot
botname = "YourBotsName"
#Enter the server you want the bot to connect to
network = "irc.server.com"
#Enter the port you want the bot to connect on (**NO QUOTES!**)
port = 6667
#Enter the channel you would like your bot to join
channel = "#channel"

	
	#CONNECTING
randnum = random.randint(1, 10000)
shutdowncmd = "!die " + str(randnum)
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )

	#SET NICKS AND USERNAMES
irc.send ( 'NICK %s\r\n' % botname)
irc.send ( 'USER Python IRC bot :Python IRC\r\n' )
time.sleep(0.5)

	#THE BOT'S BEHAVIOR AND ACTIONS
while True:
	data = irc.recv ( 4096 )
	
		#PINGS AND PONGS
	if data.find ( 'PING' ) != -1:
		irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
		
		#JOINING CHANNELS, SENDING THE RANDOM NUMBER
	if data.find ( '376' ) != -1:
		irc.send ( 'PRIVMSG YourName :The random number is %d\r\n' % randnum)
		irc.send ( 'JOIN %s\r\n' % channel)
		
		#SHUTTING DOWN WHEN FINDING THE RANDOM NUMBER
	if data.find(shutdowncmd) != -1:
		irc.send ('QUIT :by direct order\r\n')
		sys.exit()
		
		#REFUSING TO SHUT DOWN TO STRANGERS
	if data.find ('!die') !=-1:
		irc.send ( 'PRIVMSG %s :Access denied. This incident will be reported.\r\n' % channel)
		irc.send ( 'PRIVMSG %s :Someone tried to shut me down!\r\n' % owner)

                #REJOIN ON KICK
	if data.find ('KICK') !=-1:
		irc.send ( 'JOIN %s\r\n' % channel)


print data
