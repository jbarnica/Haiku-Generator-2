import json
import random
syls = {}
fileName = "dictionary.txt"

def Log(message):
    print(message)

def GenerateValidWords():

    results = []

     #create a list of reasonable words
    from nltk.corpus import gutenberg
    gresults = [gutenberg.words(x) for x in gutenberg.fileids()]
    gresults = [j for sub in gresults for j in sub]

    results += gresults

    from nltk.corpus import nps_chat
    wresults = [nps_chat.words(x) for x in nps_chat.fileids()]
    wresults = [j for sub in wresults for j in sub]    

    results += wresults

    from nltk.corpus import webtext
    wresults = [webtext.words(x) for x in webtext.fileids()]
    wresults = [j for sub in wresults for j in sub]

    results += wresults
    results = tuple(set(results))

    return results

def createDictFile():

    from nltk.corpus import cmudict    

    validDict = GenerateValidWords()
   
    d = cmudict.dict()

    def nsyl(word):
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]     

    tempDict = {}
    for word in validDict:
        if d.get(word) is not None:
            tempDict[word] = nsyl(word)[0]
    with open(fileName, "w") as f:
        r = json.dumps(tempDict)
        f.write(r)

def loadDictionary():
    global syls
    try:
        with open(fileName, 'r') as f:
            file = f.read().replace('\n', '')

    except IOError:
        createDictFile()
        with open(fileName, 'r') as f:
            file = f.read().replace('\n', '')  
    syls = json.loads(file)       

def GetWords(number):
    #work on this
    return dict((key, value) for key, value in syls.iteritems() if value <= number )

def ChooseWords(number): 
    s = []   
    goodWords = GetWords(number)
    choice = random.choice(goodWords.keys())
    result = (choice, goodWords[choice])
    s += [result[0]]
    if result[1] < number:
        s += ChooseWords(number - result[1])
    random.shuffle(s)
    return s

def ChooseLine(number):
    elements = ChooseWords(number)
    random.shuffle(elements)
    return '{}\n'.format(' '.join(elements))

def WriteHaiku():
    haiku = "{}{}{}".format(ChooseLine(5), ChooseLine(7), ChooseLine(5))
    return haiku

def WriteUndefined(syllabelCounts):
    s = ''
    for i in syllabelCounts:
        s += ChooseLine(i)
    return s

def main():
    loadDictionary()     
    Log(WriteHaiku())
    
main()

