import json
import os
import nltk

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
        text = [word for word in tokens]# if word not in stopwords]
        tagged_text = nltk.pos_tag(text)

        for word, tag in tagged_text:
            words.append({"word": word, "pos": tag})

    pos_tag.append(words)

print(review_id)
print(stars)
print(business_id)
print(review_text)
print(pos_tag)

            

            
           
   

