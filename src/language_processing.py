import nltk
from sklearn.preprocessing import LabelEncoder
from word2number import w2n
from umap import UMAP
from sklearn.feature_extraction.text import CountVectorizer
from hdbscan import HDBSCAN
import sentence_transformers
from bertopic import BERTopic

def count_capital_words(text):
    """Count the number of capital letters"""
    return sum(1 for i in text if i.isupper())

def count_punctuations(text):
    """Count the number of each punctuation character"""
    punctuations="!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    return {f'{str(i)} count': text.count(i) for i in punctuations} 

def count_sent(text):
    """Count the number of sentences"""
    return len(nltk.sent_tokenize(text))

def count_unique_words(text):
    """Count the number of unique words"""
    return len(set(text.split()))

def count_stopwords(text):
    """Count the number of stopwords"""
    stop_words = list(set(nltk.corpus.stopwords.words('english')))+["film","el","le"]
    word_tokens = nltk.tokenize.word_tokenize(text)
    stopwords_x = [w for w in word_tokens if w in stop_words]
    return len(stopwords_x)

def remove_stopwords(text):
    """Remove stopwords"""
    text = text.lower()
    stop_words = list(set(nltk.corpus.stopwords.words('english')))+["film","el","le"]
    punctuations="!#$%&''()*+,-./:;<=>?@[\]^_`{|}~’"
    punc_table = str.maketrans(dict.fromkeys(punctuations, ''))
    output= text.translate(punc_table)
    output= [i for i in nltk.tokenize.word_tokenize(output) if i not in stop_words]
    return output

def lemmatizer(text):
    """Lemmatise the text"""
    wordnet_lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    return [wordnet_lemmatizer.lemmatize(word) for word in text]

def remove_numwords(df,lemm_col,clean_col,new_col):
    """Replace number words with numbers"""
    df[new_col] = df[clean_col]
    for i, j in enumerate(df[lemm_col]):
        word_to_num_list = []
        for word in j:
            try:
                word_to_num_list += [str(w2n.word_to_num(word))]
            except ValueError:
                word_to_num_list += [word] 
        df[new_col][i] = ' '.join(word_to_num_list)
    return df
        
def bertmodel_prep(df,col):
    """Define the bertopic model parameters"""
    umap_model = UMAP(n_neighbors=15, 
                  n_components=5, 
                  min_dist=0.0, 
                  metric='cosine', 
                  random_state=100)
    vectorizer_model = CountVectorizer(min_df=5, #stop_words="english",
                                  max_features=1000)
    hdbscan_model = HDBSCAN(min_cluster_size = 50, min_samples = 100, 
                        metric = 'euclidean', prediction_data = True)
    topic_model = BERTopic(umap_model=umap_model, 
                       vectorizer_model=vectorizer_model, 
                       hdbscan_model=hdbscan_model, #nr_topics="auto",
                       language="english", calculate_probabilities=True,
                      n_gram_range=(1, 3))#, diversity=0.4
    sentence_model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = sentence_model.encode(df[col], show_progress_bar=False)
    return topic_model, embeddings

def get_topic_preds(df,col,topic_model, embeddings):
    """Fit the bertopic model and return the topics predictions"""
    topics, probabilities = topic_model.fit_transform(df[col], embeddings)
    print(topic_model.get_topic_info())
    tree = topic_model.get_topic_tree(topic_model.hierarchical_topics(df[col]))
    print(tree)
    return topic_model.topics_[:]

def label_encode_columns(dataframe, columns):
    """Label encodes the specified columns of a dataframe"""
    for column in columns:
        le = LabelEncoder()
        dataframe[column] = le.fit_transform(dataframe[column].astype('str'))
        print(le.classes_)
    return dataframe