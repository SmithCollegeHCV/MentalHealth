import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import matplotlib.pyplot as plt
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from itertools import *
import spacy
import nltk.data


# Taken direction from:
# http://brandonrose.org/clustering

def tokenize_and_stem(text):
    stemmer = SnowballStemmer("english")
    # first tokenize by sentence, then by word
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    stemmer = SnowballStemmer("english")
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def main():
    # stopwords to filter out for collocations
    stopwords_eng = set(stopwords.words("english"))

    # sentence tokenzier from nltk
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    # bigram identifier from nltk
    bigram_measures = nltk.collocations.BigramAssocMeasures()

    # tf-idf vectorizer from nltk
    tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                 use_idf=True,
                                 tokenizer=tokenize_and_stem, ngram_range=(1,3))

    file = open('CultureRelatedDiaognosticIssues.txt','r')
    a = []
    names = []
    chapNames = []

    for line in file:
        miniList = line.split("|")
        names.append(int(miniList[0].strip()))
        a.append(miniList[1].strip())
    file.close()

    file = open('cultureidc.txt', 'r')
    for line in file:
        miniList = line.split("|")
        chapNames.append(miniList[0].strip())
    file.close()

    # finding the subjects to see if voice is passive
    nlp = spacy.load('en')
    subjectsMaster = []

    for i in range(len(a)):
        element = a[i]
        sentences = tokenizer.tokenize(element)
        subjects =[]
        for sentence in sentences:
            sent = sentence
            doc = nlp(sent)
            sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
            if len(sub_toks) > 0:
                subjects.append(sub_toks)
        flattenedSubjects  = [val for sublist in subjects for val in sublist]
        subjectsMaster.append(flattenedSubjects)

    allvocab_stemmed = []
    allvocab_tokenized = []

    for element in a:
        stemmed_result = tokenize_and_stem(element)
        allvocab_stemmed.extend(stemmed_result)

        tokenized_result = tokenize_only(element)
        allvocab_tokenized.extend(tokenized_result)

    # data frame that contains stems and tokenized words
    vocab_frame = pd.DataFrame({'words': allvocab_tokenized},
    index = allvocab_stemmed)

    # tf-idf matrix for the terms in the corpus
    tfidf_matrix = tfidf_vectorizer.fit_transform(a)
    terms = tfidf_vectorizer.get_feature_names()

    # number of clusters
    num_clusters = 8
    seed = 7

    # fitting the k-means algorithm and saving it in a .pkl file
    km = KMeans(n_clusters=num_clusters, random_state=seed)
    km.fit(tfidf_matrix)
    joblib.dump(km,  'cluster.pkl')
    km = joblib.load('cluster.pkl')
    clusters = km.labels_.tolist()

    # data frame that saves the chapter, the text, and the assigned cluster
    dsm = {'Cluster': clusters, 'Chapter': names, 'Diagnosis': chapNames, 'Subjects' : subjectsMaster}
    frame = pd.DataFrame(dsm, index = [clusters], columns = ['Cluster', 'Chapter', 'Diagnosis', 'Subjects'])

    frame.to_csv('ClusteringDataFull.csv', encoding='utf-8')

    #groupby cluster for aggregation purposes
    grouped = frame['Chapter'].groupby(frame['Cluster'])

    # getting rid of all punctuation for bigram measures - will use this later
    puncTokenizer = RegexpTokenizer(r'\w+')

    print("Top terms per cluster:")
    print()

    words=[]
    clusterNo = [0,1,2,3,4,5,6,7]

    #sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]


    for i in range(num_clusters):
        print("Cluster %d words:" % i, end='')

        interList = []
        for ind in order_centroids[i, :6]:
            # print(vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
            interList.append(vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'))
        words.append(interList)
        print()

        print("Cluster %d titles:" % i, end='')
        for title in frame.ix[i]['Diagnosis'].values.tolist():
            print(str(title) + " , ", end='')
        print()

    topwordsdf = {'Cluster': clusterNo, 'Top Words': words}
    frame2 = pd.DataFrame(topwordsdf, index = [clusterNo], columns = ['Cluster', 'Top Words'])
    frame2.to_csv('topWords.csv', encoding='utf-8')



        # this for-loop finds the most common pairs of words in each diagnosis
        # for text in frame.ix[i]['text'].values.tolist():
        #     data_tokens = puncTokenizer.tokenize(text)
        #     data_tokens = [x.lower() for x in data_tokens]
        #
        #     tokens = [w for w in data_tokens if w not in stopwords_eng]
        #
        #     finder = BigramCollocationFinder.from_words(tokens)
        #     print('Printing collocations in this chapter:')
        #     print(finder.nbest(bigram_measures.likelihood_ratio, 5))
        #     print()

    # Trying to create a dataframe of top words
    # topWords = {'cluster': range(num_clusters), 'words': words}
    # wordFrame = pd.DataFrame(topWords, index=[range(num_clusters)], columns=['cluster', 'words'])
    # print(wordFrame)

    # df = pd.DataFrame(columns=['index'])
    # going over each cluster
    # for i in range(num_clusters):
    #     # get the list of top words
    #     # for triple in combinations(words[i], 3):
    #         # make pairs
    #     if len(set(words[i])) > 3:
    #         bigram_vectorizer = CountVectorizer(ngram_range=(1, 1), vocabulary = set(words[i]))
    #         # see if those pairs exist in chapters associated with that cluster
    #         co_occurrences = bigram_vectorizer.fit_transform(frame.ix[i]['text'])
    #         count_vect_df = pd.DataFrame(co_occurrences.todense(), columns=bigram_vectorizer.get_feature_names())
    #         pd.concat([df, count_vect_df], axis=1)


main()
