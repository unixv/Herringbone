from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://10.0.0.14:27017/')
db = client['herringbone']
events_collection = db['logs']

# Docker host
DOCKER_HOST = 'tcp://10.0.0.14:2375'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/events')
def events():
    events = events_collection.find().sort("logid", -1)
    events_list = list(events)
    return render_template('events.html', events=events_list)

@app.route('/api/events')
def api_events():
    events = events_collection.find().sort("logid", -1)
    events_list = []
    for event in events:
        event['_id'] = str(event['_id'])
        events_list.append(event)
    return jsonify(events_list)

if __name__ == '__main__':
    app.run(debug=True)