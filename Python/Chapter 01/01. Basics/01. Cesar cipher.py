## Egor Kolesniokov
##
## Cesar cipher
##

import sys


def cesar_cypher(key, text):
    answer = ""
    for symbol in text:
        if symbol.islower():
            answer += chr((ord(symbol) - 97 + key) % 26 + 97)
        elif symbol.isupper():
            answer += chr((ord(symbol) - 65 + key) % 26 + 65)
        else:
            answer += symbol
            continue
    print(answer)
    return


key, text = sys.stdin.readlines()
key = int(key)
cesar_cypher(key, text)

