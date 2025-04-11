"""
Natural Language Processing functionality for Jarvis.
"""

import re
import json
import os
from pathlib import Path
from ..config import WAKE_WORD

class CommandProcessor:
    def __init__(self):
        # Command patterns with their corresponding actions
        self.command_patterns = {
            # App control commands
            r"open\s+(?P<app_name>[\w\s]+)": {"action": "open_app", "params": ["app_name"]},
            r"launch\s+(?P<app_name>[\w\s]+)": {"action": "open_app", "params": ["app_name"]},
            r"start\s+(?P<app_name>[\w\s]+)": {"action": "open_app", "params": ["app_name"]},
            r"run\s+(?P<app_name>[\w\s]+)": {"action": "open_app", "params": ["app_name"]},
            
            # Web commands
            r"search\s+(for\s+)?(?P<query>.+)": {"action": "web_search", "params": ["query"]},
            r"google\s+(?P<query>.+)": {"action": "web_search", "params": ["query"]},
            r"bing\s+(?P<query>.+)": {"action": "web_search", "params": ["query"], "engine": "bing"},
            r"(open|go\s+to|navigate\s+to)\s+(the\s+)?(website\s+)?(?P<url>[\w\.]+\.\w+)": {"action": "open_website", "params": ["url"]},
            r"(tell me about|what is|who is|search for)\s+(?P<query>.+)": {"action": "get_info", "params": ["query"]},
            r"play\s+(?P<video>.+)\s+on\s+youtube": {"action": "play_youtube", "params": ["video"]},
            r"youtube\s+(?P<video>.+)": {"action": "play_youtube", "params": ["video"]},
            
            # Weather commands
            r"(what('s| is) the )?weather( like)? (in|at|for) (?P<city>[\w\s]+)": {"action": "get_weather", "params": ["city"]},
            r"(how('s| is) the )?weather( like)? (in|at|for) (?P<city>[\w\s]+)": {"action": "get_weather", "params": ["city"]},
            r"(what('s| is) the )?temperature (in|at|for) (?P<city>[\w\s]+)": {"action": "get_weather", "params": ["city"]},
            
            # System commands
            r"(what('s| is) the )?time": {"action": "get_time", "params": []},
            r"(what('s| is) the )?date": {"action": "get_date", "params": []},
            r"(what('s| is) (my )?(system|computer) (info|information)": {"action": "get_system_info", "params": []},
            r"shutdown( computer| system)?( in (?P<delay>\d+)( seconds)?)?": {"action": "shutdown", "params": ["delay"]},
            r"restart( computer| system)?( in (?P<delay>\d+)( seconds)?)?": {"action": "restart", "params": ["delay"]},
            r"cancel shutdown": {"action": "cancel_shutdown", "params": []},

            # News commands
            r"(what('s| is) the )?news": {"action": "get_news", "params": []},
            r"(what('s| is) the )?(latest|recent) news": {"action": "get_news", "params": []},
            r"(what('s| is) the )?news (on|about|for) (?P<category>\w+)": {"action": "get_news", "params": ["category"]},
            
            # Control commands
            r"(goodbye|bye|exit|quit|stop)": {"action": "exit", "params": []},
            r"(shut( )?down|turn off)": {"action": "exit", "params": []},
            r"(hello|hi|hey|greetings)": {"action": "greet", "params": []},
            r"(thank you|thanks)": {"action": "thanks", "params": []},
            
            # General questions
            r"(what is|calculate|compute|what('s| is) the value of) (?P<query>.+)": {"action": "ask_question", "params": ["query"]},
            r"(who is|who was) (?P<query>.+)": {"action": "ask_question", "params": ["query"]},
            r"(how (to|do I)) (?P<query>.+)": {"action": "ask_question", "params": ["query"]},
            r"(where is|locate) (?P<query>.+)": {"action": "ask_question", "params": ["query"]},
        }
        
        # Load custom responses
        self.responses = self.load_responses()
    
    def load_responses(self):
        """Load custom responses from responses.json if it exists."""
        responses = {}
        try:
            responses_file = Path(__file__).parent.parent / 'data' / 'responses.json'
            if responses_file.exists():
                with open(responses_file, 'r') as f:
                    responses = json.load(f)
        except Exception as e:
            print(f"Error loading custom responses: {e}")
        return responses
    
    def save_responses(self):
        """Save custom responses to responses.json."""
        try:
            responses_file = Path(__file__).parent.parent / 'data' / 'responses.json'
            with open(responses_file, 'w') as f:
                json.dump(self.responses, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving custom responses: {e}")
            return False
    
    def process_command(self, text):
        """
        Process the user's command text and return the appropriate action and parameters.
        Returns a tuple of (action, params) where params is a dictionary of parameter values.
        """
        # Remove the wake word if present
        text = re.sub(rf"^{WAKE_WORD}\s+", "", text, flags=re.IGNORECASE)
        text = text.strip().lower()
        
        # Check each command pattern
        for pattern, command_info in self.command_patterns.items():
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                # Extract parameters
                params = {}
                for param in command_info.get("params", []):
                    if param in match.groupdict():
                        params[param] = match.group(param).strip()
                
                # Add any fixed parameters from the command definition
                for key, value in command_info.items():
                    if key not in ["action", "params"]:
                        params[key] = value
                
                return command_info["action"], params
        
        # If no match, return a generic action
        return "unknown_command", {"text": text}
    
    def is_wake_word(self, text):
        """Check if the wake word is at the beginning of the text."""
        return bool(re.match(rf"^{WAKE_WORD}\b", text, re.IGNORECASE))
    
    def get_response(self, key, default=None):
        """Get a response for a specific key."""
        return self.responses.get(key, default)
