"""
This script demonstrates how to use the `LiteLLMModel` from the `smolagents` library to interact with the "ollama_chat/mistral" model.
The script initiates a conversation with the model and asks for information about the history of the internet.

"""

from smolagents import CodeAgent
from smolagents import LiteLLMModel

# Initialize the model with the specified model ID and API key
model = LiteLLMModel(model_id="ollama_chat/mistral", api_key="ollama")
agent = CodeAgent(tools=[], model=model, add_base_tools=True)
response = agent.run("Could you tell me about the history of the internet?")
print(response)

# Tips:
# - If the `ollama_chat/mistral` model behaves abnormally or returns unexpected responses, try using a different model.
# - You can change the `model_id` to another model available in Ollama or any other compatible model.
