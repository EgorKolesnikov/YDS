## Egor Kolesnikov
##
## Text generator based on Markov's chaining.
## This module creates the database of frequency of occurrence words, pair of words and triplets.
##

import os
import re
import pickle


db_pairs = {}
db_words = {}


def create_database(start_path):
    os.chdir("Books")
    for folder in os.listdir("."):
        if os.path.isdir(folder):
            for file_name in os.listdir(start_path + "/" + folder):
                read_file(folder, start_path, file_name)
    return


def read_file(folder, start_path, file_name):
    with open(start_path + "/" + folder + "/" + file_name) as file:
        ## split words
        pattern = "([a-zA-Z]+['-]?[a-zA-Z]+[!.?]*)+"
        whole_text = ""
        for line in file:
            line = line.rstrip('\n \t') + " "
            whole_text += line
        words = re.findall(pattern, whole_text)
        for word in xrange(len(words)):
            words[word] = words[word].lower()
            if words[word][-1] in "!.?" and len(words[word]) == 1:
                pass
            elif words[word][-1] in "!.?":
                words.insert(word + 1, words[word][-1])
                words[word] = words[word][0:-1]
        ## generating statistic
        words.append(".")
        for now in xrange(len(words) - 2):
            if words[now] in "!.?":
                pass
            ## statistic for unique words
            if words[now] in db_words:
                if words[now + 1] in db_words[words[now]]:
                    db_words[words[now]][words[now + 1]] += 1
                else:
                    db_words[words[now]][words[now + 1]] = 1
            else:
                db_words[words[now]] = {}
                db_words[words[now]][words[now + 1]] = 1
            ## statistic for pairs of words
            if (words[now], words[now + 1]) in db_pairs:
                if words[now + 2] in db_pairs[(words[now], words[now + 1])]:
                    db_pairs[(words[now], words[now + 1])][words[now + 2]] += 1
                else:
                    db_pairs[(words[now], words[now + 1])][words[now + 2]] = 1
            else:
                db_pairs[(words[now], words[now + 1])] = {}
                db_pairs[(words[now], words[now + 1])][words[now + 2]] = 1
        ## check last two words, which had not been included in loop
        now = len(words) - 2
        if words[now] in db_words:
            if words[now + 1] in db_words[words[now]]:
                db_words[words[now]][words[now + 1]] += 1
            else:
                db_words[words[now]][words[now + 1]] = 1
        else:
            db_words[words[now]] = {}
            db_words[words[now]][words[now + 1]] = 1
    return


def save_database():
    os.chdir("../")
    with open('db_words.pickle', 'wb') as file:
        pickle.dump(db_words, file)
    with open('db_pairs.pickle', 'wb') as file:
        pickle.dump(db_pairs, file)
    return


def main():
    ## I'm on Linux, so "/" instead of "\\"
    start_path = os.getcwdu() + "/"
    start_path += "Books"
    create_database(start_path)
    save_database()


if __name__ == '__main__':
    main()

