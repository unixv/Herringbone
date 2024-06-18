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

"""
Define regex patterns for different cybersecurity indicators.
"""
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}\b'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
hash_pattern = r'\b[A-Fa-f0-9]{32}\b|\b[A-Fa-f0-9]{40}\b|\b[A-Fa-f0-9]{64}\b'

def extract_cybersecurity_indicators(text):
    """
    This is where the logic should go to extract cybersecurity indicators.
    """

    ip_matches = re.findall(ip_pattern, text)
    url_matches = re.findall(url_pattern, text)
    domain_matches = re.findall(domain_pattern, text)
    email_matches = re.findall(email_pattern, text)
    hash_matches = re.findall(hash_pattern, text)

    indicators = {
        'IP Addresses': ip_matches,
        'URLs': url_matches,
        'Domains': domain_matches,
        'Email Addresses': email_matches,
        'File Hashes': hash_matches
    }

    return indicators

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
            # Extract cybersecurity indicators from the text
            indicators = extract_cybersecurity_indicators(logbody)
            print(indicators)
            connection.sendall(bytes(json.dumps(indicators), "utf-8"))
        except Exception as e:
            print(f"Parser failed: {e}")
