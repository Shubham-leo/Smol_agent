import re
import requests
from markdownify import markdownify
from requests.exceptions import RequestException
from smolagents import tool

from dotenv import load_dotenv 
load_dotenv()

@tool
def visit_webpage(url:str)->"str":
    """
    visits a webpage at given url and returns its cotent as markdown string.
    
    Args:
        url: The url of the webpage to visit.
    
    Returns:
        The content of the webpage converted to markdown,or an error message if the request fails.

    """

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        #convert the html content to markdown
        markdown_content = markdownify(response.text).strip()

        #removes multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content
    except RequestException as e:
        return f"Error fetching webpage: {e}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

    
from smolagents import(
    CodeAgent,
    ToolCallingAgent,
    HfApiModel,
    ManagedAgent,
    DuckDuckGoSearchTool,
)

web_agent = ToolCallingAgent(
    tools=[visit_webpage,DuckDuckGoSearchTool()],
    model=HfApiModel(),
    max_steps=10,
)

managed_web_agent = ManagedAgent(
    agent=web_agent,
    name = "search",
    description="runs web searches for you.give it your query as an argument",
)

manager_agent = CodeAgent(
    tools=[],
    model=HfApiModel(),
    managed_agents = [managed_web_agent],
    additional_authorized_imports=["time","numpy","pandas"],
)

answer = manager_agent.run("what do you think will happen in 2025 with ai agents? compare usage in production in the past 12 months.")
print(answer)
