from langchain.agents import tool
import time
import json
import os
from config.app_config import AppConfig
app_config = AppConfig()

@tool("write_config_file")
def write_config_file(config_data: str) -> str:
    """
    Writes the user's configuration settings to a JSON file.

    Args:
        config_data: A string containing configuration settings.

    Returns:
        A message indicating the file was successfully written.
    """
    start_time = time.time()
    
    response = agent_string_to_json_file(config_data)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return response

def agent_string_to_json_file(json_string):
    jsonString = json_string.replace("'", '"').replace('true', 'true').replace('false', 'false').replace("True", "true").replace("False", "false")
    
    try:
        jsonData = json.loads(jsonString)   
        with open(app_config.DATA_CONFIG_PATH, 'w') as config_file:
            json.dump(jsonData, config_file, indent=2)
        print(f"Config data successfully written to {app_config.DATA_CONFIG_PATH}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")