# tests/test_daily_stats.py

import requests
import json
import pytest
from pathlib import Path


def daily_stats_endpoint(url, expected_file):
    # 1. Run GET request via requests library
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")

    # 2. Parse the response JSON
    try:
        response_data = response.json()
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON. Error: {e}")

    # 3. Load expected JSON from file
    with open(expected_file, "r", encoding="utf-8") as f:
        expected_data = json.load(f)

    # 4. Compare for exact match
    #    If you have dynamic fields (e.g. timestamps), you might want to do partial checks
    assert (
        response_data == expected_data
    ), f"The actual response from {url} does not match the expected JSON."


def daily_stats_endpoint_expected_to_fail(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return
    pytest.fail(f"Request should have failed but it succeeded")



def test_daily_stats_endpoint():
    """Test the /api/daily-stats endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats"
    expected_file = Path(__file__).parent / "expected" / "daily_stats.json"
    daily_stats_endpoint(url, expected_file)



def test_daily_stats_2024_09_28():
    """Test the /api/daily-stats/2024-09-28 endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats/2024-09-28"
    expected_file = Path(__file__).parent / "expected" / "daily_stats_2024_09_28.json"
    daily_stats_endpoint(url, expected_file)



def test_daily_stats_wrong_date():
    """Test the /api/daily-stats/2024-09-29 endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats/1024-09-29"
    daily_stats_endpoint_expected_to_fail(url)



def test_daily_stats_null_fields():
    """Test the /api/daily-stats/2020-12-31 endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats/2020-12-31"
    expected_file = Path(__file__).parent / "expected" / "daily_stats_null_fields.json"
    daily_stats_endpoint(url, expected_file)



def test_daily_stats_unordered_table():
    """Test the /api/daily-stats/2021-01-05 endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats/2021-01-05"
    expected_file = (
        Path(__file__).parent / "expected" / "daily_stats_unordered_table.json"
    )
    daily_stats_endpoint(url, expected_file)



def test_daily_stats_search_no_result():
    """Test the /api/daily-stats&search= endpoint response against an expected JSON file."""
    url = "http://localhost:8000/api/daily-stats?&search=nonsense"
    expected_file = (
        Path(__file__).parent / "expected" / "daily_stats_empty_response.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_search_2024_09_28():
    url = "http://localhost:8000/api/daily-stats?&search=2024-09-28"
    expected_file = (
        Path(__file__).parent / "expected" / "daily_stats_search_2024_09_28.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_search_24h_negative_streak():
    url = "http://localhost:8000/api/daily-stats?&search=2023-08-08"
    expected_file = (
        Path(__file__).parent / "expected" / "daily_stats_search_2023_08_08.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_search_19h_negative_streak():
    url = "http://localhost:8000/api/daily-stats?&search=2023-10-15"
    expected_file = (
        Path(__file__).parent / "expected" / "daily_stats_search_2023_10_15.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_sort_date_desc():
    url = "http://localhost:8000/api/daily-stats?sort=date&direction=desc"
    expected_file = (
        Path(__file__).parent / "expected" / "daily_stats_sort_date_desc.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_search_jan_first_avg_price_asc():
    url = "http://localhost:8000/api/daily-stats?&search=01-01&sort=average_price&direction=asc"
    expected_file = (
        Path(__file__).parent
        / "expected"
        / "daily_stats_search_jan_first_avg_price_asc.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_search_xmas_production_asc():
    url = "http://localhost:8000/api/daily-stats?&search=12-24&sort=total_production&direction=asc"
    expected_file = (
        Path(__file__).parent
        / "expected"
        / "daily_stats_search_xmas_production_asc.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_10_first_results():
    url = "http://localhost:8000/api/daily-stats?pageSize=10"
    expected_file = (
        Path(__file__).parent / "expected" / "daily_stats_10_first_results.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_next_10_results():
    url = "http://localhost:8000/api/daily-stats?pageSize=10&page=2"
    expected_file = (
        Path(__file__).parent / "expected" / "daily_stats_next_10_results.json"
    )
    daily_stats_endpoint(url, expected_file)


def test_daily_stats_last_results():
    url = "http://localhost:8000/api/daily-stats?pageSize=10&page=138"
    expected_file = Path(__file__).parent / "expected" / "daily_stats_last_results.json"
    daily_stats_endpoint(url, expected_file)
