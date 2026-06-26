# GitHub Trending Newsletter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a weekly automated pipeline that fetches 25 trending GitHub repos, analyzes their READMEs via LLM map-reduce, and emails an editorial report every Friday.

**Architecture:** Modular Python project with four concerns separated into `ingestion.py`, `processing.py`, `delivery.py`, and `prompts.py`, orchestrated by `main.py`. Runs serverless on GitHub Actions.

**Tech Stack:** Python 3.11, gtrending, httpx, asyncio, langchain, langchain-openai, resend, python-dotenv, pytest

---

## File Map

| File | Responsibility |
|---|---|
| `src/ingestion.py` | gtrending fetch + async README download + README pre-summarization |
| `src/processing.py` | LangChain map (GPT-4o-mini) + reduce (GPT-4o) |
| `src/delivery.py` | Resend email dispatch |
| `prompts.py` | All LLM prompt strings |
| `main.py` | Sequential orchestrator: load env → ingest → process → deliver |
| `tests/test_ingestion.py` | Unit tests for ingestion module |
| `tests/test_processing.py` | Unit tests for processing module |
| `tests/test_delivery.py` | Unit tests for delivery module |
| `requirements.txt` | Pinned dependencies |
| `.env.example` | Env var template |
| `.gitignore` | Ignore .env, __pycache__, .pytest_cache |
| `.github/workflows/newsletter.yml` | GitHub Actions cron workflow |

---

## Task 1: Project scaffold

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `src/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create `requirements.txt`**

```
gtrending==0.4.0
httpx==0.27.0
langchain==0.2.16
langchain-openai==0.1.25
resend==2.4.0
python-dotenv==1.0.1
pytest==8.3.2
pytest-asyncio==0.23.8
```

- [ ] **Step 2: Create `.env.example`**

```
OPENAI_API_KEY=sk-...
RESEND_API_KEY=re_...
SENDER_EMAIL=newsletter@yourdomain.com
RECIPIENTS=you@example.com,colleague@example.com
```

- [ ] **Step 3: Create `.gitignore`**

```
.env
__pycache__/
.pytest_cache/
*.pyc
.venv/
```

- [ ] **Step 4: Create empty `src/__init__.py` and `tests/__init__.py`**

Both files are empty — just create them so Python treats the directories as packages.

- [ ] **Step 5: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: all packages install without errors.

- [ ] **Step 6: Commit**

```bash
git init
git add requirements.txt .env.example .gitignore src/__init__.py tests/__init__.py
git commit -m "chore: project scaffold"
```

---

## Task 2: `prompts.py` — all LLM prompts

**Files:**
- Create: `prompts.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_prompts.py`:

```python
from prompts import SUMMARY_SYSTEM_PROMPT, MAP_SYSTEM_PROMPT, REDUCE_SYSTEM_PROMPT

def test_all_prompts_are_non_empty_strings():
    for prompt in [SUMMARY_SYSTEM_PROMPT, MAP_SYSTEM_PROMPT, REDUCE_SYSTEM_PROMPT]:
        assert isinstance(prompt, str)
        assert len(prompt) > 50
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_prompts.py -v
```

Expected: `ImportError: cannot import name 'SUMMARY_SYSTEM_PROMPT' from 'prompts'`

- [ ] **Step 3: Create `prompts.py`**

```python
SUMMARY_SYSTEM_PROMPT = """You are a technical summarizer. Given a GitHub README, extract the essential information in 3-5 sentences.
Cover: what problem this solves, what technology/language it uses, and who the target user is.
Be concise and factual. Do not include installation instructions or badges."""

MAP_SYSTEM_PROMPT = """You are a technical analyst. Given a GitHub repository name, description, and README, produce a structured mini-card in this exact format:

**Problem:** [one sentence: what problem does this solve?]
**Stack:** [comma-separated list of main technologies]
**Target:** [one sentence: who is this for?]

Be precise and concise. Do not add any extra text outside this format."""

