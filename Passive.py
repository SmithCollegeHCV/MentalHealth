import spacy
import nltk.data

file = open('CultureRelatedDiaognosticIssues.txt','r')
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

a = []
names = []
for line in file:
    miniList = line.split("|")
    names.append(int(miniList[0].strip()))
    a.append(miniList[1].strip())
file.close()

nlp = spacy.load('en')
for i in range(len(a)):
    element = a[i]
    sentences = tokenizer.tokenize(element)
    subjects =[]
    for sentence in sentences:
        sent = sentence
        doc=nlp(sent)
        sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
        if len(sub_toks) > 0:
            subjects.append(sub_toks)
    print("Chapter ", names[i], " = ", subjects)
