from flask import Flask, jsonify, request
import requests
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
# Replace with your MongoDB connection details
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["git_rating_db"]
mongo_collection = mongo_db["users"]

# Replace with your GitHub token
GITHUB_TOKEN = "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"

@app.route('/github_user/<username>', methods=['GET'])
def get_github_user(username):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        # Here you can add logic to calculate rating and store in MongoDB
        mongo_collection.insert_one(user_data)
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
