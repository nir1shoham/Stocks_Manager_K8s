from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
from bson import ObjectId
from bson.errors import InvalidId
from Core.Exceptions import StockNotFoundError

uri = "mongodb://db-service.stocks-manager.svc.cluster.local:27017/"
client = MongoClient(uri)
COLLECTION_NAME = "stocks"
db = client[COLLECTION_NAME]


def get_stocks(query_params = {}):
    try:
        stocks = list(db[COLLECTION_NAME].find(query_params))
        return stocks
    except Exception as e:
        raise e

def create_stock(stock_data):
    if get_stock_by_symbol(stock_data['symbol']):
        raise DuplicateKeyError("Stock with the same symbol already exists")
    try:
        stock = db[COLLECTION_NAME].insert_one(stock_data)
        return stock.inserted_id
    except PyMongoError as e:
        raise Exception(f"Database error: {str(e)}")

def get_stock_by_id(stock_id):
    try:
        stock = db[COLLECTION_NAME].find_one({"_id": ObjectId(stock_id)})
        if stock:
            stock['_id'] = str(stock['_id'])  # Convert ObjectId to string for API response
        return stock
    except InvalidId:
        # Raise StockNotFoundError for invalid ObjectId
        raise StockNotFoundError("Not found")
    except Exception as e:
        raise e


def get_stock_by_symbol(symbol):
    try:
        stock = list(db[COLLECTION_NAME].find({"symbol": symbol}))
        return stock
    except Exception as e:
        raise e

def delete_stock(stock_id):
    try:
        return db[COLLECTION_NAME].delete_one({"_id": ObjectId(stock_id)})
    except Exception as e:
        raise e 
    
def update_stock(stock_data, stock_id):
    try:
        return db[COLLECTION_NAME].update_one({"_id": ObjectId(stock_id)}, {"$set": stock_data})
    except Exception as e:
        raise e