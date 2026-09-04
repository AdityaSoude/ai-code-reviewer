import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REPO = "AdityaSoude/ai-code-reviewer"
PR_NUMBER = 1  # change this if your PR has a different number


def get_pr_changes():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    files = response.json()

    diff = ""

    for file in files:
        diff += f"""
FILE: {file["filename"]}

STATUS: {file["status"]}

PATCH:
{file.get("patch", "No patch available")}

-------------------------
"""

    return diff


def review_with_nvidia(diff):

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY
    )

    response = client.chat.completions.create(
        model="deepseek-ai/deepseek-v4-pro-0813",

        messages=[
            {
                "role": "system",
                "content": """
You are a senior software engineer reviewing a GitHub pull request.

Find:
- Bugs
- Security issues
- Performance issues
- Missing error handling
- Important edge cases

For each issue explain:
1. Severity
2. Problem
3. Suggested fix

Keep the review concise.
"""
            },
            {
                "role": "user",
                "content": f"""
Review these changes:

{diff}
"""
            }
        ],

        temperature=0.2,
        max_tokens=2000,

        extra_body={
            "chat_template_kwargs": {
                "thinking": False
            }
        }
    )

    return response.choices[0].message.content


def main():

    print("Getting PR changes...")

    diff = get_pr_changes()

    print("\n===== PR DIFF =====")
    print(diff)

    print("\nSending changes to NVIDIA...")

    review = review_with_nvidia(diff)

    print("\n===== AI REVIEW =====")
    print(review)


if __name__ == "__main__":
    main()