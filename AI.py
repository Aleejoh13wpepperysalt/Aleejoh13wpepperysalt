import tkinter as tk
from tkinter import messagebox
import random
import pickle

class LearningAI:
    def __init__(self, memory_file='memory.pkl'):
        self.memory_file = memory_file
        self.memory = self.load_memory()
        self.actions = ['correct_action', 'mistake']

    def load_memory(self):
        try:
            with open(self.memory_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {'mistakes': {}, 'learned_data': []}

    def save_memory(self):
        with open(self.memory_file, 'wb') as f:
            pickle.dump(self.memory, f)

    def choose_action(self):
        if random.random() > 0.5:
            return 'correct_action'
        else:
            return 'mistake'

    def train(self):
        action = self.choose_action()
        
        if action == 'mistake':
            mistake_id = random.randint(1, 1000)
            self.memory['mistakes'][mistake_id] = True
        else:
            learned_info = f"Learned data at {random.randint(1, 1000)}"
            self.memory['learned_data'].append(learned_info)
        
        self.save_memory()

    def talk(self):
        if not self.memory['learned_data']:
            return "I haven't learned anything yet."
        
        response = random.choice(self.memory['learned_data'])
        return response

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
        self.root.title("AI Interface")
        
        self.train_button = tk.Button(root, text="Train AI", command=self.train_ai)
        self.train_button.pack(pady=10)

        self.talk_button = tk.Button(root, text="Talk", command=self.ai_talk)
        self.talk_button.pack(pady=10)
        
        self.review_button = tk.Button(root, text="Review Mistakes", command=self.review_mistakes)
        self.review_button.pack(pady=10)

        self.kill_button = tk.Button(root, text="Kill", command=self.kill_ai)
        self.kill_button.pack(pady=10)

    def train_ai(self):
        self.ai.train()
        messagebox.showinfo("Training", "AI trained successfully!")

    def ai_talk(self):
        response = self.ai.talk()
        messagebox.showinfo("AI Says", response)

    def review_mistakes(self):
        mistakes = self.ai.review_mistakes()
        messagebox.showinfo("Mistakes", mistakes)

    def kill_ai(self):
        result = self.ai.kill()
        messagebox.showinfo("Kill", result)

# Create the main window
root = tk.Tk()
app = AIApp(root)
root.mainloop()