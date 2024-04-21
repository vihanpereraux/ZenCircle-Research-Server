from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from tinydb import TinyDB, Query
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

from Model.communication_model import manage_user_data
from Model.communication_model import manage_conversation


app = Flask(__name__)
CORS(app)

#  db init
db = TinyDB('db.json')
history = []
username = 'vihanpereraux'

# GET
@app.route("/", methods=['GET'])
def getFunction():  
  return "Sending the text !!"

# create new user end-point
@app.route("/create-user", methods=['GET'])
def create_user():
  action = "create_document"
  for item in db:
    history.append(item) 
    
  response = manage_user_data(action, username, history)
  return jsonify({ 'response': response }), 201

# update user end-point
@app.route("/update-user", methods=['GET'])
def update_user():
  action = "update_document"
  for item in db:
    history.append(item)
  
  response = manage_user_data(action, username, history)
  return jsonify({ 'response': response }), 201


# communication with the lmserver
@app.route("/get-response", methods=['POST'])
def get_response():
  for item in db:
    history.append(item)
  content = request.args.get('content')
  response = manage_conversation(content, history)
  # updates the temp db
  db.insert( {'user': content, 'system': response })
  
  for item in db:
    history.append(item)
  
  return jsonify({ 'message': response }), 201
  
if __name__ == "__main__":
  app.run(debug=True) 
  

