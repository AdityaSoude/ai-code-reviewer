# 🤖 AI Code Reviewer

An automated GitHub Pull Request code reviewer that uses **GitHub Actions** and an **AI coding model** to analyze code changes and post actionable feedback directly to the Pull Request.

The goal is to catch common bugs, edge cases, security concerns, and error-handling issues before code is merged — without requiring a dedicated QA process.

## 🚀 Overview

When a developer opens or updates a Pull Request:

1. GitHub triggers a GitHub Actions workflow.
2. The workflow retrieves the files changed in the Pull Request.
3. The code diff is sent to an AI model through the NVIDIA API.
4. The AI analyzes the changes for meaningful issues.
5. The generated review is posted automatically as a comment on the Pull Request.

```text
Developer
    │
    ▼
GitHub Pull Request
    │
    ▼
GitHub Actions
    │
    ▼
Get PR Diff
    │
    ▼
NVIDIA AI API
    │
    ▼
AI Code Review
    │
    ▼
GitHub API
    │
    ▼
Pull Request Comment
```

## 🎯 Problem

In smaller engineering teams, code reviews may not always catch every issue, especially when there is no dedicated QA team.

Traditional review can miss:

- Runtime bugs
- Missing error handling
- Edge cases
- Security issues
- Performance problems
- Incorrect assumptions in business logic

This project uses an AI reviewer as an **additional automated layer of feedback** during the Pull Request process.

The AI reviewer is not intended to replace human code review. Instead, it provides an early automated check before code is merged.

## ✨ Features

- Automatic review when a Pull Request is opened
- Automatic re-review when new commits are pushed
- Retrieves the actual Pull Request diff
- AI-powered code analysis
- Identifies meaningful bugs and edge cases
- Highlights missing error handling
- Checks for potential security and performance problems
- Posts the review directly to the Pull Request
- No local execution required
- API credentials stored securely using GitHub Secrets

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Reviewer implementation |
| GitHub Actions | CI/CD automation |
| GitHub REST API | Retrieve PR changes and post reviews |
| NVIDIA API | AI inference |
| DeepSeek V4 Flash | Code analysis |
| OpenAI Python SDK | Communicate with NVIDIA's OpenAI-compatible API |

## 📁 Project Structure

```text
ai-code-reviewer/
│
├── .github/
│   └── workflows/
│       └── review.yml
│
├── reviewer.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `reviewer.py`

Contains the main code-review logic:

- Retrieves Pull Request changes
- Sends the diff to the AI model
- Processes the AI response
- Posts the review to GitHub

### `.github/workflows/review.yml`

Defines when and how GitHub Actions runs the reviewer.

### `requirements.txt`

Contains the Python dependencies required by the GitHub Actions runner.

## ⚙️ How It Works

### 1. Pull Request is created

A developer creates a Pull Request:

```text
test-review-2 → main
```

GitHub generates a `pull_request` event.

### 2. GitHub Actions starts

The workflow listens for:

```yaml
on:
  pull_request:
    types: [opened, synchronize]
```

This means the reviewer runs when:

- A PR is opened
- New commits are pushed to an existing PR

### 3. Retrieve the PR changes

The reviewer calls the GitHub API:

```text
GET /repos/{owner}/{repo}/pulls/{pull_number}/files
```

It extracts the relevant patches from the changed files.

### 4. Send the changes to the AI model

The code diff is sent to the NVIDIA API using the OpenAI-compatible Python SDK.

The reviewer asks the model to focus on meaningful issues such as:

- Bugs
- Security issues
- Performance problems
- Missing error handling
- Important edge cases

Trivial formatting issues are ignored.

### 5. Post the result to GitHub

The generated review is posted to the Pull Request using the GitHub API.

Example:

```text
🤖 AI Code Review

Severity: High

File: sample.py
Line: 3

Problem:
user is always None, so accessing user.name
will raise AttributeError.

Suggested fix:
Retrieve the user before accessing its attributes
and handle the case where the user does not exist.
```

## 🔐 Configuration

The NVIDIA API key is stored as a **GitHub Repository Secret**.

Navigate to:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ Repository secrets
```

Create:

```text
NVIDIA_API_KEY
```

The key is injected into the GitHub Actions environment at runtime and does not need to be stored in the repository.

## 🔌 Integrating AI Code Reviewer Into Your Repository

The AI Code Reviewer can be integrated into any GitHub repository that uses GitHub Actions.

### 1. Add the reviewer

Copy these components into your repository:

```text
your-repository/
├── .github/
│   └── workflows/
│       └── ai-code-review.yml
├── reviewer.py
└── requirements.txt
```

### 2. Configure the NVIDIA API Key

Go to:

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Create:

