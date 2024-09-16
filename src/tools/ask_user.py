from langchain.agents import tool
import time

@tool("ask_user")
def ask_user(question: str) -> str:
    """
    Prompts the user with a question and returns the user's response.

    Args:
        question: The question to ask the user.

    Returns:
        The user's response as a string.
    """
    start_time = time.time()
    
    user_response = input(question+": ")
    
    end_time = time.time()
    execution_time = end_time - start_time

    return user_response