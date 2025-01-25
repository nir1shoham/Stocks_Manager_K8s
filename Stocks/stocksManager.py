from Core.Exceptions import *
from datetime import datetime
from Core.stockValue import get_stock_price
import os
from pymongo.errors import DuplicateKeyError
from datetime import datetime
import DB.MongoDBService as mongoDBService

STOCKS_FIELDS = ['id', 'symbol', 'name', 'shares', 'purchase price', 'purchase date']

class StocksManager:
    def get_stocks(self, query_params = None):
        """
        Retrieve stocks, optionally filtering by query parameters.

        :param query_params: A dictionary of query parameters to filter the stocks.
        :return: A list of stocks (JSON representation) matching the query parameters.
        """
        query_params = query_params if query_params else {}
        stocks = mongoDBService.get_stocks(query_params)
        for stock in stocks:
            stock["_id"] = str(stock["_id"])  # Convert ObjectId to string
            
        return stocks    

    def add_stock(self, stockData):
        # Validate incoming data
        self.validate_stock_data(stockData, False)
        
        # Add default values for optional fields
        stockData['name'] = stockData.get('name', "NA")
        stockData['purchase date'] = stockData.get('purchase date', "NA")
        stockData['purchase price'] = round(stockData['purchase price'], 2)
        
        try:
            # Insert the stock into MongoDB and retrieve the generated ID
            inserted_id = mongoDBService.create_stock(stockData)
        except DuplicateKeyError:
            # Handle duplicate symbols if a unique index is enforced
            raise DuplicateStockError("Stock with the same symbol already exists")
        except Exception as e:
            # Catch other database-related errors
            raise DatabaseError(f"Failed to add stock: {str(e)}")
        
        # Return the inserted ID as a string
        return {'id': str(inserted_id)}

    def get_stock(self, stock_id):
        return self.get_stock_by_id(stock_id)

    def get_stock_by_id(self, stock_id):
        stock = mongoDBService.get_stock_by_id(stock_id)
        if not stock:
            raise StockNotFoundError("Not found")
        
        stock['_id'] = str(stock['_id'])
        
        return stock

    def delete_stock(self, stock_id):
        try:
            result = mongoDBService.delete_stock(stock_id)
            if result.deleted_count == 0:
                raise StockNotFoundError("Not found")
        except Exception as e:
            raise DatabaseError(f"Failed to delete stock: {str(e)}")

    def update_stock(self, stockData, stock_id):
        self.validate_stock_data(stockData, update=True)
        if stockData.get('id') != stock_id:
            raise RequiredFieldMissingError("Invalid input. Stock ID must match the URL")
        
        stock_symbol = stockData.get('symbol')
        stock = mongoDBService.get_stock_by_symbol(stock_symbol)
        
        # Check if there is any stock with the same symbol but different ID
        for s in stock:
            if str(s["_id"]) != stock_id:
                raise DuplicateStockError("Stock with the same symbol already exists")
        
        stockData.pop('id')
        result = mongoDBService.update_stock(stockData, stock_id)
        if result.matched_count == 0:
            raise StockNotFoundError("Not found")
        
        return self.get_stock_by_id(stock_id)

    def get_today_date(self):
        # Get today's date
        today = datetime.now()
        # Format the date as dd-mm-yyyy
        formatted_date = today.strftime("%d-%m-%Y")
        return formatted_date

    def get_portfolio_value(self):
        stocks = mongoDBService.get_stocks()
        totalValue = 0
        
        for stock in stocks:
            totalValue += stock["shares"] * get_stock_price(stock['symbol'])
            
        return {
            "date": self.get_today_date(),
            "portfolio value": round(totalValue, 2)
        }
    
    def get_stock_value(self, stock_id):
        if not stock_id:
            raise RequiredFieldMissingError("Invalid input. Stock ID must be provided.")
        
        stock = self.get_stock_by_id(stock_id)
        if not stock:
            raise StockNotFoundError("Not found")
        
        price = get_stock_price(stock['symbol'])
        
        return {
            "symbol": stock['symbol'],
            "ticker": price,
            "stock value": stock["shares"] * price
        }
        

    def validate_stock_data(self, data, update=False):
        required_fields = ['symbol', 'shares', 'purchase price'] if not update else STOCKS_FIELDS
        
        # Ensure required fields are present
        for field in required_fields:
            if field not in data or data[field] is None:
                raise RequiredFieldMissingError(f"{field} must be provided.")

        for field, value in data.items():
            # Validate if the field is allowed
            if field not in STOCKS_FIELDS:
                raise InvalidFieldError(f"Invalid field: {field}")

            if field == 'shares':
                # Ensure shares is an integer and is positive
                if not isinstance(value, int) or value < 0:
                    raise InvalidFieldError()

            elif field == 'purchase price':
                # Ensure purchase price is a positive float
                if not isinstance(value, (int, float)):
                    raise InvalidFieldError("Purchase price must be a number")
                if value < 0:
                    raise InvalidFieldError("Purchase price must be a positive number")
                # Convert to float if it's an int
                data['purchase price'] = float(value)

            elif field == 'purchase date':
                # Ensure purchase date is a valid date in the format dd-mm-yyyy
                try:
                    datetime.strptime(value, "%d-%m-%Y")
                except ValueError:
                    raise InvalidFieldError("Invalid purchase date format. Must be dd-mm-yyyy")

            elif field in {'symbol', 'name'}:
                # Ensure symbol and name are strings
                if not isinstance(value, str):
                    raise InvalidFieldError(f"{field.capitalize()} must be a string")
                if field == 'symbol' and not value.isupper():
                    raise InvalidFieldError("Symbol must be uppercase")
