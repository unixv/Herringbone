from flask import Flask, render_template, request, jsonify
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
    return render_template('events.html')

@app.route('/api/events')
def api_events():
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    search_value = request.args.get('search[value]', type=str)
    order_column_index = request.args.get('order[0][column]', type=int)
    order_column_name = request.args.get(f'columns[{order_column_index}][data]')
    order_direction = request.args.get('order[0][dir]')
    order = 1 if order_direction == 'asc' else -1

    # Total records count
    total_records = events_collection.count_documents({})

    # Filtered records
    if search_value:
        query = {"$or": [
            {"source_address": {"$regex": search_value, "$options": "i"}},
            {"source_port": {"$regex": search_value, "$options": "i"}},
            {"message": {"$regex": search_value, "$options": "i"}},
            {"type": {"$regex": search_value, "$options": "i"}},
            {"indicators": {"$regex": search_value, "$options": "i"}},
            {"logid": {"$regex": search_value, "$options": "i"}}
        ]}
    else:
        query = {}

    filtered_records = events_collection.count_documents(query)
    events = events_collection.find(query).sort(order_column_name, order).skip(start).limit(length)

    events_list = []
    for event in events:
        event['_id'] = str(event['_id'])
        events_list.append(event)

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': events_list
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
