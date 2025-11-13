from flask import Flask, jsonify, request 


app = Flask(__name__)

notes = [] 

@app.route('/')
def home():
    return "Welcome to the Notes APP!"  

@app.route("/notes", methods=["GET"])
def get_notes(): 
    return jsonify(notes) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
