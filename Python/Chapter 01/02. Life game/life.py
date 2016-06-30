## Egor Kolesnikov
##
## Life game (in the sea). 
## Input data: size of the world, world, number of generations (k) to generate.
## Output data: world's state after k generations
##

class Life:

    Empty = 0
    Rock = 1
    Fish = 2
    Shrimp = 3

    def __init__(self, input_size, input_sea, generations):
        self.rows = input_size[0]
        self.columns = input_size[1]
        self.new_sea = [[0]*self.columns for i in range(self.rows)]
        self.old_sea = [[0]*self.columns for i in range(self.rows)]
        for row in range(self.rows):
            for column in range(self.columns):
                self.old_sea[row][column] = input_sea[row][column]
                self.new_sea[row][column] = input_sea[row][column]

    def copy_state(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.old_sea[row][column] = self.new_sea[row][column]

    def start(self, generations):
        while generations > 0:
            for row in range(self.rows):
                for column in range(self.columns):
                    if self.old_sea[row][column] == Life.Empty:
                        self.check_empty(row, column)
                    elif self.old_sea[row][column] != Life.Rock:
                        self.check_living_thing(row, column)
            self.copy_state()
            generations -= 1

    def check_empty(self, row, column):
        count_fish = 0
        count_shrimps = 0
        for i in xrange(row - 1, row + 2):
            for j in xrange(column - 1, column + 2):
                if(i not in range(self.rows) or
                   j not in range(self.columns) or
                   i == row and j == column):
                    pass
                elif self.old_sea[i][j] == 2:
                    count_fish += 1
                elif self.old_sea[i][j] == 3:
                    count_shrimps += 1
        if count_shrimps == 3:
            self.new_sea[row][column] = 3
        if count_fish == 3:
            self.new_sea[row][column] = 2
        return

    def check_living_thing(self, row, column):
        count = 0
        for i in xrange(row - 1, row + 2):
            for j in xrange(column - 1, column + 2):
                if(i not in range(self.rows) or
                   j not in range(self.columns) or
                   i == row and j == column):
                    pass
                elif self.old_sea[i][j] == self.old_sea[row][column]:
                    count += 1
        if count < 2 or count > 3:
            self.new_sea[row][column] = 0
        return

    def write_state(self):
        for row in self.new_sea:
            print(' '.join(list(map(str, row))))

generations = int(input())
sea_size = list(map(int, raw_input().split()))
sea = [list(map(int, raw_input().split())) for j in range(sea_size[0])]
life_game = Life(sea_size, sea, generations)
life_game.start(generations)
life_game.write_state()

