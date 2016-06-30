## Egor Kolesnikov
##
## Text generator based on Markov's chaining.
## Tis module generating the text using database, created by Generator.py
##

import pickle
import random


def load_database():
    with open('db_words.pickle', 'rb') as file:
        db_words = pickle.load(file)
    with open('db_pairs.pickle', 'rb') as file:
        db_pairs = pickle.load(file)
    return db_words, db_pairs


def generate(sentences, db_words, db_pairs):
    generated_text = "\t"
    db_words_keys = db_words.keys()
    text_length = -1
    while sentences:
        generated_text += generate_sentence(db_words, db_pairs, db_words_keys)
        generated_text += " "
        if random.randrange(0, 1000) > 800:
            generated_text += "\n"
            generated_text += "\t"
        sentences -= 1
    return generated_text


def generate_sentence(db_words, db_pairs, db_words_keys):
    sentence_capacity = 73
    sentence = ""
    first = db_words_keys[random.randrange(0, len(db_words_keys))]
    sentence += first
    second = db_words[first].keys()[random.randrange(0, len(db_words[first]))]
    if second not in "!.?":
        sentence += " "
    sentence += second
    while sentence_capacity and second not in "!.?":
        index = random.randrange(0, len(db_pairs[(first, second)]))
        word = db_pairs[(first, second)].keys()[index]
        if word not in "!.?":
            sentence += " "
        sentence += word
        first = second
        second = word
        sentence_capacity -= 1
    if sentence[-1] not in "!.?":
        sentence += "."
    sentence = sentence[0].upper() + sentence[1:]
    return sentence


def main():
    db_words, db_pairs = load_database()
    result = generate(400, db_words, db_pairs)
    with open('result.dat', 'wb') as file:
        file.write(result)


if __name__ == '__main__':
    main()

