# server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище данных и счётчик ID
items = []
next_id = 1

def find_item(item_id):
    """Вспомогательная функция для поиска элемента по id."""
    return next((item for item in items if item['id'] == item_id), None)

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item), 200

@app.route('/api/items', methods=['POST'])
def create_item():
    global next_id
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No JSON data provided'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400

    new_item = {
        'id': next_id,
        'name': data['name'],
        'description': data.get('description', '')
    }
    items.append(new_item)
    next_id += 1
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No JSON data provided'}), 400

    if 'name' in data:
        item['name'] = data['name']
    if 'description' in data:
        item['description'] = data['description']
    return jsonify(item), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    items = [i for i in items if i['id'] != item_id]
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)