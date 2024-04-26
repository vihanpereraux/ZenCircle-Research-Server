import sys
sys.setrecursionlimit(10000)

from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from tinydb import TinyDB, Query
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

from Model.communication_model import manage_user_data
from Model.communication_model import manage_conversation
from Model.communication_model import manage_ai_assistant
from Model.communication_model import get_personal_history
from Model.communication_model import clean_db


app = Flask(__name__)
CORS(app)

#  db init
db = TinyDB('db.json')
history = []
username = 'vihanpereraux'

# GET
@app.route("/", methods=['GET'])
def getFunction(): 
  response = get_chat_history()
  # return jsonify({ 'response': response }), 201 
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
  content = request.args.get('content')
  response = manage_conversation(content, username, history)
  # updates the temp db
  db.insert( {'user': content, 'system': response })
  
  for item in db:
    history.append(item)
  action = "update_document"
  convo_history_response = manage_user_data(action, username, history)
  
  if convo_history_response == 'User updated':
    return jsonify({ 'message': response, 
                      'db_response': 'db is updated' }), 201
  else:
    return jsonify({ 
                    'message': response, 
                    'db_response': 'db is not updated due to an error, check the local connectivity' }), 201
  

@app.route("/get-ai-assistant-response", methods=['POST'])
def get_response_2():
  content = request.args.get('content')
  response = manage_ai_assistant(content)
  return jsonify({ 'message': response }), 201


@app.route("/get-chat-history", methods=['GET'])
def get_chat_history():
  response = get_personal_history()
  return jsonify({ 'response': response }), 201

# clean the conversation history
@app.route("/clean-conversation-history", methods=['POST'])
def clean_conversation_history():
  if len(db.all()) == 0:
    return jsonify({ 'message': 'history alreday cleared' }), 201
  else:
    db.truncate()
    history = []
    response = clean_db(username, history)
    if response:  
      return jsonify({ 'message': 'history cleared' }), 201
    else:
      return jsonify({ 'message': 'history not cleared, something happened' }), 500


if __name__ == "__main__":
  app.run(debug=True) 
  

