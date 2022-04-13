import qrcode
import random
from datetime import datetime
import telebot
import mysql.connector as mysql

bot = telebot.TeleBot("5239236978:AAFYs8tCXGI9sGh5UhIjNCh9uOqANi1Yp8Y")

cLetters = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ]
sLetters = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]
numbers = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
symbols = [ "@", "#", "$" ]

idCharacters = cLetters + sLetters + numbers + symbols

qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
        

@bot.message_handler(commands=["start"])
def send_welcome(message):
    fName = message.from_user.first_name
    bot.send_message(message.chat.id, "Hi " + fName + "! I'll help you to create an event.\n\n\
/newevent - Add a new event.\n\
/delevent - Delete an event.\n\
/eevent - Edit event.\n\
/test - QR generation", parse_mode="HTML")
                             
host = "141.8.192.151"
database = "f0658097_telegram"
user = "f0658097_telegram"
password = "hapaumucdi$"

myConnection = mysql.connect()
print(mysql.__version_info__)

@bot.message_handler(commands=["test"])
def send_code(message):
    now = datetime.now()

    uID = message.from_user.id
    uName = message.from_user.username

    fName = message.from_user.first_name
    lName = message.from_user.last_name
    currentDate = now.strftime("%d-%m-%Y %H:%M:%S")

    tempID = random.sample(idCharacters, 24)
    unicalID = "".join(tempID)

    input_data = {
        "unicalID": unicalID,
        "userID": uID,
        "userName": uName,
        "eventID": "Test Event",
        "fName": fName,
        "lName": lName,
        "rDate": currentDate
    }

    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('database/'+ unicalID + '.png')
    bot.send_photo(message.from_user.id, open('database/' + unicalID + '.png', 'rb'))

bot.polling(none_stop=True, interval=0)