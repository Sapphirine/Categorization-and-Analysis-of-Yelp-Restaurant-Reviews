import json
import os
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

stopwords = {}
with open('stopwords.txt', 'rU') as f:
    for line in f:
        stopwords[line.strip()] = 1
reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION]
tags_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.REVIEWS_COLLECTION]
corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION]

        

#Read from Json File
review_id=[]
stars=[]
business_id=[]
review_text=[]
with open("samplereviewdata.json") as dataset:
    next(dataset)
    for line in dataset:
        try:
            data = json.loads(line)
        except ValueError:
            print 'Error'
    
        if data["type"] == "review":
            review_id.append(data["review_id"])
            stars.append(data["stars"])
            business_id.append(data["business_id"])
            review_text.append(data["text"])
            
#POS tagging          
pos_tag=[]
for review in review_text:
    words = []
    sentences = nltk.sent_tokenize(review.lower())

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        text = [word for word in tokens if word not in stopwords]
        tagged_text = nltk.pos_tag(text)

        for word, tag in tagged_text:
            words.append({"word": word, "pos": tag})

    pos_tag.append(words)
    tags_collection.insert({
        "reviewId": review["reviewId"],
        "business": review["business"],
        "text": review["text"],
        "words": words
    })

#WordNet Lemma    
lemma=[]
lem = WordNetLemmatizer()

for pos in pos_tag:
    nouns = []
    words = [word for word in pos if word["pos"] in ["NN", "NNS"]]

    for word in words:
        nouns.append(lem.lemmatize(word["word"]))
    lemma.append(nouns)
    
    corpus_collection.insert({
        "reviewId": review["reviewId"],
        "business": review["business"],
        "text": review["text"],
        "words": nouns
    })

"""
print(review_id)
print(stars)
print(business_id)
print(review_text)
print(pos_tag)
print(len(review_id))
print(len(stars))
print(len(business_id))
print(len(review_text))
print(len(pos_tag))
print(len(lemma))    
print(lemma)
"""

    

            

            
           
   

