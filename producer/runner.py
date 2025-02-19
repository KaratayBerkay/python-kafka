import time
import json

from typing import Union
from kafka import KafkaProducer
from kafka.errors import KafkaError

time.sleep(20)
producer = KafkaProducer(
    bootstrap_servers='broker-1:19092,broker-2:19092,broker-3:19092',
    retries=5,
    request_timeout_ms=2000,       # Adjust timeout if needed
    max_request_size=2000000,       # 1MB (adjust as needed)
    compression_type='gzip'         # Options: 'gzip', 'snappy', 'lz4', 'zstd'
)


# On send success callback metadata
def on_send_success(metadata):
    print("Sent message to broker is successful \n metadata : ", dict(
        topic=metadata.topic,
        partition=metadata.partition,
        offset=metadata.offset
    ))


# On send error callback
def on_send_error(exc):
    print(f'I am an errback : {exc}')


# Send message to broker
def send_message_to_broker(producer_: KafkaProducer, topic: str, message: Union[str, bytes]) -> None:
    # produce asynchronously with callbacks
    try:
        if isinstance(message, str):
            producer_.send(topic, message.encode()).add_callback(on_send_success).add_errback(on_send_error)
        else:
            producer_.send(topic, message).add_callback(on_send_success).add_errback(on_send_error)
        # block until all async messages are sent
        producer_.flush()
    except KafkaError as kafka_error:
        # Decide what to do if produce request failed...
        print('kafka_error', kafka_error)
        raise kafka_error
    finally:
        # producer_.close()
        return


if __name__ == '__main__':
    print('Producer started ...')
    i = 1001
    while True:
        try:
            send_in_bytes = json.dumps({
                'data': [f'val back {i}', f'val2 back {i}'], 'metadata': {'node': str(producer)}
            }).encode()
            send_message_to_broker(producer_=producer, topic='data-from-producer', message=send_in_bytes)
            time.sleep(3)
            i += 1
        except Exception as e:
            print(f'Producer stopped error raised : {e}')
            # producer.close()
            pass
