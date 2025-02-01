"""
Herringbone Log Ingestion : Parser

"""
import socket
import json
import os
import re

"""
Server Bind Settings: If you change the PORT, ensure that the same port is exposed in the 
Dockerfile when building a new parser container.
"""
PORT = 7005
HOST = "0.0.0.0"
MAX_CONNECTIONS = 20

patterns = {
    "syslog":"pattern = r'^<(\d+)>(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\S+)\s([\w\.\-]+\[\d+\]):\s(\w+\[\d+\]):\s(.+)$'"
}

def parse(data):
    """
    This is where the logic should go to parse incoming data
    """

    print(data)

    if data["logtype"].lower() == "syslog":
        regex = re.compile(patterns["syslog"])
        match = regex.match(data["data"])

        if match:
            priority = match.group(1)
            timestamp = match.group(2)
            hostname = match.group(3)

            return {
                "priority": priority,
                "timestamp": timestamp,
                "hostname": hostname,
            }
        else:
            return {"parser":"could not parse syslog"}
    else:
        return {"parser":"unknown logtype"}


if __name__ == "__main__":
    # Start listening for TCP connections
    tcp_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_receiver.bind((HOST, PORT))
    tcp_receiver.listen(MAX_CONNECTIONS)
    print(f"Parser is listening on {HOST}:{PORT}")

    while(True):
        connection, address = tcp_receiver.accept()
        logbody = connection.recv(1024).decode("utf-8")
        print(f"Parsing new log from {address}")
        try:
            indicators = parse(json.loads(logbody))
            print(indicators)
            connection.sendall(bytes(json.dumps(indicators), "utf-8"))
        except Exception as e:
            print(f"Parser failed: {e}")
