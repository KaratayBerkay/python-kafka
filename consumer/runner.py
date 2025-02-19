# join a consumer group for dynamic partition assignment and offset commits
import time

from kafka import KafkaConsumer

time.sleep(20)
consumer = KafkaConsumer('data-from-producer', bootstrap_servers='broker-1:19092,broker-2:19092, broker-3:19092',)

while True:
    print('Consumer started ...')
    if not consumer:
        time.sleep(5)

    for msg in consumer:
        if isinstance(msg.value, bytes):
            print('broker-1 sending : ',msg.value.decode())
        else:
            print('broker-1 sending : ',msg.value)
