import sys
import copy
import codecs
import random
import string
import StringIO
import argparse
import unittest
import collections


not_alphas = ':;,.?!'


class ChainStat:
    '''
    Little class-helper to store chains statistic
    '''

    def __init__(self, count=0):
        self.count = count
        self.words = collections.defaultdict(lambda: float())

    def __str__(self):
        return str(self.count) + str(self.words)

    def __repr__(self):
        return str(self.count) + str(self.words)

#
#   Printing results. Only print statistic result
#   needed special type of output. But for the whole
#   pack - let there be others too.
#


def print_tokenize_result(result):
    print '\n'.join(result)


def print_count_statistic_result(result):
    all_blocks = result[0]
    for depth in xrange(1, len(result), 1):
        all_blocks.update(result[depth])
    for chain in sorted(all_blocks):
        if len(all_blocks[chain].words) > 0:
            print ' '.join(list(chain))
            words = sorted(all_blocks[chain].words.keys())
            for word in words:
                print '  {w}: {f:.2f}'.format(
                    w=word,
                    f=all_blocks[chain].words[word]
                )


def print_generate_result(result):
    print result


#
#   Help methods for making statistic.
#


def parse_args(string):
    commands = ['tokenize', 'probabilities', 'generate', 'test']
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, choices=commands)
    parser.add_argument("-d", "--depth", default=1, type=int)
    parser.add_argument("-s", "--size", default=1, type=int)
    opts = parser.parse_args(string.split())
    return opts


def add_token_after_chain(depth_result, chain, token):
    '''
    Add token after particular chain to result dict
    (making that operation as subfunction to make
    code more readable)
    '''
    depth_result[chain].words[token] += 1
    depth_result[chain].count += 1


def make_probabilities(result):
    '''
    We want to reassign number of appearances of chains and words
    to equal frequency of appearance. This method will do that.
    '''
    count_chains = float(sum(value.count for chain, value in result.iteritems()))
    for chain in result:
        result[chain].count /= count_chains
        count_words = float(sum(result[chain].words.values()))
        for word in result[chain].words:
            result[chain].words[word] /= count_words


#
#   Task methods (tokenize, count_statistic, generate)
#


def tokenize(string, need_not_alpha=True, need_space=True):
    '''
    Tokenize one string on tokens, where ' '
    and ',?! ...' are also tokens
    '''
    string = string.rstrip('\n\t')
    result = []
    left = right = 0

    while right < len(string):
        left = right
        while right < len(string) and string[right].isalpha():
            right += 1
        if right > left:
            result.append(string[left:right])
            continue

        left = right
        while right < len(string) and string[right].isdigit():
            right += 1
        if right > left:
            result.append(string[left:right])
            continue

        left = right
        while (right < len(string) and
               not string[right].isalpha() and
               not string[right].isdigit()):
            if (need_not_alpha and (string[right] in not_alphas) or
                    need_space and string[right] == ' '):
                        result.append(string[right])
            right += 1
    return result


def count_statistic(args_depth, inf=sys.stdin, need_not_alpha=False, need_space=False):
    '''
    Get statistic about frequency of appearance of
    k-and-less-word samples, where k - from args (--depth parameter)
    Result is storing in dictionary 'result', where key - depth of the
    chain, value - another dictionary with key - particular chain
    and value - ChainStat() object.
    (later 'number of appearances' will transform to 'frequency')
    '''
    max_depth = args_depth
    result = [collections.defaultdict(lambda: ChainStat()) for i in xrange(max_depth + 1)]

    for line in inf:
        tokens = tokenize(line.decode("utf8"), need_not_alpha, need_space)
        for index in xrange(len(tokens)):
            token = tokens[index]
            add_token_after_chain(result[0], (''), token)
            for depth in xrange(1, max_depth + 1):
                if index - depth < 0:
                    break
                else:
                    chain = tuple(tokens[(index - depth):index])
                    add_token_after_chain(result[depth], chain, token)
        # Editional last 'depth' words as another chain. But after
        # that chain there is nothing following it.
        for depth in xrange(1, max_depth + 1):
            index = len(tokens)
            chain = tuple(tokens[(index - depth):index])
            if chain in result[depth]:
                result[depth][chain].count += 1
            else:
                result[depth][chain] = ChainStat(1)

    # As long as list is changable, so it will be passed to the
    # function by value. Map is not changable, so it will be passed
    # by reference. That's why we call 'make_probabilities' for each
    # length of chain and not doing it for all lengths in function
    for depth in xrange(max_depth + 1):
        make_probabilities(result[depth])
    return result


