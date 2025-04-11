"""
System operations for Jarvis, including application launching and file operations.
"""

import os
import subprocess
import json
import time
from pathlib import Path
import sys
from ..config import DEFAULT_APPLICATIONS

class SystemOperations:
    def __init__(self):
        self.app_paths = DEFAULT_APPLICATIONS.copy()
        self.load_custom_app_paths()
    
    def load_custom_app_paths(self):
        """Load custom application paths from app_paths.json if it exists."""
        try:
            app_paths_file = Path(__file__).parent.parent / 'data' / 'app_paths.json'
            if app_paths_file.exists():
                with open(app_paths_file, 'r') as f:
                    custom_paths = json.load(f)
                    self.app_paths.update(custom_paths)
        except Exception as e:
            print(f"Error loading custom app paths: {e}")
    
    def save_custom_app_path(self, app_name, app_path):
        """Save a custom application path to app_paths.json."""
        try:
            app_paths_file = Path(__file__).parent.parent / 'data' / 'app_paths.json'
            
            # If file exists, load existing data
            custom_paths = {}
            if app_paths_file.exists():
                with open(app_paths_file, 'r') as f:
                    custom_paths = json.load(f)
            
            # Update with new path and save
            custom_paths[app_name.lower()] = app_path
            
            with open(app_paths_file, 'w') as f:
                json.dump(custom_paths, f, indent=4)
            
            # Update current paths
            self.app_paths[app_name.lower()] = app_path
            return True
        except Exception as e:
            print(f"Error saving custom app path: {e}")
            return False
    
    def open_application(self, app_name):
        """Open an application by name."""
        app_name = app_name.lower()
        
        # Check if app is in our known applications
        if app_name in self.app_paths:
            try:
                subprocess.Popen(self.app_paths[app_name])
                return True, f"Opening {app_name}"
            except Exception as e:
                return False, f"Error opening {app_name}: {e}"
        else:
            # Try to open using just the app name (if it's in PATH)
            try:
                subprocess.Popen(app_name)
                return True, f"Opening {app_name}"
            except:
                return False, f"Could not find application: {app_name}"
    
    def open_website(self, url):
        """Open a website in the default browser."""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            import webbrowser
            webbrowser.open(url)
            return True, f"Opening {url}"
        except Exception as e:
            return False, f"Error opening website: {e}"
    
    def get_system_info(self):
        """Get basic system information."""
        import platform
        
        info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        
        return info
    
    def shutdown_computer(self, delay=0):
        """Shutdown the computer (Windows only)."""
        os_name = os.name
        
        if os_name == 'nt':  # Windows
            try:
                if delay > 0:
                    subprocess.Popen(f'shutdown /s /t {delay}', shell=True)
                    return True, f"Shutting down computer in {delay} seconds"
                else:
                    subprocess.Popen('shutdown /s /t 0', shell=True)
                    return True, "Shutting down computer now"
            except Exception as e:
                return False, f"Error shutting down: {e}"
        else:
            return False, "Shutdown functionality is only available on Windows"
    
    def restart_computer(self, delay=0):
        """Restart the computer (Windows only)."""
        os_name = os.name
        
        if os_name == 'nt':  # Windows
            try:
                if delay > 0:
                    subprocess.Popen(f'shutdown /r /t {delay}', shell=True)
                    return True, f"Restarting computer in {delay} seconds"
                else:
                    subprocess.Popen('shutdown /r /t 0', shell=True)
                    return True, "Restarting computer now"
            except Exception as e:
                return False, f"Error restarting: {e}"
        else:
            return False, "Restart functionality is only available on Windows"
    
    def cancel_shutdown(self):
        """Cancel a scheduled shutdown (Windows only)."""
        os_name = os.name
        
        if os_name == 'nt':  # Windows
            try:
                subprocess.Popen('shutdown /a', shell=True)
                return True, "Shutdown cancelled"
            except Exception as e:
                return False, f"Error cancelling shutdown: {e}"
        else:
            return False, "Cancel shutdown functionality is only available on Windows"
