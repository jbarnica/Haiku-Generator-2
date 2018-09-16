import Markov
import Twitter
import generateLovecraft 

def get_lovecraft_model():
    text = generateLovecraft.return_documents()    
    return Markov.get_model_from_block(text)

def gen_lovecraft_haiku():
    model = get_lovecraft_model()
    for i in range(100):
        print('{}\n'.format(Twitter.find_poem(model, (5,7,5))))    

if __name__ == "__main__":    
    gen_lovecraft_haiku()
    