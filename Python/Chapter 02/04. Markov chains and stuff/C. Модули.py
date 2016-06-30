# -*- coding: utf-8 -*-
import re
import sys


def get_imports(found):
    return [i for i in found if i != "from" and i != "import"]


def main():
    regex = '(?:(^from [a-z]+ import)+|(import [\w,. ]+)+)'
    all_imports = set()

    line = sys.stdin.readline()
    while line:
        line = line.strip()
        result = re.findall(regex, line)
        if result:
            for found in result:
                found = [element for element in found if len(element) > 0]
                all_imports.update(get_imports(re.split(", | ", found[0])))
        line = sys.stdin.readline()
    print (', '.join(sorted(list(all_imports)))).strip()

if __name__ == '__main__':
    main()
