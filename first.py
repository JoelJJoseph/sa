import json
import random
import speech_recognition as sr
from gtts import gTTS
import os
import streamlit as st
import pygame
from PIL import Image

def app():
        

    # Specify the absolute path to the intent.json file
    intent_file_path = './firstaid/intent.json'  # Replace with the actual path

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
        output_path = './firstaid/outputs'  # Replace with the actual output directory
        os.makedirs(output_path, exist_ok=True)
        output_file = os.path.join(output_path, 'output.mp3')
        tts.save(output_file)
        pygame.mixer.music.load(output_file)  # Load the correct file path
        pygame.mixer.music.play()

    # Streamlit UI
    st.title("Voice Assistant Chatbot")
    
    image_path = "images/first.jpg"
    image = Image.open(image_path)
    st.image(image)

    user_input = st.text_input("Type exit to exit with the interaction with the bot.")

    if st.button("Enter Voice"):
        if user_input.lower() == 'exit':
            st.text("Bot: Goodbye!")
        else:
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    st.text("You (Speak):")
                    audio = r.listen(source)

                user_input = r.recognize_google(audio)
                st.text(f"You (Voice): {user_input}")

                matched_intent = recognize_intent(user_input)
                if matched_intent:
                    response = get_response(matched_intent)
                    st.text(f"Bot: {response}")
                    text_to_audio(response)
                else:
                    st.text("Bot: I'm sorry, I didn't understand that. Please ask another question.")

            except sr.UnknownValueError:
                st.text("Bot: I couldn't understand your audio. Please try again.")
            except sr.RequestError as e:
                st.text(f"Bot: There was an error with the speech recognition service: {e}")
