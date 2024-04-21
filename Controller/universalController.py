from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from tinydb import TinyDB, Query
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

app = Flask(__name__)
CORS(app)

#  db init
db = TinyDB('db.json')
history = []

# mongo client
client = MongoClient('mongodb://localhost:27017/')
database = client['zen-circle-test-db']
collection = database['users']
username = 'vihanpereraux'

# GET
@app.route("/", methods=['GET'])
def getFunction():  
  return "Sending the text !!"

# GET - 2
@app.route("/test-create-user", methods=['GET'])
def test():
  for item in db:
    history.append(item) 
  
  data = {
    "_id": ObjectId("123456789012345678901234"),
    'username': username,
    'password' : '1',
    'conversation': str(history)
  }
  data["_id"] = json.loads(json.dumps({"_id": str(data["_id"])}))
  collection.insert_one(data)
  # collection.update_one({"username": username}, data)
  
  cursor = collection.find()
  documents = []
  for doc in cursor:
    documents.append(doc)
  
  return jsonify(documents), 201

# GET - 3
@app.route("/test-update-user", methods=['GET'])
def test_2():
  for item in db:
    history.append(item)
    
  update_data = {
    "$set": {
      'username': username,
      'password' : '12',
      'conversation': str(history)
    }
  }
  collection.update_one({"username": username}, update_data)
  return jsonify({'message': 'user updated !'}), 201

# POST
@app.route("/get-response", methods=['POST'])
def getResponse():
  content = request.args.get('content')
  
  system_content = "Always respond in a very human-like behaviour and here's the conversation history - " + str(history) + "It has the user input and the AI generated answer in a json format wrapped in an array. When generaring something always refer to the conversation history"
  
  # Point to the local server
  client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

  completion = client.chat.completions.create(
    model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
    messages=[
      {"role": "system", "content": system_content},
      {"role": "user", "content": content}
    ],
    temperature=0.7,
  )

  db.insert(
    {
      'user': content,
      'system': completion.choices[0].message.content
    }
  )
  
  item = {
    'item_id' : 1,
    'message' : completion.choices[0].message.content   
  }
  
  for item in db:
    history.append(item)
  print(str(history))
  
  return jsonify(item), 201
  
if __name__ == "__main__":
  app.run(debug=True) 
  

