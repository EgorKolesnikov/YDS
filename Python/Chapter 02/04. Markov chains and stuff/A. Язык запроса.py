# -*- coding: utf-8 -*-
import sys


def init_alphabets():
    alphabets = {}
    line = sys.stdin.readline()
    while len(line) > 1:
        country, alphabet = line.split()
        alphabets[country] = alphabet
        line = sys.stdin.readline()
    return alphabets


def get_word_language(alphabets, word):
    count_language_letters = {country: 0 for country in alphabets.keys()}
    for letter in word:
        for country, alphabet in alphabets.iteritems():
            if letter.lower() in alphabet or letter.upper() in alphabet:
                count_language_letters[country] += 1
    max_letter_count = 0
    max_country = ''
    for key in sorted(alphabets):
        if count_language_letters[key] > max_letter_count:
            max_letter_count = count_language_letters[key]
            max_country = key
    return max_country


def check_language(alphabets, words):
    verdict = set()
    for word in words:
        verdict.add(get_word_language(alphabets, word))
    return verdict


def main():
    reload(sys)
    sys.setdefaultencoding("utf8")
    alphabets = init_alphabets()
    line = sys.stdin.readline()
    result = []
    while line:
        line = line.decode("utf8")
        result.append(check_language(alphabets, line.split()))
        line = sys.stdin.readline()
    for test in result:
        print (' '.join(sorted(list(map(str, test))))).strip()


if __name__ == '__main__':
    main()
