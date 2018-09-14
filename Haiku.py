import importlib
import json
import nltk.corpus as nc
import random

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
        nc.brown,
        nc.gutenberg, 
        nc.nps_chat, 
        nc.reuters,
        nc.webtext))
    return results

def create_dict_file():

    validDict = generate_valid_words()   
    cmudict = nc.cmudict.dict()

    def nsyl(word):
        return [len(list(y for y in x if y[-1].isdigit())) for x in cmudict[word.lower()]]     

    tempDict = {}
    for word in validDict:
        if cmudict.get(word) is not None:
            tempDict[word] = nsyl(word)[0]
    with open(FILE_NAME, "w") as f:
        r = json.dumps(tempDict)
        f.write(r)

def load_dictionary():
    global syllable_dict

    try:
        with open(FILE_NAME, 'r') as f:
            file = f.read().replace('\n', '')
    except IOError:
        create_dict_file()
        with open(FILE_NAME, 'r') as f:
            file = f.read().replace('\n', '')  
    syllable_dict = json.loads(file)       

def get_words(number):
    #work on this
    return dict((key, value) for key, value in syllable_dict.items() if value <= number )

def choose_words(number): 
    s = []   
    goodWords = get_words(number)
    choice = random.choice(list(goodWords.keys()))
    result = (choice, goodWords[choice])
    s += [result[0]]
    if result[1] < number:
        s += choose_words(number - result[1])
    random.shuffle(s)
    return s

def choose_line(number):
    elements = choose_words(number)
    random.shuffle(elements)
    return '{}\n'.format(' '.join(elements))

def write_haiku():
    haiku = "{}{}{}".format(choose_line(5), choose_line(7), choose_line(5))
    return haiku

def write_undefined(syllabelCounts):
    s = ''
    for i in syllabelCounts:
        s += choose_line(i)
    return s

def get_haiku():
    return write_haiku()    

load_dictionary()    

if __name__ == "__main__":
    output_message(get_haiku())