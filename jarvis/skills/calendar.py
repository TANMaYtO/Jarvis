"""
Calendar functionality for Jarvis.
"""

import json
import os
import datetime
from pathlib import Path

class CalendarSkill:
    def __init__(self):
        self.events_file = Path(__file__).parent.parent / 'data' / 'calendar_events.json'
        self.events = self.load_events()
    
    def load_events(self):
        """Load events from the calendar_events.json file."""
        events = {}
        
        try:
            if self.events_file.exists():
                with open(self.events_file, 'r') as f:
                    events = json.load(f)
        except Exception as e:
            print(f"Error loading calendar events: {e}")
        
        return events
    
    def save_events(self):
        """Save events to the calendar_events.json file."""
        try:
            os.makedirs(self.events_file.parent, exist_ok=True)
            
            with open(self.events_file, 'w') as f:
                json.dump(self.events, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving calendar events: {e}")
            return False
    
    def add_event(self, title, date_str, time_str=None, description=None):
        """
        Add an event to the calendar.
        
        Args:
            title (str): The title of the event
            date_str (str): The date of the event in format YYYY-MM-DD
            time_str (str, optional): The time of the event in format HH:MM
            description (str, optional): A description of the event
            
        Returns:
            tuple: (success, message)
        """
        try:
            # Validate date format
            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                date_str = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                try:
                    # Try alternative format MM/DD/YYYY
                    date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                    date_str = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    return False, f"Invalid date format: {date_str}. Please use YYYY-MM-DD or MM/DD/YYYY."
            
            # Validate time format if provided
            time_obj = None
            if time_str:
                try:
                    time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()
                    time_str = time_obj.strftime("%H:%M")
                except ValueError:
                    try:
                        # Try alternative format HH:MM AM/PM
                        time_obj = datetime.datetime.strptime(time_str, "%I:%M %p").time()
                        time_str = time_obj.strftime("%H:%M")
                    except ValueError:
                        return False, f"Invalid time format: {time_str}. Please use HH:MM or HH:MM AM/PM."
            
            # Create event
            event = {
                "title": title,
                "date": date_str,
                "time": time_str,
                "description": description
            }
            
            # Add to events
            if date_str not in self.events:
                self.events[date_str] = []
            
            self.events[date_str].append(event)
            
            # Save events
            if self.save_events():
                return True, f"Event '{title}' added to calendar for {date_str}"
            else:
                return False, "Failed to save event"
            
        except Exception as e:
            return False, f"Error adding event: {e}"
    
    def get_events(self, date_str=None):
        """
        Get events for a specific date or today.
        
        Args:
            date_str (str, optional): The date to get events for in format YYYY-MM-DD.
                                      If None, returns today's events.
                                      
        Returns:
            tuple: (success, events or message)
        """
        try:
            # If no date provided, use today
            if not date_str:
                date_str = datetime.date.today().strftime("%Y-%m-%d")
            else:
                # Validate date format
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    date_str = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        # Try alternative format MM/DD/YYYY
                        date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                        date_str = date_obj.strftime("%Y-%m-%d")
                    except ValueError:
                        return False, f"Invalid date format: {date_str}. Please use YYYY-MM-DD or MM/DD/YYYY."
            
            # Check if there are events for this date
            if date_str in self.events and self.events[date_str]:
                return True, self.events[date_str]
            else:
                return False, f"No events scheduled for {date_str}"
            
        except Exception as e:
            return False, f"Error getting events: {e}"
    
    def remove_event(self, title, date_str=None):
        """
        Remove an event from the calendar.
        
        Args:
            title (str): The title of the event to remove
            date_str (str, optional): The date of the event in format YYYY-MM-DD.
                                      If None, searches all dates.
                                      
        Returns:
            tuple: (success, message)
        """
        try:
            # If date is provided, only search that date
            if date_str:
                # Validate date format
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    date_str = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        # Try alternative format MM/DD/YYYY
                        date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                        date_str = date_obj.strftime("%Y-%m-%d")
                    except ValueError:
                        return False, f"Invalid date format: {date_str}. Please use YYYY-MM-DD or MM/DD/YYYY."
                
                # Check if there are events for this date
                if date_str in self.events:
                    # Find the event by title
                    found = False
                    self.events[date_str] = [event for event in self.events[date_str] if event["title"].lower() != title.lower() or (found := True) is False]
                    
                    if found:
                        # Save changes
                        if self.save_events():
                            return True, f"Event '{title}' removed from calendar"
                        else:
                            return False, "Failed to save changes"
                    else:
                        return False, f"No event '{title}' found for {date_str}"
                else:
                    return False, f"No events scheduled for {date_str}"
            else:
                # Search all dates
                found = False
                for date in list(self.events.keys()):
                    original_length = len(self.events[date])
                    self.events[date] = [event for event in self.events[date] if event["title"].lower() != title.lower()]
                    
                    if len(self.events[date]) < original_length:
                        found = True
                    
                    # Remove empty dates
                    if not self.events[date]:
                        del self.events[date]
                
                if found:
                    # Save changes
                    if self.save_events():
                        return True, f"Event '{title}' removed from calendar"
                    else:
                        return False, "Failed to save changes"
                else:
                    return False, f"No event '{title}' found in calendar"
            
        except Exception as e:
            return False, f"Error removing event: {e}"
