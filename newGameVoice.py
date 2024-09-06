import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import speech_recognition as sr

# Extended list of items (images and names) for identification
items = {
    "apple": "apple.png",
    "banana": "banana.png",
    "orange": "orange.png",
    "grape": "grape.png",
    "carrot": "carrot.png",
    "tomato": "tomato.png",
    "strawberry": "strawberry.png",
    "watermelon": "watermelon.png",
    "pineapple": "pineapple.png",
    "broccoli": "broccoli.png",
    "kiwi": "kiwi.png",
    "mango": "mango.png",
    "peach": "peach.png",
    "pear": "pear.png",
    "plum": "plum.png",
    "raspberry": "raspberry.png",
    "blueberry": "blueberry.png",
    "cherry": "cherry.png",
    "melon": "melon.png",
    "pomegranate": "pomegranate.png"
}

# Shuffle the item list for each game session
item_keys = list(items.keys())
random.shuffle(item_keys)

# Initialize the recognizer
recognizer = sr.Recognizer()

class VoiceRecognitionGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Voice Recognition Game")
        self.geometry("600x600")

        # Create a canvas to hold the image and text
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.pack()

        # Labels for displaying information with Times New Roman font
        self.instruction_label = tk.Label(self, text="Identify the item shown in the picture", font=("Times New Roman", 14))
        self.instruction_label.pack(padx=10)

        self.score_label = tk.Label(self, text="Score: 0", font=("Times New Roman", 14))
        self.score_label.pack(padx=5)

        self.level_label = tk.Label(self, text="Level: 1", font=("Times New Roman", 14))
        self.level_label.pack(padx=5)

        self.item_name_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.item_name_label.pack(padx=5)

        self.message_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.message_label.pack(padx=10)

        self.score_history_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.score_history_label.pack(padx=10)

        # Buttons for actions
        self.start_button = tk.Button(self, text="Start", command=self.start_game, font=("Times New Roman", 12))
        self.start_button.pack(padx=10)

        self.listen_button = tk.Button(self, text="Listen", command=self.listen_and_recognize, font=("Times New Roman", 12), state=tk.DISABLED)
        self.listen_button.pack(padx=10)

        self.auto_listen_button = tk.Button(self, text="Auto Listen", command=self.toggle_auto_listen, font=("Times New Roman", 12), state=tk.DISABLED)
        self.auto_listen_button.pack(padx=10)

        self.next_button = tk.Button(self, text="Next Item", command=self.next_item, font=("Times New Roman", 12), state=tk.DISABLED)
        self.next_button.pack(padx=10)

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.quit_game, font=("Times New Roman", 12))
        self.quit_button.pack(padx=10)

        # Initialize game state
        self.current_item = None
        self.attempts = 0
        self.score = 0
        self.level = 1
        self.items_to_identify = 5
        self.items_identified = 0
        self.auto_listening = False
        self.scores = []

    def start_game(self):
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"Level: {self.level}")
        self.score_label.config(text=f"Score: {self.score}")
        self.message_label.config(text="Game started! Identify the item.")
        self.next_item()
        self.listen_button.config(state=tk.NORMAL)
        self.auto_listen_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

    def reset_game(self):
        # Save the current score
        self.scores.append(self.score)

        # Reset game state
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"Level: {self.level}")
        self.score_label.config(text=f"Score: {self.score}")
        self.message_label.config(text="Game has been reset. Click 'Start' to play again.")
        self.listen_button.config(state=tk.DISABLED)
        self.auto_listen_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.display_score_history()

    def display_score_history(self):
        score_history = "\n".join([f"Game {i + 1}: {score}" for i, score in enumerate(self.scores)])
        self.score_history_label.config(text=f"Score History:\n{score_history}")

    def get_random_item(self):
        # Get a random item from the shuffled list
        return random.choice(item_keys)

    def display_image(self, item):
        # Load the image and display it on the canvas
        image_path = items[item]
        img = Image.open(image_path)
        img = img.resize((200, 200))  # Resize the image to fit the canvas
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 150, image=img_tk)
        self.canvas.image = img_tk  # Keep a reference to prevent garbage collection

    def listen_and_recognize(self):
        with sr.Microphone() as source:
            # Adjust for background noise and listen
            recognizer.adjust_for_ambient_noise(source)
            self.message_label.config(text="Listening... Please say the name of the item.")
            audio = recognizer.listen(source, timeout=10)

            try:
                # Recognize speech
                text = recognizer.recognize_google(audio).lower()
                self.message_label.config(text=f"You said: {text}")

                # Check the result
                if text == self.current_item:
                    self.score += 1
                    self.items_identified += 1
                    self.score_label.config(text=f"Score: {self.score}")
                    self.message_label.config(text="Correct! You identified the item.")
                    if self.items_identified >= self.items_to_identify:
                        self.message_label.config(text="Congratulations! You completed the level.")
                        self.reset_game()
                else:
                    self.attempts += 1
                    if self.attempts >= 2:
                        self.message_label.config(text=f"You lost! The correct answer was '{self.current_item}'.")
                        self.reset_game()
                    else:
                        self.message_label.config(text=f"Incorrect. You have {2 - self.attempts} attempts left.")
            except sr.UnknownValueError:
                self.message_label.config(text="Sorry, I did not understand that.")
            except sr.RequestError as e:
                self.message_label.config(text=f"Could not request results; {e}")
            except sr.WaitTimeoutError:
                self.message_label.config(text="You ran out of time!")

    def next_item(self):
        # Reset attempts and load a new item
        self.attempts = 0
        self.current_item = self.get_random_item()
        self.display_image(self.current_item)
        self.item_name_label.config(text=f"Item: {self.current_item}")

    def toggle_auto_listen(self):
        if self.auto_listening:
            self.auto_listening = False
            self.auto_listen_button.config(text="Auto Listen")
            self.message_label.config(text="Auto listening disabled.")
        else:
            self.auto_listening = True
            self.auto_listen_button.config(text="Stop Auto Listen")
            self.message_label.config(text="Auto listening enabled.")
            self.auto_listen()

    def auto_listen(self):
        if self.auto_listening:
            self.listen_and_recognize()
            self.after(5000, self.auto_listen)  # Automatically listen every 5 seconds

    def quit_game(self):
        self.destroy()

if __name__ == "__main__":
    # Create and start the game GUI
    app = VoiceRecognitionGame()
    app.mainloop()
