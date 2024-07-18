from api import api
api_code = api


from openai import OpenAI #version 
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from gtts import gTTS
import os
import playsound #version 1.2.2

# Function to get response from ChatGPT
def get_chatgpt_response(prompt):
    
    client = OpenAI(api_key="api-key")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": prompt}
        
                 ]
                                               )
         
    return str(completion.choices[0].message.content)

# Function to handle voice input
def listen_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio_data = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, there seems to be an issue with the speech recognition service."

# Function to handle voice output
def speak_text(text):
    tts = gTTS(text=text, lang='fr')
    filename = "temp_voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# Function to send input to ChatGPT and display the response
def send_input():
    user_input = user_entry.get()
    chat_area.insert(tk.END, "You: " + user_input + "\n")
    user_entry.delete(0, tk.END)
    
    response = get_chatgpt_response(user_input)
    chat_area.insert(tk.END, "ChatGPT: " + response + "\n")
    speak_text(response)

# Function to handle voice input button click
def handle_voice_input():
    user_input = listen_voice_input()
    chat_area.insert(tk.END, "You: " + user_input + "\n")
    
    response = get_chatgpt_response(user_input)
    chat_area.insert(tk.END, "ChatGPT: " + response + "\n")
    speak_text(response)

# Setting up the GUI
window = tk.Tk()
window.title("Voice ChatGPT")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_entry = tk.Entry(window, width=80)
user_entry.pack(padx=10, pady=10, side=tk.LEFT)

send_button = tk.Button(window, text="Send", command=send_input)
send_button.pack(padx=10, pady=10, side=tk.LEFT)

voice_button = tk.Button(window, text="Voice Input", command=handle_voice_input)
voice_button.pack(padx=10, pady=10, side=tk.LEFT)

window.mainloop()
