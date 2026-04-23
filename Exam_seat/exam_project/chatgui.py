import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
import tkinter as tk
import customtkinter as ctk
import threading
from datetime import datetime
import time
from typing import List, Dict

class EnhancedChatbot:
    def __init__(self):
        # NLP & model
        self.lemmatizer = WordNetLemmatizer()
        self.model = load_model('chatbot_model.h5')
        self.intents = json.loads(open('intents.json', encoding='utf-8').read())
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.classes = pickle.load(open('classes.pkl', 'rb'))

        # Window
        self.window = ctk.CTk()
        self.window.title("NotesAI - Career Chatbot")
        self.window.geometry("900x700")
        self.window.minsize(800, 600)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.typing_speed = 0.02
        self.is_typing = False
        self.chat_history: List[Dict] = []

        self.setup_ui()

    def setup_ui(self):
        # --- Top Header ---
        self.header_frame = ctk.CTkFrame(self.window, height=60, fg_color="#1abc9c")
        self.header_frame.pack(fill=tk.X)
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="NotesAI - Your Career Assistant",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.header_label.pack(pady=10)

        # --- Chat Frame ---
        self.chat_frame_container = ctk.CTkFrame(self.window)
        self.chat_frame_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,5))

        # Scrollable chat canvas
        self.chat_canvas = tk.Canvas(
            self.chat_frame_container, bg="#2c3e50", highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.chat_frame_container, orient="vertical", command=self.chat_canvas.yview
        )
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.chat_frame = tk.Frame(self.chat_canvas, bg="#2c3e50")
        self.chat_canvas.create_window((0,0), window=self.chat_frame, anchor="nw")
        self.chat_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

        # --- Input area ---
        self.input_frame = ctk.CTkFrame(self.window, height=100)
        self.input_frame.pack(fill=tk.X, padx=10, pady=(5,10))

        self.message_input = ctk.CTkTextbox(
            self.input_frame, height=50, wrap=tk.WORD, corner_radius=10
        )
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0), pady=5)
        self.message_input.bind("<Return>", self.handle_return)

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=90,
            fg_color="#2980b9",
            hover_color="#3498db",
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # --- Quick suggestions ---
        self.suggestion_frame = ctk.CTkFrame(self.window, height=50)
        self.suggestion_frame.pack(fill=tk.X, padx=10, pady=(0,10))
        self.update_suggestions([
            "Tell me about careers",
            "Top universities",
            "Best courses",
            "How to choose career?"
        ])

    # Quick suggestions
    def update_suggestions(self, suggestions: List[str]):
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()
        for suggestion in suggestions:
            btn = ctk.CTkButton(
                self.suggestion_frame,
                text=suggestion,
                width=180,
                height=30,
                fg_color="#16a085",
                hover_color="#1abc9c",
                command=lambda s=suggestion: self.use_suggestion(s)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def use_suggestion(self, suggestion: str):
        self.message_input.delete("1.0", tk.END)
        self.message_input.insert("1.0", suggestion)
        self.send_message()

    # Append chat bubbles
    def append_message(self, message: str, sender: str):
        bubble_color = "#2980b9" if sender=="bot" else "#27ae60"
        text_color = "white"

        bubble = tk.Label(
            self.chat_frame,
            text=message,
            bg=bubble_color,
            fg=text_color,
            font=("Helvetica", 12),
            wraplength=500,
            justify="left" if sender=="bot" else "right",
            padx=10,
            pady=6
        )
        bubble.pack(anchor="w" if sender=="bot" else "e", pady=5, padx=10)
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

        if sender=="bot":
            # Typing animation
            threading.Thread(target=self.animate_typing, args=(bubble, message)).start()

    # Simulated typing (optional)
    def animate_typing(self, bubble, message):
        pass  # Already displaying full bubble for simplicity

    # Enter key
    def handle_return(self, event):
        if not event.state & 0x1:
            self.send_message()
            return "break"

    # --- NLP Logic ---
    def clean_up_sentence(self, sentence: str) -> List[str]:
        return [self.lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(sentence)]

    def bow(self, sentence: str, words: List[str]) -> np.ndarray:
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w==s: bag[i]=1
        return np.array(bag)

    def predict_class(self, sentence: str) -> List[Dict]:
        p = self.bow(sentence,self.words)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return [{"intent":self.classes[r[0]],"probability":str(r[1])} for r in results]

    def get_response(self, ints: List[Dict]) -> str:
        if not ints: return "I'm not sure how to respond. Please rephrase."
        tag = ints[0]['intent']
        for intent in self.intents['intents']:
            if intent['tag']==tag: return random.choice(intent['responses'])
        return "Sorry, I don’t have info on that topic yet."

    def process_message(self, message: str) -> str:
        ints = self.predict_class(message)
        return self.get_response(ints)

    # Send message
    def send_message(self):
        message = self.message_input.get("1.0", tk.END).strip()
        if not message: return
        self.message_input.delete("1.0", tk.END)
        self.append_message(message, "user")

        def bot_reply():
            response = self.process_message(message)
            self.append_message(response, "bot")

        threading.Thread(target=bot_reply).start()
        self.update_suggestions([
            "Tell me more", "How does this help?", "Requirements?"
        ])

    def run(self):
        self.append_message("Hello! I'm NotesAI, your Career Assistant. How can I help you today?", "bot")
        self.window.mainloop()


if __name__ == "__main__":
    chatbot = EnhancedChatbot()
    chatbot.run()
