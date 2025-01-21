"""
🚀 Exploring Smol Agent Capabilities with Web Interaction and Managed Agents 🚀

This script demonstrates how to leverage Smol Agent tools to perform advanced tasks like visiting webpages, 
fetching and converting webpage content to markdown, running web searches, and managing agents for dynamic workflows.

Key Highlights of My Implementation:
1. **Webpage Interaction**:
   - Used `visit_webpage` to fetch webpage content and convert it to markdown format, removing extra line breaks for cleaner output.
   - Example Use: Querying real-time data or extracting readable content from any webpage.

2. **Managed Agents for Web Search**:
   - Integrated `DuckDuckGoSearchTool` with `ToolCallingAgent` to perform live web queries.
   - Example Use: Running searches for future trends like AI developments in 2025.

3. **Dynamic Multi-Agent Management**:
   - Configured `ManagedAgent` to orchestrate multiple agents for seamless task execution.
   - Example Use: Enabling complex workflows with additional imports like NumPy and Pandas for advanced data processing.
"""

import re
import requests
from markdownify import markdownify
from requests.exceptions import RequestException
from smolagents import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def visit_webpage(url: str) -> "str":
    """
    Visits a webpage at a given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to markdown or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Convert the HTML content to markdown
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content
    except RequestException as e:
        return f"Error fetching webpage: {e}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    HfApiModel,
    ManagedAgent,
    DuckDuckGoSearchTool,
)

# Initialize a ToolCallingAgent with tools for web interaction
web_agent = ToolCallingAgent(
    tools=[visit_webpage, DuckDuckGoSearchTool()],
    model=HfApiModel(),
    max_steps=10,
)

# Create a ManagedAgent for web search tasks
managed_web_agent = ManagedAgent(
    agent=web_agent,
    name="search",
    description="Runs web searches for you. Give it your query as an argument.",
)

# Configure a CodeAgent for advanced workflows with additional imports
manager_agent = CodeAgent(
    tools=[],
    model=HfApiModel(),
    managed_agents=[managed_web_agent],
    additional_authorized_imports=["time", "numpy", "pandas"],
)

# Example Query: Exploring AI trends in 2025
answer = manager_agent.run(
    "What do you think will happen in 2025 with AI agents? Compare usage in production in the past 12 months."
)
print(answer)
