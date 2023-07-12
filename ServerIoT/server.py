from paho.mqtt import client as mqtt_client
import ssl

#Brocker info
broker = 'localhost'	# broker ip
port = 1883 # 9001 or 1883

#Client-Server info
my_topics = [
	('gamedata', 1),
	('instructions', 1)
]
client_id = f'publish-{999}' # generate this


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.publish(my_topics, "OFF")


def client_forever():
	client = mqtt_client.Client()
	print(1)
	client.on_connect = on_connect
	client.username_pw_set(username='Kyala', password='123')
	print(1)
	#client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
	client.connect(broker, port, 60)
	print(1)
	client.loop_forever()


if __name__ == "__main__":  
    client_forever()