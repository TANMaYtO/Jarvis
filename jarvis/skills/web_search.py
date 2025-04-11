"""
Web search functionality for Jarvis.
"""

from ..utils.web import WebTools
import random

class WebSearchSkill:
    def __init__(self):
        self.web_tools = WebTools()
    
    def search(self, query, engine=None):
        """Search the web for the given query."""
        if not query:
            return False, "No search query provided"
        
        return self.web_tools.search(query, engine)
    
    def get_info(self, query, sentences=3):
        """Get information about a topic from Wikipedia."""
        if not query:
            return False, "No query provided"
        
        # Try to get information from Wikipedia
        success, result = self.web_tools.get_wikipedia_info(query, sentences)
        
        if success:
            # Format the response
            response = f"{result['title']}: {result['summary']}"
            return True, response
        else:
            # If Wikipedia fails, try a web search instead
            return self.search(query)
    
    def play_youtube(self, video):
        """Play a video on YouTube."""
        if not video:
            return False, "No video title provided"
        
        return self.web_tools.play_youtube(video)
    
    def open_website(self, url):
        """Open a website in the default browser."""
        if not url:
            return False, "No URL provided"
        
        from ..utils.system import SystemOperations
        system = SystemOperations()
        return system.open_website(url)
    
    def get_weather(self, city):
        """Get weather information for a city."""
        if not city:
            return False, "No city name provided"
        
        success, result = self.web_tools.get_weather(city)
        
        if success:
            # Format the response
            response = (
                f"The current weather in {result['city']}, {result['country']} is "
                f"{result['description']} with a temperature of {result['temperature']}°C, "
                f"feels like {result['feels_like']}°C. "
                f"Humidity is {result['humidity']}% and wind speed is {result['wind_speed']} m/s."
            )
            return True, response
        else:
            return False, result
    
    def get_news(self, category="general", country="us", count=5):
        """Get the latest news headlines."""
        success, result = self.web_tools.get_news(category, country, count)
        
        if success:
            # Format the response
            response = "Here are the latest headlines:\n\n"
            for i, article in enumerate(result, 1):
                response += f"{i}. {article['title']} - {article['source']}\n"
            
            return True, response
        else:
            return False, result
    
    def ask_question(self, query):
        """Ask a general knowledge question."""
        if not query:
            return False, "No question provided"
        
        # Try Wolfram Alpha first for factual questions
        success, result = self.web_tools.ask_wolfram(query)
        
        if success:
            return True, result
        else:
            # If Wolfram Alpha fails, try Wikipedia
            return self.get_info(query)
