from flask import Flask,request, render_template, g, session,redirect, Response,send_file
import os,sys
from flask import Flask, request, redirect, url_for
from settings import Settings
import os
import time
import json
from pymongo import MongoClient
import ast


app = Flask(__name__)
app.debug = True

tags_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.TEST_COLLECTION]
# configuration
'''MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# create the little application object
app.config.from_object(__name__)

# connect to the database
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])


'''
@app.route("/",methods=['GET','POST'])
def homepage():
	return render_template("display.html")

@app.route("/results", methods=['GET', 'POST'])
def matches():
	search_tags = request.form.getlist('checkbox') #Tags Checked by user
	print (search_tags)
        tag_cursor=tags_collection.find()
        result={}
        senti=[]
        matching_tags={}

        #for r in tag_cursor:
                #print r
        '''for record in tag_cursor:
                print record['topic']
                if all (l in record["topic"] for l in search_tags):
                         if  not record["name"] in result:
                                 result[record["name"]]=record["topic"]
        '''
        """
        for tag in search_tags:
                for record in tag_cursor:
                        print record
                        if tag in record['topic']:
                                if tag in result:
                                        result[record["name"]].append(tag)
                                else:
                                        result[record["name"]]=tag
 #result.add("rest":topics["name"],"match_tag":tag)
         """
        #count=0
        for tag in search_tags:
            #count=0    
            tag=tag.lower()    
            tag_cursor.rewind()
            for record in tag_cursor:
                #if 'topic' in record:
                    
                #print (record)    
                if  u'topic' in record:
                    #print "Here"
                    #print(record[u'topic'])
                    if tag in record[u'topic']:
                        result[record[u'name']]=[tag,record[u'sentiment']]
                        #senti[count]=record[u'sentiment']
                        #count=count+1
                #result[record["name"]].append(tag)
        print result
                        
	return render_template("restaurants.html",matches=result)
	#return "hello"
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')

	 
