python-telegram-bot
===================

This is a telegram bot written in python. It uses the CLI of telegram by vysheng to connect. 

## Note: There is a better bot ##
This python based bot was written when I did not know how to use lua (which is embedded in tg-cli) to extend tg-cli.

But user yagop came up with [a better bot written in lua](https://github.com/yagop/telegram-bot)

I will be submitting my improvements to his repo. If you want to keep up with my own fork, [check this out](https://github.com/asdofindia/telegram-bot)

Since Lua is a lovable language and sicne tg-cli can pass it structured arguments, I will be trying to develop pure Lua modules in the lua bot rather than continue developing in python in this bot here.

Also, currently the way this bot operates is by reading lines from tg-cli output and parsing who sent it, to which group, etc based on the colours of the output. This is very unreliable and buggy and therefore not the preferred way of doing things. Although it works now, it could break any time. So it is wiser to follow the Lua version.

If you still want to use this bot, continue reading. 


## Installation ##

### Install and setup vysheng/tg ###
Install [vysheng's tg cli](http://github.com/vysheng/tg/#installation)

Run that and configure an account
    
    ./telegram -k tg-server.pub
    
### Install dependencies ###
The twitter module requires [Python Twitter Tools](http://mike.verdone.ca/twitter/)
    
    sudo easy_install twitter
    twitter authorize

Install BeautifulSoup and other python modules with easy_install

    sudo easy_install BeautifulSoup

### Download python-telegram-bot ###
Clone this repository by doing
    
    git clone https://github.com/asdofindia/python-telegram-bot.git && cd python-telegram-bot
    
### Configure python-telegram-bot ###
There are a few changes to be made to the source code before it can start working.

In bot.py, change pathtotg to the path to the vysheng's tg CLI
In bot.py, in the twitter function, change groupeer to the telegram user to whom you want the bot to send a message when there's a new tweet.
In bot.py, in the twitter function, change the follow array to the accounts you want to get updates from
In wolfram.py, put an appid by signing up at wolfram developers

### Disabling modules ###
If you don't want some of these modules, just remove them from the modules array in callmodule function
If you want to disable twitter, just comment out all lines with 'twitbot' in it in the main function.
If you want to disable robotic replies turn chattybot to False

## Features ##
The features as of now are
  
* can be invoked from within a group or a direct message
* wiki "search terms" will return the first paragraph of the wikipedia article
* google "search terms" will return a few google results
* bot "question" will fetch the answer from wolfram alpha api
* new twitter messages from your feed are automatically sent to the defined peer
* talks random shit based on pandorabots web service thanks to chatterbotapi

## Known Bugs ##

* twitter module repeats tweets. This is more of a problem with the twitter python module rather than this code. Todo: prevent duplicate tweets using timestamp
* chatting with oneself is buggy, I suppose. Not tested very much. No time :P
