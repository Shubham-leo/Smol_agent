from smolagents import CodeAgent
from smolagents import LiteLLMModel

model = LiteLLMModel(model_id="ollama_chat/mistral",
                     api_key="ollama")

agent = CodeAgent(tools=[],model=model,add_base_tools=True)
#
agent.run("could you tell me about the history of the internet?")

#ollama behaves abnormally in some cases try to change model and rerun the code