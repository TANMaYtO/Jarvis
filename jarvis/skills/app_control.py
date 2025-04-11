"""
App control functionality for Jarvis.
"""

from ..utils.system import SystemOperations

class AppController:
    def __init__(self):
        self.system = SystemOperations()
    
    def open_app(self, app_name):
        """Open an application by name."""
        if not app_name:
            return False, "No application name provided"
        
        # Clean up the app name
        app_name = app_name.strip().lower()
        
        # Remove common phrases
        phrases_to_remove = ["the", "application", "app", "program", "for me", "please"]
        for phrase in phrases_to_remove:
            app_name = app_name.replace(phrase, "").strip()
        
        # Try to open the app
        success, message = self.system.open_application(app_name)
        return success, message
    
    def register_app(self, app_name, app_path):
        """Register a new application path."""
        if not app_name or not app_path:
            return False, "Both application name and path are required"
        
        # Save the custom app path
        success = self.system.save_custom_app_path(app_name.lower(), app_path)
        
        if success:
            return True, f"Successfully registered {app_name}"
        else:
            return False, f"Failed to register {app_name}"
