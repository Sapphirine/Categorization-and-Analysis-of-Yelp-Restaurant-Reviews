import logging
import json
from gensim.models import LdaModel
from gensim import corpora
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import pymongo
from pymongo import MongoClient
from settings import Settings


class Predict():
    def __init__(self):
        dictionary_path = "models/dictionary.dict"
        lda_model_path = "models/lda_model_50_topics.lda"
        self.dictionary = corpora.Dictionary.load(dictionary_path)
        self.lda = LdaModel.load(lda_model_path)

    def load_stopwords(self):
        stopwords = {}
        with open('stopwords.txt', 'rU') as f:
            for line in f:
                stopwords[line.strip()] = 1

        return stopwords

    def extract_lemmatized_nouns(self, new_review):
        stopwords = self.load_stopwords()
        words = []

        sentences = nltk.sent_tokenize(new_review.lower())
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"word": word, "pos": tag})

        lem = WordNetLemmatizer()
        nouns = []
        for word in words:
            if word["pos"] in ["NN", "NNS"]:
                nouns.append(lem.lemmatize(word["word"]))

        return nouns

    def run(self, new_review):
        topics={0:"trip",1:"experience",2:"location",3:["drinks", "margarita"],4:
["dessert", "fancy", "garden"],5:"parking",6:"facility",7:"con",8:["pizza", "delivery", "pie"
],9:"appointment",10:["bbq", "lunch", "sandwich", "meat", "american"],11:["seafood", "shrimp", "fish", "salmon"],
12:["location", "ice cream"],13:["hotdog", "american"],14:["customer service", "experience"
],15:["pasta", "calamari"],16:"juice",17:["burritto", "student", "refund"],18:
["steak", "meat", "lover"],19:["game", "video"],20:"security",21:["cheese", "salad", "vegetables"
],22:["parking", "tax"],23:["buffet", "price", "quality"],24:"pancake",25:["cake", "cupcake", "bakery"],26:["popcorn", "environment"],
27:"kid-friendly",28:["breakfast", "brunch", "waffle"],29:["music", "friend", "club", "bar"],
30:["hotel", "casino"],31:"architecture",32:"kid-friendly",33:"view",34:["service", "price", "staff"],
35:["chocolate", "candy", "dessert"],36:"crepe",37:["time", "service"],38:"online",39:"pricey",40:"pub",
41:["burger", "order" ,"service"],42:["ambience", "beef"],43:["spicy", "chicken", "meat"],44:["price", "discount"],
45:["wine", "service", "dessert"],46:["bar", "night", "bartender"],47:["taco", "mexican"],48:["cafe", "coffee"],
49:["party", "birthday"]
}
        business_ids=["9-pGDHbyIoP_KhguG6vI1Q","ArtsD3RqfCVjIRSZunIh_g","CVakWZjk_j44AB-Jbe0DPQ","iYk5QEI3IZmr25L3QWz4KQ","7Hmr1TDJah-14zprHUMlqw","J6i_Tt4dI7IUTIG9xaC8cg","7Hmr1TDJah-14zprHUMlqw","cjJvvEbpo9b_76hV_lyFXg","rtqtZ0_kOA-GP33mn6-Kpg","T-LhjPRqlS7hLGRmSMBbfA"]       
        business_id=business_ids[0]
        nouns = self.extract_lemmatized_nouns(new_review)
        new_review_bow = self.dictionary.doc2bow(nouns)
        
        new_review_lda = self.lda[new_review_bow]
        reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
        Settings.TEST_COLLECTION]
        reviews_cursor = reviews_collection.find()
        answer=[]

        print (new_review_lda)
        
        for i,j in new_review_lda:
            answer.append(topics[i])
        print (new_review_lda)
        reviews_collection.update({'topic': ""},{'$set':{"topic":answer
                              }})
        

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    business_ids=["9-pGDHbyIoP_KhguG6vI1Q","ArtsD3RqfCVjIRSZunIh_g","CVakWZjk_j44AB-Jbe0DPQ","iYk5QEI3IZmr25L3QWz4KQ","7Hmr1TDJah-14zprHUMlqw","J6i_Tt4dI7IUTIG9xaC8cg","7Hmr1TDJah-14zprHUMlqw","cjJvvEbpo9b_76hV_lyFXg","rtqtZ0_kOA-GP33mn6-Kpg","T-LhjPRqlS7hLGRmSMBbfA"]       
    business_id="T-LhjPRqlS7hLGRmSMBbfA"
    reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.TEST_COLLECTION]
    reviews_cursor = reviews_collection.find({},{'text':1,'business':1})
    reviews_cursor2 = reviews_collection.find({},{'business':1})


    for reviews in reviews_cursor:
        if reviews["business"]==business_id:
            predict=Predict()
            predict.run(reviews["text"])
    """
    for reviews,r2 in zip(reviews_cursor,reviews_cursor2):
        if r2==business_id:
            predict = Predict()
            predict.run(reviews)
            """
 



if __name__ == '__main__':
    main()


