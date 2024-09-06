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
        self.instruction_label.pack(pady=10)

        self.score_label = tk.Label(self, text="Score: 0", font=("Times New Roman", 14))
        self.score_label.pack(pady=5)

        self.level_label = tk.Label(self, text="Level: 1", font=("Times New Roman", 14))
        self.level_label.pack(pady=5)

        self.item_name_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.item_name_label.pack(pady=5)

        self.message_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.message_label.pack(pady=10)

        self.score_history_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.score_history_label.pack(pady=10)

        # Buttons for actions
        self.start_button = tk.Button(self, text="Start", command=self.start_game, font=("Times New Roman", 12))
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit_game, font=("Times New Roman", 12))
        self.quit_button.pack(padx=10)

        # Initialize game state
        self.current_item = None
        self.attempts = 0
        self.score = 0
        self.level = 1
        self.items_to_identify = 5
        self.items_identified = 0
        self.scores = []
        self.high_score = 0

        self.auto_listening = True  # Enable auto-listening by default

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

    def reset_game(self):
        # Save the current score and track the highest score
        self.scores.append(self.score)
        self.high_score = max(self.high_score, self.score)

        # Reset game state
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"Level: {self.level}")
        self.score_label.config(text=f"Score: {self.score}")
        self.message_label.config(text="Game has been reset. Click 'Start' to play again.")
        self.display_score_history()

    def display_score_history(self):
        score_history = "\n".join([f"Game {i + 1}: {score}" for i, score in enumerate(self.scores)])
        self.score_history_label.config(text=f"Score History:\n{score_history}\nHigh Score: {self.high_score}")

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
                    self.after(1000, self.check_level_progress)
                else:
                    self.attempts += 1
                    if self.attempts >= 2:
                        self.message_label.config(text=f"You lost! The correct answer was '{self.current_item}'.")
                        self.after(2000, self.next_item)
                    else:
                        self.message_label.config(text=f"Incorrect. You have {2 - self.attempts} attempts left.")
            except sr.UnknownValueError:
                self.message_label.config(text="Sorry, I did not understand that.")
            except sr.RequestError as e:
                self.message_label.config(text=f"Could not request results; {e}")
            except sr.WaitTimeoutError:
                self.message_label.config(text="You ran out of time!")

    def check_level_progress(self):
        if self.items_identified >= self.items_to_identify:
            self.message_label.config(text="Congratulations! You completed the level.")
            self.reset_game()
        else:
            self.next_item()

    def next_item(self):
        # Reset attempts and load a new item
        self.attempts = 0
        self.current_item = self.get_random_item()
        self.display_image(self.current_item)
        self.item_name_label.config(text=f"Item: {self.current_item}")
        self.auto_listen()

    def auto_listen(self):
        if self.auto_listening:
            self.listen_and_recognize()
            self.after(3000, self.auto_listen)  # Automatically listen every 5 seconds

    def quit_game(self):
        self.destroy()

if __name__ == "__main__":
    # Create and start the game GUI
    app = VoiceRecognitionGame()
    app.mainloop()
