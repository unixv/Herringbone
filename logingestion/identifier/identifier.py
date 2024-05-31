"""
Herringbone Log Ingestion : Identifier

The identifier receives messages containing raw event logs over TCP and returns a tag 
most likely to be the format the data is in.

"""
from assistant import Assistant
import socket
import json
import os

"""
Server Bind Settings: If you change the PORT, ensure that the same port is exposed in the 
Dockerfile when building a new identifier container.
"""
PORT = 7000
HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
MAX_CONNECTIONS = 20

# Load the assistant for learning
learning = Assistant(dataset="./dataset.csv")

# Start listening for TCP connections
tcp_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_receiver.bind((HOST, PORT))
tcp_receiver.listen(MAX_CONNECTIONS)
print(f"Identifier is listening on {HOST}:{PORT}")

def identify(logbody):
	"""
	This is where the logic should go to identify raw event log formats.
	"""

	loaded_model = learning.load_model()
	predicted_type = learning.predict_log_type(logbody["body"], loaded_model)
	print(f"The predicted log type is: {predicted_type}")

	if "correct_type" in logbody.keys():
		correct_type = logbody["correct_type"]

		if predicted_type != correct_type:
			print(f"Updating model with correct log type: {correct_type}")
			loaded_model = learning.retrain_model([logbody["body"]], [correct_type], loaded_model)
			updated_predicted_type = learning.predict_log_type(logbody["body"], loaded_model)
			print(f"The updated predicted log type is: {updated_predicted_type}")
			predicted_type = updated_predicted_type

	return predicted_type

while(True):
	connection, address = tcp_receiver.accept()
	logbody = connection.recv(1024).decode("utf-8")
	print(f"Identifying new log fromv {address}")
	try:
		connection.sendall(bytes(identify(json.loads(logbody)), "utf-8"))
	except Exception as e:
		print(f"Identifier failed: {e}")

