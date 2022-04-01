from gensim.models import KeyedVectors
from datetime import date

DATE_GENESIS = date(2022, 3, 29)

class Semantle:

    FILENAME_WORD_OF_THE_DAY = "word-of-the-day.txt"
    FILENAME_PAST_WORDS = "past-words.txt"

    COUNT_GETTING_CLOSE_LIST = 999

    FUNC_LOAD_MODEL = lambda _ : KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    
    def __init__(self, puzzle_number=1):
        self.puzzle_number = puzzle_number
        self.word_of_the_day = self.get_word_of_the_day()
        self.word_bank = self.load_words()

        self.model = self.load_model()
        self.close_list = self.load_close_list()

    def get_word_of_the_day(self):
        with open(Semantle.FILENAME_WORD_OF_THE_DAY, 'r') as f:
            while self.puzzle_number > 1:
                f.readline()
                self.puzzle_number -= 1
            return f.readline().strip()
    
    def load_model(self):
        model = self.FUNC_LOAD_MODEL()
        return model

    def load_words(self):
        with open('words_alpha.txt') as word_file:
            valid_words = set(word_file.read().split())
        return valid_words

    def load_close_list(self, close_count=COUNT_GETTING_CLOSE_LIST):
        most_similar = self.model.most_similar(self.word_of_the_day, topn=close_count*10)
        close_list = list(filter(lambda word : word in self.word_bank, [word for word, _ in most_similar]))[:close_count]
        self.thousandth_simililarity = self.model.similarity(self.word_of_the_day, close_list[-1])
        self.question_mark_list = set(filter(lambda word : word not in self.word_bank, [word for word, similarity in most_similar if similarity > self.thousandth_simililarity]))
        return close_list

    def position_in_close_list(self, word):
        position = -1
        for i in range(len(self.close_list)):
            if self.close_list[i] == word:
                position = i
        return position

    def guess_word(self, word, player):
        try:
            if word in player.guesses:
                return print("You already guessed that word.")
            similarity = self.model.similarity(self.word_of_the_day, word.replace(' ', '_').strip())
            position = self.map_position(self.position_in_close_list(word.replace(' ', '_').strip()), similarity)
            similarity = self.map_similarity(similarity)
            player.guess_number += 1
            print(f'{x[0]:5d} {x[1]:26s} {x[2]:8.2f} {x[3]:8s}' for x in ['#', 'Guess', 'Similarity', 'Getting close?'])
            if player.guess_number > 1:
                print('-' * 50)
            for x in player.guesses:
                print(f'{x[0]:5d} {x[1]:26s} {x[2]:8.2f} {x[3]:8s}')
            print('-' * 50)
            print("{:5d} {:26s} {:8.2f} {:8s}".format(player.guess_number, word, similarity, position))
            player.guesses.append((player.guess_number, word, similarity, position))
            player.sort_guess_list()
        except KeyError:
            print(f'I don\'t know the word {word}.')

    def map_position(self, position, similarity):
        return str(self.COUNT_GETTING_CLOSE_LIST - position) + '/1000' if position != -1 else 'FOUND!' if similarity == 1.0 else '????' if similarity > self.thousandth_simililarity else '(cold)'

    def map_similarity(self, similarity):
        return similarity * 100

    def play(self, player):
        while True:
            word = input("\nGuess a word: ")
            print()
            self.guess_word(word, player)

class Player:

    def __init__(self, game, guess_number=0, guesses=[]):
        self.guess_number = guess_number
        self.guesses = guesses
        self.game = game

    def sort_guess_list(self):
        self.guesses.sort(key=lambda x: x[2])

game = Semantle((date.today() - DATE_GENESIS).days)
player = Player(game)
# print(game.question_mark_list)
# for i in range(len(game.close_list)):
#     print(f'{i+1:<5d} {game.close_list[i]:<28s}')
game.play(player)