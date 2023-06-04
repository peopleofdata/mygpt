key = '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'

import random
import numpy as np
import pickle
import openai
openai.api_key = key
phrases = {}
storage_file = 'memory.pickle'

def load_phrases():
    global phrases
    try:
        with open(storage_file, 'rb') as f:
            phrases = pickle.load(f)
    except FileNotFoundError:
        phrases = {}

def save_phrases():
    with open(storage_file, 'wb') as f:
        pickle.dump(phrases, f)

def query_openai(phrase):
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": "You translate user input into english"},
            {"role": "user", "content": f"{phrase}"}
        ]
    )
    return response['choices'][0]['message']['content']

def memorization():
    while True:
        phrase = input("Enter a phrase in your learning language (or 'exit' to stop): ")
        if phrase.lower() == 'exit':
            break
        # Use OpenAI API to get the translation
        translation = query_openai(phrase)
        phrases[phrase] = {"translation": translation, "score": 0}
        print(f"English translation: {translation}")
        print("Phrase added to the memory bank.\n")

def recall():
    if not phrases:
        print("There are no phrases in the memory bank. Switch to memorization mode to add phrases.")
        return

    # Sort phrases by score in descending order
    sorted_phrases = sorted(phrases.items(), key=lambda x: x[1]['score'], reverse=True)

    for phrase, info in sorted_phrases:
        if random.choice([True, False]):
            user_translation = input(f"Translate the following phrase into English: {phrase}\n")
            correct_translation = info['translation']
        else:
            user_translation = input(f"Translate the following English phrase: {info['translation']}\n")
            correct_translation = phrase

        # Use OpenAI API to check the translation
        # is_correct = OpenAI_API.check_translation(user_translation, correct_translation)
        is_correct = np.random.choice([True, False])  # This is a placeholder
        if is_correct:
            phrases[phrase]['score'] -= 1
            print("Correct! Well done.")
        else:
            phrases[phrase]['score'] += 1
            print(f"Incorrect. The correct translation is: {correct_translation}")
        print("\n")

def run():
    load_phrases()
    while True:
        mode = input("Enter the mode (M for memorization or R for recall) or 'exit' to quit: ")
        if mode.lower() == 'exit':
            save_phrases()
            break
        elif mode.lower() == 'check':
            print(phrases)
            continue
        elif mode.lower() in ['m','M']:
            memorization()
        elif mode.lower() in ['r','R']:
            recall()
        else:
            print("Invalid mode. Please enter either 'memorization' or 'recall'.\n")

if __name__ == "__main__":
    run()
