import requests
from Core.Exceptions import *

def get_stock_price(symbol):
    api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
    response = requests.get(api_url, headers={'X-Api-Key': 'peWnazBtxCHAPRycoAEieg==GPY29SAAvj4oRqYI'})
    if not response or response.status_code != 200:
        raise ExternalAPIServiceError(f"API response code {response.status_code}")
    
    response_json = response.json()
    if isinstance(response_json, list) or 'price' not in response_json:
        raise StockNotFoundError("Stock not found")
   
    return response_json.get('price')