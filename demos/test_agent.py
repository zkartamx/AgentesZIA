from agents import Agent, Runner
from dotenv import load_dotenv
import os

load_dotenv()

# Configurar para usar z.ai API
os.environ["OPENAI_BASE_URL"] = "https://api.z.ai"

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
