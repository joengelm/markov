import random
 
class Markov(object):
     
    def __init__(self, open_file):
        self.chain = {}
        self.open_file = open_file
        self.words = self.get_words()
        self.word_count = len(self.words)
        self.build_chain()
         
    def get_words(self):
        self.open_file.seek(0)
        file_data = self.open_file.read()
        words = file_data.split()
        return words
            
    # Creates triples from the word array
    def get_triples(self):
        if self.word_count < 3:
           	return
        for i in range(self.word_count - 2):
            yield (self.words[i], self.words[i + 1], self.words[i + 2])
                 
    def build_chain(self):
        for word1, word2, word3 in self.get_triples():
            key = (word1, word2)
            if key in self.chain:
                self.chain[key].append(word3)
            else:
                self.chain[key] = [word3]
                          
    def generate_markov_text(self, size=200):
        seed = random.randint(0, self.word_count - 3)
        word1, word2 = self.words[seed], self.words[seed + 1]
        generated_words = []
        generated_words.append(word1)
        for i in xrange(size):
            word1, word2 = word2, random.choice(self.chain[(word1, word2)])
            generated_words.append(word1)
        return ' '.join(generated_words)

filename = raw_input("\nSeed File: ")
continuing = 'y'

while continuing == 'y' or continuing == 'yes':
	gen_length = int(raw_input("\nHow many words should be generated? "))
	m = Markov(open(filename))
	print "\n" + m.generate_markov_text(gen_length) + "\n"
	continuing = raw_input("Continue with this Markov chain? (y/n) ")

                