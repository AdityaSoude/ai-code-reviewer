import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

response = client.chat.completions.create(
    model="deepseek-ai/deepseek-v4-pro-0813",
    messages=[
        {
            "role": "user",
            "content": """
Review this Python code and find the bug:

def divide(a, b):
    return a / b
"""
        }
    ],
    temperature=0.2,
    max_tokens=1000,
    extra_body={
        "chat_template_kwargs": {
            "thinking": False
        }
    },
    stream=False
)

print("\n===== AI REVIEW =====\n")
print(response.choices[0].message.content)