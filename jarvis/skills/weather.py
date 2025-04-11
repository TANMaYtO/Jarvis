"""
Weather functionality for Jarvis.
"""

from ..utils.web import WebTools

class WeatherSkill:
    def __init__(self):
        self.web_tools = WebTools()
    
    def get_weather(self, city):
        """
        Get the current weather for a city.
        
        Args:
            city (str): The city to get weather for
            
        Returns:
            tuple: (success, weather_response or error_message)
        """
        if not city:
            return False, "Please specify a city"
        
        # Clean up the city name
        city = city.strip()
        
        # Get the weather data
        success, result = self.web_tools.get_weather(city)
        
        if success:
            # Format the response
            weather_response = self._format_weather_response(result)
            return True, weather_response
        else:
            return False, result
    
    def _format_weather_response(self, weather_data):
        """Format the weather data into a readable response."""
        # Basic weather information
        response = (
            f"The current weather in {weather_data['city']}, {weather_data['country']} is "
            f"{weather_data['description']} with a temperature of {weather_data['temperature']}°C. "
        )
        
        # Add feels like temperature if different enough
        if abs(weather_data['temperature'] - weather_data['feels_like']) > 2:
            response += f"It feels like {weather_data['feels_like']}°C. "
        
        # Add humidity information
        response += f"The humidity is {weather_data['humidity']}% "
        
        # Add wind information
        response += f"and wind speed is {weather_data['wind_speed']} m/s."
        
        return response
    
    def get_forecast(self, city, days=5):
        """
        Get the weather forecast for a city.
        This is a placeholder method for future implementation.
        
        Args:
            city (str): The city to get forecast for
            days (int): Number of days for the forecast
            
        Returns:
            tuple: (success, forecast_response or error_message)
        """
        # Currently, we don't have a forecast feature implemented
        # This is a placeholder for future expansion
        return False, "Weather forecast feature is not yet implemented"
