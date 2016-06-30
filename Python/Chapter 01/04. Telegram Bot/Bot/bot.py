# -*- coding: utf-8 -*-
import telebot
import config
import math_game
import weather
import urllib2
from telebot import types
from time import sleep


class BotState:
    def __init__(self):
        self.bot = telebot.TeleBot(config.token)
        self.playing = False
        self.weather = False
        self.busy = False
        self.answer = ""


my_bot = BotState()


@my_bot.bot.message_handler(commands=['help'])
def handle_start_help(message):
    my_bot.bot.send_message(message.chat.id, config.help_info)
    pass


@my_bot.bot.message_handler(commands=['weather'])
def handle_start_help(message):
    my_bot.busy = True
    my_bot.weather = True
    my_bot.answer = ""
    try:
        my_bot.bot.send_message(message.chat.id, "Conntecting...")
        weather_checker = weather.Weather()
        my_bot.bot.send_message(message.chat.id, config.weather_intro)
        while my_bot.answer == "":
            pass
        location = my_bot.answer.split(" ")
        if my_bot.answer != config.stop_weather_request.lower():
            result = weather_checker.getWeather(location[0], location[1])
            my_bot.bot.send_message(message.chat.id, u"В городе " + location[1] +
                                                     u" сейчас " + result[1] +
                                                     u". Температура составляет " +
                                                     result[0] + u" градус(а) по Цельсию.")
        else:
            my_bot.bot.send_message(message.chat.id, config.stop_weather_answer)
    except LookupError:
        if len(location) != 2:
            my_bot.bot.send_message(message.chat.id, 
                                    config.ERROR_invalid_parameter)
        else:
            my_bot.bot.send_message(message.chat.id, 
                                    config.ERROR_invalid_city_country)
    except urllib2.URLError:
        my_bot.bot.send_message(message.chat.id, config.ERROR_connection_failed)
    finally:
        my_bot.busy = False
        my_bot.weather = False
        my_bot.answer = ""


@my_bot.bot.message_handler(commands=['math'])
def handle_start_help(message):
    game = math_game.MathGame()
    my_bot.busy = True
    my_bot.playing = True
    my_bot.bot.send_message(message.chat.id, config.game_intro)
    sleep(4)
    while True:
        round = game.getNextRound()
        my_bot.bot.send_message(message.chat.id, round[0],
                                reply_markup=round[1])
        while my_bot.answer == "":
            pass
        if my_bot.answer == config.stop_playing_request.lower():
            my_bot.bot.send_message(message.chat.id,
                                    config.stop_playing_answer,
                                    reply_markup=types.ReplyKeyboardHide())
            break
        else:
            result = game.checkAnswer(round[0], my_bot.answer)
            my_bot.bot.send_message(message.chat.id, 
                                    config.game_answer[result])
        my_bot.answer = ""
    my_bot.bot.send_message(message.chat.id,
                            "You answered " + str(game.answered_all) +
                            " times. " + str(game.answered_right) +
                            " of them were correct.")
    my_bot.busy = False
    my_bot.playing = False
    my_bot.answer = ""


@my_bot.bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    if my_bot.busy:
        if my_bot.playing:
            if message.text.lower() == config.stop_playing_request.lower():
                my_bot.answer = config.stop_playing_request.lower()
            else:
                my_bot.answer = message.text
        if my_bot.weather:
            if message.text.lower() == config.stop_weather_request.lower():
                my_bot.answer = config.stop_weather_request.lower()
            else:
                my_bot.answer = message.text
    else:
        my_bot.bot.send_message(message.chat.id, 
                                "Evetyone can say " + message.text
                                + " but you just do it and buy an elephant.")
    pass


if __name__ == '__main__':
    my_bot.bot.polling(none_stop=True)
