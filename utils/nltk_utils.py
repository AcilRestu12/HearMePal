import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

# nltk.download('punkt')
stemmer = PorterStemmer()

def tokenize(setence):
    return nltk.word_tokenize(setence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_setence, all_words):
    # Example
    """
    setence = ['hello', 'how', 'are', 'you']
    words   = ['hi', 'hello', 'I', 'you', 'bye', 'thank', 'cool']   -> all words from pattern
    bog     = [  0 ,     1  ,  0 ,   1  ,   0  ,    0   ,    0  ]   -> result of bag of word
    """
    
    # Stemming
    tokenized_setence = [stem(w) for w in tokenized_setence]
    
    # Make zero value array
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        # When word there in tokenized_setence
        if w in tokenized_setence:
            # Change value from 0 to 1
            bag[idx] = 1.0
    
    # Return the result bag of word
    return bag
    