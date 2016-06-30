# -*- coding: utf-8 -*-
import re
import sys


regex_string = ur'(\d{4}-\d{2}-\d{2}\n)+|(\d{4}/\d{2}/\d{2}\n)+|' + \
               ur'(\d{4}\.\d{2}\.\d{2}\n)+|(\d{2}-\d{2}-\d{4}\n)+|' +\
               ur'(\d{2}[/]\d{2}[/]\d{4}\n)+|(\d{2}\.\d{2}\.\d{4}\n)+|' +\
               ur'(\d{1,2}[ ]*[а-я]+[ ]*\d{4})+'


def main():
    reload(sys)
    sys.setdefaultencoding("utf8")
    line = sys.stdin.readline()
    reg = re.compile(regex_string, re.UNICODE)
    while line:
        line = line.decode("utf8") + '\n'
        found = reg.match(line)
        print "NO" if found is None else "YES"
        line = sys.stdin.readline()

if __name__ == '__main__':
    main()
