"""
Speech recognition and text-to-speech functionality for Jarvis.
"""

import speech_recognition as sr
import pyttsx3
import random
import time
from ..config import VOICE_RATE, VOICE_MALE, GREETING_RESPONSES, FAREWELL_RESPONSES

class Speech:
    def __init__(self):
        # Initialize the speech recognition engine
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', VOICE_RATE)
        
        # Set voice
        voices = self.engine.getProperty('voices')
        voice_id = voices[0].id if VOICE_MALE else voices[1].id
        self.engine.setProperty('voice', voice_id)
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen(self, timeout=5, phrase_time_limit=5):
        """Listen for voice input and convert to text."""
        text = ""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period.")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error in speech recognition: {e}")
        
        return text.lower() if text else ""
    
    def speak(self, text):
        """Convert text to speech."""
        if not text:
            return
        
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def greet(self):
        """Greet the user with a random greeting."""
        greeting = random.choice(GREETING_RESPONSES)
        self.speak(greeting)
    
    def farewell(self):
        """Say goodbye to the user with a random farewell."""
        farewell = random.choice(FAREWELL_RESPONSES)
        self.speak(farewell)
