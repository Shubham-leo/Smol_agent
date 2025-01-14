#run code in e2b sandbox and get output
from smolagents import CodeAgent,VisitWebpageTool,HfApiModel
from dotenv import load_dotenv

load_dotenv()
agent = CodeAgent(tools=[VisitWebpageTool()],
                  model=HfApiModel(),
                  additional_authorized_imports=["requests","markdownify","bs4"],
                  use_e2b_executor=True)

agent.run("what was abraham lincoln's first pet?")
