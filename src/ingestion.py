import asyncio
import httpx
from gtrending import fetch_repos
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import SUMMARY_SYSTEM_PROMPT

README_THRESHOLD = 3000
PRESUMMARY_MODEL = "gpt-4o-mini"
TRENDING_PERIOD = "weekly"
NUM_REPOS = 25


def fetch_trending_repos() -> list[dict]:
    repos = fetch_repos(language="", spoken_language_code="en", since=TRENDING_PERIOD)
    result = []
    for repo in repos[:NUM_REPOS]:
        result.append({
            "name": repo.full_name,
            "url": repo.url,
            "description": repo.description or "",
            "stars": repo.stars,
        })
    return result
