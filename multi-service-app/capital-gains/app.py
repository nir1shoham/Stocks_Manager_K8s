from flask import Flask, request, jsonify
import capitalGains
from Exceptions import *
import threading

app = Flask(__name__)
lock = threading.Lock()  # Create a lock for thread safety

@app.get('/capital-gains')
def get_capital_gains():
    query_params = request.args.to_dict()
    with lock:
        result = capitalGains.get_capital_gains(query_params)
    return jsonify(result), 200

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, InvalidQueryParameterError):
        return jsonify({"error": "Invalid query parameter"}), 400
    return jsonify({"server error": str(e)}), 500

if __name__ == '__main__':
    print("Running capital gains app")
    app.run(host='0.0.0.0', port=8080)