#
#  Help methods for generating texts
#


def choose(probabilities):
    '''
    Choose the next word after particular chain to be generated.
    We only have probabilities of words, so return value - index
    of the next word in list of words after chain.
    If there very very very much words after particular chain,
    probability of each one can be equal to 0.
    In that case return random index. (For example in english books
    after 'the' will be too many words, if our text is actually big.)
    '''
    if (p != 0 for p in probabilities):
        rand = random.random()
        accumulate = 0.0
        last = accumulate
        for index in xrange(len(probabilities)):
            accumulate += probabilities[index]
            if rand >= last and rand <= accumulate:
                return index
            last = accumulate
    return random.randrange(0, len(probabilities) - 1)


def add_new_begining(text, depth_chains, probabilities):
    '''
    Generating begining of each text by randobly picking (using
    choose) first chain. But there can be a situation described in
    count_statistic(...):
    By making some chains without anything following it (the last
    words on the end of sentence) we can face the ploblem with
    picking next word. In that case - generating new begining chain
    (with, maybe, another length) and continue working with that
    chain and that length.
    '''
    last_chain = '.'
    while not last_chain or last_chain[0] in not_alphas:
        last_chain = depth_chains[choose(probabilities)]

    new_text = [text]
    for token in last_chain:
        if token in not_alphas:
            new_text[-1] += token
        else:
            new_text.append(
                (token.title() if new_text[-1][-1] in '.?!' else token)
            )

    return ' '.join(new_text), last_chain


def generate(args_depth, args_size, inf=sys.stdin, generate_texts=10):
    '''
    Generate text, using sample text. First generate
    statistic using count_statistic(args). Then generate
    k words using that statistic (--size parameter).
    '''
    statistic = count_statistic(args_depth, inf, True, False)
    base_chain_length = args_depth
    texts = []

    while generate_texts:
        max_length = args_size
        text = '.'

        # Generate first --depth words.
        chains = statistic[base_chain_length].keys()
        probabilitis_of_chains =\
            [v.count for k, v in statistic[base_chain_length].iteritems()]
        new_text, last_chain = add_new_begining(text, chains, probabilitis_of_chains)
        text = new_text.strip()[1:]

        # Generate other max_length - (--depth) words
        last_chain = list(last_chain)
        while max_length > 0:
            last_symbol = text[-1]
            possible_next_words = statistic[base_chain_length][tuple(last_chain)].words.keys()
            possible_words_probabilitis =\
                [statistic[base_chain_length][tuple(last_chain)].words[word]
                 for word in possible_next_words]

            # If we face the empty list of possible next words
            # (situation described in add_new_begining)
            if len(possible_next_words) == 0:
                chains = statistic[base_chain_length].keys()
                probabilitis_of_chains =\
                    [v.count for k, v in statistic[base_chain_length].iteritems()]
                text, last_chain = add_new_begining(text, chains, probabilitis_of_chains)
                last_chain = list(last_chain)
                max_length -= len(last_chain)
            else:
                generated_word = possible_next_words[choose(possible_words_probabilitis)]
                last_chain = last_chain[1:] + [generated_word]
                if (generated_word[0].isupper() and
                   (len(generated_word) == 1 or
                        (len(generated_word) > 1 and not generated_word.isupper()))):
                    generated_word = generated_word[0].lower() + generated_word[1:]
                if generated_word not in '.?!,:;':
                    if last_symbol in '.?!':
                        generated_word = ' ' + generated_word.title()
                    else:
                        generated_word = ' ' + generated_word
                    text += generated_word
                else:
                    if generated_word in '?!' and last_symbol in '?!':
                        text += generated_word

                max_length -= 1

            # We can't just stop generating sentence on ',:;'
            # But if we managed to do that - continue generation.
            if max_length <= 0 and text[-1] in ',:;':
                max_length = 1
        texts.append(text.strip() + '.')
        generate_texts -= 1
    return texts


