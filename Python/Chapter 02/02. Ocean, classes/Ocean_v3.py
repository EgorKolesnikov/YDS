import copy
import random
from time import sleep


class Cell(object):
    '''
    Cell - some kind of structure, that we will save in each cell in out
    ocean's matrix. Each cell can represent one of the following:
    empty cell, barrier, predator or victim. When new creature is born
    (or initialized) we set creature's:
    *   time to eat (How long it can live without
        food. For all, except predators - every possible number).
    *   time to reproduce (When self.reproduse == 0, then creature can
        reproduce. Type of reproduction - gemmation.)
    *   when this creature has been born. We need that information to be
        able to differ new and old predators and victims.

    . - empty space
    * - barrier
    P - predator
    V - victim
    '''

    def __init__(self, what, eat, reprod, iteration):
        self.eat = eat
        self.what = what
        self.reproduce = reprod
        self.when_born = iteration

    def __eq__(self, other):
        return self.what == other

    def __str__(self):
        return self.what


class Ocean(object):

    '''
    Ocean class. Handle the lifestream of the ocean's world
    and it's magical creatures, that inhabited there.
    '''

    def __init__(self, rows, columns, eat_time, reproduce_time):
        self.save = []
        self.predators = 0
        self.victims = 0
        self.state = 0
        self.rows = rows
        self.columns = columns
        self.ocean = [[Cell('.', 0, 0, 0) for i in xrange(self.columns)]
                      for j in xrange(self.rows)]
        self.init_eat = eat_time
        self.init_reproduce = reproduce_time

    def set_ocean(self, new_ocean):
        self.rows = len(new_ocean)
        self.columns = len(new_ocean[0])

        self.predators = 0
        self.victims = 0
        for row in xrange(self.rows):
            for column in xrange(self.rows):
                self.ocean[row][column] = Cell(
                    new_ocean[row][column],
                    self.init_eat,
                    self.init_reproduce,
                    self.state - 1
                )
                if new_ocean[row][column] == 'P':
                    self.predators += 1
                elif new_ocean[row][column] == 'V':
                    self.victims += 1

    def print_state(self):
        print '\nState:', self.state
        print 'Predators:', self.predators, ', Victims:', self.victims
        for row in self.ocean:
            print '[', (' '.join(list(map(str, row)))), ']'

    def update(self):
        '''
        Sub-method that allows to update self.state id and number of
        predators and victims.
        '''

        self.predators = 0
        self.victims = 0
        for row in xrange(self.rows):
            for column in xrange(self.rows):
                self.ocean[row][column].when_born = self.state
                if self.ocean[row][column] == 'P':
                    self.predators += 1
                elif self.ocean[row][column] == 'V':
                    self.victims += 1
        self.state += 1

    def simulate(self, ticks, output=False, sleep_time=0.0):
        '''
        Simulation work. First, simulate one tick of time. Then rewrite
        number predators and victims and change the state of the ocean
        (each state has it's own id). On each step save tuple like:
        '(number_of_predators, number_of_victims)', so we can build some
        graphs to visualize the Ocean's Life Process.
        '''

        if(output):
            self.print_state()
            sleep(sleep_time)

        self.save.append((self.predators, self.victims))
        for tick in xrange(ticks):
            self.simulate_one_tick()
            self.save.append((self.predators, self.victims))
            self.update()

            if output:
                self.print_state()
                sleep(sleep_time)
            if self.victims == 0:
                print 'Simulation terminated. No victims left.\n'
                return
            if self.predators == 0:
                print 'Simulation terminated. No predators left.\n'
                return
        self.state = 0

    def simulate_one_tick(self):
        '''
        Simulate one tick of time. We want to handle each creature
        only ones. For example, if one victim moves one line to the bottom
        then we will handle that victims twice (throgh one line of cells in
        the ocean). That is why we have 'when_born' parameter of every
        creature.
        '''

        for row in xrange(self.rows):
            for column in xrange(self.columns):
                if (self.ocean[row][column] == 'P' and
                        self.ocean[row][column].when_born != self.state):
                    self.handle_predator(row, column)
                elif (self.ocean[row][column] == 'V' and
                        self.ocean[row][column].when_born != self.state):
                    self.handle_victim(row, column)

    def handle_predator(self, row, column):
        '''
        Handle actions of predators. If there is time to reproduce, then
        check availiable empty cells, where we can put new predator.
        (Reproduction of predators and victims - gemmation reproduction)
        Then, if there are a lot of victims near predator, or he is very
        hungry, and know, that he is gonna die soon, then preadator
        eats one of the victims. And in conclusion, if he didn't eat, than
        he can move (we can't do two actions at time).
        '''

        empty = self.get_nearest(row, column, '.')
        victims = self.get_nearest(row, column, 'V')

        self.ocean[row][column].eat -= 1
        self.ocean[row][column].reproduce -= 1
        if self.ocean[row][column].eat == 0:
            self.ocean[row][column] = Cell('.', 0, 0, 0)
        else:
            if self.ocean[row][column].reproduce == 0:
                if len(empty) != 0:
                    where = random.randint(0, len(empty) - 1)
                    self.ocean[empty[where][0]][empty[where][1]] = Cell(
                        'P',
                        self.init_eat,
                        self.init_reproduce,
                        self.state
                    )
                    self.ocean[row][column].reproduce = self.init_reproduce
                else:
                    self.ocean[row][column].reproduce = 1

            if self.ocean[row][column].eat <= 2 or len(victims) >= 2:
                if len(victims) != 0:
                    eat = random.randint(0, len(victims) - 1)
                    self.ocean[victims[eat - 1][0]][victims[eat - 1][1]] = Cell(
                        'P',
                        self.init_eat,
                        self.init_reproduce,
                        self.state
                    )
                    self.ocean[row][column] = Cell('.', 0, 0, 0)
                    return

            if len(empty) != 0:
                move = random.randint(0, len(empty) - 1)
                self.ocean[empty[move - 1][0]][empty[move - 1][1]] = Cell(
                    'P',
                    self.ocean[row][column].eat,
                    self.ocean[row][column].reproduce,
                    self.state
                )
                self.ocean[row][column] = Cell('.', 0, 0, 0)

    def handle_victim(self, row, column):
        '''
        Handle victims actions. This case is simplier, because victim can
        die only because of predators hunger. Like in the predators case:
        if there is time to reproduce, then we check availiable nearest
        cells, where we can put our little poor baby-victim. Then we check
        nearest empty cells, where we can move (we can reproduce and move
        at one time).
        '''

        self.ocean[row][column].reproduce -= 1
        empty = self.get_nearest(row, column, '.')

        if self.ocean[row][column].reproduce == 0:
            if len(empty) != 0:
                where = random.randint(0, len(empty) - 1)
                self.ocean[empty[where][0]][empty[where][1]] = Cell(
                    'V',
                    0,
                    self.init_reproduce,
                    self.state
                )
                self.ocean[row][column].reproduce = self.init_reproduce
            else:
                self.ocean[row][column].reproduce = 1

        if len(empty) != 0:
            move = random.randint(0, len(empty) - 1)
            self.ocean[empty[move - 1][0]][empty[move - 1][1]] = Cell(
                'V',
                self.ocean[row][column].eat,
                self.ocean[row][column].reproduce,
                self.state
            )
            self.ocean[row][column] = Cell('.', 0, 0, 0)

    def get_nearest(self, row, column, cell='.'):
        '''
        Check the nearest cells. If victim reproduced another
        victim and want to move then we can tell, that there
        is another (new one) victim near it. But if victim
        reproduced new victim and predator want to know:
        'is there victims near me', then we can't tell that
        there is new victim (can tell him only about old victims).
        That is done because actions of predators and victims
        are independent on each state.
        '''

        result = []
        if column > 0 and self.ocean[row][column - 1] == cell:
            if cell == '.':
                result.append((row, column - 1))
            elif self.ocean[row][column - 1].when_born != self.state:
                result.append((row, column - 1))
        if row > 0 and self.ocean[row - 1][column] == cell:
            if cell == '.':
                result.append((row - 1, column))
            elif self.ocean[row - 1][column].when_born != self.state:
                result.append((row - 1, column))
        if column < self.columns - 1 and self.ocean[row][column + 1] == cell:
            if cell == '.':
                result.append((row, column + 1))
            elif self.ocean[row][column + 1].when_born != self.state:
                result.append((row, column + 1))
        if row < self.rows - 1 and self.ocean[row + 1][column] == cell:
            if cell == '.':
                result.append((row + 1, column))
            elif self.ocean[row + 1][column].when_born != self.state:
                result.append((row + 1, column))
        return result


