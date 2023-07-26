from paho.mqtt import client as mqtt_client
import ssl
import logg

global_message = ''


def on_connect(client, userdata, flags, rc):
    logg.server_logger.info(f'Connect with broker')
    #print('Connect with broker')

def on_message(client, userdata, message,tmp=None):
    global global_message
    global_message = str(message.payload.decode('utf-8'))

def on_publish(client,userdata,result):
    logg.server_logger.info(f'Data published')
    #print('Data published')

class mqtt_unit:

    def __init__(self, broker_ip, port, client_id, topic, client_username, client_password):
        self.broker_ip = broker_ip
        self.port = port
        self.client_id = client_id
        self.topic = topic
        self.client_username = client_username
        self.client_password = client_password

        client = mqtt_client.Client(client_id)
        client.username_pw_set(username=client_username, password=client_password)
        client.on_message = on_message
        client.on_publish= on_publish
        client.on_connect = on_connect

        self.client = client

    #Connect to server
    def connect(self):
        try:
            self.client.connect(self.broker_ip, self.port, 60)
            logg.server_logger.info(f'MQQT successful connection: {self.broker_ip}:{self.port}')
        except:
            logg.server_logger.exception(f'MQQT connection failed\r\n')
            #print("Connection failed")

    #Subscribe to topics
    def subscribe(self):
        try:
            self.client.subscribe(self.topic)
            logg.server_logger.info(f'MQQT successful subscribe: {self.topic}')
        except:
            logg.server_logger.exception(f'MQQT subscribe failed\r\n')
            #print("Subscribe failed")

    #Send message      
    def publish_message(self, topic, msg):
        try:
            result = self.client.publish(topic, msg)
            if result.rc == 0:
                logg.server_logger.info(f"Send {msg} to topic {topic}")
                #print(f"Send {msg} to topic {topic}")
            else:
                logg.server_logger.info(f"Failed to send message to topic {topic}")
                #print(f"Failed to send message to topic {topic}")
        except: 
            logg.server_logger.exception(f'MQQT publish failed\r\n')
            #print("Publish failed")