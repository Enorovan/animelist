from http.client import responses
from operator import contains

from cv2 import log
import models
import tools
import tensorflow as tf
import gc
import numpy
from pluginFactory import PluginFactory
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
subjects = None
types = None
stopwords = None
dictionnary = None

def analyse(sentence):
    subjects, types, stopwords, dictionnary = tools.defaultValues()
    modelSubjects= models.getModelSubjects(dictionnary, subjects)
    modelSubjects.load("data/modelSubjects.tflearn")
    resultS= modelSubjects.predict([tools.bagOfWords(sentence, dictionnary, stopwords)])
    tf.keras.backend.clear_session()
    del modelSubjects
    gc.collect()

    modelTypes= models.getModelTypes(dictionnary, types)
    modelTypes.load("data/modelTypes.tflearn")
    resultT= modelTypes.predict([tools.bagOfWords(sentence, dictionnary, stopwords)])
    tf.keras.backend.clear_session()
    del modelTypes
    gc.collect()

    modelValues= models.getModelValues(dictionnary)
    modelValues.load("data/modelValues.tflearn")
    resultV= modelValues.predict([tools.bagOfWords(sentence, dictionnary, stopwords)])
    tf.keras.backend.clear_session()
    del modelValues
    gc.collect()
    return resultS[0], resultT[0], resultV[0][0]

def editSentence(sentence,sub, newSub: str):
    subR = sub.split(".")
    fileName = subR[0]
    subjectFile = subR[1]

    newSubR = newSub.split(".")
    newFileName = newSubR[0]
    newSubjectFile = newSubR[1]

    file = open("./training_data/"+fileName+".json",'r')
    arr = json.loads(file.read())
    newFile= None
    newArr = None
    if fileName != newFileName:
        newFile = open("./training_data/"+newFileName+".json",'r')
        newArr = json.loads(newFile.read())
    else:
        newArr = arr


    el2 = [x for x in newArr if x["subject"] == newSubjectFile]
    for a in el2:
        if sentence not in a["sentences"]:
            a["sentences"].append(sentence)


    el = [x for x in arr if x["subject"] == subjectFile and sentence in x["sentences"]]
    # print(el)
    for a in el:
        a["sentences"].remove(sentence)
    
    # print(el)
    file.close()
    if newFile != None:
        newFile.close()
        file = open("./training_data/"+newFileName+".json",'w')
        file.write(json.dumps(newArr, indent=6))
        file.close()


    file = open("./training_data/"+fileName+".json",'w')
    file.write(json.dumps(arr, indent=6))
    file.close()
    # models.train()

def searchAnswer(sentence, subject, typeS):
    plugin = PluginFactory.getPlugin(subject, typeS)
    return plugin.response(sentence)
    

class Subject(Resource):
    def get(self):
        return {'data': tools.defaultValues()[0]}, 200

class Sentence(Resource):

    def put(self):
        body = request.get_json()
        sentence = body["sentence"]
        subject = body["subject"]
        newSubject = body["newSubject"]
        editSentence(sentence=sentence, sub=subject, newSub=newSubject)
        models.train()
        return {'data': 'Vous avez modifié le sujet.'}, 200

    def get(self):
        sent = request.args.get("text")
        rSubject, rType, rValue= analyse(sent)
        result = searchAnswer(sent, subjects[numpy.argmax(rSubject)], types[numpy.argmax(rType)])
        return {'data': result,'subject': subjects[numpy.argmax(rSubject)]}, 200
    
    def post(self):
        print("Change request")
        body = request.get_json()
        sentence = body["sentence"]
        response = body["response"]
        newResponse = body["newResponse"]
        rSubject, rType, rValue= analyse(sentence)
        sub = subjects[numpy.argmax(rSubject)]
        subR = sub.split(".")
        fileName = subR[0]
        subjectFile = subR[1]
        file = open("./training_data/"+fileName+".json",'r')
        arr = json.loads(file.read())
        el = [x for x in arr if x["subject"] == subjectFile and response in x["responses"]]
        file.close()
        for a in el:
            a["responses"].remove(response)
            a["responses"].append(newResponse)
        file = open("./training_data/"+fileName+".json",'w')
        file.write(json.dumps(arr, indent=6))
        file.close()
        models.train()
        return {'message' : "Response Updated"},200
        

api.add_resource(Sentence,"/sentence")
api.add_resource(Subject ,"/subject")

if __name__ == '__main__':
    subjects, types, stopwords, dictionnary = tools.defaultValues()
    app.run()
    