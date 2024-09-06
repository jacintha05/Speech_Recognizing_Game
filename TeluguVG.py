import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import speech_recognition as sr

# Updated list of items (images and names) for identification
items = {
    "ఆపిల్": "apple.png",
    "అరటిపండు": "banana.png",
    "ఒరంజు": "orange.png",
    "ద్రాక్ష": "grape.png",
    "క్యారెట్": "carrot.png",
    "టమాటా": "tomato.png",
    "స్ట్రాబెర్రీ": "strawberry.png",
    "తరబూస": "watermelon.png",
    "అనాసపండు": "pineapple.png",
    "బ్రొకోలీ": "broccoli.png",
    "కివి": "kiwi.png",
    "మామిడి": "mango.png",
    "పీచ్": "peach.png",
    "నాస్పాతి": "pear.png",
    "ప్లమ్": "plum.png",
    "రాస్ప్‌బెర్రీ": "raspberry.png",
    "బ్లూబెర్రీ": "blueberry.png",
    "చెర్రీ": "cherry.png",
    "తొలగి": "melon.png",
    "పomegranate": "pomegranate.png"
}

# Shuffle the item list for each game session
item_keys = list(items.keys())
random.shuffle(item_keys)

# Initialize the recognizer
recognizer = sr.Recognizer()

class VoiceRecognitionGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("వాయిస్ రికగ్నిషన్ ఆట")
        self.geometry("600x600")
# Create a canvas to hold the image and text
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
# Centered Labels for displaying information with Times New Roman font
        self.instruction_label = tk.Label(self, text="చిత్రాన్ని గుర్తించండి", font=("Times New Roman", 14))
        self.instruction_label.grid(row=1, column=0, columnspan=4, pady=10, sticky="nsew")

        self.score_label = tk.Label(self, text="మొత్తం స్కోరు: 0", font=("Times New Roman", 14))
        self.score_label.grid(row=2, column=0, columnspan=4, pady=5, sticky="nsew")

        self.level_label = tk.Label(self, text="పదవి: 1", font=("Times New Roman", 14))
        self.level_label.grid(row=3, column=0, columnspan=4, pady=5, sticky="nsew")

        self.item_name_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.item_name_label.grid(row=4, column=0, columnspan=4, pady=5, sticky="nsew")

        self.message_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.message_label.grid(row=5, column=0, columnspan=4, pady=10, sticky="nsew")

        self.score_history_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.score_history_label.grid(row=6, column=0, columnspan=4, pady=10, sticky="nsew")

# Centered Buttons for actions arranged in a row
        self.start_button = tk.Button(self, text="ప్రారంభించు", command=self.start_game, font=("Times New Roman", 12))
        self.start_button.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

        self.listen_button = tk.Button(self, text="శ్రవణం", command=self.listen_and_recognize, font=("Times New Roman", 12), state=tk.DISABLED)
        self.listen_button.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")

        self.auto_listen_button = tk.Button(self, text="ఆటో శ్రవణం", command=self.toggle_auto_listen, font=("Times New Roman", 12), state=tk.DISABLED)
        self.auto_listen_button.grid(row=7, column=2, padx=5, pady=5, sticky="nsew")

        self.next_button = tk.Button(self, text="తరువాత చిత్రం", command=self.next_item, font=("Times New Roman", 12), state=tk.DISABLED)
        self.next_button.grid(row=7, column=3, padx=5, pady=5, sticky="nsew")

# Centered Quit button
        self.quit_button = tk.Button(self, text="విడిచిపోండి", command=self.quit_game, font=("Times New Roman", 12))
        self.quit_button.grid(row=8, column=0, columnspan=4, pady=10, sticky="nsew")

# Configure grid row and column weights for centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
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
        score_history = "\n".join([f"ఆట {i + 1}: {score}" for i, score in enumerate(self.scores)])
        self.score_history_label.config(text=f"స్కోర్ చరిత్ర:\n{score_history}")

    def start_game(self):
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"పదవి: {self.level}")
        self.score_label.config(text=f"మొత్తం స్కోరు: {self.score}")
        self.message_label.config(text="ఆట ప్రారంభించబడింది! చిత్రాన్ని గుర్తించండి.")
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
        self.level_label.config(text=f"పదవి: {self.level}")
        self.score_label.config(text=f"మొత్తం స్కోరు: {self.score}")
        self.message_label.config(text="ఆట మళ్లీ ప్రారంభించబడింది. 'ప్రారంభించు' బటన్‌ను నొక్కండి.")
        self.listen_button.config(state=tk.DISABLED)
        self.auto_listen_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.display_score_history()

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
            self.message_label.config(text="శ్రవణం చేస్తోంది... చిత్రానికి పేరు చెప్పండి.")
            audio = recognizer.listen(source, timeout=10)

            try:
                # Recognize speech
                text = recognizer.recognize_google(audio, language='te-IN').lower()
                self.message_label.config(text=f"మీరు చెప్పినది: {text}")

                # Check the result
                if text == self.current_item:
                    self.score += 1
                    self.items_identified += 1
                    self.score_label.config(text=f"మొత్తం స్కోరు: {self.score}")
                    self.message_label.config(text="సరే! మీరు చిత్రాన్ని గుర్తించారు.")
                    if self.items_identified >= self.items_to_identify:
                        self.message_label.config(text="సమాధానం! మీరు స్థాయిని పూర్తి చేసారు.")
                        self.reset_game()
                else:
                    self.attempts += 1
                    if self.attempts >= 2:
                        self.message_label.config(text=f"మీరు ఓడారు! సరిగ్గా '{self.current_item}' అని చెప్పాల్సి ఉంది.")
                        self.reset_game()
                    else:
                        self.message_label.config(text=f"తప్పు. మీకు {2 - self.attempts} ప్రయత్నాలు మిగిలాయి.")
            except sr.UnknownValueError:
                self.message_label.config(text="క్షమించండి, నేను అర్థం చేసుకోలేకపోయాను.")
            except sr.RequestError as e:
                self.message_label.config(text=f"సేవను పొందలేకపోయాను; {e}")
            except sr.WaitTimeoutError:
                self.message_label.config(text="సమయం ముగిసింది!")

    def next_item(self):
        # Reset attempts and load a new item
        self.attempts = 0
        self.current_item = self.get_random_item()
        self.display_image(self.current_item)
        self.item_name_label.config(text=f"చిత్రం పేరు: {self.current_item}")

    def toggle_auto_listen(self):
        if self.auto_listening:
            self.auto_listening = False
            self.auto_listen_button.config(text="ఆటో శ్రవణం")
            self.message_label.config(text="ఆటో శ్రవణం ఆపబడింది.")
        else:
            self.auto_listening = True
            self.auto_listen_button.config(text="ఆటో వినండి")
            self.message_label.config(text="ఆటో శ్రవణం ప్రారంభించబడింది.")
            self.auto_listen()

    def auto_listen(self):
        if self.auto_listening:
            self.listen_and_recognize()
            self.after(10000, self.auto_listen)  # Listen every 10 seconds

    def quit_game(self):
        self.destroy()

if __name__ == "__main__":
    app = VoiceRecognitionGame()
    app.mainloop()
