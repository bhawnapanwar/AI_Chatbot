import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI


load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# ---------------------------------------------------------
# PART A: The TV Management Plugin (The "Memory")
# ---------------------------------------------------------
class TVManagementPlugin:
    def __init__(self):
        # Initial State
        self.is_on = False
        self.volume = 15
        self.brightness = 50
        self.current_channel_id = 1
        
        # Hardcoded Channel List (Metadata)
        self.channels = [
            {"id": 1, "name": "RTP1", "category": "General"},
            {"id": 2, "name": "CNN", "category": "News"},
            {"id": 3, "name": "Cartoon Network", "category": "Kids"},
            {"id": 4, "name": "SportTV", "category": "Sports"},
            {"id": 5, "name": "MTV", "category": "Music"},
        ]

    def list_channels(self):
        """Returns list of channels with metadata and boolean if it's current."""
        result = []
        for ch in self.channels:
            ch_data = ch.copy()
            ch_data["is_current"] = (ch["id"] == self.current_channel_id)
            result.append(ch_data)
        return json.dumps(result)

    def set_channel(self, channel_id):
        """Sets current channel by ID."""
        if not any(ch['id'] == channel_id for ch in self.channels):
            return json.dumps({"error": "Channel ID not found."})
        
        self.current_channel_id = channel_id
        return json.dumps({"status": f"Channel set to {channel_id}"})

    def get_tv_settings(self):
        """Returns list of current settings."""
        return json.dumps({
            "is_on": self.is_on,
            "volume": self.volume,
            "brightness": self.brightness,
            "current_channel_id": self.current_channel_id
        })

    def set_volume(self, value):
        """Sets volume (0-100)."""
        self.volume = max(0, min(100, value)) 
        return json.dumps({"status": f"Volume set to {self.volume}"})

    def set_tv_state(self, is_on):
        """Turns TV on (True) or off (False)."""
        self.is_on = is_on
        state_str = "ON" if is_on else "OFF"
        return json.dumps({"status": f"TV turned {state_str}"})

    def set_brightness(self, value):
        """Sets brightness (0-100)."""
        self.brightness = max(0, min(100, value))
        return json.dumps({"status": f"Brightness set to {self.brightness}"})

# Initialize the plugin
tv_plugin = TVManagementPlugin()

# ---------------------------------------------------------
# PART B: Tool Definitions 
# ---------------------------------------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_channels",
            "description": "Get a list of all available TV channels and their categories.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_channel",
            "description": "Change the TV channel to a specific ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "channel_id": {"type": "integer", "description": "The ID of the channel to switch to."}
                },
                "required": ["channel_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_tv_settings",
            "description": "Get current TV status including volume, brightness, and power state.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_volume",
            "description": "Set the TV volume (0-100).",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "integer", "description": "Target volume level (0-100)."}
                },
                "required": ["value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_tv_state",
            "description": "Turn the TV On or Off.",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_on": {"type": "boolean", "description": "True for ON, False for OFF."}
                },
                "required": ["is_on"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_brightness",
            "description": "Set the TV brightness (0-100).",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "integer", "description": "Target brightness level (0-100)."}
                },
                "required": ["value"],
            },
        },
    },
]

# ---------------------------------------------------------
# PART C: The Chat Loop 
# ---------------------------------------------------------
system_message = """
You are a smart TV assistant. You have access to a TVManagementPlugin to control the TV.

RULES:
1. CONTINUOUS ACTION: If a user request requires multiple steps (e.g., "Change channel" but TV is Off), you must perform ALL steps until the request is complete. Do not stop halfway.
2. TV OFF STATE: If the TV is OFF, you cannot change channels or volume. You must turn the TV ON first, and THEN perform the action.
3. AUTOMATION: Do not ask the user for permission to turn the TV on. Just do it.
"""

conversation_history = [{"role": "system", "content": system_message}]

print("--- TV Bot (Type 'quit' to exit) ---")

while True:
    user_input = input("\nUser: ")
    if user_input.strip().lower() == "quit":
        break

    conversation_history.append({"role": "user", "content": user_input})

    
    while True:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=conversation_history,
            tools=tools,
            tool_choice="auto", 
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        
        if tool_calls:
            
            conversation_history.append(response_message)

            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"[System] Calling function: {function_name} with args: {function_args}")

                function_response = ""
                if function_name == "list_channels":
                    function_response = tv_plugin.list_channels()
                elif function_name == "set_channel":
                    function_response = tv_plugin.set_channel(function_args.get("channel_id"))
                elif function_name == "get_tv_settings":
                    function_response = tv_plugin.get_tv_settings()
                elif function_name == "set_volume":
                    function_response = tv_plugin.set_volume(function_args.get("value"))
                elif function_name == "set_tv_state":
                    function_response = tv_plugin.set_tv_state(function_args.get("is_on"))
                elif function_name == "set_brightness":
                    function_response = tv_plugin.set_brightness(function_args.get("value"))

                conversation_history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
            
            continue
        
        else:
            print(f"TV Bot: {response_message.content}")
            conversation_history.append(response_message)
            break 