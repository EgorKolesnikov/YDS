import argparse
import sys


class ImageMagick:
    brightness = "@%#*+=-:. "

    def __init__(self, picture):
        self.picture = [picture[i][:-1] for i in xrange(len(picture))]
        self.height = len(self.picture)
        self.width = len(self.picture[0])

    def do_command(self, command, params):
        if command == 'crop':
            self.crop(params)
        elif command == 'expose':
            self.expose(params)
        else:
            self.rotate(params)
        self.print_picture()

    def crop(self, params):
        new_picture = [[''] * (self.width -
                               (params['left'] + params['right']))
                       for i in xrange(self.height -
                                       (params['top'] + params['bottom']))]
        for row in xrange(len(new_picture)):
            for column in xrange(len(new_picture[row])):
                new_picture[row][column] = \
                    self.picture[row + params['top']][column + params['left']]
        self.picture = new_picture

    def expose(self, param):
        param = int(param[0])
        new_picture = [[''] * self.width
                       for i in xrange(self.height)]
        for row in xrange(self.height):
            for column in xrange(self.width):
                now = ImageMagick.brightness.index(self.picture[row][column])
                if param > 0:
                    new_picture[row][column] = ImageMagick.brightness[min(now + param, 9)]
                else:
                    new_picture[row][column] = ImageMagick.brightness[max(0, now + param)]
        self.picture = new_picture

    def rotate(self, param):
        rotate = int(param[0]) % 360
        if rotate == 90:
            new_picture = [[''] * self.height
                           for i in xrange(self.width)]
            for row in xrange(self.height):
                for column in xrange(self.width):
                    new_picture[self.width - column - 1][row] = self.picture[row][column]
            self.picture = new_picture
        elif rotate == 180:
            new_picture = [[''] * self.width
                           for i in xrange(self.height)]
            for row in xrange(self.height):
                for column in xrange(self.width):
                    new_picture[self.height - row - 1][self.width - column - 1] = \
                        self.picture[row][column]
            self.picture = new_picture
        elif rotate == 270:
            new_picture = [[''] * self.height
                           for i in xrange(self.width)]
            for row in xrange(self.height):
                for column in xrange(self.width):
                    new_picture[column][self.height - row - 1] = self.picture[row][column]
            self.picture = new_picture

    def print_picture(self):
        for row in self.picture:
            print ''.join(list(map(str, row)))


def read():
    command = raw_input().split()
    params = command[1:]
    command = command[0]
    if command == 'crop':
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--left', type=int, default=0)
        parser.add_argument('-r', '--right', type=int, default=0)
        parser.add_argument('-t', '--top', type=int, default=0)
        parser.add_argument('-b', '--bottom', type=int, default=0)
        params = vars(parser.parse_args(params))
    picture = sys.stdin.readlines()
    return command, params, picture


def main():
    command, params, picture = read()
    image = ImageMagick(picture)
    image.do_command(command, params)


if __name__ == '__main__':
    main()
