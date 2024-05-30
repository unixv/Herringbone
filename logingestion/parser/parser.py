import re

def extract_cybersecurity_indicators(text):
    # Define regex patterns for different cybersecurity indicators
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}\b'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    hash_pattern = r'\b[A-Fa-f0-9]{32}\b|\b[A-Fa-f0-9]{40}\b|\b[A-Fa-f0-9]{64}\b'

    # Find all matches for each pattern
    ip_matches = re.findall(ip_pattern, text)
    url_matches = re.findall(url_pattern, text)
    domain_matches = re.findall(domain_pattern, text)
    email_matches = re.findall(email_pattern, text)
    hash_matches = re.findall(hash_pattern, text)

    # Combine all matches into a single list
    indicators = {
        'IP Addresses': ip_matches,
        'URLs': url_matches,
        'Domains': domain_matches,
        'Email Addresses': email_matches,
        'File Hashes': hash_matches
    }

    return indicators

# Example text containing cybersecurity indicators
text = """
    The attacker used IP address 192.168.1.1 to access the system. 
    They also used the domain malicious.example.com for their phishing attack.
    The phishing emails contained a link to http://phishing.example.com.
    Contact was made through john.doe@example.com. The file hash was d41d8cd98f00b204e9800998ecf8427e.
"""

# Extract cybersecurity indicators from the text
indicators = extract_cybersecurity_indicators(text)
print(indicators)
