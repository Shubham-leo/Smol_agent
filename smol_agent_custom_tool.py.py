"""
This script showcases the use of a custom tool integrated with Smol Agent. The custom tool,
`get_travel_duration`, calculates travel times between two locations using the Google Maps API.
The script highlights Smol Agent's flexibility in supporting user-defined functions and tools.

Requirements:
- Install the `smolagents` library and dependencies.
- Set up an environment variable `GMAPS_API_KEY` with your Google Maps API key.
"""

from typing import Optional
from smolagents import CodeAgent, HfApiModel, tool

@tool
def get_travel_duration(start_location: str, destination_location: str, transportation_mode: Optional[str] = None) -> str:
    """
    Custom tool to calculate travel duration between two locations.

    Args:
        start_location: The starting point for the journey.
        destination_location: The destination point for the journey.
        transportation_mode: The mode of transport ('driving', 'walking', 'bicycling', or 'transit').
                             Defaults to 'driving'.

    Returns:
        A string describing the travel duration or an error message if no route is found.
    """
    import os  # All imports within the function for better sharing and modularity.
    import googlemaps
    from datetime import datetime

    # Initialize Google Maps client
    gmaps = googlemaps.Client(os.getenv("GMAPS_API_KEY"))

    # Default transportation mode
    if transportation_mode is None:
        transportation_mode = "driving"

    try:
        # Fetch directions using Google Maps API
        directions_result = gmaps.directions(
            start_location,
            destination_location,
            mode=transportation_mode,
            departure_time=datetime(2025, 6, 6, 11, 0)  # Arbitrary date/time in the future
        )

        # Check and return results
        if not directions_result:
            return "No route found between these locations with the selected transportation mode."
        return directions_result[0]["legs"][0]["duration"]["text"]
    except Exception as e:
        # Log and return errors
        print(f"Error: {e}")
        return str(e)

# Create a Smol Agent with the custom tool
agent = CodeAgent(
    tools=[get_travel_duration],  # Include the custom travel duration tool
    model=HfApiModel(),          # Use Hugging Face API as the underlying model
    additional_authorized_imports=["datetime"]  # Allow datetime for sandbox execution
)

# Query the agent with a scenario
response = agent.run(
    "Can you give me a nice one-day trip around Paris with a few locations and the times? "
    "Could be in the city or outside, but should fit in one day. I'm travelling only with a rented bicycle."
)

# Display the response from the agent
print(response)

# Tips:
# - Ensure your Google Maps API key has permissions for Directions API.
# - Modularize custom tools for easy reuse in other agents or scenarios.
# - Experiment with `departure_time` for dynamic time-based results.
