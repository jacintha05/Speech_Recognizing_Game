import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import speech_recognition as sr

# Updated list of items (images and names) for identification
items = {
    "আপেল": "apple.png",
    "কলা": "banana.png",
    "কমলা": "orange.png",
    "আঙ্গুর": "grape.png",
    "গাজর": "carrot.png",
    "টমেটো": "tomato.png",
    "স্ট্রবেরি": "strawberry.png",
    "তরমুজ": "watermelon.png",
    "আনানাস": "pineapple.png",
    "ব্রকলি": "broccoli.png",
    "কিভি": "kiwi.png",
    "আম": "mango.png",
    "পীচ": "peach.png",
    "নাশপাতি": "pear.png",
    "প্লাম": "plum.png",
    "রসবেরি": "raspberry.png",
    "ব্লুবেরি": "blueberry.png",
    "চেরি": "cherry.png",
    "খরবুজা": "melon.png",
    "দানাপত্র": "pomegranate.png"
}

# Shuffle the item list for each game session
item_keys = list(items.keys())
random.shuffle(item_keys)

# Initialize the recognizer
recognizer = sr.Recognizer()

class VoiceRecognitionGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ভয়েস রিকগনিশন গেম")
        self.geometry("600x600")

        # Create a canvas to hold the image and text
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Labels for displaying information with Times New Roman font
        self.instruction_label = tk.Label(self, text="চিত্রে প্রদর্শিত বস্তুটি চিহ্নিত করুন", font=("Times New Roman", 14))
        self.instruction_label.grid(row=1, column=0, columnspan=4, pady=10)

        self.score_label = tk.Label(self, text="মোট স্কোর: 0", font=("Times New Roman", 14))
        self.score_label.grid(row=2, column=0, columnspan=4, pady=5)

        self.level_label = tk.Label(self, text="স্তর: 1", font=("Times New Roman", 14))
        self.level_label.grid(row=3, column=0, columnspan=4, pady=5)

        self.item_name_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.item_name_label.grid(row=4, column=0, columnspan=4, pady=5)

        self.message_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.message_label.grid(row=5, column=0, columnspan=4, pady=10)

        self.score_history_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.score_history_label.grid(row=6, column=0, columnspan=4, pady=10)

        # Buttons for actions arranged in a row
        self.start_button = tk.Button(self, text="শুরু করুন", command=self.start_game, font=("Times New Roman", 12))
        self.start_button.grid(row=7, column=0, padx=5, pady=5)

        self.listen_button = tk.Button(self, text="শুনুন", command=self.listen_and_recognize, font=("Times New Roman", 12), state=tk.DISABLED)
        self.listen_button.grid(row=7, column=1, padx=5, pady=5)

        self.auto_listen_button = tk.Button(self, text="অটো শুনুন", command=self.toggle_auto_listen, font=("Times New Roman", 12), state=tk.DISABLED)
        self.auto_listen_button.grid(row=7, column=2, padx=5, pady=5)

        self.next_button = tk.Button(self, text="পরবর্তী বস্তু", command=self.next_item, font=("Times New Roman", 12), state=tk.DISABLED)
        self.next_button.grid(row=7, column=3, padx=5, pady=5)

        # Quit button
        self.quit_button = tk.Button(self, text="প্রস্থান", command=self.quit_game, font=("Times New Roman", 12))
        self.quit_button.grid(row=8, column=0, columnspan=4, pady=10)

        # Initialize game state
        self.current_item = None
        self.attempts = 0
        self.score = 0
        self.level = 1
        self.items_to_identify = 5
        self.items_identified = 0
        self.auto_listening = False

        # Initialize scores history
        self.scores = []
        self.display_score_history()

    def display_score_history(self):
        score_history = "\n".join([f"গেম {i + 1}: {score}" for i, score in enumerate(self.scores)])
        self.score_history_label.config(text=f"স্কোর ইতিহাস:\n{score_history}")

    def start_game(self):
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"স্তর: {self.level}")
        self.score_label.config(text=f"মোট স্কোর: {self.score}")
        self.message_label.config(text="গেম শুরু হয়েছে! বস্তু চিহ্নিত করুন।")
        self.next_item()
        self.listen_button.config(state=tk.NORMAL)
        self.auto_listen_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

    def reset_game(self):
        # Save the current score
        self.scores.append(self.score)
        self.display_score_history()

        # Reset game state
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"স্তর: {self.level}")
        self.score_label.config(text=f"মোট স্কোর: {self.score}")
        self.message_label.config(text="গেম পুনরায় শুরু হয়েছে। 'শুরু করুন' বাটনে ক্লিক করুন।")
        self.listen_button.config(state=tk.DISABLED)
        self.auto_listen_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

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
            self.message_label.config(text="শুনছি... দয়া করে বস্তুটির নাম বলুন।")
            audio = recognizer.listen(source, timeout=10)

            try:
                # Recognize speech
                text = recognizer.recognize_google(audio, language='bn-IN').lower()
                self.message_label.config(text=f"আপনি বলেছেন: {text}")

                # Check the result
                if text == self.current_item:
                    self.score += 1
                    self.items_identified += 1
                    self.score_label.config(text=f"মোট স্কোর: {self.score}")
                    self.message_label.config(text="সঠিক! আপনি বস্তুটি চিহ্নিত করেছেন।")
                    if self.items_identified >= self.items_to_identify:
                        self.message_label.config(text="অভিনন্দন! আপনি স্তর সম্পন্ন করেছেন।")
                        self.reset_game()
                    else:
                        # Automatically proceed to the next item
                        self.after(2000, self.next_item)  # 2 seconds delay before next item
                else:
                    self.attempts += 1
                    if self.attempts >= 2:
                        self.message_label.config(text=f"আপনি হারালেন! সঠিক উত্তর ছিল '{self.current_item}'।")
                        self.reset_game()
                    else:
                        self.message_label.config(text=f"ভুল উত্তর। আপনার {2 - self.attempts} চেষ্টা বাকি আছে।")
            except sr.UnknownValueError:
                self.message_label.config(text="দুঃখিত, আমি তা বুঝতে পারিনি।")
            except sr.RequestError as e:
                self.message_label.config(text=f"ফলাফলগুলি অনুরোধ করা যায়নি; {e}")
            except sr.WaitTimeoutError:
                self.message_label.config(text="সময় শেষ হয়ে গেছে!")

    def next_item(self):
        # Reset attempts and load a new item
        self.attempts = 0
        self.current_item = self.get_random_item()
        self.display_image(self.current_item)
        self.item_name_label.config(text=f"বস্তু: {self.current_item}")

    def toggle_auto_listen(self):
        if self.auto_listening:
            self.auto_listening = False
            self.auto_listen_button.config(text="অটো শুনুন")
            self.message_label.config(text="অটো শুনুন বন্ধ করা হয়েছে।")
        else:
            self.auto_listening = True
            self.auto_listen_button.config(text="অটো শুনুন বন্ধ করুন")
            self.message_label.config(text="অটো শুনুন শুরু করা হয়েছে।")
            self.auto_listen()

    def auto_listen(self):
        if self.auto_listening:
            self.listen_and_recognize()
            self.after(5000, self.auto_listen)  # Listen every 10 seconds
            self.after(1000, self.next_item)  # Move to next item every 20 seconds

    def quit_game(self):
        self.destroy()

if __name__ == "__main__":
    app = VoiceRecognitionGame()
    app.mainloop()
