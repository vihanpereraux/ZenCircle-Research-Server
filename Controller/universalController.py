from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# GET
@app.route("/", methods=['GET'])
def getFunction():
  return "Sending the text !!"

# POST
@app.route("/get-response", methods=['POST'])
def getResponse():
  # if request.json or 'name' not in request.json:
  #   return jsonify({'error': 'Ivalid Payload !!'}), 400
  
  item = {
    'item_id' : 1,
    'message' : 'Im doing good !! '    
  }
  
  return jsonify(item), 201
  
if __name__ == "__main__":
  app.run(debug=True) 
  
  
  
  

# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local serverls
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="YanaS/llama-2-7b-langchain-chat-GGUF",
  messages=[
    {"role": "system", "content": "Always answer in rhymes."},
    {"role": "user", "content": "Introduce yourself."}
  ],
  temperature=0.7,
)

print(completion.choices[0].message.content)


# def mainFunc():
#     print("Universal Copntroller is running")
