from abc import abstractmethod
import random
import copy
import sys


class Player(object):

    Human = 'human'
    Computer = 'computer'

    def __init__(self, type):
        self.type = type

    @abstractmethod
    def make_move(self, range, game=0, marks=[], debug=False):
        '''
        Abstract method of making move. Some arguments used only
        by computer, some - by both computer and human.
        '''
        pass


class Human(Player):

    def __init__(self):
        super(Human, self).__init__(Player.Human)

    def make_move(self, range, game=0, marks=[], debug=False):
        '''
        Make player's move. Player have range of possible columns
        one of which he can pick.
        '''
        move = -1
        while move not in xrange(range):
            try:
                move = input('Enter column (player ' + marks[0] + '):')
            except Exception:
                continue
        return move


class Computer(Player):

    def __init__(self, need_to_think=True):
        self.need_to_think = need_to_think
        self.mark = '-'
        super(Computer, self).__init__(Player.Computer)

    def analyze(self, max_column, analyze_game, marks):
        '''
        Analyze game state. First check - if we can win on that move.
        If we can - make that move. Second check - if our opponent can win
        on next move. If he can - stop him doing. Third check - think on
        two steps ahead: if we can win in next two steps than do first of them.
        (ofcourse we don't think that our opponent will know our strategy)
        '''
        counter = 0
        game = copy.deepcopy(analyze_game)

        # if I can win - make move
        for column in xrange(game.columns):
            if game.table[0][column] == FourInRow.Empty:
                game.change_table(column, marks[0])
                if not game.check_state():
                    if game.verdict == FourInRow.Draw:
                        return column
                    elif game.winner == marks[0]:
                        return column
                game.table = copy.deepcopy(analyze_game.table)

        # if other player can win - stop him
        for column in xrange(game.columns):
            if game.table[0][column] == FourInRow.Empty:
                game.change_table(column, marks[1])
                if not game.check_state():
                    if game.verdict == FourInRow.Draw:
                        return column
                    elif game.winner == marks[1]:
                        return column
                game.table = copy.deepcopy(analyze_game.table)

        # check two moves ahead
        for column in xrange(game.columns):
            if game.table[0][column] == FourInRow.Empty:
                game.change_table(column, marks[0])
                for next_step_column in xrange(game.columns):
                    if game.table[0][next_step_column] == FourInRow.Empty:
                        save = copy.deepcopy(game.table)
                        game.change_table(next_step_column, marks[0])
                        if not game.check_state():
                            if game.verdict == FourInRow.Draw:
                                return column
                            elif game.winner == marks[1]:
                                counter += 1
                        game.table = save
                if counter > 1:
                    return column
                game.table = copy.deepcopy(analyze_game.table)

        # if nothing worked - pick first empty column
        for column in xrange(analyze_game.columns):
            if analyze_game.table[0][column] == FourInRow.Empty:
                return column

    def make_move(self, max_column, game, marks, debug):
        '''
        If computer need to think, then analyze game state.
        If don't need to think (when testing our bot for winning
        percentage) than make random move.
        '''
        move = random.randrange(0, max_column)
        if self.need_to_think:
            move = self.analyze(max_column, game, marks)
        return move


