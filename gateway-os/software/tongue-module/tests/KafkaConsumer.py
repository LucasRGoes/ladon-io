## IMPORTS ##
import json

from kafka import KafkaConsumer

## TESTING ##

# Opens image
photoFile = open("/home/lucas/Downloads/Teste2.png", "wb")

# Creates a buffer
photoBuffer = {}

# Creates a consumer
consumer = KafkaConsumer(
			'ladon',
			bootstrap_servers="orcinus",
			value_deserializer=lambda v: json.loads(v.decode('utf-8'))
		   )

# Receives message
for msg in consumer:

	# Gets and converts chunk
	chunk = bytes(msg.value['chunk']['__value__'])

	# Writing to file
	photoFile.write(chunk)

photoFile.close()