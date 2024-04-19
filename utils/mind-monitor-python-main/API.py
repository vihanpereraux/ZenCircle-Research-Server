from flask import Flask
from Rec import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    kuku = getData()
    return kuku

if __name__ == "__main__":
    app.run()

    