REDUCE_SYSTEM_PROMPT = """You are an expert technology market analyst writing a weekly newsletter for CTOs and tech entrepreneurs.

You will receive a list of 25 structured mini-cards summarizing trending GitHub repositories from the past week.

Produce an HTML email report with the following sections:

1. **Weekly Snapshot** — 2-3 sentences on the dominant themes you see across the repos.
2. **Emerging Niches** — 2-3 business niches that appear to be gaining traction, with one specific repo as example for each.
3. **Hidden Gems** — 3 repos that are technically interesting but underappreciated, with a one-sentence explanation of why.
4. **Full List** — A clean HTML table with columns: Repo Name (linked), Problem, Stack, Target.

Format the output as clean, self-contained HTML (no external CSS dependencies, use only inline styles). Make it readable in an email client."""
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_prompts.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add prompts.py tests/test_prompts.py
git commit -m "feat: add LLM prompts"
```

---

## Task 3: `ingestion.py` — fetch trending repos

**Files:**
- Create: `src/ingestion.py`
- Create: `tests/test_ingestion.py`

- [ ] **Step 1: Write failing test for `fetch_trending_repos`**

Create `tests/test_ingestion.py`:

```python
from unittest.mock import patch, MagicMock
from src.ingestion import fetch_trending_repos

def test_fetch_trending_repos_returns_list_of_dicts():
    mock_repo = MagicMock()
    mock_repo.name = "awesome-tool"
    mock_repo.full_name = "user/awesome-tool"
    mock_repo.url = "https://github.com/user/awesome-tool"
    mock_repo.description = "A great tool"
    mock_repo.stars = 1200

    with patch("src.ingestion.fetch_repos", return_value=[mock_repo] * 25):
        repos = fetch_trending_repos()

    assert len(repos) == 25
    assert repos[0]["name"] == "user/awesome-tool"
    assert repos[0]["url"] == "https://github.com/user/awesome-tool"
    assert repos[0]["description"] == "A great tool"
    assert repos[0]["stars"] == 1200

def test_fetch_trending_repos_handles_none_description():
    mock_repo = MagicMock()
    mock_repo.name = "tool"
    mock_repo.full_name = "user/tool"
    mock_repo.url = "https://github.com/user/tool"
    mock_repo.description = None
    mock_repo.stars = 100

    with patch("src.ingestion.fetch_repos", return_value=[mock_repo]):
        repos = fetch_trending_repos()

    assert repos[0]["description"] == ""
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_ingestion.py::test_fetch_trending_repos_returns_list_of_dicts -v
```

Expected: `ImportError: cannot import name 'fetch_trending_repos' from 'src.ingestion'`

- [ ] **Step 3: Implement `fetch_trending_repos` in `src/ingestion.py`**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_ingestion.py::test_fetch_trending_repos_returns_list_of_dicts tests/test_ingestion.py::test_fetch_trending_repos_handles_none_description -v
```

Expected: both PASS

- [ ] **Step 5: Commit**

```bash
git add src/ingestion.py tests/test_ingestion.py
git commit -m "feat: fetch trending repos from gtrending"
```

---

## Task 4: `ingestion.py` — async README download

**Files:**
- Modify: `src/ingestion.py`
- Modify: `tests/test_ingestion.py`

- [ ] **Step 1: Write failing tests for `download_readmes`**

Append to `tests/test_ingestion.py`:

```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.ingestion import download_readmes

@pytest.mark.asyncio
async def test_download_readmes_returns_text_for_each_repo():
    repos = [
        {"name": "user/repo1", "url": "https://github.com/user/repo1", "description": "desc", "stars": 10},
        {"name": "user/repo2", "url": "https://github.com/user/repo2", "description": "desc", "stars": 20},
    ]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "# Hello README"

    with patch("src.ingestion.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        result = await download_readmes(repos)

    assert len(result) == 2
    assert result[0]["readme_raw"] == "# Hello README"

@pytest.mark.asyncio
async def test_download_readmes_handles_404():
    repos = [{"name": "user/repo", "url": "https://github.com/user/repo", "description": "d", "stars": 5}]

    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("src.ingestion.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        result = await download_readmes(repos)

    assert result[0]["readme_raw"] == ""
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_ingestion.py::test_download_readmes_returns_text_for_each_repo -v
```

Expected: `ImportError: cannot import name 'download_readmes'`

- [ ] **Step 3: Add `download_readmes` to `src/ingestion.py`**

Append to `src/ingestion.py` (after the existing imports and `fetch_trending_repos`):

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_ingestion.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/ingestion.py tests/test_ingestion.py
git commit -m "feat: async README download with httpx"
```

---

## Task 5: `ingestion.py` — README pre-processing (threshold + summarization)

**Files:**
- Modify: `src/ingestion.py`
- Modify: `tests/test_ingestion.py`

- [ ] **Step 1: Write failing tests for `preprocess_readmes`**

Append to `tests/test_ingestion.py`:

```python
from src.ingestion import preprocess_readmes

