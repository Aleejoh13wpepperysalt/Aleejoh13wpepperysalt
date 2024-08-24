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
        print(f"AI chose: {action}")
        
        if action == 'mistake':
            mistake_id = random.randint(1, 1000)
            self.memory['mistakes'][mistake_id] = True
            print(f"Mistake made! Logged mistake ID: {mistake_id}")
        else:
            learned_info = f"Learned data at {random.randint(1, 1000)}"
            self.memory['learned_data'].append(learned_info)
            print(f"AI learned: {learned_info}")
        
        self.save_memory()

    def talk(self):
        if not self.memory['learned_data']:
            return "I haven't learned anything yet."
        
        response = random.choice(self.memory['learned_data'])
        print(f"AI says: {response}")

    def review_mistakes(self):
        if not self.memory['mistakes']:
            return "No mistakes logged."
        
        print("Reviewing mistakes:")
        for mistake_id in self.memory['mistakes']:
            print(f"Mistake ID: {mistake_id}")

    def kill(self):
        print("AI acknowledges the mistake. Marking as false information.")

# Usage
ai = LearningAI()

# Training loop
for _ in range(10):  # Train the AI over 10 iterations
    ai.train()

# Talking with the AI
ai.talk()

# Reviewing mistakes
ai.review_mistakes()

# Kill command example
ai.kill()
