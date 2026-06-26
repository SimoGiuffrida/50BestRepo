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


async def _fetch_readme(client: httpx.AsyncClient, repo: dict) -> dict:
    owner, name = repo["name"].split("/")
    url = f"https://raw.githubusercontent.com/{owner}/{name}/main/README.md"
    response = await client.get(url)
    if response.status_code == 200:
        readme_raw = response.text
    else:
        # try master branch
        url = f"https://raw.githubusercontent.com/{owner}/{name}/master/README.md"
        response = await client.get(url)
        readme_raw = response.text if response.status_code == 200 else ""
    return {**repo, "readme_raw": readme_raw}


async def download_readmes(repos: list[dict]) -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [_fetch_readme(client, repo) for repo in repos]
        return await asyncio.gather(*tasks)


def preprocess_readmes(repos: list[dict]) -> list[dict]:
    llm = ChatOpenAI(model=PRESUMMARY_MODEL, temperature=0)
    result = []
    for repo in repos:
        raw = repo["readme_raw"]
        if len(raw) > README_THRESHOLD:
            messages = [
                SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
                HumanMessage(content=raw),
            ]
            response = llm.invoke(messages)
            readme_text = response.content
        else:
            readme_text = raw
        result.append({**repo, "readme_text": readme_text})
    return result


def run_ingestion() -> list[dict]:
    repos = fetch_trending_repos()
    repos_with_readmes = asyncio.run(download_readmes(repos))
    return preprocess_readmes(repos_with_readmes)
