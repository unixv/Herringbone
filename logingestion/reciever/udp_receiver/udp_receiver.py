import socket
import json
import pymongo
import os

print("Setting up...")
LOG_ID = 0
IDENTIFIER = os.environ.get("IDENTIFIER", None)
if IDENTIFIER is not None:
	IDENTIFIER = os.environ.get("IDENTIFIER").split(":")
	IDENTIFIER_HOST = IDENTIFIER[0]
	IDENTIFIER_PORT = int(IDENTIFIER[1])
MONGO_DB = os.environ.get("MONGO_DB", None)
PORT = 7002
print("Aquiring host info...")
HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
print(f"Binding to {HOST}:{PORT}")
udp_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_receiver.bind((HOST, PORT))
print(f"UDP receiver running...with identifier set to {IDENTIFIER}...and MongoDB set to {MONGO_DB}")

def create_connection(): 
	"""Quick function to create mongo connection objects.
	"""

	client = pymongo.MongoClient("mongodb://"+ HOST +":27017/")
	db = client["herringbone"]
	collection = db["logs"]

	return client, db, collection

def insert_log(logdata):
	"""Inserts one logdata dictionary into MongoDB datastore.
	"""
	client, db, collection = create_connection()
	collection.insert_one(logdata)

def get_last_id():
	"""Gets the last log id in the collection.
	"""

	client, db, collection = create_connection()

	last_log = db.docs.find_one(
	  {'doc_id': doc_id},
	  sort=[( '_id', pymongo.DESCENDING )]
	)

	return last_log["logid"]

while(True):
	data, address = udp_receiver.recvfrom(1024)
	logsource = address
	logbody = data.decode('ascii')

	if IDENTIFIER:
		print("Identifying log...")
		tcp_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_sender.connect((IDENTIFIER_HOST, IDENTIFIER_PORT))
		tcp_sender.sendall(logbody.encode('ascii'))
		logtype = tcp_sender.recv(1024).decode('ascii')
		tcp_sender.close()
	else:
		logtype = "Unidentified"

	logdata = {
		"source_address": logsource[0],
		"source_port": logsource[1],
		"message": logbody,
		"type": logtype,
		"logid": LOG_ID
	}

	if MONGO_DB:
		insert_log(logdata)
	print(logdata)
	LOG_ID += 1
	