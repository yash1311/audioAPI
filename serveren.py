"""
This script runs the application using a flask development server.
It contains the definition of routes and views for the application.
"""

# Import the required libraries

from flask import Flask, Response, request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine import *
import json
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)

################# Create Database Connection ##################

try:
    app.config['MONGODB_SETTINGS'] = {
                                        'db': 'audio_metadata',
                                        'host': 'localhost',
                                        'port': 27017
                                      }
    db = MongoEngine()
    db.init_app(app)
    print("Database Connection Done.")
except Exception as e:
    print("Error: Database Connection Failed: ", e)
     
####################################
#list of supported audio file types. 
audiotypeList=['Song','Podcast','Audiobook']      

## Define seperate class for each type of audio file to create seperate document for each in database
## Defining document to store song metadata
class Song(db.Document):
    # defineing varables 
    Id = db.IntField(min_value = 0, unique=True, required=True)
    songName = db.StringField(unique=True,max_length = 100, required = True)
    songDuration = db.IntField(min_value = 0, required=True)
    songUpload = db.DateTimeField(default=datetime.now, required=True)


## Defining document to store podcast metadata
class Podcast(db.Document):
    Id = db.IntField(min_value = 0,unique = True, required = True)
    podcastName = db.StringField(unique = True, max_length = 100, required = True)
    podcastDuration = db.IntField(min_value = 0, required = True)
    podcastUpload = db.DateTimeField(default = datetime.now, required = True)
    podcastHost = db.StringField(required = True, max_length = 100)
    podcastParticipants = db.ListField(db.StringField(unique = True, max_length = 100),max_length = 10, required = False)



## Definining document to store Audiobook metadata
class Audiobook(db.Document):
    Id = db.IntField(min_value = 0,unique = True, required = True)
    audiobookName = db.StringField(unique = True, max_length = 100, required = True)
    audiobookAuthor = db.StringField(required = True, max_length = 100)
    audiobookUpload = db.DateTimeField(default = datetime.now, required = True)
    audiobookNarrator = db.StringField(required = True, max_length = 100)
    audiobookDuration = db.IntField(min_value = 0, required = True)



######################################
## Define route to create database and added the data to the database.
@app.route('/audiometa', methods=['POST'])
def create_audiometa():
    try:
        _json = request.json
        if _json['audioFileType'] in audiotypeList:
            audioFileType =_json['audioFileType']
            try:
                record=eval(audioFileType)(**_json['audioFileMetadata'])
                record.save() 
                return Response(response = json.dumps({"message": "Record Added Succesfully"}),status=200)
            except Exception as e:
                return Response(response = json.dumps({"Error" : "Error \n %s" % (e)}),status=400)
        else:
             return Response(response = json.dumps({"message": "Audio file type is not Valid. Choose any from (Song, Podcast & Audiobook) only"}),status=400)
    except Exception as e:
        return Response(response = json.dumps({"Error" : "Error \n %s" % (e)}),status=400)
####################################################################
# Get data from database
@app.route('/<audioFileType>', methods=['GET'])
@app.route('/<audioFileType>/<audioFileID>', methods=['GET'])
def query_audiometa(audioFileType,audioFileID = None):
    ## Use the class objects attribute to make queries. A keyword argument looks for an equal value on the field. ##
    if audioFileID is not None:
        if audioFileType in audiotypeList:
            try: 
                records = eval(audioFileType).objects(Id = audioFileID).get_or_404()
                return Response(response = records.to_json(),status=200)
            except Exception as e:
                return Response(response = json.dumps({"Error" : "Error \n %s" % (e)}),status=400)

        else:
            return Response(response = json.dumps({"Error": "Audio file type is not Valid. Choose any from (Song, Podcast & Audiobook) only"}),status=400)
    else:
        if audioFileType in audiotypeList:
            try: 
                recordList = eval(audioFileType).objects()
                records = recordList.to_json()
                return Response(response = records,status=200)
            except Exception as e:
                return Response(response = json.dumps({"Error" : "Error \n %s" % (e)}),status=400)
        else:
            return Response(response = json.dumps({"Error": "Audio file type is not Valid. Choose any from (Song, Podcast & Audiobook) only"}),status=400)

####################################################################
# Delet data from database
@app.route('/<audioFileType>/<audioFileID>', methods=['DELETE'])
def delete_audiometa(audioFileType,audioFileID = None):
    ## Use the class objects attribute to make queries. A keyword argument looks for an equal value on the field. ##

    if audioFileID is not None:
        if audioFileType in audiotypeList:
            try:
                records = eval(audioFileType).objects(Id = audioFileID).get_or_404()
                records = eval(audioFileType).objects(Id = audioFileID).delete()
                return Response(response = json.dumps({"Done" : f"{audioFileID} Record delete successfully."}),status=200)
            except Exception as e:
                return Response(response = json.dumps({"Error" : "Error \n %s" % (e)}),status=400)
        else:
            return Response(response = json.dumps({"Error": "Audio file type is not Valid. Choose any from (Song, Podcast & Audiobook) only"}),status=400)
    else:
            return Response(response = json.dumps({"Error": "Enter /<audioFileID> to delet record with particular ID"}),status=400)

####################################################################
# Update data from database
@app.route('/<audioFileType>/<audioFileID>', methods=['PUT'])
def dpdate_audiometa(audioFileType,audioFileID = None):
    try:
        _json = request.json
        print(_json)
        if audioFileType in audiotypeList:
            try:
                records = eval(audioFileType).objects(Id = audioFileID).get()
                records.update(**_json)
                return Response(response = json.dumps({"Done": "Record Updated Succesfully"}),status=200)
            except Exception as e:
                return Response(response = json.dumps({"Error" : "Error \n %s" % (e)}),status=400)
        else:
             return Response(response = json.dumps({"message": "Audio file type is not Valid. Choose any from (Song, Podcast & Audiobook) only"}),status=400)
             #print('Error: Audio file type is not Valid. Choose any from (song, podcast & audiobook) only')
    except Exception as e:
        return Response(response = json.dumps({"Error" : "Error \n %s" % (e)}),status=400)
###############################################

if __name__ == '__main__':
    app.run(debug=True)

##Yash##
