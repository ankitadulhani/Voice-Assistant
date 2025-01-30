import speech_recognition as sr
import webbrowser
import cv2
import os
import subprocess
import platform
import datetime
import pyttsx3

class VoiceAssistant:
    def __init__(self):
        # Initialize the speech recognizer and text-to-speech engine
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice input and convert to text"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
            
        try:
            print("Recognizing...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError:
            self.speak("Sorry, there was an error with the speech recognition service")
            return None

    def open_youtube(self, query=None):
        """Open YouTube, optionally with a search query"""
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        else:
            url = "https://www.youtube.com"
        webbrowser.open(url)
        self.speak("Opening YouTube")

    def open_camera(self):
        """Open the system camera"""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.speak("Unable to access camera")
                return

            self.speak("Opening camera. Press 'q' to quit.")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                cv2.imshow('Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            cap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            self.speak(f"An error occurred while accessing the camera: {str(e)}")

    def open_calculator(self):
        """Open the system calculator"""
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.Popen("calc.exe")
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "Calculator"])
            elif system == "Linux":
                subprocess.Popen("gnome-calculator")
            self.speak("Opening calculator")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open the calculator: {str(e)}")

    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")

    def process_command(self, command):
        """Process the voice command"""
        if not command:
            return

        if "youtube" in command:
            # Check if there's a search query
            if "search for" in command:
                query = command.split("search for")[-1].strip()
                self.open_youtube(query)
            else:
                self.open_youtube()
                
        elif "camera" in command:
            self.open_camera()
            
        elif "calculator" in command:
            self.open_calculator()
            
        elif "time" in command:
            self.get_time()
            
        elif "exit" in command or "quit" in command or "stop" in command:
            self.speak("Goodbye!")
            return False
            
        else:
            self.speak("Sorry, I don't understand that command")
            
        return True

    def run(self):
        """Main loop for the voice assistant"""
        self.speak("Hello! I'm your voice assistant. How can I help you?")
        
        while True:
            command = self.listen()
            if not self.process_command(command):
                break

def main():
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
    