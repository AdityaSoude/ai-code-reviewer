import os
import requests
from openai import OpenAI


# -----------------------------
# GitHub Actions environment
# -----------------------------

NVIDIA_API_KEY = os.environ["NVIDIA_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

REPO = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = os.environ["PR_NUMBER"]


# -----------------------------
# GitHub headers
# -----------------------------

GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


# -----------------------------
# Get PR changes
# -----------------------------

def get_pr_changes():

    print("Getting PR changes...")

    url = (
        f"https://api.github.com/repos/"
        f"{REPO}/pulls/{PR_NUMBER}/files"
    )

    response = requests.get(
        url,
        headers=GITHUB_HEADERS
    )

    response.raise_for_status()

    files = response.json()

    diff_parts = []

    for file in files:

        patch = file.get("patch")

        if not patch:
            continue

        diff_parts.append(
            f"""
FILE: {file["filename"]}

STATUS: {file["status"]}

PATCH:
{patch}
"""
        )

    return "\n".join(diff_parts)


# -----------------------------
# NVIDIA review
# -----------------------------

def review_with_nvidia(diff):

    print("Sending code to NVIDIA...")

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY
    )

    response = client.chat.completions.create(

        model="deepseek-ai/deepseek-v4-flash-0731",

        messages=[
            {
                "role": "system",
                "content": """
You are a senior software engineer reviewing
a GitHub pull request.

Find meaningful:

- Bugs
- Security issues
- Performance problems
- Missing error handling
- Important edge cases

For every issue provide:

Severity:
File:
Line:
Problem:
Suggested fix:

Ignore trivial formatting issues.

If there are no meaningful issues, say:

No significant issues found.
"""
            },
            {
                "role": "user",
                "content": f"""
Review these pull request changes:

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
        },

        stream=False
    )

    return response.choices[0].message.content


# -----------------------------
# Post GitHub comment
# -----------------------------

def post_comment(review):

    print("Posting review to GitHub...")

    url = (
        f"https://api.github.com/repos/"
        f"{REPO}/issues/{PR_NUMBER}/comments"
    )

    body = f"""
## 🤖 AI Code Review

{review}

---

*Generated automatically by the AI Code Reviewer.*
"""

    response = requests.post(
        url,
        headers=GITHUB_HEADERS,
        json={"body": body}
    )

    response.raise_for_status()

    print("Review posted successfully!")


# -----------------------------
# Main
# -----------------------------

def main():

    diff = get_pr_changes()

    if not diff:

        print("No reviewable changes found.")

        return

    review = review_with_nvidia(diff)

    print("\n===== AI REVIEW =====")
    print(review)

    post_comment(review)


if __name__ == "__main__":
    main()