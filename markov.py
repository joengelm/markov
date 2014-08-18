import sys
import random
from optparse import OptionParser
 
class Markov(object):
    # open_file: an opened file to read data from
    # ngram: the n-gram of this Markov generator
    def __init__(self, open_file, ngram):
        self.chain = {}
        self.open_file = open_file
        self.words = self._get_words()
        self.word_count = len(self.words)
        self.ngram = ngram
        self._build_chain()
    
    # Gets words from source file
    def _get_words(self):
        self.open_file.seek(0)
        file_data = self.open_file.read()
        words = file_data.split()
        return words

    # Creates tuples of length 'length' from the word array
    def _get_adjacent_words(self):
        if self.word_count < self.ngram:
            return
        for w in range(self.word_count - self.ngram + 1):
            adjacent_words = []
            for i in range(w, w + self.ngram):
                adjacent_words.append(self.words[i])
            yield tuple(adjacent_words)

    # Builds a Markov chain based on adjacent words
    def _build_chain(self):
        for adjacent_words in self._get_adjacent_words():
            key = adjacent_words[:-1]
            if key in self.chain:
                self.chain[key].append(adjacent_words[-1])
            else:
                self.chain[key] = [adjacent_words[-1]]
    
    # Beginning with a random location in the Markov chain, this function
    #    aggregates a randomly generated string of data in the chain based
    #    on the n-gram
    def generate_text(self, word_count=200):
        seed = random.randint(0, self.word_count - self.ngram)
        # everything below this line must be adapted to variable length prefixes
        prefix = tuple(self.words[seed:seed+self.ngram-1])
        suffix = self.words[seed+self.ngram-1]
        generated_words = []
        generated_words.extend(prefix)
        for i in xrange(word_count-self.ngram+1):
            generated_words.append(suffix)
            prefix = prefix[1:] + (suffix,)
            suffix = random.choice(self.chain[prefix])
        return ' '.join(generated_words)

def main():
    usage = "Usage: %prog [-w] [-n] <source_filename>"
    version = "%prog 0.1"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-w", "--words", dest="word_count", type=int,
                      help="number of words in output [default: %default]", default=200)
    parser.add_option("-n", "--ngram", dest="ngram", type=int,
                      help="n-gram for this Markov generator [default: %default]", default=3)
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("There should be exactly one argument (i.e. the filename).")
    if opts.ngram < 2:
        parser.error("The n-gram must be greater than 1. An n-gram of 1 is a completely random sample of data. [Hint: Use random.choice()]")
    if opts.word_count < opts.ngram:
        parser.error("The output word count must not be less than the n-gram. Refer to the default values with '-h' flag.")
    open_file = None
    try:
        open_file = open(args[0])
    except IOError:
        parser.error("That filename is invalid.")

    m = Markov(open_file, opts.ngram)
    print "\n" + m.generate_text(opts.word_count) + "\n"
    sys.exit(0)

if __name__ == "__main__":
    main()
                