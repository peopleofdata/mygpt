import os, openai, apikey
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")
openai.api_key = os.environ.get('OPENAI_API_KEY')
instruction = 'You are a helpful assistant.'
history = []

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get_history', methods=['GET'])
def get_history():
    global history
    return jsonify({"history": history}), 200

def process_history(history, limit):
    if len(history)<limit:
        n=len(history)
    else:
        n=limit
    return history[-n:]

def query_openai():
    global history
    global instruction
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            #process_history(history, 5)
            {'role':'system','content':f'{instruction}'},
            *process_history(history, 5)
        ]
    )
    openai_response = response['choices'][0]['message']
    return openai_response['content']

@app.route('/store_text', methods=['POST'])
def store_text():
    global history
    global instruction
    text = request.form.get('text')
    user_message = {"role": "user", "content": text}
    history.append(user_message)
    system_response = {'role':'assistant','content':query_openai()}
    history.append(system_response)
    print(history)
    return jsonify({"response": "This doesn't work anyway"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
