# tests/test_daily_stats.py

import subprocess
import json
import pytest
from pathlib import Path


def curl_get(url):
    cmd = ["curl", "-X", "GET", url, "-H", "accept: application/json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def daily_stats_endpoint(url, expected_file):
    # 1. Run curl via curl_get function
    result = curl_get(url)

    # 2. Check if curl encountered an error
    if result.returncode != 0:
        # Print stderr for debugging
        print("Error output:", result.stderr)
        pytest.fail("Curl command failed to execute.")

    # 3. Parse the response JSON
    try:
        response_data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON. Error: {e}")

    # 4. Load expected JSON from file
    with open(expected_file, "r", encoding="utf-8") as f:
        expected_data = json.load(f)

    # 5. Compare for exact match
    #    If you have dynamic fields (e.g. timestamps), you might want to do partial checks
    assert (
        response_data == expected_data
    ), f"The actual response from {url} does not match the expected JSON."


@pytest.mark.integration
def test_daily_stats_endpoint():
    """Test the /api/daily-stats endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats"
    expected_file = Path(__file__).parent / "expected" / "daily_stats.json"
    daily_stats_endpoint(url, expected_file)


@pytest.mark.integration
def test_daily_stats_2024_09_28():
    """Test the /api/daily-stats/2024-09-28 endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats/2024-09-28"
    expected_file = Path(__file__).parent / "expected" / "daily_stats_2024_09_28.json"
    daily_stats_endpoint(url, expected_file)


@pytest.mark.integration
def test_daily_stats_wrong_date():
    """Test the /api/daily-stats/2024-09-29 endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats/1024-09-29"
    expected_file = Path(__file__).parent / "expected" / "daily_stats_wrong_date.json"
    daily_stats_endpoint(url, expected_file)

@pytest.mark.integration
def test_daily_stats_null_fields():
    """Test the /api/daily-stats/2020-12-31 endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats/2020-12-31"
    expected_file = Path(__file__).parent / "expected" / "daily_stats_null_fields.json"
    daily_stats_endpoint(url, expected_file)


@pytest.mark.integration
def test_daily_stats_unordered_table():
    """Test the /api/daily-stats/2021-01-05 endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats/2021-01-05"
    expected_file = Path(__file__).parent / "expected" / "daily_stats_unordered_table.json"
    daily_stats_endpoint(url, expected_file)
