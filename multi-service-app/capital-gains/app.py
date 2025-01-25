from flask import Flask, request, jsonify
import capitalGains

app = Flask(__name__)
from Core.Exceptions import *

@app.get('/capital-gains')
def get_capital_gains():
    query_params = request.args.to_dict()
    return jsonify(capitalGains.get_capital_gains(query_params)) , 200

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, InvalidQueryParameterError):
        return jsonify({"error": "Invalid query parameter"}), 400
    return jsonify({"server error": str(e)}), 500

if __name__ == '__main__':
    print("Running stocks manager app")
    app.run(host='0.0.0.0', port=8080)