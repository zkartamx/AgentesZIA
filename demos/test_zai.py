from zai import ZaiClient
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize client
client = ZaiClient(api_key=os.getenv("ZAI_API_KEY"))

# Create chat completion
response = client.chat.completions.create(
    model="glm-4.6",
    messages=[
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ]
)

print(response.choices[0].message.content)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
