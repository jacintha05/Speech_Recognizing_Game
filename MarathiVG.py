import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import speech_recognition as sr

# Updated list of items (images and names) for identification in Marathi
items = {
    "सफरचंद": "apple.png",
    "केळी": "banana.png",
    "संत्रा": "orange.png",
    "द्राक्षे": "grape.png",
    "गाजर": "carrot.png",
    "टमाटर": "tomato.png",
    "स्ट्रॉबेरी": "strawberry.png",
    "तरबूज": "watermelon.png",
    "अननस": "pineapple.png",
    "ब्रोकोली": "broccoli.png",
    "किवी": "kiwi.png",
    "आंबा": "mango.png",
    "पीच": "peach.png",
    "नाशपाती": "pear.png",
    "अळू": "plum.png",
    "रास्पबेरी": "raspberry.png",
    "ब्लूबेरी": "blueberry.png",
    "चेर्री": "cherry.png",
    "मेलन": "melon.png",
    "डाळिंब": "pomegranate.png"
}

# Shuffle the item list for each game session
item_keys = list(items.keys())
random.shuffle(item_keys)

# Initialize the recognizer
recognizer = sr.Recognizer()

class VoiceRecognitionGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("वॉईस रेकग्निशन गेम")
        self.geometry("600x600")

        # Create a canvas to hold the image and text
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

        # Labels for displaying information with Times New Roman font
        self.instruction_label = tk.Label(self, text="चित्रात दर्शविलेले वस्तू ओळखा", font=("Times New Roman", 14))
        self.instruction_label.grid(row=1, column=0, columnspan=4, pady=10, sticky="nsew")

        self.score_label = tk.Label(self, text="एकूण स्कोअर: 0", font=("Times New Roman", 14))
        self.score_label.grid(row=2, column=0, columnspan=4, pady=5, sticky="nsew")

        self.level_label = tk.Label(self, text="स्तर: 1", font=("Times New Roman", 14))
        self.level_label.grid(row=3, column=0, columnspan=4, pady=5, sticky="nsew")

        self.item_name_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.item_name_label.grid(row=4, column=0, columnspan=4, pady=5, sticky="nsew")

        self.message_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.message_label.grid(row=5, column=0, columnspan=4, pady=10, sticky="nsew")

        self.score_history_label = tk.Label(self, text="", font=("Times New Roman", 12))
        self.score_history_label.grid(row=6, column=0, columnspan=4, pady=10, sticky="nsew")

        # Buttons for actions arranged in a row
        self.start_button = tk.Button(self, text="सुरू करा", command=self.start_game, font=("Times New Roman", 12))
        self.start_button.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

        self.listen_button = tk.Button(self, text="ऐका", command=self.listen_and_recognize, font=("Times New Roman", 12), state=tk.DISABLED)
        self.listen_button.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")

        self.auto_listen_button = tk.Button(self, text="ऑटो ऐका", command=self.toggle_auto_listen, font=("Times New Roman", 12), state=tk.DISABLED)
        self.auto_listen_button.grid(row=7, column=2, padx=5, pady=5, sticky="nsew")

        self.next_button = tk.Button(self, text="पुढील वस्तू", command=self.next_item, font=("Times New Roman", 12), state=tk.DISABLED)
        self.next_button.grid(row=7, column=3, padx=5, pady=5, sticky="nsew")

        # Quit button
        self.quit_button = tk.Button(self, text="बाहेर पडणे", command=self.quit_game, font=("Times New Roman", 12))
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
        score_history = "\n".join([f"खेळ {i + 1}: {score}" for i, score in enumerate(self.scores)])
        self.score_history_label.config(text=f"स्कोअर इतिहास:\n{score_history}")

    def start_game(self):
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"स्तर: {self.level}")
        self.score_label.config(text=f"एकूण स्कोअर: {self.score}")
        self.message_label.config(text="गेम सुरू झाला आहे! वस्तू ओळखा.")
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
        self.level_label.config(text=f"स्तर: {self.level}")
        self.score_label.config(text=f"एकूण स्कोअर: {self.score}")
        self.message_label.config(text="गेम पुन्हा सुरू झाला आहे. 'सुरू करा' बटणावर क्लिक करा.")
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
            self.message_label.config(text="ऐकणारे... कृपया वस्तूचे नाव सांगा.")
            audio = recognizer.listen(source, timeout=10)

            try:
                # Recognize speech
                text = recognizer.recognize_google(audio, language='mr-IN').lower()
                self.message_label.config(text=f"तुम्ही म्हटले: {text}")

                # Check the result
                if text == self.current_item:
                    self.score += 1
                    self.items_identified += 1
                    self.score_label.config(text=f"एकूण स्कोअर: {self.score}")
                    self.message_label.config(text="सही! तुम्ही वस्तू ओळखली आहे.")
                    if self.items_identified >= self.items_to_identify:
                        self.message_label.config(text="अभिनंदन! तुम्ही स्तर पूर्ण केले आहे.")
                        self.reset_game()
                    else:
                        # Automatically proceed to the next item
                        self.after(2000, self.next_item)  # 2 seconds delay before next item
                else:
                    self.attempts += 1
                    if self.attempts >= 2:
                        self.message_label.config(text=f"तुम्ही हरलात! योग्य उत्तर '{self.current_item}' होते.")
                        self.reset_game()
                    else:
                        self.message_label.config(text=f"चूक. तुम्हाला {2 - self.attempts} प्रयत्न बाकी आहेत.")
            except sr.UnknownValueError:
                self.message_label.config(text="क्षमस्व, मी ते समजू शकत नाही.")
            except sr.RequestError as e:
                self.message_label.config(text=f"परिणामांची विनंती करता येईना; {e}")
            except sr.WaitTimeoutError:
                self.message_label.config(text="वेळ संपली!")

    def next_item(self):
        # Reset attempts and load a new item
        self.attempts = 0
        self.current_item = self.get_random_item()
        self.display_image(self.current_item)
        self.item_name_label.config(text=f"वस्तू: {self.current_item}")

    def toggle_auto_listen(self):
        if self.auto_listening:
            self.auto_listening = False
            self.auto_listen_button.config(text="ऑटो ऐका")
            self.message_label.config(text="ऑटो ऐकणे बंद करण्यात आले.")
        else:
            self.auto_listening = True
            self.auto_listen_button.config(text="ऑटो ऐकणे थांबवा")
            self.message_label.config(text="ऑटो ऐकणे सुरू झाले.")
            self.auto_listen()

    def auto_listen(self):
        if self.auto_listening:
            self.listen_and_recognize()
            self.after(10000, self.auto_listen)  # Listen every 10 seconds
            self.after(20000, self.next_item)  # Move to next item every 20 seconds

    def quit_game(self):
        self.destroy()

if __name__ == "__main__":
    app = VoiceRecognitionGame()
    app.mainloop()
