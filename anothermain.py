import requests
import pywhatkit as pwt
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import Canvas, Button, Label
from PIL import Image, ImageTk
import datetime
import pyttsx3
import webbrowser
import random
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("rate", 185)
engine.setProperty('voice', voices[1].id)

# Define chatbot questions and responses
questions = [
    "Which is the capital of Karnataka?",
    "Who is the current prime minister of India?",
    "When is the independence day?",
    "What is the pincode of Puttur?",
    "Who is the father of Infosys?",
    "Who is the male lead in KGF movie?",
    "Who is the father of C?",
    "Give me some fruits name?",
    "In 2024 world cup winner?",
    "What is ML?"
]

responses = {
    "Which is the capital of Karnataka?": "Bangalore",
    "Who is the current prime minister of India?": "Narendra Modi",
    "When is the independence day?": "August 15",
    "What is the pincode of Puttur?": "564203",
    "Who is the father of Infosys?": "Sudha Murthy",
    "Who is the male lead in KGF movie?": "Rocking Star Yash",
    "Who is the father of C?": "Dennis Ritchie",
    "Give me some fruits name?": "Mango, orange, banana etc.",
    "In 2024 world cup winner?": "India",
    "What is ML?": "Machine learning (ML) is a branch of artificial intelligence and computer science that focuses on using data and algorithms to enable AI to imitate the way that humans learn, gradually improving its accuracy."
}

# Vectorize the predefined questions
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

def chatbot_response(user_input):
    # Vectorize the user input
    user_input_vec = vectorizer.transform([user_input])

    # Compute cosine similarity between user input and predefined questions
    similarities = cosine_similarity(user_input_vec, X)

    # Find the index of the most similar question
    most_similar_index = similarities.argmax()

    # Get the corresponding response
    response = responses.get(questions[most_similar_index], "I'm not sure how to respond to that.")
    return response

def open_chatbot_window():
    chatbot_window = tk.Toplevel(root)
    chatbot_window.title("Chatbot")
    chatbot_window.geometry("400x500")

    # Create and place the chat history text widget
    global chat_history
    chat_history = scrolledtext.ScrolledText(chatbot_window, wrap=tk.WORD, state=tk.DISABLED)
    chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create and place the user input field
    global user_input_field
    user_input_field = tk.Entry(chatbot_window, width=50)
    user_input_field.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

    # Create and place the submit button
    submit_button = tk.Button(chatbot_window, text="Send", command=process_chatbot_input)
    submit_button.pack(padx=10, pady=5, side=tk.RIGHT)

def process_chatbot_input():
    user_input = user_input_field.get()  # Get the user input from the entry field
    if user_input:
        response = chatbot_response(user_input)  # Process the input using the chatbot_response function
        chat_history.config(state=tk.NORMAL)  # Allow editing the chat history text widget
        chat_history.insert(tk.END, f"You: {user_input}\n")  # Add user input to chat history
        chat_history.insert(tk.END, f"Bot: {response}\n")  # Add bot response to chat history
        chat_history.config(state=tk.DISABLED)  # Disable editing the chat history text widget
        user_input_field.delete(0, tk.END)  # Clear the entry field

# Initialize main application window
root = tk.Tk()
root.geometry("2000x1100")
root.title("JARVIS")

canvas = Canvas(root, width=1000, height=1000)
canvas.pack(fill="both", expand=True)

# Load images
img = ImageTk.PhotoImage(file="finalmic (1).jpg")
vision = ImageTk.PhotoImage(file="face (1).png")
Loop = ImageTk.PhotoImage(file="reload-refresh-arrows-loop-flat-icon-vector-20383569 (1).jpg")
limg = ImageTk.PhotoImage(file="final.jpg")

# Create buttons
MIC_button = Button(root, command=lambda: take_listen(), image=img)
Loop_mic = Button(root, text="Loop", command=open_chatbot_window, image=Loop)
# Face_Detection = Button(root, text="Face", command=detection, image=vision)


# Place widgets on canvas
lbl = Label(root, image=limg)
lbl_canvas = canvas.create_window(850, 100, anchor="nw", window=lbl)
button1_canvas = canvas.create_window(400, 600, anchor="nw", window=MIC_button)
Loop_button = canvas.create_window(1500, 600, anchor='nw', window=Loop_mic)
# face_button = canvas.create_window(400, 600, anchor="nw", window=Face_Detection) # Left commented out

info_frame = tk.Frame(root, padx=10, pady=10)
info_frame.place(x=1300, y=170)  # Adjust the position as needed

time_label = ttk.Label(info_frame, text="", font=("Helvetica", 24))
time_label.pack(pady=10)

date_label = ttk.Label(info_frame, text="", font=("Helvetica", 18))
date_label.pack(pady=10)

def update_time_date():
    current_time = time.strftime('%H:%M:%S')
    current_date = time.strftime('%Y-%m-%d')
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    root.after(1000, update_time_date)

# Define location function
def get_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        location = f"{data['city']}, {data['region']}, {data['country']}"
        return location
    except Exception as e:
        return "Unable to fetch location"

location = get_location()
location_label = ttk.Label(info_frame, text=f"Location: {location}", font=("Helvetica", 14))
location_label.pack(pady=10)

# Update time and date
update_time_date()

root.mainloop()
