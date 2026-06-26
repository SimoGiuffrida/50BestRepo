import asyncio
import datetime
import os
import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import SUMMARY_SYSTEM_PROMPT

README_THRESHOLD = 3000
PRESUMMARY_MODEL = "gpt-4o-mini"
NUM_REPOS = 25
DAYS_AGO = 7


def fetch_trending_repos() -> list[dict]:
    date_start = (datetime.date.today() - datetime.timedelta(days=DAYS_AGO)).strftime("%Y-%m-%d")
    url = (
        f"https://api.github.com/search/repositories"
        f"?q=created:>{date_start}&sort=stars&order=desc&per_page={NUM_REPOS}"
    )
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    response = httpx.get(url, headers=headers, timeout=15.0)
    response.raise_for_status()
    items = response.json().get("items", [])

    return [
        {
            "name": repo["full_name"],
            "url": repo["html_url"],
            "description": repo.get("description") or "",
            "stars": repo["stargazers_count"],
        }
        for repo in items
    ]


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
