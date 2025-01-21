"""
This script demonstrates how to set up and use Smol Agent with selected tools.
It utilizes DuckDuckGoSearchTool for web-based queries and HfApiModel as the underlying
AI model. Smol Agent provides a lightweight, efficient framework for building intelligent agents.

Requirements:
- Install the `smolagents` library via pip if not already installed.
"""

from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

# Initialize the Smol Agent with tools and a model
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],  # Add web-search capabilities via DuckDuckGo
    model=HfApiModel()              # Use Hugging Face API as the default model
)

# Run a query using the agent
response = agent.run(
    "lets assume its possible to fly using plane to then moon how many hrs it will take to reach moon?"
)

# Display the agent's output
print(response)