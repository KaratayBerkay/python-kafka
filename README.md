
# Python Kafka Distributor Apache
It is a high-level library that provides a Pythonic API for interacting with Kafka.

Python Kafka Distributor is a simple Kafka producer that sends messages to a Kafka topic.
A distributed system can be built by running multiple instances of this producer.
Specify the Kafka broker address and the topic name in the configuration file.
Set the message frequency and the message content in the configuration file.
Collect the messages from the Kafka topic using a Kafka consumer.


## Dependencies:
- kafka-python==2.0.3

All brokers are depend on 3 main controllers:
```yaml
    controller-2:
    image: apache/kafka:latest
    container_name: controller-2
    networks:
      - kafka-network
    environment:
      KAFKA_NODE_ID: 2
      KAFKA_PROCESS_ROLES: controller
      KAFKA_LISTENERS: CONTROLLER://:9093
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@controller-1:9093,2@controller-2:9093,3@controller-3:9093
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
```

There 3 main brokers 
```yaml
  broker-1:
    image: apache/kafka:latest
    container_name: broker-1
    ports:
      - "29092:9092"
    environment:
      KAFKA_NODE_ID: 4
      KAFKA_PROCESS_ROLES: broker
      KAFKA_LISTENERS: 'PLAINTEXT://:19092,PLAINTEXT_HOST://:9092'
      KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://broker-1:19092,PLAINTEXT_HOST://localhost:29092'
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@controller-1:9093,2@controller-2:9093,3@controller-3:9093
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
    networks:
      - kafka-network
    depends_on:
      - controller-1
      - controller-2
      - controller-3
```

There is one producer which produce messages to the topic:
```yaml
  producer-kafka:
    container_name: producer-kafka
    build:
      context: .
      dockerfile: producer/Dockerfile
    networks:
      - kafka-network
    depends_on:
      - broker-1
      - broker-2
      - broker-3
```
There is one consumer which consume messages from the topic:
```yaml
  consumer-kafka:
    container_name: consumer-kafka
    build:
      context: .
      dockerfile: consumer/Dockerfile
    networks:
      - kafka-network
    depends_on:
      - broker-1
      - broker-2
      - broker-3
```

### Kafka Broker’s Message Limits Are Too Low
📌 Issue:
The Kafka broker rejects messages exceeding message.max.bytes (default: 100MB).
```python
message.max.bytes=209715200  # 200MB
replica.fetch.max.bytes=209715200  # 200MB
fetch.message.max.bytes=209715200  # 200MB
```

### All brokers are connected to the same network
```yaml
networks:
  - kafka-network
```

### Instead using external port 9092, use internal port 29092
```yaml
KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://broker-1:19092,PLAINTEXT_HOST://localhost:9092'
```

by simply running the following command:
@ both consumer and producer
```dockerfile
CMD ["python", "runner.py"]
```

## Run with docker compose
Run all services with 
```bash
docker-compose up --build
```
Output 4 service init:
```python
 ✔ Network python-kafka_kafka-network  Created                                                                                                                                                                                                              0.1s 
 ✔ Container controller-2              Created                                                                                                                                                                                                              0.4s 
 ✔ Container controller-1              Created                                                                                                                                                                                                              0.6s 
 ✔ Container controller-3              Created                                                                                                                                                                                                              1.3s 
 ✔ Container broker-1                  Created                                                                                                                                                                                                              0.3s 
 ✔ Container consumer-kafka            Created                                                                                                                                                                                                              0.2s 
 ✔ Container producer-kafka            Created                                                                                                                                                                                                              0.2s 
Attaching to broker-1, consumer-kafka, controller-1, controller-2, controller-3, producer-kafka
controller-1    | ===> User
controller-1    | uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
controller-1    | ===> Setting default values of environment variables if not already set.
controller-1    | CLUSTER_ID not set. Setting it to default value: "5L6g3nShT-eMCtK--X86sw"
controller-1    | ===> Configuring ...
controller-1    | Running in KRaft mode...
controller-1    | ===> Launching ... 
controller-1    | ===> Using provided cluster id 5L6g3nShT-eMCtK--X86sw ...
controller-3    | ===> User
controller-3    | uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
controller-3    | ===> Setting default values of environment variables if not already set.
controller-3    | CLUSTER_ID not set. Setting it to default value: "5L6g3nShT-eMCtK--X86sw"
controller-3    | ===> Configuring ...
controller-3    | Running in KRaft mode...
controller-3    | ===> Launching ... 
controller-3    | ===> Using provided cluster id 5L6g3nShT-eMCtK--X86sw ...
controller-2    | ===> User
controller-2    | uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
controller-2    | ===> Setting default values of environment variables if not already set.
controller-2    | CLUSTER_ID not set. Setting it to default value: "5L6g3nShT-eMCtK--X86sw"
controller-2    | ===> Configuring ...
controller-2    | Running in KRaft mode...
controller-2    | ===> Launching ... 
controller-2    | ===> Using provided cluster id 5L6g3nShT-eMCtK--X86sw ...
broker-1        | ===> User
broker-1        | uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
broker-1        | ===> Setting default values of environment variables if not already set.
broker-1        | CLUSTER_ID not set. Setting it to default value: "5L6g3nShT-eMCtK--X86sw"
broker-1        | ===> Configuring ...
broker-1        | Running in KRaft mode...
broker-1        | ===> Launching ... 
broker-1        | ===> Using provided cluster id 5L6g3nShT-eMCtK--X86sw ...
```


