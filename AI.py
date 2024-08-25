import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import random
import pickle
import re

class LearningAI:
    def __init__(self, memory_file='memory.pkl'):
        self.memory_file = memory_file
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open(self.memory_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {'mistakes': {}, 'learned_data': []}

    def save_memory(self):
        with open(self.memory_file, 'wb') as f:
            pickle.dump(self.memory, f)

    def learn_from_website(self, url, tag, limit=50):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find_all(tag)
            learned_data = [element.get_text() for element in content if element.get_text().strip() != '']
            learned_data = learned_data[:limit]
            self.memory['learned_data'].extend(learned_data)
            self.save_memory()
        except requests.RequestException as e:
            print(f"An error occurred while accessing {url}: {e}")

    def talk(self, user_input):
        if not self.memory['learned_data']:
            return "I haven't learned anything yet."

        user_input_lower = user_input.lower()
        for data in self.memory['learned_data']:
            if re.search(r'\b{}\b'.format(re.escape(user_input_lower)), data.lower()):
                return data

        return "I didn't understand that. Can you please elaborate?"

    def review_mistakes(self):
        if not self.memory['mistakes']:
            return "No mistakes logged."
        mistakes = "\n".join([f"Mistake ID: {mistake_id}" for mistake_id in self.memory['mistakes']])
        return mistakes

    def kill(self):
        return "AI acknowledges the mistake. Marking as false information."

# GUI Class
class AIApp:
    def __init__(self, root):
        self.ai = LearningAI()
        self.root = root
        self.root.title("AI Chat Interface")

        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_window.pack(pady=10)

        self.user_input = tk.Entry(root, width=40)
        self.user_input.pack(pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.process_input)
        self.send_button.pack(pady=10)

        self.learn_button = tk.Button(root, text="Learn from Website", command=self.learn_from_website)
        self.learn_button.pack(pady=10)

    def process_input(self):
        user_text = self.user_input.get()
        if user_text.lower() == "kill":
            response = self.ai.kill()
        elif user_text.lower() == "review mistakes":
            response = self.ai.review_mistakes()
        else:
            response = self.ai.talk(user_text)

        self.display_message("You: " + user_text)
        self.display_message("AI: " + response)
        self.user_input.delete(0, tk.END)

    def display_message(self, message):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, message + "\n")
        self.chat_window.config(state='disabled')
        self.chat_window.yview(tk.END)

    def learn_from_website(self):
        # Example URLs and tags to learn from
        sites_to_learn = [
            {"url": "https://www.dictionary.com", "tag": "p"},  # Dictionary
            {"url": "https://www.learnpython.org/", "tag": "p"},  # Python
            {"url": "https://minecraft.fandom.com/wiki/Tutorials/Setting_up_a_server", "tag": "p"}  # Minecraft server
        ]

        for site in sites_to_learn:
            self.ai.learn_from_website(site['url'], site['tag'])

        messagebox.showinfo("Learning", "AI learned from specified websites!")

# Create the main window
root = tk.Tk()
app = AIApp(root)
root.mainloop()
