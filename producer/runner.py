import time
import json

from typing import Union
from kafka import KafkaProducer
from kafka.errors import KafkaError


producer = KafkaProducer(bootstrap_servers=['broker1:1234'])

# Asynchronous by default
future = producer.send('my-topic', b'raw_bytes')

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
    # Successful result returns assigned partition and offset
    print('topic', record_metadata.topic)
    print('partition', record_metadata.partition)
    print('offset', record_metadata.offset)
except KafkaError as kafka_error:
    # Decide what to do if produce request failed...
    print('kafka_error', kafka_error)
    raise kafka_error


# produce asynchronously
for _ in range(100):
    producer.send('my-topic', b'msg')

def on_send_success(metadata):
    print('On send success ----------------------------------------')
    print(metadata.topic)
    print(metadata.partition)
    print(metadata.offset)
    print('On send success ----------------------------------------')

def on_send_error(excp):
    print('I am an errback')
    # handle exception


def send_message_to_broker(producer_: KafkaProducer, topic: str, message: Union[str, bytes]):
    # produce asynchronously with callbacks
    if isinstance(message, str):
        producer_.send(topic, message).add_callback(on_send_success).add_errback(on_send_error)
    else:
        producer_.send(topic, message).add_callback(on_send_success).add_errback(on_send_error)

    # block until all async messages are sent
    producer_.flush()
    # configure multiple retries
    KafkaProducer(retries=5)


if __name__ == '__main__':
    print('Producer started ...')
    i = 1
    while True:
        try:
            # produce asynchronously with callbacks
            send_in_dict = json.dumps({'data': [f'val back {i}', f'val2 back {i}'], 'meta': {'key': f'val {i}'}})
            send_in_bytes = send_in_dict.encode('utf-8')
            send_message_to_broker(producer_=producer, topic='data-from-producer', message=send_in_bytes)
            time.sleep(3)
            i += 1
        except Exception as e:
            print(f'Producer stopped error raised : {e}')
            producer.close()
            break
