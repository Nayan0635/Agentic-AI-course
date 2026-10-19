# from openai import OpenAI
from groq import Groq
import requests
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
api_key=os.getenv("groq_key")

)

# Example:
# https://github.com/react/react
owner = "react"
repo = "react"


url = f"https://api.github.com/repos/{owner}/{repo}/contents"
response = requests.get(url)
files = response.json()
repo_content = ""


for file in files:
    # Read only source/code files
    if file["type"] == "file":
        file_name = file["name"]
        if file_name.endswith((
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".md"
            )):

            download_url = file["download_url"]
            file_response = requests.get(download_url)
            repo_content += f"\n\nFILE: {file_name}\n"
            repo_content += file_response.text[:3000]

prompt = f"""
    Analyze this GitHub repository.

    Repository Content: {repo_content[:15000]}

    Please provide:

    1. Project Summary
    2. Tech Stack
    3. Important Modules
    4. Architecture Overview
    5. Code Quality Review
    6. Suggestions for Improvement
    7. Security Concerns
    """

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{
        "role": "user",
        "content": prompt
}])

print(response.choices[0].message.content)

# Set API Key
# Windows CMD
# set OPENAI_API_KEY=your_api_key
# PowerShell
# $env:OPENAI_API_KEY="your_api_key"

# Run
# python github_repo_analyzer.py

# Example Repo
# owner = "langchain-ai"
# repo = "langchain"
# or
# owner = "openai"
# repo = "openai-python"

# Example Output
# PROJECT SUMMARY:
# This repository is a frontend JavaScript library for building UI.

# TECH STACK:
# - JavaScript
# - React
# - Node.js

# ARCHITECTURE:
# Component-based architecture.

# CODE QUALITY:
# Well structured and modular.

# SUGGESTIONS:
# - Improve test coverage
# - Add more documentation

# Better Version (Clone Full Repo)
# Install GitPython:
# pip install gitpython
# Clone repo:
# from git import Repo

# Repo.clone_from(
# "https://github.com/user/repo.git",
# "./repo"
# )

# Then analyze all files locally.