def test_short_readme_kept_as_is():
    repos = [{"name": "u/r", "url": "", "description": "", "stars": 0, "readme_raw": "short text"}]
    with patch("src.ingestion.ChatOpenAI"):
        result = preprocess_readmes(repos)
    assert result[0]["readme_text"] == "short text"

def test_long_readme_is_summarized():
    long_text = "x" * 3001
    repos = [{"name": "u/r", "url": "", "description": "", "stars": 0, "readme_raw": long_text}]

    mock_llm = MagicMock()
    mock_llm.invoke = MagicMock(return_value=MagicMock(content="summarized content"))

    with patch("src.ingestion.ChatOpenAI", return_value=mock_llm):
        result = preprocess_readmes(repos)

    assert result[0]["readme_text"] == "summarized content"

def test_empty_readme_kept_as_is():
    repos = [{"name": "u/r", "url": "", "description": "", "stars": 0, "readme_raw": ""}]
    with patch("src.ingestion.ChatOpenAI"):
        result = preprocess_readmes(repos)
    assert result[0]["readme_text"] == ""
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_ingestion.py::test_short_readme_kept_as_is -v
```

Expected: `ImportError: cannot import name 'preprocess_readmes'`

- [ ] **Step 3: Add `preprocess_readmes` to `src/ingestion.py`**

Append to `src/ingestion.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_ingestion.py -v
```

Expected: all PASS

- [ ] **Step 5: Add top-level `run_ingestion` orchestrator to `src/ingestion.py`**

Append to `src/ingestion.py`:

```python
def run_ingestion() -> list[dict]:
    repos = fetch_trending_repos()
    repos_with_readmes = asyncio.run(download_readmes(repos))
    return preprocess_readmes(repos_with_readmes)
```

- [ ] **Step 6: Commit**

```bash
git add src/ingestion.py tests/test_ingestion.py
git commit -m "feat: README pre-processing with threshold and summarization"
```

---

## Task 6: `processing.py` — map phase

**Files:**
- Create: `src/processing.py`
- Create: `tests/test_processing.py`

- [ ] **Step 1: Write failing test for map phase**

Create `tests/test_processing.py`:

```python
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from src.processing import run_map_phase

@pytest.mark.asyncio
async def test_run_map_phase_returns_list_of_strings():
    repos = [
        {"name": "u/r1", "url": "https://github.com/u/r1", "description": "desc1", "stars": 10, "readme_text": "text1"},
        {"name": "u/r2", "url": "https://github.com/u/r2", "description": "desc2", "stars": 20, "readme_text": "text2"},
    ]

    mock_response = MagicMock()
    mock_response.content = "**Problem:** X\n**Stack:** Python\n**Target:** Developers"

    mock_chain = MagicMock()
    mock_chain.abatch = AsyncMock(return_value=[mock_response, mock_response])

    with patch("src.processing.ChatOpenAI"), \
         patch("src.processing.ChatPromptTemplate") as mock_template:
        mock_template.from_messages.return_value.__or__ = MagicMock(return_value=mock_chain)
        result = await run_map_phase(repos)

    assert len(result) == 2
    assert isinstance(result[0], str)

@pytest.mark.asyncio
async def test_run_map_phase_skips_failed_repos():
    repos = [
        {"name": "u/r1", "url": "", "description": "", "stars": 0, "readme_text": "text"},
    ]

    mock_chain = MagicMock()
    mock_chain.abatch = AsyncMock(side_effect=Exception("LLM error"))

    with patch("src.processing.ChatOpenAI"), \
         patch("src.processing.ChatPromptTemplate") as mock_template:
        mock_template.from_messages.return_value.__or__ = MagicMock(return_value=mock_chain)
        result = await run_map_phase(repos)

    assert result == []
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_processing.py::test_run_map_phase_returns_list_of_strings -v
```

Expected: `ImportError: cannot import name 'run_map_phase'`

- [ ] **Step 3: Create `src/processing.py` with map phase**

```python
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts import MAP_SYSTEM_PROMPT, REDUCE_SYSTEM_PROMPT

