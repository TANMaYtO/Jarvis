"""
Reminder functionality for Jarvis.
"""

import json
import os
import datetime
import threading
import time
from pathlib import Path

class ReminderSkill:
    def __init__(self, speech_callback=None):
        self.reminders_file = Path(__file__).parent.parent / 'data' / 'reminders.json'
        self.reminders = self.load_reminders()
        self.active_reminders = {}  # Dictionary to track active reminder threads
        self.speech_callback = speech_callback  # Callback function to speak reminders
    
    def load_reminders(self):
        """Load reminders from the reminders.json file."""
        reminders = []
        
        try:
            if self.reminders_file.exists():
                with open(self.reminders_file, 'r') as f:
                    reminders = json.load(f)
        except Exception as e:
            print(f"Error loading reminders: {e}")
        
        return reminders
    
    def save_reminders(self):
        """Save reminders to the reminders.json file."""
        try:
            os.makedirs(self.reminders_file.parent, exist_ok=True)
            
            with open(self.reminders_file, 'w') as f:
                json.dump(self.reminders, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving reminders: {e}")
            return False
    
    def set_speech_callback(self, callback):
        """Set the speech callback function."""
        self.speech_callback = callback
    
    def _reminder_alert(self, reminder_id, title):
        """Alert when a reminder is due."""
        # Remove from active reminders
        if reminder_id in self.active_reminders:
            del self.active_reminders[reminder_id]
        
        # Update reminder status
        for reminder in self.reminders:
            if reminder.get('id') == reminder_id:
                reminder['status'] = 'completed'
                self.save_reminders()
                break
        
        # Call the speech callback if available
        if self.speech_callback:
            message = f"Reminder: {title}"
            self.speech_callback(message)
        else:
            print(f"REMINDER: {title}")
    
    def add_reminder(self, title, time_str, date_str=None):
        """
        Add a reminder.
        
        Args:
            title (str): The title/content of the reminder
            time_str (str): The time for the reminder in format HH:MM or HH:MM AM/PM
            date_str (str, optional): The date for the reminder in format YYYY-MM-DD or MM/DD/YYYY.
                                      If not provided, the reminder is for today.
                                      
        Returns:
            tuple: (success, message)
        """
        try:
            # Get current datetime
            now = datetime.datetime.now()
            
            # Validate and parse time
            try:
                time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                try:
                    time_obj = datetime.datetime.strptime(time_str, "%I:%M %p").time()
                except ValueError:
                    return False, f"Invalid time format: {time_str}. Please use HH:MM or HH:MM AM/PM."
            
            # If date is provided, validate and parse it
            if date_str:
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    try:
                        date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                    except ValueError:
                        return False, f"Invalid date format: {date_str}. Please use YYYY-MM-DD or MM/DD/YYYY."
            else:
                # Use today's date
                date_obj = now.date()
            
            # Create a datetime object for the reminder
            reminder_datetime = datetime.datetime.combine(date_obj, time_obj)
            
            # Check if the reminder is in the past
            if reminder_datetime < now:
                if date_str:  # If specific date was provided and it's in the past
                    return False, "Cannot set reminder for a past date and time."
                else:  # If only time was provided, assume it's for tomorrow
                    date_obj = now.date() + datetime.timedelta(days=1)
                    reminder_datetime = datetime.datetime.combine(date_obj, time_obj)
            
            # Generate a unique ID for the reminder
            reminder_id = str(int(time.time()))
            
            # Create the reminder object
            reminder = {
                "id": reminder_id,
                "title": title,
                "datetime": reminder_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending"
            }
            
            # Add to reminders list
            self.reminders.append(reminder)
            
            # Save reminders
            if not self.save_reminders():
                return False, "Failed to save reminder"
            
            # Calculate seconds until the reminder
            seconds_until_reminder = (reminder_datetime - now).total_seconds()
            
            # Set up the reminder thread
            if seconds_until_reminder > 0:
                reminder_thread = threading.Timer(
                    seconds_until_reminder,
                    self._reminder_alert,
                    args=[reminder_id, title]
                )
                reminder_thread.daemon = True
                reminder_thread.start()
                
                # Track the active reminder
                self.active_reminders[reminder_id] = reminder_thread
            
            # Format a human-readable response
            time_str = reminder_datetime.strftime("%I:%M %p")
            date_str = reminder_datetime.strftime("%A, %B %d, %Y")
            return True, f"Reminder set for {time_str} on {date_str}: {title}"
            
        except Exception as e:
            return False, f"Error setting reminder: {e}"
    
    def get_reminders(self, status="pending"):
        """
        Get all reminders with the specified status.
        
        Args:
            status (str, optional): The status of reminders to get (pending or completed).
                                   If None, returns all reminders.
                                   
        Returns:
            tuple: (success, reminders or message)
        """
        try:
            filtered_reminders = []
            
            # Current time for filtering out past reminders
            now = datetime.datetime.now()
            
            for reminder in self.reminders:
                # If status is specified, filter by it
                if status and reminder.get('status') != status:
                    continue
                
                # If pending, skip reminders that have passed
                if status == "pending":
                    reminder_time = datetime.datetime.strptime(
                        reminder.get('datetime'), "%Y-%m-%d %H:%M:%S"
                    )
                    if reminder_time < now:
                        continue
                
                filtered_reminders.append(reminder)
            
            if filtered_reminders:
                return True, filtered_reminders
            else:
                if status:
                    return False, f"No {status} reminders found."
                else:
                    return False, "No reminders found."
            
        except Exception as e:
            return False, f"Error getting reminders: {e}"
    
    def cancel_reminder(self, reminder_id=None, title=None):
        """
        Cancel a reminder by ID or title.
        
        Args:
            reminder_id (str, optional): The ID of the reminder to cancel.
            title (str, optional): The title of the reminder to cancel.
                                 If both are provided, ID takes precedence.
                                 
        Returns:
            tuple: (success, message)
        """
        try:
            if not reminder_id and not title:
                return False, "Either reminder ID or title must be provided."
            
            # Find the reminder to cancel
            found = False
            for i, reminder in enumerate(self.reminders):
                if (reminder_id and reminder.get('id') == reminder_id) or \
                   (title and reminder.get('title').lower() == title.lower() and reminder.get('status') == 'pending'):
                    # Cancel the timer if active
                    if reminder.get('id') in self.active_reminders:
                        self.active_reminders[reminder.get('id')].cancel()
                        del self.active_reminders[reminder.get('id')]
                    
                    # Update reminder status
                    self.reminders[i]['status'] = 'cancelled'
                    found = True
                    
                    # If we found by ID, we can break after the first match
                    if reminder_id:
                        break
            
            if found:
                # Save changes
                if self.save_reminders():
                    return True, "Reminder cancelled successfully."
                else:
                    return False, "Failed to save changes."
            else:
                if reminder_id:
                    return False, f"No active reminder found with ID: {reminder_id}"
                else:
                    return False, f"No active reminder found with title: {title}"
            
        except Exception as e:
            return False, f"Error cancelling reminder: {e}"
    
    def clear_completed_reminders(self):
        """
        Clear all completed or cancelled reminders.
        
        Returns:
            tuple: (success, message)
        """
        try:
            original_count = len(self.reminders)
            self.reminders = [r for r in self.reminders if r.get('status') == 'pending']
            
            if len(self.reminders) < original_count:
                if self.save_reminders():
                    removed_count = original_count - len(self.reminders)
                    return True, f"Cleared {removed_count} completed/cancelled reminders."
                else:
                    return False, "Failed to save changes."
            else:
                return False, "No completed or cancelled reminders to clear."
            
        except Exception as e:
            return False, f"Error clearing reminders: {e}"
