from openai import OpenAI
from flask import jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

# mongo client init
client = MongoClient('mongodb://localhost:27017/')
database = client['zen-circle-test-db']
collection = database['users']

def manage_user_data(action, username, history):
    if action == 'update_document':
        update_data = {
            "$set": {
            'username': username,
            'password' : '9999',
            'conversation': str(history)
            }
        }
        collection.update_one({"username": username}, update_data)
        return "User updated"
    
    elif action == 'create_document':
        data = {
            "_id": ObjectId("123456789012345678901234"),
            'username': username,
            'password' : '1',
            'conversation': str(history)
        }
        data["_id"] = json.loads(json.dumps({"_id": str(data["_id"])}))
        collection.insert_one(data)
        return "User added"

    else:
        return "action not found"
    
    
def manage_conversation(content, history):
    system_content = "Always respond in a very human-like behaviour and here's the conversation history - " + str(history) + "It has the user input and the AI generated answer in a json format wrapped in an array. When generaring something always refer to the conversation history"
  
    #point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": content}
        ],
        temperature=0.7,
    )
    response = completion.choices[0].message.content
    return response    