```text
NVIDIA_API_KEY
```

### 3. Add the GitHub Actions workflow

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run AI reviewer
        env:
          NVIDIA_API_KEY: ${{ secrets.NVIDIA_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: python reviewer.py
```

GitHub automatically provides `GITHUB_TOKEN`; it does not need to be manually created.

### 4. Add dependencies

```text
openai
requests
```

### 5. Create a Pull Request

Once configured, developers continue using the normal Git workflow:

```text
Developer
    ↓
git push
    ↓
Pull Request
    ↓
GitHub Actions
    ↓
AI Review
    ↓
Pull Request Comment
```

No additional command is required from the developer.

## 🏢 Example: Existing Team Repository

Suppose a company has:

```text
company-backend/
├── src/
├── tests/
├── Dockerfile
└── ...
```

They can add:

```text
company-backend/
├── .github/
│   └── workflows/
│       └── ai-code-review.yml
├── reviewer.py
├── requirements.txt
├── src/
├── tests/
└── Dockerfile
```

After adding the `NVIDIA_API_KEY` secret, every Pull Request can automatically receive an AI review.

The existing development process remains:

```text
Developer
   ↓
Pull Request
   ↓
Human Code Review
   +
AI Code Review
   ↓
Merge
```

The AI reviewer acts as an **additional review layer**, not a replacement for human review.

## 🌎 Repository Requirements

The repository needs:

- GitHub repository
- GitHub Actions enabled
- Permission to run Pull Request workflows
- `NVIDIA_API_KEY` configured as a repository secret
- Python environment supported by the GitHub Actions runner

No database, server, Docker container, or locally running service is required for the current MVP.

## 🧪 Testing the System

Create a test branch:

```bash
git checkout -b test-review-2
```

Add code containing an obvious issue:

```python
def divide(a, b):
    return a / b
```

Commit and push:

```bash
git add .
git commit -m "Add test case for AI review"
git push -u origin test-review-2
```

Create a Pull Request:

```text
test-review-2 → main
```

GitHub Actions will automatically execute the reviewer.

Check:

```text
GitHub
→ Actions
→ AI Code Review
```

Then open the Pull Request and look for the generated:

```text
🤖 AI Code Review
```

comment.

## 🔒 Security Considerations

The project uses GitHub Secrets for sensitive credentials.

Never commit:

```text
NVIDIA_API_KEY
.env
API keys
access tokens
private credentials
```

Recommended `.gitignore`:

```text
.env
__pycache__/
.venv/
venv/
*.pyc
```

The GitHub Actions workflow receives the API key only at runtime.

## ⚠️ Current Limitations

This is currently an MVP.

### Review comments

The reviewer currently posts one summarized comment on the Pull Request rather than GitHub's native inline comments on individual lines.

### Large Pull Requests

Very large diffs may exceed model context limits or become slow to process.

### AI accuracy

AI-generated reviews can contain false positives or miss real problems.

Human review is still required before merging code.

### Duplicate reviews

Updating a Pull Request triggers another review, so the current MVP can generate multiple review comments.

## 🗺️ Future Improvements

### Phase 1 — Better Reviews

- Inline GitHub review comments
- File and line-level feedback
- Severity classification
- Duplicate-review prevention

### Phase 2 — Better Context

- Repository-level coding guidelines
- `CONTRIBUTING.md` support
- Project-specific review rules
- Language/framework-aware prompts

### Phase 3 — Performance

- Review only changed lines
- Parallel file analysis
- Large-diff chunking
- Caching previous reviews

### Phase 4 — Developer Experience

- `/ai-review` Pull Request command
- Review status checks
- Configurable severity thresholds
- Automatic review summaries

## 🧠 Design Philosophy

The project intentionally starts simple:

```text
GitHub Event
     ↓
GitHub Actions
     ↓
PR Diff
     ↓
AI Model
     ↓
GitHub Comment
```

There is no need for a database, vector database, LangChain, or complex agent architecture for the initial use case.

The goal is to first build a reliable end-to-end workflow and then add complexity only when it solves a real problem.

## 📌 Example Use Case

A developer submits:

```python
def get_user(user_id):
    user = None
    return user.name
```

The AI reviewer identifies that `user` is always `None` and accessing `user.name` will cause a runtime exception.

Instead of waiting for the application to fail or relying entirely on manual review, the developer receives feedback directly in the Pull Request.

## 🎓 Project Goal

This project demonstrates how AI can be integrated into an existing software-development workflow using:

- Event-driven automation
- CI/CD
- REST APIs
- Secure secret management
- AI-assisted code analysis
- Automated developer feedback

The core objective is to make code review **faster and more proactive** while keeping humans in the final decision-making loop.
