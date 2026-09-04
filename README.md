# AI GitHub Code Reviewer

A simple GitHub Actions bot that reviews pull request changes with an LLM and posts the review as a PR comment.

## Setup

1. Create a GitHub repository.
2. Add these files:
   - `.github/workflows/review.yml`
   - `reviewer.py`
   - `requirements.txt`
3. In GitHub, go to:
   `Settings -> Secrets and variables -> Actions`
4. Add a repository secret named:
   `OPENAI_API_KEY`
5. Open or update a pull request.

The workflow will run automatically and post the AI review as a comment.

## Important

The bot only suggests changes. It does not modify or commit code automatically.
