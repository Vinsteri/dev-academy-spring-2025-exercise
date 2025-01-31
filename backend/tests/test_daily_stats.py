# tests/test_daily_stats.py

import subprocess
import json
import pytest
from pathlib import Path

def curl_get(url):
    cmd = [
        "curl",
        "-X", "GET",
        url,
        "-H", "accept: application/json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

@pytest.mark.integration
def test_daily_stats_endpoint():
    """Test the /api/daily-stats endpoint response against an expected JSON file."""

    # 1. Run curl via curl_get function
    result = curl_get("http://localhost:8000/api/daily-stats")

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
    expected_file = Path(__file__).parent / "expected" / "daily_stats.json"
    with open(expected_file, "r", encoding="utf-8") as f:
        expected_data = json.load(f)

    # 5. Compare for exact match
    #    If you have dynamic fields (e.g. timestamps), you might want to do partial checks
    assert response_data == expected_data, \
           "The actual response from /daily-stats does not match the expected JSON."


@pytest.mark.integration
def test_daily_stats_2024_09_28():

    # 1. Run curl via curl_get function
    result = curl_get("http://localhost:8000/api/daily-stats/2024-09-28")

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
    expected_file = Path(__file__).parent / "expected" / "daily_stats_2024_09_28.json"
    with open(expected_file, "r", encoding="utf-8") as f:
        expected_data = json.load(f)

    # 5. Compare for exact match
    #    If you have dynamic fields (e.g. timestamps), you might want to do partial checks
    assert response_data == expected_data, \
           "The actual response from /daily-stats/2024-09-28 does not match the expected JSON."
