"""
Configuration settings for Jarvis AI Assistant.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Assistant settings
ASSISTANT_NAME = "Jarvis"
WAKE_WORD = "jarvis"
VOICE_RATE = 145  # Speech rate for text-to-speech
VOICE_MALE = True  # Use male voice if True

# API Keys (set these in .env file or configure here)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WOLFRAM_API_KEY = os.getenv("WOLFRAM_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# Common Windows Applications (example paths - adjust as needed)
DEFAULT_APPLICATIONS = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "explorer": "explorer.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "settings": "ms-settings:",
}

# Web Search settings
DEFAULT_SEARCH_ENGINE = "google"  # Options: google, bing, duckduckgo
SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q=",
    "bing": "https://www.bing.com/search?q=",
    "duckduckgo": "https://duckduckgo.com/?q=",
}

# Responses
GREETING_RESPONSES = [
    "Hello sir, how may I assist you today?",
    "At your service, sir.",
    "How can I help you?",
    "Jarvis online. What can I do for you?",
]

FAREWELL_RESPONSES = [
    "Goodbye, sir.",
    "Shutting down.",
    "Until next time, sir.",
    "Jarvis going offline.",
]

# Debug mode
DEBUG = False