#
#  Testing with module unittest
#

def generate_random_string():
    result = ''
    length = random.randrange(5, 100)
    alphabet = ''.join([string.ascii_letters, string.digits, ' :;,.?!'])
    for symbol in xrange(length):
        position = random.randrange(0, len(alphabet))
        result += alphabet[position]
    return result


class Tests(unittest.TestCase):

    '''
    Unit testing of methods implemented earlier
    '''

    def test_tokenize(self):
        '''
        Testing tokenization function. Wornig only with ascii string
        (Simplier to generate, because can get alphabets. See more in
        generate_random_string()).
        For loop over all tokens testing that all tokens has maximum
        length (like in an example: 'abc', not 'a', 'b', 'c'). All
        other characters (not letters and not digits) are taken as
        single tokens. If that situation performed and 'string ==
        rebuild' then tokenizations working correctly.
        '''
        string = generate_random_string()
        tokens = tokenize(string)

        rebuild = tokens[0]
        last_token = tokens[0]
        for token in tokens[1:]:
            if token.isalpha() and last_token.isalpha():
                return False
            elif token.isdigit() and last_token.isdigit():
                return False
            rebuild += token
            last_token = token
        return string == rebuild

    def test_count_statistic(self):
        for depth in xrange(1, 100):
            self.count_statistic_with_depth(depth)

    def count_statistic_with_depth(self, depth=1):
        '''
        Testing statistic. That includes testing correctness of
        make_probabilities(...), add_token_after_chain(...).
        First check if all chains and words have been included
        to the statistic. Then check if sum of all probabilities
        for each chain equals to 1. (Note, that there could be the
        situation, when sum of probabilities equals 0. That situation
        described in generate(...))
        '''
        result = True
        generated = generate_random_string()
        statistic = count_statistic(
            depth,
            StringIO.StringIO(generated),
            True, True
        )

        # Check if all chains and words have been watched
        tokens = tokenize(generated, True, True)
        for index in xrange(len(tokens)):
            token = tokens[index]
            result = result and (token in statistic[0][('')].words)
            for test_depth in xrange(1, depth + 1):
                if index - test_depth < 0:
                    break
                else:
                    chain = tuple(tokens[(index - test_depth):index])
                    result = result and (chain in statistic[test_depth])
            if not result:
                return False

        # Check if sum of probabilitis equals 1
        eps = 0.0001
        for test_depth in xrange(0, depth + 1):
            for chain in statistic[test_depth]:
                test_sum = sum(statistic[test_depth][chain].words.values())
                if not (test_sum == 0 and len(statistic[test_depth][chain].words) == 0):
                    result = (1. - test_sum) < eps
            test_sum = sum(value.count for chain, value in statistic[test_depth].iteritems())
            result = result and (1. - test_sum) < eps
        return result


def main():
    reload(sys)
    sys.setdefaultencoding("utf8")
    # debug_type:
    # 0 - working with console
    # 1 - working with generated in task E files
    # (args always setting with console)
    debug_type = (1 if len(sys.argv) > 1 else 0)
    inf = sys.stdin

    if debug_type:
        inf = open('all_books.txt', 'r')

    args = parse_args(sys.stdin.readline())
    if args.command == 'tokenize':
        result = tokenize(inf.readline().decode("utf8"))
        print_tokenize_result(result)
    elif args.command == 'probabilities':
        result = count_statistic(args.depth, inf)
        print_count_statistic_result(result)
    elif args.command == 'generate':
        if debug_type:
            results = generate(args.depth, args.size, inf, generate_texts=10)
            for index in xrange(len(results)):
                with open('res' + str(index) + '.txt', 'w') as file:
                    file.write(results[index].encode('utf8'))
        else:
            result = generate(args.depth, args.size, inf)
            print_generate_result(result[0])
    else:
        unittest.main()

    if debug_type and True:
        inf.close()


if __name__ == '__main__':
    main()
