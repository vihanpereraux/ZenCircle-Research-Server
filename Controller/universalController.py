from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# GET
@app.route("/", methods=['GET'])
def getFunction():
  return "Sending the text !!"

# POST
@app.route("/get-response", methods=['POST'])
def getResponse():
  content = request.args.get('content')
  
  system_content = "Always respond in a very human-like behaviour"
  
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

  # print(completion.choices[0].message)
  
  item = {
    'item_id' : 1,
    'message' : completion.choices[0].message.content   
  }
  
  return jsonify(item), 201
  
if __name__ == "__main__":
  app.run(debug=True) 
  

