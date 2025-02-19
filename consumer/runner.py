# join a consumer group for dynamic partition assignment and offset commits
from kafka import KafkaConsumer


consumer = KafkaConsumer('my_favorite_topic', group_id='my_favorite_group')
for msg in consumer:
    print (msg)

