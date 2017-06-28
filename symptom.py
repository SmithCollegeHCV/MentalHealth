import numpy as np
import pandas as pd
import nltk
import re
import math
import csv
from itertools import chain
from collections import Counter
from nltk.util import ngrams

NGRAM1 = 1
NGRAM2 = 2
NGRAM3 = 3

re_sent_ends_naive = re.compile(r'[.\n]')
re_stripper_alpha = re.compile('[^a-zA-Z]+')
re_stripper_naive = re.compile('[^a-zA-Z\.\n]')
splitter_naive = lambda x: re_sent_ends_naive.split(re_stripper_naive.sub(' ', x))
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def get_tuples_nosentences1(txt):
    """Get tuples that ignores all punctuation (including sentences)."""
    if not txt: return None
    ng1 = ngrams(re_stripper_alpha.sub(' ', txt).split(), NGRAM1)
    return list(ng1)

def get_tuples_nosentences2(txt):
    """Get tuples that ignores all punctuation (including sentences)."""
    if not txt: return None
    ng2 = ngrams(re_stripper_alpha.sub(' ', txt).split(), NGRAM2)
    return list(ng2)

def get_tuples_nosentences3(txt):
    """Get tuples that ignores all punctuation (including sentences)."""
    if not txt: return None
    ng3 = ngrams(re_stripper_alpha.sub(' ', txt).split(), NGRAM3)
    return list(ng3)


def cosine_similarity_ngrams(a, b, lst):
    
    vec1 = Counter(a)
    vec2 = Counter(b)
    vec = Counter(lst)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    return float(numerator/denominator)


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def main():
    code_lst = []
    symptom_lst=[]
    whole_txt = ""
    symptom = open("dsm1_20.txt", 'r')
    all_txt = symptom.read()
    symptom = all_txt.strip()
    symptom = all_txt.split("!")

    num = 1

    print("Reading diagnoses...")
    for s in symptom:
        #print("Reading diagnosis", num, " of ", len(symptom))
        s = s.strip()
        s = s.split("\n")
        symptom_lst.append(s)
        code_lst.append(s[0])
        whole_txt = whole_txt+str(s[2:])
        num+= 1

    print("DONE.")
    #for i in symptom_lst:
    #    print("Reading symptom", num, " of ", len(symptom))
    #    code_lst.append(i[0])
    #    whole_txt = whole_txt+str(i[2:])
    
    one_gram_lst = []
    two_gram_lst = []
    three_gram_lst = []
    
    num = 0
    print("Processing diagnoses...")
    for i in symptom_lst:
        #print("Processing diagnosis", num, " of ", len(symptom_lst))
        one_gram_lst.append(get_tuples_nosentences1(str(i[2:])))
        two_gram_lst.append(get_tuples_nosentences2(str(i[2:])))
        three_gram_lst.append(get_tuples_nosentences3(str(i[2:])))
        num +=1
    one_word_lst = get_tuples_nosentences1(whole_txt)
    two_word_lst = get_tuples_nosentences2(whole_txt)
    three_word_lst = get_tuples_nosentences3(whole_txt)
    print("DONE.")
    
    
    '''df1 = pd.DataFrame(index=code_lst,columns = code_lst)
    for i in range(len(symptom_lst)):
        symptom1 = one_gram_lst[i]
        for j in range(len(symptom_lst)):
            symptom2 = one_gram_lst[j]
            similarity = round(cosine_similarity_ngrams(symptom1, symptom2,one_word_lst),3)
            df1.set_value(code_lst[i],code_lst[j],similarity)           
    
    df2 = pd.DataFrame(index=code_lst,columns = code_lst)
    for i in range(len(symptom_lst)):
        symptom1 = two_gram_lst[i]
        for j in range(len(symptom_lst)):
            symptom2 = two_gram_lst[j]
            similarity = round(cosine_similarity_ngrams(symptom1, symptom2,two_word_lst),3)
            df2.set_value(code_lst[i],code_lst[j],similarity)'''
    
    df3 = pd.DataFrame(index=code_lst,columns = code_lst)
    print("Comparing pairs...")
    for i in range(len(symptom_lst)):
        symptom1 = three_gram_lst[i]
        for j in range(len(symptom_lst)):
            #print("Processing pair ", i*len(symptom_lst)+j, " out of ", len(symptom_lst)**2)
            #print("Processing pair (", i, ",", j ,")")
            symptom2 = three_gram_lst[j]
            similarity = round(cosine_similarity_ngrams(symptom1, symptom2,three_word_lst),3)
            df3.set_value(code_lst[i],code_lst[j],similarity)
    print("REALLY DONE")
    df3.to_csv('cos_similarity.csv')
    

main()

