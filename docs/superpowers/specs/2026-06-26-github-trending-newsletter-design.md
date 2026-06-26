# Design: GitHub Trending Newsletter

**Date:** 2026-06-26  
**Status:** Approved

---

## Overview

A serverless, automated system that fetches the 25 weekly trending GitHub repositories, analyzes their READMEs via an LLM map-reduce pipeline, and delivers a weekly editorial report (identifying niches, business opportunities, and hidden gems) to a static list of recipients via email.

Runs every Friday via GitHub Actions cron job. No persistent storage between runs.

---

## Project Structure

```
github-trending-newsletter/
├── .github/
│   └── workflows/
│       └── newsletter.yml      # Cron job (every Friday 08:00 UTC)
├── src/
│   ├── ingestion.py            # gtrending fetch + httpx async README download
│   ├── processing.py           # LangChain map-reduce (GPT-4o-mini → GPT-4o)
│   └── delivery.py             # Resend email dispatch
├── main.py                     # Sequential orchestrator
├── prompts.py                  # All LLM prompts isolated from logic
├── requirements.txt
├── .env.example
└── .gitignore
```

`prompts.py` is intentionally separate: prompt engineering is the most frequently iterated part of the system and should not require touching business logic.

---

## Data Flow

```
gtrending (weekly, all languages, 25 repos)
    │
    ▼
[Repo list: name, url, description, stars]
    │
    ▼ httpx async (25 parallel requests)
[Raw README text per repo]
    │
    ▼ if len > 3000 chars → GPT-4o-mini summary, else keep as-is
[25 normalized texts]
    │
    ▼ LangChain .abatch() → GPT-4o-mini (map)
[25 structured mini-cards: problem, stack, target]
    │
    ▼ concatenate into single context
    ▼ LangChain invoke → GPT-4o (reduce)
[HTML report: patterns, niches, hidden gems]
    │
    ▼ Resend API
[Email to recipients]
```

Pre-processing (summarizing long READMEs) happens **before** the LangChain Map phase, not inside it. This avoids calling GPT-4o-mini twice on the same text and keeps the Map phase clean.

---

## Module Responsibilities

### `ingestion.py`
- Fetch 25 weekly trending repos via `gtrending`
- Download READMEs asynchronously via `httpx` + `asyncio`
- Pre-process: if README > 3000 chars, call GPT-4o-mini to summarize; otherwise keep as-is
- Return list of dicts: `{name, url, description, stars, readme_text}`

### `processing.py`
- Receive list of repo dicts from ingestion
- Map phase: LangChain `.abatch()` with GPT-4o-mini → structured mini-card per repo
- Reduce phase: LangChain invoke with GPT-4o → final HTML report
- Return HTML string

### `delivery.py`
- Receive HTML string
- Read `RECIPIENTS` from environment (comma-separated)
- Send email via Resend SDK
- Return send result

### `main.py`
- Load `.env` (python-dotenv)
- Call `ingestion → processing → delivery` in sequence
- Log progress at each step

### `prompts.py`
- `SUMMARY_SYSTEM_PROMPT`: for README pre-summarization
- `MAP_SYSTEM_PROMPT`: for mini-card extraction
- `REDUCE_SYSTEM_PROMPT`: for editorial report generation

---

## Error Handling

| Scenario | Behavior |
|---|---|
| Repo has no README | Include repo using name + description only, skip README text |
| Single LLM call fails during map | Skip that repo, continue with remaining |
| Full job failure (API down, email error) | GitHub Actions marks run as failed, owner notified automatically |

No retry logic or circuit breaker — weekly cadence makes this unnecessary complexity.

---

## Configuration

### Environment Variables (`.env` / GitHub Secrets)

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key |
| `RESEND_API_KEY` | Resend API key |
| `SENDER_EMAIL` | Verified sender address on Resend |
| `RECIPIENTS` | Comma-separated recipient emails |

### Constants (hardcoded in source)

| Constant | Value | Location |
|---|---|---|
| `README_THRESHOLD` | 3000 chars | `ingestion.py` |
| `PRESUMMARY_MODEL` | `gpt-4o-mini` | `ingestion.py` |
| `MAP_MODEL` | `gpt-4o-mini` | `processing.py` |
| `REDUCE_MODEL` | `gpt-4o` | `processing.py` |
| `TRENDING_PERIOD` | `weekly` | `ingestion.py` |
| `NUM_REPOS` | 25 | `ingestion.py` |

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Trending data | `gtrending` |
| HTTP client | `httpx` + `asyncio` |
| LLM orchestration | `langchain`, `langchain-openai` |
| Models | GPT-4o-mini (map + pre-summary), GPT-4o (reduce) |
| Email delivery | `resend` SDK |
| Automation | GitHub Actions (free tier) |
| Secrets (local) | `python-dotenv` |

---

## GitHub Actions Workflow

- Trigger: `schedule` cron `0 8 * * 5` (every Friday 08:00 UTC) + `workflow_dispatch` (manual run)
- Runner: `ubuntu-latest`
- Steps: checkout → setup Python 3.11 → install deps → run `main.py`
- Secrets injected as env vars at runtime

---

## Future Scalability Vectors

- **New sources:** Add loaders in `ingestion.py` (HN, Reddit, arXiv) and append to the repo list before the map phase
- **RAG / memory:** Send map-phase mini-cards to a vector DB (Pinecone/Chroma) for cross-week trend comparison
- **Dynamic recipients:** Replace env var parsing in `delivery.py` with a DB lookup (Supabase/Firebase)
