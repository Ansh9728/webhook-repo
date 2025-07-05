import os
from flask import Blueprint, json, request, jsonify, current_app
from datetime import datetime
from app.config import Config


webhook = Blueprint("webhook", __name__, url_prefix="/webhook")

@webhook.route("", methods=["GET"])
def api_root():
    return "Welcome to my Web app"


@webhook.route("/receiver", methods=["POST"])
def receiver():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    if event_type == 'push':
        request_id = data['commits'][0]['id']
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        timestamp_str = data['head_commit']['timestamp']
        timestamp = datetime.fromisoformat(timestamp_str)
        event_data = {
            "action": "push",
            "request_id": request_id,
            "author": author,
            "from_branch" : None,
            "to_branch": to_branch,
            "timestamp": timestamp
        }
    elif event_type == 'pull_request':
        
        request_id = data['pull_request']["id"]
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        timestamp_str = data['pull_request']['created_at']
        timestamp = datetime.fromisoformat(timestamp_str)
        event_data = {
            "action": "pull_request",
            "request_id": request_id,
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }
    elif event_type == 'pull_request' and data['pull_request']['merged']:
        request_id = data['pull_request']["id"]
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        timestamp_str = data['pull_request']['merged_at']
        timestamp = datetime.fromisoformat(timestamp_str)
        event_data = {
            "action": "merge",
            "author": author,
            "request_id": request_id,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }
    else:
        return jsonify({'message': 'Event not supported'}), 400

    print("event_data", event_data)
    
    mongo = current_app.extensions['pymongo']
    collection = getattr(mongo.db, Config.COLLECTION_NAME)
    collection.insert_one(event_data)
    
    
    return jsonify({'message': 'Event received'}), 200


@webhook.route('/event', methods=['GET'])
def get_event():
    mongo = current_app.extensions['pymongo']
    collection = getattr(mongo.db, Config.COLLECTION_NAME)
    results = list(collection.find().sort("timestamp", -1).limit(10))
    for ev in results:
        ev["_id"] = str(ev["_id"])
        ev["timestamp"] = ev["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ")
    return jsonify(results), 200