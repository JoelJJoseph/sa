from flask import Flask, request, jsonify
import json
import random
import speech_recognition as sr
from gtts import gTTS
import os
import pygame

# Initialize pygame
pygame.mixer.init()

# Specify the absolute path to the intent.json file
intent_file_path = './intent.json'  # Replace with the actual path

# Load the intent.json file
with open(intent_file_path, 'r') as intent_file:
    intents = json.load(intent_file)

# Function to recognize intent
def recognize_intent(user_input):
    user_input = user_input.lower()
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input:
                return intent
    return None

# Function to get a random response for an intent
def get_response(intent):
    responses = intent['responses']
    return random.choice(responses)

# Function to convert text to audio and play it using pygame
def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()

app = Flask(__name__)

@app.route('/synthesize_audio', methods=['POST'])
def synthesize_audio():
    try:
        user_input = request.form['user_input']
        matched_intent = recognize_intent(user_input)

        if matched_intent:
            response = get_response(matched_intent)
            text_to_audio(response)
            return jsonify({'message': 'Audio synthesized successfully'})
        else:
            return jsonify({'error': "I'm sorry, I didn't understand that. Please ask another question."})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
