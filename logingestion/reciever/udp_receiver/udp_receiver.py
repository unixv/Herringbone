import socket
import json
import pymongo
import os
import pprint

"""
Set the SOURCE_TYPE_DICT to hard code log types. When using an identifier, the machine learning 
model will cross-reference its predictions and re-train itself on the fly to enhance accuracy. 
To set this, add a source_type_dict.json file in the same directory as udp_receiver.py
"""
def reload_source_type_dict():
	"""
	Reload the dictionary from the source_type_dict.json file
	"""

	return json.load(open("/herringbone/config/source_type_dict.json", "r"))

SOURCE_TYPE_DICT = reload_source_type_dict()

"""
To set the Identifier, configure the environment variable IDENTIFIER at start-up with the 
HOST:PORT of a running identifier container. If left blank, it will default to None, and 
all log types will show as Unidentified.
"""
IDENTIFIER = os.environ.get("IDENTIFIER", None)
if IDENTIFIER is not None:
	IDENTIFIER = os.environ.get("IDENTIFIER").split(":")
	IDENTIFIER_HOST = IDENTIFIER[0]
	IDENTIFIER_PORT = int(IDENTIFIER[1])

"""
To set the Parser, configure the environment variable PARSER at start-up with the 
HOST:PORT of a running parser container. If left blank, it will default to None, and 
nothing will be parser.
"""
PARSER = os.environ.get("PARSER", None)
if PARSER is not None:
	PARSER = os.environ.get("PARSER").split(":")
	PARSER_HOST = PARSER[0]
	PARSER_PORT = int(PARSER[1])

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


"""
Server Bind Settings: If you change the PORT, ensure that the same port is exposed in the 
Dockerfile when building a new udp_receiver container.
"""
PORT = 7002
HOST = '0.0.0.0'

if __name__ == "__main__":
	print(f"Binding to {HOST}:{PORT}")
	udp_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_receiver.bind((HOST, PORT))
	print(f"UDP receiver running...with identifier set to {IDENTIFIER}...and MongoDB set to {MONGO_DB}...and parser set to {PARSER}")

	while(True):
		data, address = udp_receiver.recvfrom(1024)
		logsource = address
		logbody = data.decode('utf-8')
		logtype = "Unidentified"
		indicators = {}

		"""
		Identify the log type using the identifier if not set to None.
		"""
		try:
			if IDENTIFIER:
				to_identify = {"body":logbody}
				reload_source_type_dict()
				print(SOURCE_TYPE_DICT)
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
			else:
				print("No identifier set...")

		except Exception as e:
			print(f"Identifier failed: {e}")

		"""
		Parse the log using the parser if not set to None.
		"""
		try:
			if PARSER:
				print("Parsing log...")
				tcp_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				tcp_sender.connect((PARSER_HOST, PARSER_PORT))
				tcp_sender.sendall(bytes(json.dumps({"data":logbody,"logtype":logtype}), "utf-8"))
				indicators = json.loads(tcp_sender.recv(1024).decode("utf-8"))
				print(indicators)
				tcp_sender.close()
			else:
				print("No parser set...")

		except Exception as e:
			print(f"Parser failed: {e}")

		"""
		Strcture of the log object.
		"""
		logdata = {
			"source_address": logsource[0],
			"source_port": logsource[1],
			"message": logbody,
			"type": logtype,
			"indicators": indicators
		}

		"""
		Store the log object in MongoDB if not set to None.
		"""
		try:
			if MONGO_DB:
				insert_log(logdata)
			else:
				print("No mongo db set...")
		except Exception as e:
			print(f"MongoDB insert failed: {e}")

		print(logdata)
	