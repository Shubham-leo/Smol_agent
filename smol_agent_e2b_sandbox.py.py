"""

This script demonstrates the use of Smol Agent in an e2b sandbox environment. 
It integrates tools like VisitWebpageTool and utilizes Hugging Face's API for processing. 
The e2b executor allows running code in a secure, isolated sandbox, ideal for exploring dynamic data or web interactions.

Requirements:
- Install the `smolagents` library and required dependencies.
- Ensure `.env` file is correctly set up with necessary environment variables.
"""

from smolagents import CodeAgent, VisitWebpageTool, HfApiModel
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the Smol Agent with e2b executor enabled
agent = CodeAgent(
    tools=[VisitWebpageTool()],            # Tool for visiting and interacting with web pages
    model=HfApiModel(),                    # Hugging Face API for language processing
    additional_authorized_imports=[        # Allow additional imports for the sandbox
        "requests", "markdownify", "bs4"
    ],
    use_e2b_executor=True                  # Enable the e2b sandbox executor
)

# Run a query using the agent
response = agent.run(
    "Who won the last World Cup? Of the top 3 sports worldwide."
)

# Display the agent's output
print(response)

# Tips:
# - The e2b sandbox provides a secure way to execute untrusted or resource-intensive code.
# - Use `VisitWebpageTool` for tasks requiring interaction with live web pages.
# - Ensure all necessary imports are included in `additional_authorized_imports` for sandbox execution.