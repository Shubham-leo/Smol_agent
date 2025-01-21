"""
This script demonstrates how to interact with OpenAI' using the `LiteLLMModel` from the `smolagents` library.
It allows the user to input messages and receive responses from the assistant while keeping track of the conversation.

Requirements:
- Install the `smolagents` library.
- Ensure access to the OpenAI GPT-3.5-turbo model.
"""

from smolagents import CodeAgent, LiteLLMModel

model = LiteLLMModel("openai/gpt-3.5-turbo", temperature=0.2)

# List to store conversation history
message = []

while True:
    # Prompt the user to enter a message
    user_input = input("Enter your message: ")

    # Exit the loop if the user types "exit"
    if user_input == "exit":
        break

    # Append the user's message to the conversation history
    message.append({"role": "user", "content": user_input})

    # Get the model's response based on the conversation history
    response = model(message, max_tokens=500)
    assistant_response = response.content
    print("Assistant:", assistant_response)

    # Append the assistant's response to the conversation history
    message.append({"role": "assistant", "content": assistant_response})

# Tips:
# - To end the conversation, type 'exit'.
# - The conversation history is kept in the `message` list, which ensures the model remembers prior inputs.
# - refer litellm docs for more details 