import telebot as tbot
import datetime as timeframe
import random as rdm

#API_KEY = os.getenv('API_KEY')
API_KEY = ''

data = {}
QR_request_text_id = 0
bot = tbot.TeleBot(API_KEY)

# bot.send_message(message.chat.id, text) #normal reply message
# bot.send_photo(message.chat.id, output)# send photo from response of a url
@bot.message_handler(commands = ['start','flip','dice','generate_QR'])
@bot.message_handler(content_types = ['text'])
def cmd(message):
    print(message.text)
    user_details = message.from_user.first_name + ' at ' +str(timeframe.datetime.now())[:19]
    with open("./userlogs.txt","a") as log_file:
        log_file.write(str(user_details)+'\n')
    log_file.close()
    global data,QR_request_text_id
    #fliping a coin
    if message.text == '/flip':
        QR_request_text_id = 0 #turning qr code flag off
        output = coinflip()
        return bot.reply_to(message,output)
    
    #throwing a dice
    elif message.text == '/dice':
        QR_request_text_id = 0 #turning qr code flag off
        output = dice()
        return bot.reply_to(message,output)
    
    #generate QR code
    elif message.text == '/generate_QR':
        data[message.chat.username] = message.message_id
        QR_request_text_id = message.message_id
        output = qrcodeprompt(message)
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
                return bot.send_photo(message.chat.id, output)
            else:
                return bot.reply_to(message,'Invalid choice')
        except:
            return bot.reply_to(message,'Invalid choice')
            
    
    
#starting the bot
def start(message):
    output = 'Hi welcome to DeFlip!\n /flip to flip a coin 🟡\n /dice to roll a dice 🎲\n /generate_QR to generate a QR codes from your text🤳🏻'
    #custom buttons
    markup = tbot.types.ReplyKeyboardMarkup()
    itembtn1 = tbot.types.KeyboardButton('/flip')
    itembtn2 = tbot.types.KeyboardButton('/dice')
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

#qrcode text prompt
qrcodeprompt = lambda x:bot.reply_to(x,'Please send me the texts to create a QR code')

#generating QR code
#CONVERT TO LAMBDA!!!!
def qrcode(qr_text):
    request_data = 'https://api.qrserver.com/v1/create-qr-code/?data='+qr_text+'&size=500x500'
    return request_data
    
    
    
bot.polling()