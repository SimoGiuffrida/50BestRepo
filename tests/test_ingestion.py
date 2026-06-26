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
