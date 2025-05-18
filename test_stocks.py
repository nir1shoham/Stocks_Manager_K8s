import os
import time
import pytest
import requests

BASE_URL = os.getenv("STOCKS_API_URL", "http://localhost")

@pytest.fixture
def apple_stock():
    return {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "shares": 100,
        "purchase price": 150.0,
        "purchase date": "18-10-2024"
        
    }

@pytest.fixture
def google_stock():
    return {
        "symbol": "GOOG",
        "name": "Google LLC",
        "shares": 20,
        "purchase price": 1200.0,
        "purchase date": "18-10-2024"
    }

@pytest.fixture
def microsoft_stock():
    return {
        "symbol": "MSFT",
        "name": "Microsoft Corp.",
        "shares": 50,
        "purchase price": 300.0,
        "purchase date": "18-10-2024"
    }

@pytest.mark.order(1)
def test_add_and_del_stock(apple_stock):
    resp1 = requests.post(f"{BASE_URL}/stocks", json=apple_stock)
    time.sleep(1)
    assert resp1.status_code == 201
    data = resp1.json()
    stock_id = data.get("id", apple_stock["symbol"])
    
    resp2 = requests.delete(f"{BASE_URL}/stocks/{stock_id}")
    assert resp2.status_code == 204
    time.sleep(1)

@pytest.mark.order(2)
def test_get_all_stocks():
    resp = requests.get(f"{BASE_URL}/stocks")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    time.sleep(1)

@pytest.mark.order(3)
def test_get_single_stock(apple_stock):
    resp1 = requests.post(f"{BASE_URL}/stocks", json=apple_stock)
    time.sleep(1)
    assert resp1.status_code == 201
    data = resp1.json()
    stock_id = data.get("id", apple_stock["symbol"])
    
    resp = requests.get(f"{BASE_URL}/stocks/{stock_id}")
    assert resp.status_code == 200
    assert resp.json()["symbol"] == apple_stock["symbol"]
    requests.delete(f"{BASE_URL}/stocks/{stock_id}")
    time.sleep(1)
@pytest.mark.order(4)

def test_update_stock(apple_stock):
    resp = requests.post(f"{BASE_URL}/stocks", json=apple_stock)
    time.sleep(1)
    assert resp.status_code == 201
    data = resp.json()
    stock_id = data.get("id", apple_stock["symbol"])

    updated = apple_stock.copy()
    updated.pop("_id", None)  # Remove _id if exists (safe)
    updated["id"] = stock_id
    updated["shares"] = 200

    resp = requests.put(f"{BASE_URL}/stocks/{stock_id}", json=updated)
    assert resp.status_code == 200
    assert resp.json()["shares"] == 200
    requests.delete(f"{BASE_URL}/stocks/{stock_id}")
    time.sleep(1)

@pytest.mark.order(5)
def test_portfolio_value(google_stock):
    requests.post(f"{BASE_URL}/stocks", json=google_stock)
    time.sleep(1)
    resp = requests.get(f"{BASE_URL}/portfolio-value")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, dict)
    assert "portfolio value" in data
    assert isinstance(data["portfolio value"], float)
    time.sleep(1)

@pytest.mark.order(6)
def test_stock_value(microsoft_stock):
    resp = requests.post(f"{BASE_URL}/stocks", json=microsoft_stock)
    time.sleep(1)
    assert resp.status_code == 201
    data = resp.json()
    stock_id = data.get("id", microsoft_stock["symbol"])

    resp = requests.get(f"{BASE_URL}/stock-value/{stock_id}")
    assert resp.status_code == 200
    value = resp.json()["stock value"]
    assert value > 0
    requests.delete(f"{BASE_URL}/stocks/{stock_id}")
    time.sleep(1)

@pytest.mark.order(7)
def test_delete_all():
    resp = requests.get(f"{BASE_URL}/stocks")
    resp.raise_for_status()
    data = resp.json()
    response_list = []
    for stock in data:
        stock_id = stock.get("id") or stock.get("_id")
        if stock_id:
            del_resp = requests.delete(f"{BASE_URL}/stocks/{stock_id}")
            response_list.append(del_resp.status_code)
            print(f"Deleted {stock_id}: {del_resp.status_code}")
        else:
            print(f"Skipped stock (no id): {stock}")
    assert all(code == 204 for code in response_list)