Output:
```python
broker-1        | [2025-02-19 18:12:27,920] INFO [BrokerLifecycleManager id=4] The broker is in RECOVERY. (kafka.server.BrokerLifecycleManager)
broker-1        | [2025-02-19 18:12:27,922] INFO [BrokerServer id=4] Waiting for the broker to be unfenced (kafka.server.BrokerServer)
broker-1        | [2025-02-19 18:12:28,042] INFO [BrokerLifecycleManager id=4] The broker has been unfenced. Transitioning from RECOVERY to RUNNING. (kafka.server.BrokerLifecycleManager)
broker-1        | [2025-02-19 18:12:28,045] INFO [BrokerServer id=4] Finished waiting for the broker to be unfenced (kafka.server.BrokerServer)
broker-1        | [2025-02-19 18:12:28,053] INFO authorizerStart completed for endpoint PLAINTEXT. Endpoint is now READY. (org.apache.kafka.server.network.EndpointReadyFutures)
broker-1        | [2025-02-19 18:12:28,054] INFO [SocketServer listenerType=BROKER, nodeId=4] Enabling request processing. (kafka.network.SocketServer)
broker-1        | [2025-02-19 18:12:28,070] INFO Awaiting socket connections on 0.0.0.0:19092. (kafka.network.DataPlaneAcceptor)
broker-1        | [2025-02-19 18:12:28,104] INFO Awaiting socket connections on 0.0.0.0:9092. (kafka.network.DataPlaneAcceptor)
broker-1        | [2025-02-19 18:12:28,109] INFO [BrokerServer id=4] Waiting for all of the authorizer futures to be completed (kafka.server.BrokerServer)
broker-1        | [2025-02-19 18:12:28,109] INFO [BrokerServer id=4] Finished waiting for all of the authorizer futures to be completed (kafka.server.BrokerServer)
broker-1        | [2025-02-19 18:12:28,109] INFO [BrokerServer id=4] Waiting for all of the SocketServer Acceptors to be started (kafka.server.BrokerServer)
broker-1        | [2025-02-19 18:12:28,109] INFO [BrokerServer id=4] Finished waiting for all of the SocketServer Acceptors to be started (kafka.server.BrokerServer)
broker-1        | [2025-02-19 18:12:28,109] INFO [BrokerServer id=4] Transition from STARTING to STARTED (kafka.server.BrokerServer)
broker-1        | [2025-02-19 18:12:28,110] INFO Kafka version: 3.9.0 (org.apache.kafka.common.utils.AppInfoParser)
broker-1        | [2025-02-19 18:12:28,110] INFO Kafka commitId: a60e31147e6b01ee (org.apache.kafka.common.utils.AppInfoParser)
broker-1        | [2025-02-19 18:12:28,110] INFO Kafka startTimeMs: 1739988748110 (org.apache.kafka.common.utils.AppInfoParser)
broker-1        | [2025-02-19 18:12:28,114] INFO [KafkaRaftServer nodeId=4] Kafka Server started (kafka.server.KafkaRaftServer)
consumer-kafka  | Consumer started ...
broker-1        | [2025-02-19 18:12:32,626] INFO Sent auto-creation request for Set(data-from-producer) to the active controller. (kafka.server.DefaultAutoTopicCreationManager)
broker-1        | [2025-02-19 18:12:32,736] INFO Sent auto-creation request for Set(data-from-producer) to the active controller. (kafka.server.DefaultAutoTopicCreationManager)
broker-1        | [2025-02-19 18:12:32,842] INFO Sent auto-creation request for Set(data-from-producer) to the active controller. (kafka.server.DefaultAutoTopicCreationManager)
broker-1        | [2025-02-19 18:12:32,885] INFO [ReplicaFetcherManager on broker 4] Removed fetcher for partitions Set(data-from-producer-0) (kafka.server.ReplicaFetcherManager)
broker-1        | [2025-02-19 18:12:32,918] INFO [LogLoader partition=data-from-producer-0, dir=/tmp/kafka-logs] Loading producer state till offset 0 with message format version 2 (kafka.log.UnifiedLog$)
broker-1        | [2025-02-19 18:12:32,922] INFO Created log for partition data-from-producer-0 in /tmp/kafka-logs/data-from-producer-0 with properties {} (kafka.log.LogManager)
broker-1        | [2025-02-19 18:12:32,927] INFO [Partition data-from-producer-0 broker=4] No checkpointed highwatermark is found for partition data-from-producer-0 (kafka.cluster.Partition)
broker-1        | [2025-02-19 18:12:32,929] INFO [Partition data-from-producer-0 broker=4] Log loaded for partition data-from-producer-0 with initial high watermark 0 (kafka.cluster.Partition)
producer-kafka  | Producer started ...
producer-kafka  | Sent message to broker is successful 
producer-kafka  |  metadata :  {'topic': 'data-from-producer', 'partition': 0, 'offset': 0}
producer-kafka  | Sent message to broker is successful 
producer-kafka  |  metadata :  {'topic': 'data-from-producer', 'partition': 0, 'offset': 1}
consumer-kafka  | broker-1 sending :  {"data": ["val back 1002", "val2 back 1002"], "metadata": {"node": "<kafka.producer.kafka.KafkaProducer object at 0x7f1120ff31a0>"}}
producer-kafka  | Sent message to broker is successful 
producer-kafka  |  metadata :  {'topic': 'data-from-producer', 'partition': 0, 'offset': 2}
consumer-kafka  | broker-1 sending :  {"data": ["val back 1003", "val2 back 1003"], "metadata": {"node": "<kafka.producer.kafka.KafkaProducer object at 0x7f1120ff31a0>"}}
consumer-kafka  | broker-1 sending :  {"data": ["val back 1004", "val2 back 1004"], "metadata": {"node": "<kafka.producer.kafka.KafkaProducer object at 0x7f1120ff31a0>"}}
producer-kafka  | Sent message to broker is successful 
producer-kafka  |  metadata :  {'topic': 'data-from-producer', 'partition': 0, 'offset': 3}
producer-kafka  | Sent message to broker is successful 
producer-kafka  |  metadata :  {'topic': 'data-from-producer', 'partition': 0, 'offset': 4}
consumer-kafka  | broker-1 sending :  {"data": ["val back 1005", "val2 back 1005"], "metadata": {"node": "<kafka.producer.kafka.KafkaProducer object at 0x7f1120ff31a0>"}}
producer-kafka  | Sent message to broker is successful 
producer-kafka  |  metadata :  {'topic': 'data-from-producer', 'partition': 0, 'offset': 5}
consumer-kafka  | broker-1 sending :  {"data": ["val back 1006", "val2 back 1006"], "metadata": {"node": "<kafka.producer.kafka.KafkaProducer object at 0x7f1120ff31a0>"}}
producer-kafka  | Sent message to broker is successful 
producer-kafka  |  metadata :  {'topic': 'data-from-producer', 'partition': 0, 'offset': 6}
consumer-kafka  | broker-1 sending :  {"data": ["val back 1007", "val2 back 1007"], "metadata": {"node": "<kafka.producer.kafka.KafkaProducer object at 0x7f1120ff31a0>"}}
```