import telebot
import mysql.connector
from mysql.connector import Error
from config import TOKEN
from config import DB_HOST
from config import DB_USER
from config import DB_PASSWORD
from config import DB_NAME

connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
if connection.is_connected():
    print('Connected to MySQL database')

cursor = connection.cursor()

def registerUser(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_firstname = message.from_user.first_name
    user_lastname = message.from_user.last_name

    cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (user_id,))
    user = cursor.fetchone()
    print("Регистрация нового пользователя. ", message.from_user)

    if user:
        # Если пользователь уже существует, можем выполнить какие-то действия, например, обновить информацию
        print("Пользователь уже есть в БД.")
    else:
        print("Создаём новую запись в БД.")
        cursor.execute("INSERT INTO users (telegram_id, username, first_name, last_name) VALUES (%s, %s, %s, %s)",
                   (user_id, user_name, user_firstname, user_lastname))
    connection.commit()
    cursor.close()


# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    registerUser(message)
    bot.reply_to(message, "Привет! Я такси-бот")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Это простой бот. Я могу отвечать на команду /start и /help.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запускаем бота
bot.polling()
