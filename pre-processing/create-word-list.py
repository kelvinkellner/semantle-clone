

# filter and create our word of the day list
words = set()
BAD_SYMBOLS = ('!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '{', '}', '|', '\\', ':', ';', '"', '<', '>', '?', '/', '.', ',', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

with open('oxford-3000.txt', 'r') as fv:
    for line in fv:
        word = line.strip()
        # ignore all 1-letter or 2-letter words
        # ignore all words with special characters
        if len(word) > 2 and not any(symbol in word for symbol in BAD_SYMBOLS):
            words.add(word)

if "and" in words:
    words.remove("and")

with open('word-of-the-day.txt', 'w') as fw:
    for word in words:
        fw.write(word + '\n')

