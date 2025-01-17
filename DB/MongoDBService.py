from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
from bson import ObjectId
from bson.errors import InvalidId
from Core.Exceptions import StockNotFoundError

uri = "mongodb://mongodb:27017/"
client = MongoClient(uri)
db = client.get_database("portfolio")

def get_stocks(collection, query_params = {}):
    try:
        stocks = list(db[collection].find(query_params))
        return stocks
    except Exception as e:
        raise e

def create_stock(collection, stock_data):
    if get_stock_by_symbol(collection, stock_data['symbol']):
        raise DuplicateKeyError("Stock with the same symbol already exists")
    try:
        stock = db[collection].insert_one(stock_data)
        return stock.inserted_id
    except PyMongoError as e:
        raise Exception(f"Database error: {str(e)}")

def get_stock_by_id(collection, stock_id):
    try:
        stock = db[collection].find_one({"_id": ObjectId(stock_id)})
        if stock:
            stock['_id'] = str(stock['_id'])  # Convert ObjectId to string for API response
        return stock
    except InvalidId:
        # Raise StockNotFoundError for invalid ObjectId
        raise StockNotFoundError("Not found")
    except Exception as e:
        raise e


def get_stock_by_symbol(collection, symbol):
    try:
        stock = list(db[collection].find({"symbol": symbol}))
        return stock
    except Exception as e:
        raise e

def delete_stock(collection, stock_id):
    try:
        return db[collection].delete_one({"_id": ObjectId(stock_id)})
    except Exception as e:
        raise e 
    
def update_stock(collection, stock_data, stock_id):
    try:
        return db[collection].update_one({"_id": ObjectId(stock_id)}, {"$set": stock_data})
    except Exception as e:
        raise e