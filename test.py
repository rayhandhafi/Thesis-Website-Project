import paho.mqtt.client as mqtt
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# MQTT Broker details
MQTT_BROKER = '34.30.152.206'
MQTT_PORT = 1883
MQTT_USER = 'admin'
MQTT_PASSWORD = 'hivemq'
MQTT_CLIENT_ID = 'TestClient'

client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv311)

# Set username and password
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker! (Result code: {rc})")
        client.subscribe('test')  # Subscribe to 'test' topic directly
        print(f"Subscribed to topic: test")
    else:
        print(f"Failed to connect, return code {rc}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed: {mid} {granted_qos}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        # Print the received data to the console
        print(f"Received message: {payload}")
    except Exception as e:
        print(f"Failed to process message: {e}")

client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

try:
    logging.info(f"Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
except Exception as e:
    logging.error(f"Error connecting to MQTT broker: {e}")
