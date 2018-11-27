# Creating Folders
import os
# Time library to create timestamps for filenames
import time
# Convert a collection of text documents to a matrix of token counts
from sklearn.feature_extraction.text import CountVectorizer

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory ' + directory)

def save_data(df, query, path="./", time_fmt="%Y_%m_%d-%H%M%S"):
    timestr = time.strftime(time_fmt)
    create_folder(path)
    filename = f"{path}{query}-{timestr}"
    df.to_csv(f"{filename}.csv" , sep=',', encoding='utf-8')
    return filename

# https://medium.com/@cristhianboujon/how-to-list-the-most-common-words-from-text-corpus-using-scikit-learn-dad4d0cab41d
def get_top_n_words(corpus, stop_words=None):
    """
    List the top n words in a vocabulary according to occurrence in a text corpus.
    
    get_top_n_words(["I love Python", "Python is a language programming", "Hello world", "I love the world"]) -> 
    [('python', 2),
     ('world', 2),
     ('love', 2),
     ('hello', 1),
     ('is', 1),
     ('programming', 1),
     ('the', 1),
     ('language', 1)]
    """
    vectorizer = CountVectorizer(stop_words=stop_words)
    X = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    sum_words = X.sum(axis=0).tolist()[0]
    words_freq = zip(feature_names, sum_words)
    words_freq =sorted(words_freq, key = lambda x: -x[1])
    return words_freq