class FourInRow(object):

    Empty = ' '
    Draw = 'Draw'
    Win = 'Win'
    Playing = 'Playing'
    First_Player_Mark = 'X'
    Second_Player_Mark = 'O'

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.steps = 0
        self.verdict = 'Not started'
        self.winner = 0
        self.clear_table()

    def print_table(self, debug):
        if debug:
            for row in xrange(self.rows):
                print '[' + '] ['.join(self.table[row]) + ']'
            print ' ' + '   '.join(str(x) for x in xrange(self.columns))

    def clear_table(self):
        self.table = [[' ' for i in xrange(self.columns)] for j in xrange(self.rows)]

    def check_full(self):
        '''
        Check if game table is full. If it is full - then draw
        (return True). False - otherwise.
        '''
        for row in xrange(self.rows):
            for column in xrange(self.columns):
                if self.table[row][column] == FourInRow.Empty:
                    return False
        return True

    def check_winner(self):
        '''
        Check game table for winner. Check all possible horizontal,
        vertical and diagonal sets of four game cells. If found one
        where all cells are equal - return that cell as a winner
        (cell represents player's mark).
        Return 0 - otherwise (still playing, no winner yet)
        '''
        # check horizontal lines
        for row in xrange(self.rows):
            for column in xrange(self.columns - 3):
                if (self.table[row][column] != ' ' and
                        self.table[row][column + 1] == self.table[row][column] and
                        self.table[row][column + 2] == self.table[row][column] and
                        self.table[row][column + 3] == self.table[row][column]):
                    return self.table[row][column]

        # check vertical lines
        for column in xrange(self.columns):
            for row in xrange(self.rows - 3):
                if (self.table[row][column] != ' ' and
                        self.table[row + 1][column] == self.table[row][column] and
                        self.table[row + 2][column] == self.table[row][column] and
                        self.table[row + 3][column] == self.table[row][column]):
                    return self.table[row][column]

        # check diagonal \
        for row in xrange(self.rows - 3):
            for column in xrange(self.columns - 3):
                if (self.table[row][column] != ' ' and
                        self.table[row + 1][column + 1] == self.table[row][column] and
                        self.table[row + 2][column + 2] == self.table[row][column] and
                        self.table[row + 3][column + 3] == self.table[row][column]):
                    return self.table[row][column]

        # check diagonal /
        for row in xrange(self.rows - 3):
            for column in xrange(3, self.columns):
                if (self.table[row][column] != ' ' and
                        self.table[row + 1][column - 1] == self.table[row][column] and
                        self.table[row + 2][column - 2] == self.table[row][column] and
                        self.table[row + 3][column - 3] == self.table[row][column]):
                    return self.table[row][column]
        return 0

    def check_state(self):
        '''
        Check game state. First check if table is full. If it is than game
        verdict: Draw. Then check for winner. If found one - return False
        (False means 'you can no longer play') and game verdict: Win (also
        initialize winner mark).
        '''
        if self.check_full():
            self.verdict = FourInRow.Draw
            return False
        else:
            winner = self.check_winner()
            if winner == 0:
                self.verdict = FourInRow.Playing
                return True
            else:
                self.winner = winner
                self.verdict = FourInRow.Win
                return False

    def change_table(self, column, player_mark):
        '''
        Change table cell. When player make move we need to place
        his mark on the bottom most empty cell of that particular
        column. If column is full - raise IndexError exception.
        '''
        for row in xrange(self.rows - 1, -1, -1):
            if self.table[row][column] == FourInRow.Empty:
                self.table[row][column] = player_mark
                return
        raise IndexError

    def play(self, player_1, player_2, debug=True):
        '''
        Core of the game. Ckear the table and initialize player's marks.
        Game is very simple: players making moves while table is not
        full and while one of them lose. Between player's moves check
        game state and players can no longer play (check_state returned
        False) than stop and leave gaming process.
        '''
        self.clear_table()
        player_1.mark = FourInRow.First_Player_Mark
        player_2.mark = FourInRow.Second_Player_Mark

        marks = [player_2.mark, player_1.mark]
        now_move = player_2
        next_move = player_1
        while self.check_state():
            # change player:
            now_move, next_move = next_move, now_move
            marks[0], marks[1] = marks[1], marks[0]

            # make move
            self.print_table(debug)
            move = now_move.make_move(self.columns, self, marks, debug)
            while True:
                try:
                    self.change_table(move, now_move.mark)
                    break
                except IndexError:
                    move = now_move.make_move(self.columns, self, marks, debug)
            self.steps += 1
        self.print_table(debug)


def test_bot(tests):
    '''
    Test bot strategy. We make computer with brains play with computer
    witout brains 'tests' times. After that amount of games create the
    statistic's about our little experiment.
    '''
    count_stupid = 0
    count_clever = 0
    count_draws = 0

    game = FourInRow(6, 7)
    for test in xrange(tests):
        game.play(Computer(need_to_think=True), Computer(need_to_think=False), debug=False)

        verdict = game.verdict
        winner = game.winner
        if verdict == FourInRow.Draw:
            count_draws += 1
        else:
            if winner == FourInRow.First_Player_Mark:
                count_clever += 1
            else:
                count_stupid += 1

    result = 'Total games: {0}. Draws: {1}. Clever won {2} times ({3}%)'
    return result.format(tests, count_draws, count_clever, count_clever * 100.0 / tests)


def interactive(rules):
    print 'Hello. I am happy to introduce Four-In-A-Row game.'

    choise = -1
    text = 'Choose game mode:\n \
            1 - play with bot\n \
            2 - play with your friend\n \
            3 - test bot\n \
            4 - read rules\n'
    while True:
        try:
            choise = int(input(text))
            if choise not in xrange(1, 4):
                if choise == 4:
                    print rules
                continue
            break
        except Exception:
            continue

    if choise == 3:
        print test_bot(100)
    else:
        player_1 = Human()
        player_2 = Computer() if choise == 1 else Human()
        game = FourInRow(6, 7)
        game.play(player_1, player_2, debug=True)
        print game.verdict, game.winner, '\nNice game, huh?'


def main():
    rules = '''
        Game process is very simple. You have game table with empty cells.
        Players (two of them) in turns making moves. You can pick number of column
        where to drop your mark. Your mark will accommodate on the bottom most
        cell of that column. If column is full - you will have to pick another
        column. Your goal is to be the first player to create four in a row
        cells of your mark (row can be vertical, horizontal and diagonal).
    '''
    interactive(rules)


if __name__ == '__main__':
    main()
