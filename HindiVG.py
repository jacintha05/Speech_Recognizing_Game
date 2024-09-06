import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import speech_recognition as sr

# Updated list of items (images and names) for identification in Hindi
items = {
    "सेब": "apple.png",
    "केला": "banana.png",
    "संतरा": "orange.png",
    "अंगूर": "grape.png",
    "गाजर": "carrot.png",
    "टमाटर": "tomato.png",
    "स्ट्रॉबेरी": "strawberry.png",
    "तरबूज": "watermelon.png",
    "अनानास": "pineapple.png",
    "ब्रोकली": "broccoli.png",
    "कीवी": "kiwi.png",
    "आम": "mango.png",
    "आड़ू": "peach.png",
    "नाशपाती": "pear.png",
    "आलूबुखारा": "plum.png",
    "रास्पबेरी": "raspberry.png",
    "ब्लूबेरी": "blueberry.png",
    "चेरी": "cherry.png",
    "मेलन": "melon.png",
    "अनार": "pomegranate.png"
}

# Shuffle the item list for each game session
item_keys = list(items.keys())
random.shuffle(item_keys)

# Initialize the recognizer
recognizer = sr.Recognizer()

class VoiceRecognitionGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("वॉइस रिकग्निशन गेम")
        self.geometry("600x600")

        # Create a canvas to hold the image and text
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

        # Labels for displaying information with Times New Roman font
        self.instruction_label = tk.Label(self, text="चित्र में दिखाए गए वस्तु की पहचान करें", font=("Times New Roman", 14))
        self.instruction_label.grid(row=1, column=0, columnspan=4, pady=10, sticky="nsew")

        self.score_label = tk.Label(self, text="कुल अंक: 0", font=("Times New Roman", 14))
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
        self.start_button = tk.Button(self, text="शुरू करें", command=self.start_game, font=("Times New Roman", 12))
        self.start_button.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

        self.listen_button = tk.Button(self, text="सुनें", command=self.listen_and_recognize, font=("Times New Roman", 12), state=tk.DISABLED)
        self.listen_button.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")

        self.auto_listen_button = tk.Button(self, text="ऑटो सुनें", command=self.toggle_auto_listen, font=("Times New Roman", 12), state=tk.DISABLED)
        self.auto_listen_button.grid(row=7, column=2, padx=5, pady=5, sticky="nsew")

        self.next_button = tk.Button(self, text="अगली वस्तु", command=self.next_item, font=("Times New Roman", 12), state=tk.DISABLED)
        self.next_button.grid(row=7, column=3, padx=5, pady=5, sticky="nsew")

        # Quit button
        self.quit_button = tk.Button(self, text="बाहर निकलें", command=self.quit_game, font=("Times New Roman", 12))
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
        score_history = "\n".join([f"गेम {i + 1}: {score}" for i, score in enumerate(self.scores)])
        self.score_history_label.config(text=f"संग्रहीत अंक:\n{score_history}")

    def start_game(self):
        self.score = 0
        self.items_identified = 0
        self.attempts = 0
        self.level = 1
        self.items_to_identify = 5
        self.level_label.config(text=f"स्तर: {self.level}")
        self.score_label.config(text=f"कुल अंक: {self.score}")
        self.message_label.config(text="खेल शुरू हो रहा है! वस्तु की पहचान करें.")
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
        self.score_label.config(text=f"कुल अंक: {self.score}")
        self.message_label.config(text="खेल फिर से शुरू हो रहा है। 'शुरू करें' बटन पर क्लिक करें।")
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
            self.message_label.config(text="सुन रहा हूँ... वस्तु का नाम बताएं.")
            audio = recognizer.listen(source, timeout=10)

            try:
                # Recognize speech
                text = recognizer.recognize_google(audio, language='hi-IN').lower()
                self.message_label.config(text=f"आपने कहा: {text}")

                # Check the result
                if text == self.current_item:
                    self.score += 1
                    self.items_identified += 1
                    self.score_label.config(text=f"कुल अंक: {self.score}")
                    self.message_label.config(text="सही है! आपने वस्तु की पहचान की है.")
                    if self.items_identified >= self.items_to_identify:
                        self.message_label.config(text="बधाई हो! आपने इस स्तर को पूरा कर लिया है।")
                        self.reset_game()
                    else:
                        # Automatically proceed to the next item
                        self.after(2000, self.next_item)  # 2 seconds delay before next item
                else:
                    self.attempts += 1
                    if self.attempts >= 2:
                        self.message_label.config(text=f"आप हार गए हैं! सही उत्तर '{self.current_item}' था।")
                        self.reset_game()
                    else:
                        self.message_label.config(text=f"गलत है। आपके पास {2 - self.attempts} प्रयास बाकी हैं।")
            except sr.UnknownValueError:
                self.message_label.config(text="माफ कीजिए, मैं समझ नहीं सका।")
            except sr.RequestError as e:
                self.message_label.config(text=f"परिणाम की अनुरोध नहीं किया जा सका; {e}")
            except sr.WaitTimeoutError:
                self.message_label.config(text="समय समाप्त हो गया!")

    def next_item(self):
        if self.auto_listening:
            self.after(10000, self.auto_listen)  # Listen every 10 seconds
        self.current_item = self.get_random_item()
        self.display_image(self.current_item)
        self.item_name_label.config(text=f"वस्तु: {self.current_item}")

    def toggle_auto_listen(self):
        if self.auto_listening:
            self.auto_listening = False
            self.auto_listen_button.config(text="ऑटो सुनें")
            self.message_label.config(text="ऑटो सुनना बंद कर दिया गया है।")
        else:
            self.auto_listening = True
            self.auto_listen_button.config(text="ऑटो सुनना बंद करें")
            self.message_label.config(text="ऑटो सुनना शुरू हो गया है।")
            self.auto_listen()

    def auto_listen(self):
        if self.auto_listening:
            self.listen_and_recognize()
            self.after(10000, self.auto_listen)  # Continue auto listening

    def quit_game(self):
        self.destroy()

if __name__ == "__main__":
    app = VoiceRecognitionGame()
    app.mainloop()
