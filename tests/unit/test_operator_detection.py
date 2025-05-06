import os
import pytest
from bot.operator_detection import analyze_repository, save_results

@pytest.fixture
def mock_repo(tmp_path):
    """
    Creates a mock repository with Python files for testing.
    """
    repo_path = tmp_path / "mock_repo"
    repo_path.mkdir()

    # Create mock Python files
    file1 = repo_path / "file1.py"
    file1.write_text("a + b\nc == d\n")

    file2 = repo_path / "file2.py"
    file2.write_text("x - y\nz != w\n")

    return repo_path


def test_analyze_repository(mock_repo):
    """
    Test the analyze_repository function.
    """
    results = analyze_repository(mock_repo)
    assert len(results) == 2  # Two files should be analyzed
    assert "arithmetic_issues" in results[str(mock_repo / "file1.py")]
    assert "comparison_issues" in results[str(mock_repo / "file1.py")]


def test_save_results(mock_repo, tmp_path):
    """
    Test the save_results function.
    """
    results = analyze_repository(mock_repo)
    output_dir = tmp_path / "results"
    save_results("mock_repo", results, output_dir)

    output_file = output_dir / "mock_repo_results.txt"
    assert output_file.exists()

    # Verify the contents of the output file
    with open(output_file, "r") as f:
        content = f.read()
        assert "Arithmetic issues:" in content
        assert "Comparison issues:" in content
