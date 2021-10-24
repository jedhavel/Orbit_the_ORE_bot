#!/usr/bin/python

import sys
import os
import telegram
from telegram import ParseMode
import telegram.ext
import re
from random import randint
import logging
from secrets import *
from config import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if ENV == "PROD":
    apikey = API_KEY
else:
    apikey = TEST_API_KEY

dataloc = os.path.join("..", "data") # rel path to the data folder
linkfile = os.path.join(dataloc, LINKFILE)
shillfile = os.path.join(dataloc, SHILLFILE)



# Create an updater object with our API Key
updater = telegram.ext.Updater(apikey)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher

# helper functions
def readlinks(linkfile):
    with open(linkfile, 'r') as file:
        data = file.read() #.replace('\n', '')
        return data

def readshill(shillfile):
    with open(shillfile, 'r') as file:
        data = file.read() #.replace('\n', '')
        return data

def addlink(link, linkfile):
    with open(linkfile, 'a') as file:
        file.write(link)
    return readlinks(linkfile)

def userfilepath(username):
    return os.path.join(dataloc, username, linkfile)

# Our states, as integers
# WELCOME = 0
# QUESTION = 1
# CANCEL = 2
# CORRECT = 3

# Entry Functions
def link(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    #update_obj.message. (ParseMode.MARKDOWN_V2) doesn't have attribute parse_mode
    # context.from_user
    update_obj.message.reply_text(readlinks(linkfile), parse_mode="MarkdownV2")
    # end the conversation
    return telegram.ext.ConversationHandler.END

def contract(update_obj, context):
    update_obj.message.reply_text(CONTRACT)
    # end the conversation
    return telegram.ext.ConversationHandler.END

def shill(update_obj, context):
    update_obj.message.reply_text(readshill(shillfile))
    # end the conversation
    return telegram.ext.ConversationHandler.END

#def webpage(update_obj, context):
#    link(update_obj, context)

# a regular expression that matches yes or no
yes_no_regex = re.compile(r'^(yes|no|y|n)$', re.IGNORECASE)
# Create our ConversationHandler, with only one state
handler = telegram.ext.ConversationHandler(
      entry_points=[telegram.ext.CommandHandler('link', link),
      telegram.ext.CommandHandler('contract', contract),
      telegram.ext.CommandHandler('shill', shill),
      telegram.ext.CommandHandler('website', link),
      # Spanish commands
      telegram.ext.CommandHandler('contrato', contract),
      telegram.ext.CommandHandler('complice', shill),
      telegram.ext.CommandHandler('pagina', link),
      telegram.ext.CommandHandler('enlace', link),
      # Alias commands
      telegram.ext.CommandHandler('webpage', link)],
      states={},
      fallbacks=[telegram.ext.CommandHandler('link', link)],
      )
# add the handler to the dispatcher
dispatcher.add_handler(handler)

# link polling for updates from Telegram
updater.start_polling()
# block until a signal (like one sent by CTRL+C) is sent
updater.idle()
