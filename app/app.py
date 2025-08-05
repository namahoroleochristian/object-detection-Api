from flask import Flask, request, jsonify
from pymongo import MongoClient
MongoClient = MongoClient('mongodb://localhost:27017/')
db = MongoClient['mydatabase']
collection = db['mycollection']
 
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello, World!",
        "status": "success"
    }
    return jsonify(data)    
@app.route('/api/data', methods=['POST'])
def post_data():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400
    new_data = request.json

    
    if not new_data:
        return jsonify({"error": "No data provided"}), 400
    
    collection.insert_one(new_data)
    return jsonify({"message": "Data inserted successfully"}), 201
app.route('/api/data/id', methods=['PUT'])
def update_data():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400
    new_data = request.json
    id = request.args.get('id')

    if not new_data:
        return jsonify({"error": "No data provided"}), 400
    
    # Assuming you have a way to identify which document to update
    result = collection.update_one({"_id": id}, {"$set": new_data})
    
    if result.matched_count == 0:
        return jsonify({"error": "No document found with the given ID"}), 404
    
    return jsonify({"message": "Data updated successfully"}), 200
if __name__ == '__main__':
    app.run(debug=True)