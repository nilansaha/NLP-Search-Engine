import pickle
import pandas as pd
pd.set_option('display.expand_frame_repr', False)
from nltk import word_tokenize
import string
import pickle
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
df = pd.read_csv('titles.csv')

def preprocess(text):
    text = str(text)
    text = text.translate(None, string.punctuation)
    text = text.lower()
    text = word_tokenize(text)
    new_text = []
    for word in text:
        word = lemmatizer.lemmatize(word,'n')
        word = lemmatizer.lemmatize(word,'v')
        new_text.append(word)
    return new_text

def cosine_similarity(title, query):
    title = title.strip()
    query = query.strip()
    tfidf = vectorizer.fit_transform([title.lower(),query.lower()])
    return ((tfidf * tfidf.T).A)[0,1]

with open('index.pickle','r') as f:
    index = pickle.load(f)

query = raw_input("Enter you search query? ")
query = preprocess(query)
bigarray = []
for token in query:
    try:
        bigarray.append(index[token])
    except:
        print "Not in index " + token
documents = list(set().union(*bigarray))
frame = pd.DataFrame()
frame['processed'] = df.loc[documents].processed.reset_index(drop=True)
frame['cosine_similarity'] = frame.processed.apply(lambda x: cosine_similarity(x, " ".join(query)))
print frame.sort_values(by=['cosine_similarity'], ascending = [False])