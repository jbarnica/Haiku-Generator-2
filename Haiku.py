import importlib
import json
import nltk.corpus as nc
import random
import string

syllable_dict = {}
FILE_NAME = "dictionary.txt"

def output_message(message):
    print(message)

def get_library_words(names):
    results = []
    for name in names:
        words_2d = [name.words(x) for x in name.fileids()]
        results += [word for word_list in words_2d for word in word_list]
    return tuple(set(results))

def generate_valid_words():

    results = get_library_words((
        nc.brown, nc.gutenberg, nc.nps_chat, nc.reuters, nc.webtext))
    return results

def strip_punctuation(phrase):
    for i in list(string.punctuation):
        phrase = phrase.replace(i, '')
    return phrase.lower()

def nsyl(word, cmudict):      
    return [len(list(y for y in x if y[-1].isdigit())) for x in cmudict[word.lower()]]

def create_dict_file(phrase=None):
    if phrase is None:
        validDict = generate_valid_words()   
    else:
        validDict = list(set(strip_punctuation(phrase).split(' ')))
    cmudict = nc.cmudict.dict()         
    tempDict = {}
    for word in validDict:
        if cmudict.get(word) is not None:
            tempDict[word] = nsyl(word, cmudict)[0]
    if phrase is None:
        with open(FILE_NAME, "w") as f:
            r = json.dumps(tempDict)
            f.write(r)
    else:
        return tempDict    

def load_dictionary(phrase=None):
    global syllable_dict

    if phrase is not None:
        syllable_dict = create_dict_file(phrase)
    else:
        try:
            with open(FILE_NAME, 'r') as f:
                file = f.read().replace('\n', '')
        except IOError:
            create_dict_file()
            with open(FILE_NAME, 'r') as f:
                file = f.read().replace('\n', '')  
        syllable_dict = json.loads(file)       

def get_words(number, chosenWords):
    return dict((key, value) for key, value in syllable_dict.items() 
        if value <= number and key not in (chosenWords or ''))

def choose_words(number, chosenWords = []): 
    s = []   
    goodWords = get_words(number, chosenWords)
    if len(goodWords) > 0:
        choice = random.choice(list(goodWords.keys()))
        result = (choice, goodWords[choice])
        s += [result[0]]
        chosenWords.append(result[0])
        if result[1] < number:
            s += choose_words(number - result[1], chosenWords)
        random.shuffle(s)
        return s
    else:
        return ''

def get_dict():
    return nc.cmudict.dict()   

def check_syllables(text, cmudict):    
    if text is not None: 
        return sum([nsyl(x, cmudict)[0] for x in text.split(' ') if cmudict.get(x.lower()) is not None])
    return 0

def choose_line(number):
    elements = choose_words(number)
    random.shuffle(elements)
    return '{}\n'.format(' '.join(elements))

def write_haiku():
    haiku = '"{}{}{}"'.format(choose_line(5), choose_line(7), choose_line(5))
    return haiku

def write_undefined(syllabelCounts):
    s = ''
    for i in syllabelCounts:
        s += choose_line(i)
    return s

def get_haiku():
    return write_haiku()    

def haiku_from_tweet(tweet):
    load_dictionary(tweet)
    return get_haiku()    

if __name__ == "__main__":
    load_dictionary()    
    output_message(get_haiku())

