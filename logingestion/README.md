# Herringbone Log Ingestion

The starting point for creating a Log Ingestion Section is the Receivers. These are available in two variants: UDP and TCP. The primary purpose is to forward any data to them, and the configured Applications will handle the rest of the processing. The goal is to minimize or eliminate the need for configuration changes. A receiver is not bound to a single log source but can process data from multiple log sources simultaneously. For optimal performance, you can scale and deploy as many receivers and applications as needed.

### UDP Receiver setup

Launch the receiver effortlessly with Docker or Podman, and seamlessly configure application links through environment variables for optimal flexibility and integration.

```shell
docker run -d -p 7002:7002/udp \
-e IDENTIFIER=172.17.0.2:7000 \
-e MONGO_DB=172.17.0.3:27017 \
-e PARSER=172.17.0.5:7005 \
--name udp_receiver \
udp_receiver:A2.1.1
```
**Network Configuration**

*Port*: The receiver operates on container port 7002 by default, but you can easily map this to any port on the host machine as per your requirements.

**Optional Application Link Environment Variables**

*IDENTIFIER*: To forward logs to an identifier, set this environment variable with the container's HOST:PORT
of your desired identifier.

*PARSER*: To forward logs to a parser, set this environment variable with the container's HOST:PORT
of your chosen parser.

*MONGO_DB*: To send restructured logs to a MongoDB instance, specify the HOST:PORT
of your MongoDB instance in this environment variable.

### TCP Receiver setup

Launch the receiver effortlessly with Docker or Podman, and seamlessly configure application links through environment variables for optimal flexibility and integration.

```shell
docker run -d -p 7001:7001 \
-e IDENTIFIER=172.17.0.2:7000 \
-e MONGO_DB=172.17.0.3:27017 \
-e PARSER=172.17.0.5:7005 \
--name tcp_receiver \
tcp_receiver:A2.1.1
```
**Network Configuration**

*Port*: The receiver operates on container port 7001 by default, but you can easily map this to any port on the host machine as per your requirements.

**Optional Application Link Environment Variables**

*IDENTIFIER*: To forward logs to an identifier, set this environment variable with the container's HOST:PORT
of your desired identifier.

*PARSER*: To forward logs to a parser, set this environment variable with the container's HOST:PORT
of your chosen parser.

*MONGO_DB*: To send restructured logs to a MongoDB instance, specify the HOST:PORT
of your MongoDB instance in this environment variable.

### Identifier Application

The identifier's mission is to effortlessly recognize the type of log forwarded to the receiver with minimal to no configuration. Initially leveraging a basic Machine Learning model, it can be corrected and trained over time to enhance accuracy. This capability allows for seamless addition and monitoring of new assets on the fly.

```shell
docker run -d -p 7000:7000 \
--name identifier \
 identifier:A2.0.1
```

To ensure the identifier is properly trained, it is recommended to configure the source_type_dict.json file within the receiver containers. This configuration allows you to specify the correct source type for each specific source IPv4 address. If the identifier makes an incorrect prediction, it will automatically retrain to improve its accuracy over time.

*Example of source_type_dict.json*

```json
{
	"172.17.0.1":"Syslog"
}
```

### Parser Application

The parser's role is to extract cybersecurity indicators from raw log data and return a structured collection to the receiver.

```shell
docker run -d -p 7005:7005 \
--name parser \
parser:A1.0.0
```

### MongoDB

If you opt to persistently store received, identified, and parsed logs using MongoDB, the database will be named *herringbone* and the collection will be named *logs*.