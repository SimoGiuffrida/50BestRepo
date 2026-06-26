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
