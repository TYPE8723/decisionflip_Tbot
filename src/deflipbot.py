import telebot
import random as rdm

#API_KEY = os.getenv('API_KEY')
API_KEY = ''
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands = ['flip','dice'])
def cmd(message):
    #print(message)
    #print(message.from_user.first_name)
    if message.text == '/flip':
        output = coinflip()#fliping a coin
        return bot.reply_to(message,output)
    elif message.text == '/dice':
        output = dice()#throwing a dice
        return bot.reply_to(message,output)
    else:
        return bot.reply_to(message,'Invalid choice')

#fliping a coin
def coinflip():
    results = ['Heads','Tails','Heads','Tails','Heads','Tails','Heads','Tails']
    return rdm.choice(results)

#throwing a dice
def dice():
    results = ['1','2','3','4','5','6','1','2','3','4','5','6']
    return rdm.choice(results)
    
    
bot.polling()