import stickerpack
import telebot as tbot
import datetime as timeframe
import random as rdm
import sys

#API_KEY = os.getenv('API_KEY')
API_KEY = ''

data = {}
QR_request_text_id = 0


bot = tbot.TeleBot(API_KEY)

# bot.send_message(message.chat.id, text) #normal reply message
# bot.send_photo(message.chat.id, output)# send photo from response of a url
@bot.message_handler(commands = ['start','flip','roll','generate_QR'])
@bot.message_handler(content_types = ['text'])
def cmd(message):
    #print(message.text)
    user_details = message.from_user.first_name + ' at ' +str(timeframe.datetime.now())[:19]
    with open("./userlogs.txt","a") as log_file:
        log_file.write(str(user_details)+'\n')
    log_file.close()
    global data,QR_request_text_id
    #fliping a coin
    if message.text == '/flip':
        QR_request_text_id = 0 #turning qr code flag off
        output = coinflip()
        bot.send_sticker(chat_id = message.chat.id, sticker = stickerpack.stickers_TheCoin[1])
        return bot.reply_to(message,output)
    
    #throwing a dice
    elif message.text == '/roll':
        QR_request_text_id = 0 #turning qr code flag off
        output = dice()
        return bot.reply_to(message,output)
    
    #generate QR code
    elif message.text == '/generate_QR':
        data[message.chat.username] = message.message_id
        QR_request_text_id = message.message_id
        reply_text = "Please send me the texts to create a QR code"
        output = command_reply(message,reply_text)
        return output
        
       
    #start/welcome command
    elif message.text == '/start':
        output = start(message)
        return output
        
    #invalid command
    else:
        try:
            if data[message.chat.username] == QR_request_text_id:# reading text for qr code
                output = qrcode(message.text)
                if output:
                    with open("./userlogs.txt","a") as qr_log:
                       qr_log.write('****'+str(user_details)+' Generated QR text : ['+ message.text+']\n')
                    bot.send_photo(message.chat.id, output)
                return bot.send_message(message.chat.id, 'To exit 🚪 QR code generation select any other commands')
            else:
                return bot.reply_to(message,'Invalid choice')
        except:
            print('error :'+ str(sys.exc_info()[0]))
            print(' !!!!TRIGGERD Invalid choice!!!!!')
            return bot.reply_to(message,'Invalid choice')
            
    
    
#starting the bot
def start(message):
    output = 'Hey... welcome to DeFlip!\n /flip a coin 🟡\n /roll a dice 🎲\n /generate_QR to generate a QR codes from your text🤳🏻'
    #custom buttons
    markup = tbot.types.ReplyKeyboardMarkup()
    itembtn1 = tbot.types.KeyboardButton('/flip')
    itembtn2 = tbot.types.KeyboardButton('/roll')
    itembtn3 = tbot.types.KeyboardButton('/generate_QR')
    #markup = tbot.types.ReplyKeyboardMarkup(row_width = 1)
    #markup.add(itembtn1, itembtn2)
    markup.row(itembtn1)
    markup.row(itembtn2)
    markup.row(itembtn3)
    bot.send_message(message.chat.id, output , reply_markup=markup)
    return output

#fliping a coin
def coinflip():
    results = ['Heads','Tails','Heads','Tails','Heads','Tails','Heads','Tails']
    return rdm.choice(results)

#throwing a dice
def dice():
    results = ['1','2','3','4','5','6','1','2','3','4','5','6']
    return rdm.choice(results)
#generating QR code
qrcode = lambda qr_text:'https://api.qrserver.com/v1/create-qr-code/?data='+qr_text+'&size=500x500'

#bot reply prompt
command_reply = lambda message,reply_text :bot.reply_to(message,reply_text)
    
bot.polling()