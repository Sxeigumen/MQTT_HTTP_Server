from paho.mqtt import client as mqtt_client
import ssl
import http_server

#Brocker info
broker = 'localhost'	# broker ip
port = 1883 # 9001 or 1883

#Client-Server info
my_topics = [
	('gamedata', 1),
	('instructions', 1)
]
client_id = f'publish-{999}' # generate this


#Connection info
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.publish(my_topics, "OFF")

#Sub-be to topics
def subscribe_topics(client):
	#client = mqtt_client.Client()
	client.on_connect = on_connect
	client.username_pw_set(username='Kyala', password='123')
	#client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
	try:
		client.connect(broker, port, 60)
	except:
		print("Connection failed")
	#client.loop_forever()

#Send message to broker and other clients
def pubish_message(client, topic, msg):
	try:
		result = client.publish(topic, msg)
		if status == 0:
	        print(f"Send `{msg}` to topic `{topic}`")
	    else:
	        print(f"Failed to send message to topic {topic}")
	except: 
		print("Publish failed")

if __name__ == "__main__":  
	client = mqtt_client.Client()
    subscribe_topics(client)
