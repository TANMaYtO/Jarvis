"""
Jarvis AI Assistant - Main Entry Point
"""

import os
import sys
import time
import random
import datetime
from pathlib import Path

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import Jarvis modules
from jarvis.utils.speech import Speech
from jarvis.utils.nlp import CommandProcessor
from jarvis.utils.system import SystemOperations
from jarvis.skills.app_control import AppController
from jarvis.skills.web_search import WebSearchSkill
from jarvis.config import ASSISTANT_NAME, DEBUG

class Jarvis:
    def __init__(self):
        print(f"Initializing {ASSISTANT_NAME}...")
        
        # Initialize components
        self.speech = Speech()
        self.nlp = CommandProcessor()
        self.system = SystemOperations()
        self.app_controller = AppController()
        self.web_search = WebSearchSkill()
        
        # Set running flag
        self.running = True
        
        print(f"{ASSISTANT_NAME} initialized and ready.")
    
    def handle_command(self, command_text):
        """Process and execute a command."""
        # Process the command
        action, params = self.nlp.process_command(command_text)
        
        # Debug output
        if DEBUG:
            print(f"Action: {action}")
            print(f"Params: {params}")
        
        # Execute the appropriate action
        if action == "open_app":
            app_name = params.get("app_name", "")
            success, response = self.app_controller.open_app(app_name)
        
        elif action == "web_search":
            query = params.get("query", "")
            engine = params.get("engine", None)
            success, response = self.web_search.search(query, engine)
        
        elif action == "get_info":
            query = params.get("query", "")
            success, response = self.web_search.get_info(query)
        
        elif action == "play_youtube":
            video = params.get("video", "")
            success, response = self.web_search.play_youtube(video)
        
        elif action == "open_website":
            url = params.get("url", "")
            success, response = self.web_search.open_website(url)
        
        elif action == "get_weather":
            city = params.get("city", "")
            success, response = self.web_search.get_weather(city)
        
        elif action == "get_news":
            category = params.get("category", "general")
            success, response = self.web_search.get_news(category)
        
        elif action == "get_time":
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            success, response = True, f"The current time is {time_str}."
        
        elif action == "get_date":
            now = datetime.datetime.now()
            date_str = now.strftime("%A, %B %d, %Y")
            success, response = True, f"Today is {date_str}."
        
        elif action == "get_system_info":
            info = self.system.get_system_info()
            response = f"System: {info['system']} {info['release']}, Version: {info['version']}, Machine: {info['machine']}"
            success = True
        
        elif action == "shutdown":
            delay = params.get("delay", "0")
            try:
                delay = int(delay)
            except:
                delay = 0
            success, response = self.system.shutdown_computer(delay)
        
        elif action == "restart":
            delay = params.get("delay", "0")
            try:
                delay = int(delay)
            except:
                delay = 0
            success, response = self.system.restart_computer(delay)
        
        elif action == "cancel_shutdown":
            success, response = self.system.cancel_shutdown()
        
        elif action == "exit":
            success, response = True, "Goodbye!"
            self.running = False
        
        elif action == "greet":
            self.speech.greet()
            return
        
        elif action == "thanks":
            response = self.nlp.get_response("thanks", "You're welcome!")
            if isinstance(response, list):
                response = random.choice(response)
            success = True
        
        elif action == "ask_question":
            query = params.get("query", "")
            success, response = self.web_search.ask_question(query)
        
        elif action == "unknown_command":
            response = self.nlp.get_response("unknown_command", "I'm sorry, I didn't understand that command.")
            if isinstance(response, list):
                response = random.choice(response)
            success = False
        
        else:
            response = "I'm not sure how to help with that."
            success = False
        
        # Provide a response
        if success:
            # Use success response if available
            success_responses = self.nlp.get_response("success")
            if not response.strip() and success_responses:
                if isinstance(success_responses, list):
                    response = random.choice(success_responses)
                else:
                    response = success_responses
        else:
            # Use error response if available and no specific error message
            if not response.strip():
                error_responses = self.nlp.get_response("error")
                if error_responses:
                    if isinstance(error_responses, list):
                        response = random.choice(error_responses)
                    else:
                        response = error_responses
        
        # Speak the response
        if response.strip():
            self.speech.speak(response)
    
    def run(self):
        """Run the main Jarvis loop."""
        self.speech.greet()
        
        while self.running:
            try:
                # Listen for commands
                command_text = self.speech.listen()
                
                # Check if we heard anything
                if not command_text:
                    continue
                
                # Check for wake word if not in continuous mode
                if not self.nlp.is_wake_word(command_text):
                    continue
                
                # Process and execute the command
                self.handle_command(command_text)
                
            except KeyboardInterrupt:
                self.running = False
                print("\nShutting down...")
            except Exception as e:
                print(f"Error: {e}")
                if DEBUG:
                    import traceback
                    traceback.print_exc()
        
        # Say goodbye
        self.speech.farewell()

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
