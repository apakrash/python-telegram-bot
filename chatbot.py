# <libraries>


import nltk
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from wakeonlan import send_magic_packet
import sys,os



from pyHS100 import SmartPlug, SmartBulb
from pprint import pformat as pf


# </libraries>


# <global settings>


#setting up the TPLink plug
plug = SmartPlug("192.168.1.2")




global allMessages
allMessages=[]


#just to test if interupt has broken sequence
print('The Matrix has you')


#sample file name
file='allMessages.txt'


# </global settings>






# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


logger = logging.getLogger(__name__)


# <functions>




def tokenLemmatizer(text):
    
        ###### <brain of the code> ######
        ### return  text in  the variable token 
    
    
        '''lemmatizer=nltk.stem.WordNetLemmatizer()
        tokenizer3 = nltk.tokenize.WordPunctTokenizer()
        tokens = tokenizer3.tokenize(text)'''
    
    
        if text == 'off' or text == 'Off':
            plug.turn_off()
            token = 'off'
            token = 'bulb is  ' + str(plug.state)


        elif text == 'on' or text == 'On':
            plug.turn_on()
            token = 'on'
            token = 'bulb is  ' + str(plug.state)


        elif text == 'state' or text == 'State':
            token = 'bulb is  ' + str(plug.state)
                        
        elif text == 'imperium' or text == 'Imperium':
            token = 'powering up Mark IV'
            send_magic_packet('08.62.66.37.2a.f0')
        
        elif text == 'dormir' or text == 'Dormir':
            token = 'powering down mark IV'
            os.system('sh shutdownTelnet.sh')
            
        elif text == 'dmc' or text == 'Dmc':
            token = 'Launching DevilMayCry'
            os.system('sh dmc_start.sh')
                    
    
        return token


        #this is the NLP return code, for now using the light status
        #return (" ".join(lemmatizer.lemmatize(token) for token in tokens))


                
        ###### <brain of the code> ######
    




def writeFile(file,allMessages):
        fh = open("allMessages.txt",'a')
        sampleString=''
        for listElement in allMessages:
            sampleString+=listElement
            sampleString+='\n'
        fh.write(sampleString)
        fh.close()


def writeLineToFile(file,line):
        fh = open("allMessages.txt",'a')
        line+='\n'
        fh.write(line)
        fh.close()


def printFile(file):
        fh = open("hello1.txt","r")
        print(fh.read())
        fh.close()
    
    
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Welcome back sir!')




def help(bot, update):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')


'''


The function echo is the game changing function


'''
    
def echo(bot, update):
        """Echo the user message."""
        print(update.message.text)
        allMessages.append(update.message.text)
        writeLineToFile(file,update.message.text)
        update.message.text = tokenLemmatizer(update.message.text)
        update.message.reply_text(update.message.text)




def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)




def main():
        """Start the bot."""
        # Create the EventHandler and pass it your bot's token.
        
        ### This is the telegram bot token
        
        updater = Updater("BOT TOKEN")


        # Get the dispatcher to register handlers
        dp = updater.dispatcher


        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))


        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))


        # log all errors
        dp.add_error_handler(error)


        # Start the Bot
        updater.start_polling()


        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
    
# <functions>


if __name__ == '__main__':
        main()