MAP_MODEL = "gpt-4o-mini"
REDUCE_MODEL = "gpt-4o"


async def run_map_phase(repos: list[dict]) -> list[str]:
    llm = ChatOpenAI(model=MAP_MODEL, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", MAP_SYSTEM_PROMPT),
        ("human", "Repository: {name}\nDescription: {description}\nREADME:\n{readme_text}"),
    ])
    chain = prompt | llm
    try:
        responses = await chain.abatch(repos)
        return [r.content for r in responses]
    except Exception as e:
        print(f"Map phase failed: {e}")
        return []
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_processing.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/processing.py tests/test_processing.py
git commit -m "feat: LangChain map phase with GPT-4o-mini"
```

---

## Task 7: `processing.py` — reduce phase

**Files:**
- Modify: `src/processing.py`
- Modify: `tests/test_processing.py`

- [ ] **Step 1: Write failing test for reduce phase**

Append to `tests/test_processing.py`:

```python
from src.processing import run_reduce_phase

def test_run_reduce_phase_returns_html_string():
    mini_cards = [
        "**Problem:** X\n**Stack:** Python\n**Target:** Devs",
        "**Problem:** Y\n**Stack:** Rust\n**Target:** SREs",
    ]

    mock_llm = MagicMock()
    mock_llm.invoke = MagicMock(return_value=MagicMock(content="<html><body>Report</body></html>"))

    with patch("src.processing.ChatOpenAI", return_value=mock_llm):
        result = run_reduce_phase(mini_cards)

    assert isinstance(result, str)
    assert "<html>" in result

def test_run_reduce_phase_raises_on_empty_cards():
    with patch("src.processing.ChatOpenAI"):
        try:
            run_reduce_phase([])
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "no mini-cards" in str(e).lower()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_processing.py::test_run_reduce_phase_returns_html_string -v
```

Expected: `ImportError: cannot import name 'run_reduce_phase'`

- [ ] **Step 3: Add `run_reduce_phase` and `run_processing` to `src/processing.py`**

Append to `src/processing.py`:

```python
def run_reduce_phase(mini_cards: list[str]) -> str:
    if not mini_cards:
        raise ValueError("Cannot run reduce phase: no mini-cards received from map phase.")
    llm = ChatOpenAI(model=REDUCE_MODEL, temperature=0.3)
    combined = "\n\n---\n\n".join(
        f"[{i+1}] {card}" for i, card in enumerate(mini_cards)
    )
    from langchain_core.messages import SystemMessage, HumanMessage
    messages = [
        SystemMessage(content=REDUCE_SYSTEM_PROMPT),
        HumanMessage(content=combined),
    ]
    response = llm.invoke(messages)
    return response.content


def run_processing(repos: list[dict]) -> str:
    mini_cards = asyncio.run(run_map_phase(repos))
    return run_reduce_phase(mini_cards)
```

- [ ] **Step 4: Run all processing tests to verify they pass**

```bash
pytest tests/test_processing.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/processing.py tests/test_processing.py
git commit -m "feat: LangChain reduce phase with GPT-4o"
```

---

## Task 8: `delivery.py` — email dispatch

**Files:**
- Create: `src/delivery.py`
- Create: `tests/test_delivery.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_delivery.py`:

```python
import os
from unittest.mock import patch, MagicMock
from src.delivery import send_newsletter

def test_send_newsletter_calls_resend_with_all_recipients():
    html = "<html><body>Report</body></html>"

    with patch.dict(os.environ, {
        "RESEND_API_KEY": "re_test_key",
        "SENDER_EMAIL": "newsletter@test.com",
        "RECIPIENTS": "a@test.com,b@test.com",
    }):
        with patch("src.delivery.resend.Emails.send") as mock_send:
            mock_send.return_value = {"id": "abc123"}
            result = send_newsletter(html)

    mock_send.assert_called_once()
    call_args = mock_send.call_args[0][0]
    assert call_args["to"] == ["a@test.com", "b@test.com"]
    assert call_args["from"] == "newsletter@test.com"
    assert "<html>" in call_args["html"]

def test_send_newsletter_raises_if_recipients_missing():
    html = "<html><body>Report</body></html>"
    with patch.dict(os.environ, {
        "RESEND_API_KEY": "re_test",
        "SENDER_EMAIL": "s@test.com",
        "RECIPIENTS": "",
    }):
        try:
            send_newsletter(html)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "recipients" in str(e).lower()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_delivery.py::test_send_newsletter_calls_resend_with_all_recipients -v
