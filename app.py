from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message')
    payload = request.form.get('payload')


    data = {"sender": "user", "message": user_message or payload}


    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
    response = requests.post(rasa_url, json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