def main():
    # Choosing source of the ocean's data is done
    # only because of better debuging.
    # INPUT = 0 - from file, INPUT = 1 - from static matrix
    INPUT = 1

    input_size = 0
    input_ocean = 0
    if INPUT == 1:
        input_size = [7, 7]
        input_ocean = [
            ['*', 'V', '.', '*', '.', '.', 'V'],
            ['.', '.', 'V', '.', 'P', 'V', '.'],
            ['P', '.', '*', 'P', '.', '.', '.'],
            ['V', '.', 'P', '*', '.', 'V', '*'],
            ['.', 'P', '.', 'V', '.', '.', '.'],
            ['*', '.', 'V', '.', '*', 'P', '.'],
            ['P', '.', '*', 'V', 'P', '.', '.']
        ]
    else:
        with open('ocean.txt', 'r') as ocean:
            input_size = list(map(int, ocean.readline().split()))
            input_ocean = [line.split() for line in ocean]

    # Initialization and simulation of the Ocean's world
    ocean = Ocean(input_size[0], input_size[1], 5, 3)
    ocean.set_ocean(input_ocean)
    ocean.simulate(50, output=False)

    # Save results to build statistic
    with open('result.txt', 'w') as file:
        for element in ocean.save:
            file.write(str(element[0]) + ' ' + str(element[1]) + '\n')


if __name__ == '__main__':
    main()
