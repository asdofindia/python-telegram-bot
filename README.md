python-telegram-bot
===================

This is a telegram bot written in python. It uses the CLI of telegram by vysheng to connect. 

## Installation ##

### Install and setup vysheng/tg ###
Install [vysheng's tg cli](http://github.com/vysheng/tg)
    git clone https://github.com/vysheng/tg.git && cd tg
    ./configure
    make
Run that and configure an account
    ./telegram -k tg-server.pub
    
### Install dependencies ###
The twitter module requires [Python Twitter Tools](http://mike.verdone.ca/twitter/)
    sudo easy_install twitter
    twitter authorize

### Download python-telegram-bot ###
Clone this repository by doing
    git clone https://github.com/asdofindia/python-telegram-bot.git && cd tg
    
### Configure python-telegram-bot ###
There are a few changes to be made to the source code before it can start working.

In bot.py, change pathtotg to the path to the vysheng's tg CLI
In bot.py, in the twitter function, change groupeer to the telegram user to whom you want the bot to send a message when there's a new tweet.
In bot.py, in the twitter function, change the follow array to the accounts you want to get updates from
In wolfram.py, put an appid by signing up at wolfram developers

### Disabling modules ###
If you don't want some of these modules, just remove them from the modules array in callmodule function
If you want to disable twitter, just comment out all lines with 'twitbot' in it in the main function.


## Features ##
The features as of now are
  
* can be invoked from within a group or a direct message
* wiki <search terms> will return the first paragraph of the wikipedia article
* google <search terms> will return a few google results
* bot <question> will fetch the answer from wolfram alpha api
* new twitter messages from your feed are automatically sent to the defined peer
