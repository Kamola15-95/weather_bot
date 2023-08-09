import requests
from telebot import TeleBot
from telebot.types import Message
from keyboards import generate_start_button
from datetime import datetime

TOKEN = '6267674591:AAHpHvUmHBybeFIEIVZW7eHxRbiFwTSh-UQ'

bot = TeleBot(TOKEN)

weather_emojis = {
    'ясно': '☀️',
    'небольшая облачность': '🌤',
    'облачно': '☁️',
    'дождь': '🌧️',
    'гроза': '⛈️',
    'снег': '❄️',
    'туман': '🌫️'
}

@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    text = 'Здравствуйте! Чтобы узнать погоду, нажмите кнопку ниже: '
    bot.send_message(chat_id, text, reply_markup=generate_start_button())

@bot.message_handler(commands=['help'])
def command_help(message: Message):
    chat_id = message.chat.id
    text = 'Вас приветствует бот погоды. С моей помощью Вы можете узнать погоду в любом город мира. Чтобы узнать погоду, нажмите кнопку ниже:'
    bot.send_message(chat_id, text, reply_markup=generate_start_button())

@bot.message_handler(regexp='Weather')
def reaction_to_weather_button(message: Message):
    chat_id = message.chat.id
    text = 'Введите город, в котором хотите узнать погоду: '
    bot.send_message(chat_id, text)

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    chat_id = message.chat.id
    city = message.text
    parameters = {
        'appid': '3c5d80d981b08e6f688a773aaacf017d',
        'units': 'metric',
        'lang': 'ru'
    }
    parameters['q'] = city
    try:
        data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters).json()
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        timezone = data['timezone']
        sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + timezone).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + timezone).strftime('%H:%M:%S')
        emoji = weather_emojis.get(description, '')
        weather = f'''В городе {city} сейчас {description} {emoji}
Температура: {temp} °C
Скорость ветра: {wind_speed} м/с
Рассвет: {sunrise}
Закат: {sunset}'''
        bot.send_message(chat_id, weather, reply_markup=generate_start_button())
        bot.send_message(chat_id, 'Введите город, в котором хотите узнать погоду: ')
    except:
        text = 'Неверный город. Попробуйте снова'
        bot.send_message(chat_id, text)

bot.polling(none_stop=True)