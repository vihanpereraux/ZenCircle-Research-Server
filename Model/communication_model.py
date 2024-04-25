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
    
    
# <s>[/INST] I feel so overwhelmed today</s>[INST] Model [/INST] Behave as a mental health professional and generate answers on a human-like approach. Use kind and lovely words all the time when ending a sentence<s>[INST]
def manage_conversation(content, username, history):
    system_content = "Always respond in a very human-like behaviour and here's the conversation history - " + str(history) + "When generating an answer always refer to the conversation history. Strictly Don't generate answers that has more that 30 words."
    system_content_2 = "Always repond as a kind, loving lady while referencing to the conversation history -" + str(history) + "Strictly Don't generate answers that has more that 50 words"
    system_content_3 = "Always repond as a kind, loving lady"
    
    #point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    # prompt reshaping - v.0
    updated_content = "<s>[/INST]" + str(content) + "</s>[INST] Model [/INST] Behave as a mental health professional and generate answers on a human-like approach. Use kind and lovely words all the time when ending a sentence<s>[INST]"
    updated_content_2 = "<s>[INST] "+ str(content) + " [/INST] Sad mood right now"
    updated_content_3 = "[INST] "+ str(content) + " [/INST]" 
    

    completion = client.chat.completions.create(
    model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    messages=[
        {"role": "system", "content": system_content_2},
        {"role": "user", "content": updated_content_2}
    ],
    temperature=0.7,
    )
    
    response = completion.choices[0].message.content
    # updates the permenant conversation history
    manage_user_data('update_document', username, history)
    return response    


def clean_db(username, history):
    manage_user_data('update_document', username, history)
    return True