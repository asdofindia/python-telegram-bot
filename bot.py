import subprocess
import re
from wiki import wiki
from google import google
import lxml.html
from wolfram import wolfram
from threading import Thread
import time

from BeautifulSoup import BeautifulSoup
from chatterbotapi import ChatterBotFactory, ChatterBotType


pathtotg='~/tg/'    #include trailing slash. I don't know if '~' notation works
lastmessage=None
proc=None
chattybot=True


factory = ChatterBotFactory()
bot1 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
botsessions={}

#this function somehow works in preventing duplicate messages
def mymessage(message):
	global lastmessage
	if (message==lastmessage):
		return True
	else:
		return False

def callmodule(message,peer):
	message=message.lower()
	modules=["wiki","bot","google"]  #Add module name here so that the for loop below works
	for module in modules:
		if (message.find(module)==0):
			message=message[len(module)+1:]
			if module=="wiki":
				reply=wiki(message)
				if ("Cannot acces link!" in reply):
					reply="No wikipedia article on that, googling instead\n"+google(message)
				return reply
			if module=="google":
				return google(message)
			if module=="bot":
				message=message.lstrip()
				reply=wolfram(message)
				if (reply=="noidea"):
					reply="tough. I'll google that\n"+google(message)
				return reply
	global chattybot
	if chattybot:
		global botsessions
		global bot1
		if peer not in botsessions:
			botsessions[peer]=bot1.create_session()
		reply = botsessions[peer].think(message)
		VALID_TAGS = ['br']
		soup = BeautifulSoup(reply)
		for tag in soup.findAll(True):
			if tag.name not in VALID_TAGS:
				tag.hidden = True
		reply=soup.renderContents()
		reply=reply.replace('<br />','\n')
		return reply

def AI(group,peer,message):
	#uncomment for debug
	#if lastmessage is not None:
	#	print 'message is '+message+' and lastmessage is '+lastmessage+'\n'
	if mymessage(message):
		return
	replyrequired=False
	reply=None
	if group is None:
		replyrequired=True
	if (message[:3].lower()=="bot"):
		replyrequired=True
	reply=callmodule(message,peer)
	if((message[:4]=="http") and (message.find(' ')==-1)):
		t = lxml.html.parse(message)
		reply = t.find(".//title").text
	#if ((replyrequired==True) and (reply is None)):
		#reply="underconstruction"
	if reply is not None:
		msg(group,peer,reply)
			
def spam(message):
	if (message == lastmessage):
		return True
	else:
		return False

	
def msg(group,peer,message):
	global proc
	if (group is not None):
		message=peer.split(' ')[0] + ": " + message
		peer=group
	if (not spam(message)):
		if(('\n' in message)or('\r' in message) or ('\r\n' in message)):
			tempfile='temp'
			temp=open(tempfile,'w')
			temp.write(message)
			temp.close()
			proc.stdin.write('send_text '+peer.replace(' ','_')+' '+tempfile+'\n')
		else:
			proc.stdin.write('msg '+peer.replace(' ','_')+' '+message+'\n')
		global lastmessage
		lastmessage=message

def bot():

	COLOR_RED="\033[0;31m"
	COLOR_REDB="\033[1;31m"
	COLOR_NORMAL="\033[0m"
	COLOR_GREEN="\033[32;1m"
	COLOR_GREY="\033[37;1m"
	COLOR_YELLOW="\033[33;1m"
	COLOR_BLUE="\033[34;1m"
	COLOR_MAGENTA="\033[35;1m"
	COLOR_CYAN="\033[36;1m"
	COLOR_LCYAN="\033[0;36m"
	COLOR_INVERSE="\033[7m"
	
	global pathtotg
	global proc
	proc=subprocess.Popen([pathtotg+'bin/telegram','-k',pathtotg+'tg-server.pub'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
	lastmessage=None
	multiline=False
	for line in iter(proc.stdout.readline,''):
		if multiline:
			message+=line
			if line.endswith('[0m\n'):
				message=message.rstrip('[0m\n')
				multiline=False
		else:
			if ((COLOR_YELLOW+" is now online" in line) or (COLOR_YELLOW+" is now offline" in line) or (COLOR_YELLOW+": 0 unread" in line)):
				pass
			print line.rstrip()
			with open('output','a') as fil:
				fil.write(line)
			group=None
			peer=None
			message=None
			try:
				if ((COLOR_BLUE+" >>>" in line) and (COLOR_BLUE+"[" in line)):
					#if you get change colour level errors, uncomment the below line, and comment the line below that.
					#peer=line.split(COLOR_REDB)[1].split(COLOR_RED)[0]
					peer=line.split(COLOR_RED)[1].split(COLOR_NORMAL)[0]
					message=line.split(COLOR_BLUE+" >>> ")[1].split("\033")[0]
					if not line.endswith("[0m\n"):
						multiline=True
				if ((COLOR_GREEN+" >>>" in line)):
					group=line.split(COLOR_MAGENTA)[2].split(COLOR_NORMAL)[0]
					#For change colour level
					#peer=line.split(COLOR_REDB)[1].split(COLOR_RED)[0]
					peer=line.split(COLOR_RED)[1].split(COLOR_NORMAL)[0]
					message=line.split(COLOR_GREEN+" >>> ")[1].strip(COLOR_NORMAL).split("\033")[0]
					if not line.endswith("[0m\n"):
						multiline=True
				if ((COLOR_BLUE+" >>>" in line) and (COLOR_MAGENTA+"[" in line)):
					group=line.split(COLOR_MAGENTA)[2].split(COLOR_NORMAL)[0]
					#for change colour level
					#peer=line.split(COLOR_REDB)[1].split(COLOR_RED)[0]
					peer=line.split(COLOR_RED)[1].split(COLOR_NORMAL)[0]
					message=line.split(COLOR_BLUE+" >>> ")[1].strip(COLOR_NORMAL).split("\033")[0]
					if not line.endswith("[0m\n"):
						multiline=True
			except IndexError:
				print "Error: Change colour levels"
		if( ((group is not None) or (peer is not None)) and (message is not None) and (not multiline)):
			AI(group,peer,message)
	
	
#for twitter to work you need to 'sudo easy_install twitter'
#after that, choose a recepient by changing groupeer below
def twitter():
	#change the group/peer name here to choose where the tweets are sent to
	groupeer="Akshay S Dinesh"
	time.sleep(10)
	tweets=subprocess.Popen(['twitter','-r'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
	for tweet in iter(tweets.stdout.readline,''):
		try:
			author,tweet=tweet.split(' ',1)
		except ValueError:
			continue
		tweet=tweet.replace('\n','')
		follow=["TheHindu","premierleague","WHO","IPL"]
		if (author in follow):
			msg(groupeer,"@"+author,tweet)
		else:
			pass
		time.sleep(1)


#this doesn't work for now
def timeresponse():
	while True:
		if time.strftime("%H")=="00":
			print "time is 12 o'clock"
	
	
def main():
	botthread = Thread(target = bot)
	botthread.start()
	
	twitbot = Thread(target=twitter)
	twitbot.start()
	
	botthread.join()
	twitbot.join()
	
if __name__ == "__main__":
    main()
