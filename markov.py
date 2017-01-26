import random
from collections import defaultdict

class MarkovChain(object):
    # symbols: a list of symbols in order
    # ngram: the n-gram of this Markov chain generator
    def __init__(self, symbols, ngram):
        self.symbols = symbols
        self.ngram = ngram
        self.chain = defaultdict(list)
        self.num_symbols = len(self.symbols)
        if self.num_symbols < self.ngram:
            raise AttributeError('Not enough symbols for this n-gram')
        self._build_chain()

    # Creates tuples of n-gram length from the symbol list
    def _generate_adjacent_symbols(self):
        for s in range(self.num_symbols - self.ngram + 1):
            yield tuple(self.symbols[s:s+self.ngram])
        # loop from last symbol to first to ensure every n-1 symbols form a 
        #     prefix with a valid suffix
        for s in range(self.num_symbols - self.ngram + 1, self.num_symbols):
            yield tuple(self.symbols[s:] + self.symbols[:(s+self.ngram)%self.num_symbols])

    # Builds a Markov chain based on adjacent symbols
    def _build_chain(self):
        for adjacent_symbols in self._generate_adjacent_symbols():
            # Use first n-1 symbols as a prefix
            prefix = adjacent_symbols[:-1]
            # Use nth symbol as the suffix
            suffix = adjacent_symbols[-1]
            self.chain[prefix].append(suffix)

    # Beginning with a random location in the Markov chain, this function
    #    aggregates a randomly generated list of symbols in the chain
    #    based on the n-gram
    def generate(self, length=15):
        seed = random.randint(0, self.num_symbols - self.ngram)
        prefix = tuple(self.symbols[seed:seed+self.ngram-1])
        suffix = self.symbols[seed+self.ngram-1]
        for s in range(length):
            yield suffix
            prefix = prefix[1:] + (suffix,)
            suffix = random.choice(self.chain[prefix])

class TextMarkovChain(MarkovChain):

    # Randomly chooses a starting word for the generator, and returns
    #    its index in the list of symbols
    def _choose_index_of_first_word(self):
        first_guess = random.randint(0, self.num_symbols - self.ngram - 1)
        idx = first_guess + 1
        while idx != first_guess:
            symbol = self.symbols[idx]
            if len(symbol) > 0 and symbol[0].isupper():
                return idx

            if idx >= self.num_symbols - self.ngram - 1:
                idx = 0
            else:
                idx += 1


    # Generate as in MarkovChain, but choose the beginning of a
    #    sentence as the beginning of the result
    def generate(self, length=15):
        seed = self._choose_index_of_first_word()
        prefix = tuple(self.symbols[seed:seed+self.ngram-1])

        # Ensure the prefix is included in the result because the
        #    starting word is the first word of the prefix
        for word in prefix:
            yield word

        suffix = self.symbols[seed+self.ngram-1]
        for s in range(length - self.ngram - 1):
            yield suffix
            prefix = prefix[1:] + (suffix,)
            suffix = random.choice(self.chain[prefix])


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: python markov.py <filename>")
        exit()

    filename = sys.argv[1]
    symbols = []
    with open(filename, 'r') as f:
        symbols = f.read().split()
    chain = TextMarkovChain(symbols, 4)
    result = ' '.join(chain.generate(100))
    print(result)

