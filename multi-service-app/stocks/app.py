import os
from flask import Flask, request, jsonify
from functools import wraps
from stocksManager import StocksManager
from Exceptions import *
import threading

app = Flask(__name__)
stocks_manager = StocksManager()  # Create an instance of the StocksManager
lock = threading.Lock()

def require_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.content_type != 'application/json':
            raise UnsupportedContentType()
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, StockNotFoundError):
        return jsonify({"error": "Not found"}), 404
    elif isinstance(e, RequiredFieldMissingError) or isinstance(e, InvalidFieldError):
        return jsonify({"error": "Malformed data"}), 400
    elif isinstance(e, DuplicateStockError):
        return jsonify({"error": "Stock with the same symbol already exists"}), 400
    elif isinstance(e, UnsupportedContentType):
        return jsonify({"error": "Expected application/json media type"}), 415
    return jsonify({"server error": str(e)}), 500

@app.get('/stocks')
def get_stocks():
    query_params = request.args.to_dict()
    with lock:
        stocks = stocks_manager.get_stocks(query_params)
    return jsonify(stocks), 200

@app.post('/stocks')
@require_json
def add_stock():
    stockData = request.get_json()
    with lock:
        result = stocks_manager.add_stock(stockData)
    return jsonify(result), 201

@app.get('/stocks/<stock_id>')
def get_stock(stock_id):
    with lock:
        stock = stocks_manager.get_stock(stock_id)
    return jsonify(stock), 200

@app.delete('/stocks/<stock_id>')
def delete_stock(stock_id):
    with lock:
        stocks_manager.delete_stock(stock_id)
    return '', 204

@app.put('/stocks/<stock_id>')
@require_json
def update_stock(stock_id):
    stockData = request.get_json()
    with lock:
        result = stocks_manager.update_stock(stockData, stock_id)
    return jsonify(result), 200

@app.get('/stock-value/<stock_id>')
def get_stock_value(stock_id):
    with lock:
        stock_value = stocks_manager.get_stock_value(stock_id)
    return jsonify(stock_value), 200

@app.get('/portfolio-value')
def get_portfolio_value():
    with lock:
        portfolio_value = stocks_manager.get_portfolio_value()
    return jsonify(portfolio_value), 200

@app.get('/kill')
def kill_container():
    os._exit(1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)