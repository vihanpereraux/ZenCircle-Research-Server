# module import
import time
from openai import OpenAI
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tinydb import TinyDB, Query
# from pymongo import Mongllls
# oClient
from bson.objectid import ObjectId
import json

# functions import
from Model.communication_model import manage_user_data
from Model.communication_model import manage_conversation
from Model.communication_model import manage_ai_assistant
from Model.communication_model import get_personal_history
from Model.communication_model import clean_db
from Model.communication_model import update_emotion_prediction_state
from Model.communication_model import get_emotion_predictions

from TTS_Service.text_2_speech_XTTS2 import text_to_speech
from SPT_Service.speech_2_text import audio_2_text


app = Flask(__name__)
CORS(app)

#  tinydb init
db = TinyDB('db.json')
history = []
username = 'vihanpereraux'


# default get end point
@app.route("/", methods=['GET'])
def getFunction(): 
  return jsonify({ 'response': "Flask app is up and running on port 5000 !" })


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


# get voice note from the backend
@app.route("/send-voice-note", methods=['POST']) 
def send_voice_note():
  if 'audio' not in request.files:
        return 'No file part'
  else:
    audio_file = request.files['audio']
    audio_file.save('SPT_Service/uploaded_audio.wav')  # Save the uploaded audio file
    time.sleep(5)
    audio_2_text()
    return 'File uploaded successfully'


# get text summarization
@app.route("/get_text_summary", methods=['GET'])
def get_text_summary():
  content = request.args.get('content')

  # Point to the local server
  client = OpenAI(base_url="http://localhost:1235/v1", api_key="lm-studio")

  history = [
      {"role": "system", "content": "You are an intelligent assistant. just do what user says"},
      {"role": "user", "content": content},
  ]
  
  completion = client.chat.completions.create(
      model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
      messages=history,
      temperature=0.7,
      stream=True,
  )

  new_message = {"role": "assistant", "content": ""}
  
  for chunk in completion:
      if chunk.choices[0].delta.content:
          print(chunk.choices[0].delta.content, end="", flush=True)
          new_message["content"] += chunk.choices[0].delta.content

  history.append(new_message)

  # print(completion.choices[/0].message.content)
  return jsonify({ 'response': new_message["content"] })


# communication with the lmserver - ai assistant workflow
@app.route("/get-ai-assistant-response", methods=['GET'])
def get_AI_assistant_response():
  content = request.args.get('content')
  response = manage_ai_assistant(content)
  text_to_speech(response)
  voice_note = 'TTS_Service/audio/output.wav'
  return send_file(voice_note), 201


# save facial emotions prediction and eeg emotion prediction data
@app.route("/process_prediction_data", methods=['POST'])
def process_prediction_data():
  # facial ones
  emotions_prediction = request.args.get('emotions_prediction')
  response = update_emotion_prediction_state(emotions_prediction)
  if response == "User updated":
    return jsonify({ 'message': 'user is updated' })


# get predictions
@app.route("/get_predictions", methods=['GET'])
def get_predictions():
  response = get_emotion_predictions()
  return jsonify({ 'response': response })


# retrieve the conversation history
@app.route("/get-chat-history", methods=['GET'])
def get_chat_history():
  response = get_personal_history()
  return jsonify({ 'response': response }), 201


# clean the conversation history
@app.route("/clean-conversation-history", methods=['POST'])
def clean_conversation_history():
  response = clean_db(username, history)
  if response:  
    return jsonify({ 'message': 'history cleared' }), 201
  else:
    return jsonify({ 'message': 'history not cleared, something happened' }), 500
  
   
  
if __name__ == "__main__":
  app.run(debug=True) 
  

