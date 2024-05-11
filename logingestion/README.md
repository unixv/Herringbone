# Herringbone Log Ingestion

Essentially the most bare-bones yet effective foundation for SIEM. The **TCP and UDP receivers** collect anything 
that lands on them and forwards them to any additional services for analysis. Learn how to use these tools below.

#### TCP Receiver

To quickly start the TCP Receiver bare with no additional options:
```bash
docker run -p 7001:<DESIRED_EXTERNAL_PORT> tcp_receiver:latest
```

*Note the TCP Receiver exposes port 7001*

Once running you can forward any message you want to the receiver and it will cache it.

Example:
```python
{
	'source_address': '172.17.0.1', 
	'source_port': 61490, 
	'message': '{"test":"test"}', 
	'type': 'JSON', 
	'logid': 0
}
```

#### UDP Receiver

To quickly start the UDP Receiver bare with no additional options:
```bash
docker run -p 7001:<DESIRED_EXTERNAL_PORT>/udp udp_receiver:latest
```

*Note the UDP Receiver exposes port 7002*

Once running you can forward any message you want to the receiver and it will cache it.

Example:
```python
{
	'source_address': '172.17.0.1', 
	'source_port': 61490, 
	'message': '{"test":"test"}', 
	'type': 'JSON', 
	'logid': 0
}
```

#### Identifier

An analysis tool add-on that identifies the most probable data format of raw text.

To run the identifier
```bash
docker run -p 7000:<DESIRED_EXTERNAL_PORT> identifier:latest
```

*Note the identifier exposes port 7000*

To add the identifier to the TCP Receiver:
```bash
docker run -p 7001:<DESIRED_EXTERNAL_PORT> \
		   -e IDENTIFIER=<IP Address of identifier>:<Port of identifier> \
		   tcp_receiver:latest
```

To add the identifier to the UDP Receiver:
```bash
docker run -p 7002:<DESIRED_EXTERNAL_PORT> \
		   -e IDENTIFIER=<IP Address of identifier>:<Port of identifier> \
		   udp_receiver:latest
```

*Note the identifier IP Address and port can be internal to the container network*

#### Parser

