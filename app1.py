#Dynamic version
from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import logging
import os

app = Flask(__name__)


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# MQTT Broker details
MQTT_BROKER = '34.30.152.206'
MQTT_PORT = 1883
MQTT_USER = 'admin'
MQTT_PASSWORD = 'hivemq'
MQTT_CLIENT_ID = 'Maell'
MQTT_TOPIC = ''  # Initialize with an empty topic

# Create a global MQTT client
client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv311)

# Set username and password
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

tracked_data = {
    'longitude': 0,
    'latitude': 0,
    'temperature': 0,
    'humidity': 0
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"Connected to MQTT Broker! (Result code: {rc})")
        if MQTT_TOPIC:  # Subscribe only if the topic is set
            client.subscribe(MQTT_TOPIC)
            logging.info(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        logging.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global tracked_data
    try:
        payload = msg.payload.decode()
        longitude, latitude, temperature, humidity = map(float, payload.split(','))
        tracked_data = {
            'longitude': longitude,
            'latitude': latitude,
            'temperature': temperature,
            'humidity': humidity
        }
        logging.info(f"Received message: {payload}")
        logging.info(f"Updated tracked data: {tracked_data}")
    except Exception as e:
        logging.error(f"Failed to process message: {e}")

client.on_connect = on_connect
client.on_message = on_message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('regist.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashb.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    global MQTT_TOPIC
    code = request.json.get('code')
    MQTT_TOPIC = code  # Use the code directly as the topic
    try:
        result = client.subscribe(MQTT_TOPIC)
        logging.info(f"Subscription result: {result}")
        logging.info(f"Subscribed to topic: {MQTT_TOPIC}")
        return jsonify({'status': 'subscribed', 'topic': MQTT_TOPIC})
    except Exception as e:
        logging.error(f"Subscription error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/data')
def data():
    return jsonify(tracked_data)

if __name__ == "__main__":
    try:
        logging.info(f"Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        logging.error(f"Error connecting to MQTT broker: {e}")
