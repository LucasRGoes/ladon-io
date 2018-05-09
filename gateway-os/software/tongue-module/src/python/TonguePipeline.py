## IMPORTS ##
import json 							# Json: is a lightweight data interchange format inspired by JavaScript object literal syntax

from kafka import KafkaProducer

## ladon05121995

producer = KafkaProducer(bootstrap_servers='orcinus:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(100):
	future = producer.send('ladon', {'index': i})
	result = future.get(timeout=60)