from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
from imageai.Detection import ObjectDetection
MongoClient = MongoClient('mongodb://localhost:27017/')
db = MongoClient['mydatabase']
collection = db['mycollection']
 
app = Flask(__name__)

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
@app.route('/api/data/<item_id>', methods=['PUT'])
def update_data(item_id):
    content_type = request.headers.get('Content-Type')
    # return jsonify(item_id)
    if not ObjectId.is_valid(item_id):
        return jsonify({"error": "Invalid ID format"}), 400
    if content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400
    new_data = request.json
     # <-- Getting ID from query parameters

    if not new_data:
        return jsonify({"error": "No data provided"}), 400

    # Assuming you have a way to identify which document to update
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": new_data}) # <-- Using string ID directly

    
    if result.modified_count == 0:
        return jsonify({"message": "No changes made to the document"}), 400
    if result.modified_count > 0:
        return jsonify({"message": "Data updated successfully"}), 200
    



import os 
execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "yolo-tiny.0.1.h5"))
detector.loadModel()
@app.route('/api/detect_objects', methods=['POST'])
def detect_objects():
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image provided"}), 400
    
   
    detections = detector.detectObjectFromImage( input_image = os.path
                                            .join(execution_path,image.filename),
                                            output_image = os.path
                                            .join(execution_path,"NewImage.jpg"))
    for Object in detections:
        print(Object["name"],":",Object["percentage_probability"])
        return jsonify({"detections": detections}), 200


if __name__ == '__main__':
    app.run(debug=True)