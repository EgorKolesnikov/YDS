## Egor Kolesnikov
##
## Shuffling letters in words. First and last letters are not changing their positiona.
##

import sys
import random
import string
import re


def shuffle_one_word(word):
    if len(word) > 3:
        temp_list = list(word[1:-1])
        random.shuffle(temp_list)
        word = word[0] + ''.join(temp_list) + word[-1]
    return word


def check_scientists_theory(whole_text):
    pattern = re.compile("[^a-zA-Z_]")
    only_words = re.sub(pattern, ' ', whole_text).split()
    position = 0
    word_count = 0
    while position < len(whole_text):
        if whole_text[position].isalpha():
            shuffled = shuffle_one_word(only_words[word_count])
            length = len(shuffled)
            whole_text = (whole_text[0:position] +
                          shuffled +
                          whole_text[(position + length):])
            word_count += 1
            position += length
        else:
            position += 1
    return whole_text


text = sys.stdin.read()
result = check_scientists_theory(text)
print(result)

