import socket
import json
import pymongo
import os

"""
By default, the LOG_ID is set to 0. However, if the receiver connects to a MongoDB instance 
with existing records, it will automatically update to the logid of the latest record.
"""
LOG_ID = 0

"""
Set the SOURCE_TYPE_DICT to hard code log types. When using an identifier, the machine learning 
model will cross-reference its predictions and re-train itself on the fly to enhance accuracy. 
To set this, add a source_type_dict.json file in the same directory as tcp_receiver.py
"""
def reload_source_type_dict():
	"""
	Reload the dictionary from the source_type_dict.json file
	"""

	return json.load(open("source_type_dict.json", "r"))

SOURCE_TYPE_DICT = reload_source_type_dict()

"""
To set the IDENTIFIER, configure the environment variable IDENTIFIER at start-up with the 
HOST:PORT of a running identifier container. If left blank, it will default to None, and 
all log types will show as Unidentified.
"""
IDENTIFIER = os.environ.get("IDENTIFIER", None)
if IDENTIFIER is not None:
	IDENTIFIER = os.environ.get("IDENTIFIER").split(":")
	IDENTIFIER_HOST = IDENTIFIER[0]
	IDENTIFIER_PORT = int(IDENTIFIER[1])

"""
To forward all logs to a MongoDB instance, set the MONGO_DB environment variable with the 
HOST:PORT. Otherwise, all logs will remain ephemeral to the container.
"""
MONGO_DB = os.environ.get("MONGO_DB", None)

def create_connection(): 
	"""
	Quick function to create mongo connection objects.
	"""

	print(f"Connecting to MongoDB at {MONGO_DB}")
	client = pymongo.MongoClient("mongodb://"+ MONGO_DB +"/")
	db = client["herringbone"]
	collection = db["logs"]
	return client, db, collection

def insert_log(logdata):
	"""
	Inserts one logdata dictionary into MongoDB datastore.
	"""
	client, db, collection = create_connection()
	collection.insert_one(logdata)

def get_last_id():
	"""
	Gets the last log id in the collection.
	"""

	client, db, collection = create_connection()

	last_log = db.docs.find_one(
	  {'doc_id': doc_id},
	  sort=[( '_id', pymongo.DESCENDING )]
	)

	return last_log["logid"]

"""
Server Bind Settings: If you change the PORT, ensure that the same port is exposed in the 
Dockerfile when building a new tcp_receiver container.
"""
PORT = 7001
HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)

if __name__ == "__main__":
	print(f"Binding to {HOST}:{PORT}")
	tcp_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_receiver.bind((HOST, PORT))
	print(f"TCP receiver running...with identifier set to {IDENTIFIER}...and MongoDB set to {MONGO_DB}")

	while(True):
		connection, address = tcp_receiver.accept()
		logsource = address
		logbody = connection.recv(1024).decode('utf-8')
		logtype = "Unidentified"
		
		"""
		Identify the log type using the identifier if not set to None.
		"""
		try:
			if IDENTIFIER:
				to_identify = {"body":logbody}
				if address[0] in list(SOURCE_TYPE_DICT.keys()):
					correct_type = SOURCE_TYPE_DICT[address[0]]
					print(f"Will train identifier with correct type: {correct_type} for {address[0]}")
					to_identify["correct_type"] = correct_type

				print("Identifying log...")
				tcp_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				tcp_sender.connect((IDENTIFIER_HOST, IDENTIFIER_PORT))
				tcp_sender.sendall(bytes(json.dumps(to_identify), "utf-8"))
				logtype = tcp_sender.recv(1024).decode("utf-8")
				tcp_sender.close()

		except Exception as e:
			print(f"Identifier failed: {e}")

		"""
		Strcture of the log object.
		"""
		logdata = {
			"source_address": logsource[0],
			"source_port": logsource[1],
			"message": logbody,
			"type": logtype,
			"logid": LOG_ID
		}

		"""
		Store the log object in MongoDB if not set to None.
		"""
		try:
			if MONGO_DB:
				insert_log(logdata)
		except Exception as e:
			print(f"MongoDB insert failed: {e}")

		print(logdata)
		LOG_ID += 1
	