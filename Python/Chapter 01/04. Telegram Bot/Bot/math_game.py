import re
import copy
import random
import config
from telebot import types


class MathGame:
    def __init__(self):
        self.database = {}
        self.answered_all = 0
        self.answered_right = 0
        with open(config.math_db) as file:
            for line in file:
                line = line.strip()
                tokens = re.split(':|,', line)
                self.database[tokens[0]] = tokens[1:]
        self.keys = self.database.keys()

    def getNextRound(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        next_round = self.keys[random.randrange(0, len(self.keys))]
        answers = copy.copy(self.database[next_round])
        random.shuffle(answers)
        for item in answers:
            markup.add(item)
        return (next_round, markup)

    def checkAnswer(self, key, answer):
        self.answered_all += 1
        if self.database[key][0] == answer:
            self.answered_right += 1
            return True
        else:
            return False
