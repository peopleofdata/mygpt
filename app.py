import os, openai
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")
openai.api_key = key = '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'#os.environ.get('openai')
history = [{'role':'user','content':'Hi! You are in default mode: (C)heck, (M)emorize or (R)ecall or just chat!'}]
mode = 'default'
phrases = {'hello':{'translation':'hello','score':0}}
storage_file = 'memory.pickle'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get_history', methods=['GET'])
def get_history():
    global history
    return jsonify({"history": history}), 200

def query_openai(prompt, text):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{text}"}
        ]
    )
    return response['choices'][0]['message']['content']

@app.route('/store_text', methods=['POST'])
def store_text():
    global history
    global mode
    global phrases
    text = request.form.get('text')
    history.append({'role':'user','content': text})
    if not text:
        system_response = {'role':'shell', 'content': 'No content?'}
    if text.lower() in ['e','E','exit','d','default','q']:
        mode = 'default'
        system_response = {'role':'shell', 'content': 'Exited to default.'}
    elif mode == 'default':
        if text.lower() in ['c','C','check']:
            system_response = {'role':'shell','content':str(phrases)}
        elif text.lower() in ['m','M']:
            mode = 'memorization'
            system_response = {'role':'shell','content':mode}
        elif text.lower() in ['r','R']:
            mode = 'recall'
            system_response = {'role':'shell','content':mode}
        else:
            system_response = {'role':'assistant','content':query_openai("Respond smart and short.", text)}
    elif mode =='memorization':
        try:
            openai_response = query_openai("You translate user input into english", text)
            phrases[text] = {"translation": openai_response, "score": 0}
            system_response= {'role':'assistant','content':openai_response}
        except Exception as e:
            system_response = {'role':'shell', 'content':str(e)}
    elif mode =='recall':
        print('recall_mode')
        sorted_phrases = sorted(phrases.items(), key=lambda x: x[1]['score'], reverse=True)
        for phrase, info in sorted_phrases[0]:
            system_response = {'role':'shell', 'content':phrase}
            history.append(system_response)
            prompt = "You respond only CORRECT or INCORRECT. You receive USER input and TRANSLATION and respond CORRECT if the meaning is the same but the language is different."
            openai_response = query_openai(prompt, f'USER:{text}, TRANSLATION:{phrase}')
            system_response = {'role':'assistant', 'content':openai_response}
    history.append(system_response)
    return jsonify({"response": "This doesn't work anyway"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))