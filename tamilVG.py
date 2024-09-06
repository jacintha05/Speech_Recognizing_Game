import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import speech_recognition as sr

# Updated list of items (images and names) for identification
items = {
    "ஆப்பிள்": "apple.png",
    "வாழைப்பழம்": "banana.png",
    "ஆரஞ்சு": "orange.png",
    "திராட்சை": "grape.png",
    "காரட்": "carrot.png",
    "தக்காளி": "tomato.png",
    "ஸ்ட்ராபெர்ரி": "strawberry.png",
    "தர்பூசணி": "watermelon.png",
    "அன்னாசி": "pineapple.png",
    "பிரொக்கோலி": "broccoli.png",
    "கிவி": "kiwi.png",
    "மாங்காய்": "mango.png",
    "பீச்": "peach.png",
    "நாசிக்காய்": "pear.png",
    "சேரி": "plum.png",
    "ராஸ்பெர்ரி": "raspberry.png",
    "நீலம் பழம்": "blueberry.png",
    "செர்ரி": "cherry.png",
    "மரக்காய்": "melon.png",
    "மாதுளை": "pomegranate.png"
}

# Shuffle the item list for each game session
item_keys = list(items.keys())
random.shuffle(item_keys)

# Initialize the recognizer
recognizer = sr.Recognizer()

class VoiceRecognitionGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("சத்தம் ஒளிரும் விளையாட்டு")
        self.geometry("800x800")

        # Create a canvas to hold the image and text
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

        # Labels for displaying information with Times New Roman font
        self.instruction_label = tk.Label(self, text="படத்தை அடையாளம் காண்க", font=("Times New Roman", 14))
        self.instruction_label.grid(row=1, column=0, columnspan=4, pady=10, sticky="nsew")

        self.score_label = tk.Label(self, text="மொத்த புள்ளி: 0", font=("Times New Roman", 14))
        self.score_label.grid(row=2, column=0, columnspan=4, pady=5, sticky="nsew")

        self.level_label = tk.Label(self, text="நிலை: 1", font=("Times New Roman", 14))
        self.level_label.grid(row=3, column=0, columnspan=4, pady=5, sticky="nsew")

        self.item_name_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.item_name_label.grid(row=4, column=0, columnspan=4, pady=5, sticky="nsew")

        self.message_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.message_label.grid(row=5, column=0, columnspan=4, pady=10, sticky="nsew")

        self.score_history_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.score_history_label.grid(row=6, column=0, columnspan=4, pady=10, sticky="nsew")

        # Buttons for actions arranged in a row
        self.start_button = tk.Button(self, text="தொடங்கு", command=self.start_game, font=("Times New Roman", 12))
        self.start_button.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

        self.listen_button = tk.Button(self, text="கேள்", command=self.listen_and_recognize, font=("Times New Roman", 12), state=tk.DISABLED)
        self.listen_button.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")

        self.auto_listen_button = tk.Button(self, text="ஆட்டோ கேள்", command=self.toggle_auto_listen, font=("Times New Roman", 12), state=tk.DISABLED)
        self.auto_listen_button.grid(row=7, column=2, padx=5, pady=5, sticky="nsew")

        self.next_button = tk.Button(self, text="அடுத்த படம்", command=self.next_item, font=("Times New Roman", 12), state=tk.DISABLED)
        self.next_button.grid(row=7, column=3, padx=5, pady=5, sticky="nsew")

        # Quit button
        self.quit_button = tk.Button(self, text="விலக்கி", command=self.quit_game, font=("Times New Roman", 12))
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
        score_history = "\n".join([f"விளையாட்டு {i + 1}: {score}" for i, score in enumerate(self.scores)])
        self.score_history_label.config(text=f"அணிகை வரலாறு:\n{score_history}")

    def start_game(self):
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"நிலை: {self.level}")
        self.score_label.config(text=f"மொத்த புள்ளி: {self.score}")
        self.message_label.config(text="விளையாட்டு துவங்கியது! படத்தை கண்டுபிடிக்கவும்.")
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
        self.level_label.config(text=f"நிலை: {self.level}")
        self.score_label.config(text=f"மொத்த புள்ளி: {self.score}")
        self.message_label.config(text="விளையாட்டு மீண்டும் ஆரம்பிக்கப்பட்டது. 'தொடங்கு' பொத்தானை அழுத்தி விளையாடவும்.")
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
            self.message_label.config(text="கேட்கும் போது... உருப்படியின் பெயரை கூறவும்.")
            audio = recognizer.listen(source, timeout=10)

            try:
                # Recognize speech
                text = recognizer.recognize_google(audio, language='ta-IN').lower()
                self.message_label.config(text=f"நீங்கள் கூறியது: {text}")

                # Check the result
                if text == self.current_item:
                    self.score += 1
                    self.items_identified += 1
                    self.score_label.config(text=f"மொத்த புள்ளி: {self.score}")
                    self.message_label.config(text="சரி! நீங்கள் உருப்படியை அடையாளம் கண்டீர்கள்.")
                    if self.items_identified >= self.items_to_identify:
                        self.message_label.config(text="வாழ்த்துக்கள்! நீங்கள் நிலையை முடித்துவிட்டீர்கள்.")
                        self.reset_game()
                else:
                    self.attempts += 1
                    if self.attempts >= 2:
                        self.message_label.config(text=f"நீங்கள் தோல்வி அடைந்தீர்கள்! சரியான பதில் '{self.current_item}' என்பது.")
                        self.reset_game()
                    else:
                        self.message_label.config(text=f"தவறானது. உங்களுக்கு {2 - self.attempts} முயற்சிகள் மீதம் உள்ளது.")
            except sr.UnknownValueError:
                self.message_label.config(text="மன்னிக்கவும், நான் அதைப் புரிந்து கொள்ளவில்லை.")
            except sr.RequestError as e:
                self.message_label.config(text=f"தரவை கோர முடியவில்லை; {e}")
            except sr.WaitTimeoutError:
                self.message_label.config(text="நேரம் முடிந்து விட்டது!")

    def next_item(self):
        # Reset attempts and load a new item
        self.attempts = 0
        self.current_item = self.get_random_item()
        self.display_image(self.current_item)
        self.item_name_label.config(text=f"உருப்படியின் பெயர்: {self.current_item}")

    def toggle_auto_listen(self):
        if self.auto_listening:
            self.auto_listening = False
            self.auto_listen_button.config(text="ஆட்டோ கேள்")
            self.message_label.config(text="ஆட்டோ கேட்கும் செயலியை நிறுத்தியுள்ளீர்கள்.")
        else:
            self.auto_listening = True
            self.auto_listen_button.config(text="ஆட்டோ கேளுங்கள்")
            self.message_label.config(text="ஆட்டோ கேட்கும் செயலியை தொடங்கியுள்ளீர்கள்.")
            self.auto_listen()
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
            self.after(3000, self.auto_listen)
            
    def quit_game(self):
        self.destroy()

if __name__ == "__main__":
    app = VoiceRecognitionGame()
    app.mainloop()
