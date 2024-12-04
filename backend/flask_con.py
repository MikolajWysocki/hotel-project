from flask import Flask, jsonify, request

app = Flask(__name__)

# Przykładowa trasa (endpoint)
@app.route('/api/reservations', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from backend!', 'data': [1, 2, 3]})

@app.route('/api/reservations', methods=['POST'])
def post_data():
    received_data = request.json
    return jsonify({'received': received_data, 'status': 'success'})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()