import socket
import json
import os

print("Setting up...")
PORT = 7000
print("Aquiring host info...")
HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
print(f"Binding to {HOST}:{PORT}")
tcp_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_receiver.bind((HOST, PORT))
tcp_receiver.listen(20)
print("Identifier running...")

while(True):
	connection, address = tcp_receiver.accept()
	logsource = address
	logbody = connection.recv(1024).decode('ascii')
	print(f"Identifying new log fromv {address}")
	
	# Replace with better code to classify and send back what type of log it is.
	try:
		json.loads(logbody)
		connection.sendall(b"JSON")
	except:
		connection.sendall(b"TEXT")