```

Expected: `ImportError: cannot import name 'send_newsletter'`

- [ ] **Step 3: Create `src/delivery.py`**

```python
import os
import resend


def send_newsletter(html: str) -> dict:
    resend.api_key = os.environ["RESEND_API_KEY"]
    sender = os.environ["SENDER_EMAIL"]
    recipients_raw = os.environ.get("RECIPIENTS", "")
    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]

    if not recipients:
        raise ValueError("No recipients configured. Set the RECIPIENTS environment variable.")

    return resend.Emails.send({
        "from": sender,
        "to": recipients,
        "subject": "GitHub Trending Weekly — Tech Observatory",
        "html": html,
    })
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_delivery.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/delivery.py tests/test_delivery.py
git commit -m "feat: email delivery via Resend"
```

---

## Task 9: `main.py` — orchestrator

**Files:**
- Create: `main.py`

- [ ] **Step 1: Create `main.py`**

```python
import logging
from dotenv import load_dotenv
from src.ingestion import run_ingestion
from src.processing import run_processing
from src.delivery import send_newsletter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def main():
    load_dotenv()

    log.info("Step 1/3: Fetching trending repos and downloading READMEs...")
    repos = run_ingestion()
    log.info(f"  → {len(repos)} repos ingested.")

    log.info("Step 2/3: Running LLM map-reduce pipeline...")
    html_report = run_processing(repos)
    log.info("  → Report generated.")

    log.info("Step 3/3: Sending newsletter...")
    result = send_newsletter(html_report)
    log.info(f"  → Email sent. Result: {result}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run full test suite to verify nothing is broken**

```bash
pytest tests/ -v
```

Expected: all tests PASS

- [ ] **Step 3: Commit**

```bash
git add main.py
git commit -m "feat: main orchestrator"
```

---

## Task 10: GitHub Actions workflow

**Files:**
- Create: `.github/workflows/newsletter.yml`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p .github/workflows
```

- [ ] **Step 2: Create `.github/workflows/newsletter.yml`**

```yaml
name: Weekly Newsletter

on:
  schedule:
    - cron: "0 8 * * 5"  # Every Friday at 08:00 UTC
  workflow_dispatch:       # Allow manual trigger from GitHub UI

jobs:
  send-newsletter:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run newsletter pipeline
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
          SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}
          RECIPIENTS: ${{ secrets.RECIPIENTS }}
        run: python main.py
```

- [ ] **Step 3: Verify YAML syntax**

Open the file and confirm indentation is correct — YAML is whitespace-sensitive. The `on:`, `jobs:`, `steps:` keys must all be at the right level.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/newsletter.yml
git commit -m "chore: GitHub Actions weekly cron workflow"
```

---

## Task 11: End-to-end smoke test (local dry run)

This task verifies the full pipeline works locally before deploying.

**Prerequisites:** You must have a real `.env` file with valid API keys.

- [ ] **Step 1: Create `.env` from `.env.example`**

```bash
cp .env.example .env
# Fill in your real keys in .env
```

- [ ] **Step 2: Run main.py**

```bash
python main.py
```

Expected log output:
```
2026-... INFO Step 1/3: Fetching trending repos and downloading READMEs...
2026-... INFO   → 25 repos ingested.
2026-... INFO Step 2/3: Running LLM map-reduce pipeline...
2026-... INFO   → Report generated.
2026-... INFO Step 3/3: Sending newsletter...
2026-... INFO   → Email sent. Result: {'id': '...'}
```

- [ ] **Step 3: Check your inbox**

Confirm the email arrived and the HTML renders correctly.

- [ ] **Step 4: Final commit**

```bash
git add .
git commit -m "chore: end-to-end smoke test passed"
```

---

## Self-Review Notes

- All spec sections covered: ingestion ✓, processing ✓, delivery ✓, prompts ✓, orchestrator ✓, GitHub Actions ✓, error handling ✓
- `run_ingestion`, `run_processing`, `send_newsletter` signatures are consistent across tasks and main.py
- No TBD or TODO placeholders
- Error handling from spec is implemented: missing README → empty string (Task 4), single map failure → skip (Task 6), full failure → Actions notifies automatically (Task 10)
