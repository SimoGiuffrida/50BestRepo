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

@pytest.mark.asyncio
async def test_download_readmes_falls_back_to_master_branch():
    """Verifies fallback: main returns 404, master returns 200."""
    repos = [{"name": "user/repo", "url": "https://github.com/user/repo", "description": "d", "stars": 5}]

    main_404 = MagicMock()
    main_404.status_code = 404

    master_200 = MagicMock()
    master_200.status_code = 200
    master_200.text = "# Master README"

    with patch("src.ingestion.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=[main_404, master_200])
        mock_client_class.return_value = mock_client

        result = await download_readmes(repos)

    assert result[0]["readme_raw"] == "# Master README"

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
