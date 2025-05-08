import datetime
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from google.adk.agents import Agent # type: ignore

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Optional: Check if the API key was loaded successfully
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Make sure it's set in your .env file.")

# --- Your existing functions ---
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    print(f"--- Tool: get_weather called with city='{city}' ---") # Added for debugging
    if city.lower() == "new york":
        result = {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        result = {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }
    print(f"--- Tool: get_weather returning: {result} ---") # Added for debugging
    return result


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    print(f"--- Tool: get_current_time called with city='{city}' ---") # Added for debugging
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        result = {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }
        print(f"--- Tool: get_current_time returning: {result} ---") # Added for debugging
        return result

    try:
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = (
            f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        )
        result = {"status": "success", "report": report}
    except Exception as e: # Catch potential ZoneInfo errors
        result = {
            "status": "error",
            "error_message": f"Error getting time for {city}: {e}",
        }
    print(f"--- Tool: get_current_time returning: {result} ---") # Added for debugging
    return result

# --- Agent Definition ---
# NOTE: Ensure GOOGLE_API_KEY is used correctly by the underlying library.
# Often, setting it as an environment variable is sufficient.
# If the Agent class specifically needs it passed, you would do:
# root_agent = Agent(..., api_key=GOOGLE_API_KEY)
# Check the google-adk documentation for specifics.
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash", # Make sure this model identifier is correct for ADK
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city. "
        "When asked for information, first determine if it's a weather or time request. "
        "Then, identify the city. "
        "Use the appropriate tool to find the information and respond to the user based on the tool's output."
    ),
    tools=[get_weather, get_current_time],
    # Example if API key needs to be passed directly:
    # api_key=GOOGLE_API_KEY
)

# --- Agent Interaction ---
print("Agent Initialized. Starting interaction...")

# Corrected method call from invoke to execute
print("\nAsking about weather...")
try:
    # Use execute instead of invoke
    result_weather = root_agent.execute("What's the weather like in New York?")
    print("\nWeather Result:")
    print(result_weather) # Print the entire result structure
    # You might need to access a specific field like result_weather['output'] depending on the Agent's return format
    # print(f"Agent Response: {result_weather.get('output', 'No output field found')}")


except Exception as e:
    print(f"\nError during weather execution: {e}")
    import traceback
    traceback.print_exc()


print("\nAsking about time...")
try:
    # Use execute instead of invoke
    result_time = root_agent.execute("What time is it in New York?")
    print("\nTime Result:")
    print(result_time) # Print the entire result structure
    # print(f"Agent Response: {result_time.get('output', 'No output field found')}")

except Exception as e:
    print(f"\nError during time execution: {e}")
    import traceback
    traceback.print_exc()

print("\nAsking about unsupported city...")
try:
    # Use execute instead of invoke
    result_unsupported = root_agent.execute("What's the weather in London?")
    print("\nUnsupported City Result:")
    print(result_unsupported) # Print the entire result structure
    # print(f"Agent Response: {result_unsupported.get('output', 'No output field found')}")

except Exception as e:
    print(f"\nError during unsupported city execution: {e}")
    import traceback
    traceback.print_exc()

print("\nInteraction finished.")