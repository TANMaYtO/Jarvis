"""
Web functionality for Jarvis, including search and information retrieval.
"""

import requests
import webbrowser
import urllib.parse
import json
import wikipedia
import pywhatkit
from bs4 import BeautifulSoup
from ..config import SEARCH_ENGINES, DEFAULT_SEARCH_ENGINE, WEATHER_API_KEY, WOLFRAM_API_KEY, NEWS_API_KEY

class WebTools:
    def __init__(self):
        self.search_engines = SEARCH_ENGINES
        self.default_engine = DEFAULT_SEARCH_ENGINE
    
    def search(self, query, engine=None):
        """Search the web using the specified search engine and open in browser."""
        if not engine:
            engine = self.default_engine
        
        if engine not in self.search_engines:
            return False, f"Search engine '{engine}' not found"
        
        try:
            search_url = self.search_engines[engine] + urllib.parse.quote_plus(query)
            webbrowser.open(search_url)
            return True, f"Searching for '{query}' using {engine}"
        except Exception as e:
            return False, f"Error searching the web: {e}"
    
    def get_wikipedia_info(self, query, sentences=2):
        """Get a summary from Wikipedia."""
        try:
            # Set language to English
            wikipedia.set_lang("en")
            
            # Search for the query
            results = wikipedia.search(query)
            if not results:
                return False, f"No Wikipedia results found for '{query}'"
            
            # Get summary of the first result
            page = wikipedia.page(results[0])
            summary = wikipedia.summary(results[0], sentences=sentences)
            url = page.url
            
            return True, {
                "title": page.title,
                "summary": summary,
                "url": url
            }
        except wikipedia.exceptions.DisambiguationError as e:
            # If we get a disambiguation page, pick the first option
            try:
                page = wikipedia.page(e.options[0])
                summary = wikipedia.summary(e.options[0], sentences=sentences)
                url = page.url
                
                return True, {
                    "title": page.title,
                    "summary": summary,
                    "url": url,
                    "note": "Disambiguation: multiple options found"
                }
            except:
                return False, f"Disambiguation error for '{query}'"
        except wikipedia.exceptions.PageError:
            return False, f"No Wikipedia page found for '{query}'"
        except Exception as e:
            return False, f"Error retrieving Wikipedia information: {e}"
    
    def play_youtube(self, query):
        """Play a YouTube video based on the query."""
        try:
            pywhatkit.playonyt(query)
            return True, f"Playing '{query}' on YouTube"
        except Exception as e:
            return False, f"Error playing YouTube video: {e}"
    
    def get_weather(self, city):
        """Get weather information for a city."""
        if not WEATHER_API_KEY:
            return False, "Weather API key not configured"
        
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": WEATHER_API_KEY,
                "units": "metric"  # For Celsius
            }
            
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                weather = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "condition": data["weather"][0]["main"]
                }
                return True, weather
            else:
                return False, f"Error: {data['message']}"
        except Exception as e:
            return False, f"Error retrieving weather information: {e}"
    
    def get_news(self, category="general", country="us", count=5):
        """Get latest news headlines."""
        if not NEWS_API_KEY:
            return False, "News API key not configured"
        
        try:
            base_url = "https://newsapi.org/v2/top-headlines"
            params = {
                "category": category,
                "country": country,
                "apiKey": NEWS_API_KEY,
                "pageSize": count
            }
            
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200 and data["status"] == "ok":
                articles = []
                for article in data["articles"]:
                    articles.append({
                        "title": article["title"],
                        "source": article["source"]["name"],
                        "description": article["description"],
                        "url": article["url"]
                    })
                return True, articles
            else:
                return False, f"Error: {data.get('message', 'Unknown error')}"
        except Exception as e:
            return False, f"Error retrieving news: {e}"
    
    def ask_wolfram(self, query):
        """Ask Wolfram Alpha a question."""
        if not WOLFRAM_API_KEY:
            return False, "Wolfram Alpha API key not configured"
        
        try:
            base_url = "http://api.wolframalpha.com/v1/result"
            params = {
                "appid": WOLFRAM_API_KEY,
                "i": query,
                "units": "metric"
            }
            
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                return True, response.text
            else:
                return False, "I don't know how to answer that"
        except Exception as e:
            return False, f"Error asking Wolfram Alpha: {e}"
