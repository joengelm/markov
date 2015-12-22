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
        self._build_chain()

    # Creates tuples of n-gram length from the symbol list
    def _get_adjacent_symbols(self):
        if self.num_symbols < self.ngram:
            return
        for s in range(self.num_symbols - self.ngram + 1):
            yield tuple(self.symbols[s:s+self.ngram])
        # loop from last symbol to first to ensure every n-1 symbols form a 
        #     prefix with a valid suffix
        for s in range(self.num_symbols - self.ngram + 1, self.num_symbols):
        	yield tuple(self.symbols[s:] + self.symbols[:(s+self.ngram)%self.num_symbols])

    # Builds a Markov chain based on adjacent symbols
    def _build_chain(self):
        for adjacent_symbols in self._get_adjacent_symbols():
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
        generated_symbols = []
        generated_symbols.extend(list(prefix))
        for s in range(length-self.ngram+1):
            generated_symbols.append(suffix)
            prefix = prefix[1:] + (suffix,)
            suffix = random.choice(self.chain[prefix])
        return generated_symbols
