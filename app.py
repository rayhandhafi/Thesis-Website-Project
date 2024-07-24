from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import logging
import threading
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

# MQTT Broker details
MQTT_BROKER = '34.30.152.206'
MQTT_PORT = 1883
MQTT_USER = 'admin'
MQTT_PASSWORD = 'hivemq'
MQTT_CLIENT_ID = 'WebApp'

# Initialize tracked data
tracked_data = {'longitude': 0, 'latitude': 0, 'temperature': 0, 'humidity': 0}

# Global MQTT topic
current_topic = None

# MQTT client singleton
mqtt_client = None


def get_mqtt_client():
    global mqtt_client
    if mqtt_client is None:
        mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID,
                                  protocol=mqtt.MQTTv311)
        mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        #mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        #mqtt_client.loop_start()
    return mqtt_client


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"Connected to MQTT Broker! (Result code: {rc})")
        if current_topic:
            result, mid = client.subscribe(current_topic)
            if result == mqtt.MQTT_ERR_SUCCESS:
                logging.info(f"Subscribed to topic: {current_topic}")
            else:
                logging.error(
                    f"Subscription to {current_topic} failed with result code: {result}"
                )
    else:
        logging.error(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    global tracked_data
    try:
        payload = msg.payload.decode()
        longitude, latitude, temperature, humidity = map(
            float, payload.split(','))
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


def mqtt_connect():
    client = get_mqtt_client()
    while True:
        try:
            logging.info(
                f"Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.loop_forever()
        except Exception as e:
            logging.error(f"Error connecting to MQTT broker: {e}")
            time.sleep(5)  #Wait 5 seconds before retrying


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    global current_topic
    #new_topic = request.json.get('code')
    new_topic = request.get_json().get('code')
    client = get_mqtt_client()
    logging.info(f"Attempting to subscribe to topic: {new_topic}")

    try:
        if current_topic:
            result, mid = client.unsubscribe(current_topic)
            if result != mqtt.MQTT_ERR_SUCCESS:
                raise Exception(
                    f"Unsubscription failed with result code {result}")
            logging.info(f"Unsubscribed from topic: {current_topic}")

        result, mid = client.subscribe(new_topic)
        if result == mqtt.MQTT_ERR_SUCCESS:
            logging.info(f"Successfully subscribed to topic: {new_topic}")
            current_topic = new_topic
            return jsonify({'status': 'subscribed', 'topic': new_topic})
        else:
            raise Exception(f"Subscription failed with result code {result}")
    except Exception as e:
        logging.error(f"Subscription error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    global current_topic
    if current_topic:
        client = get_mqtt_client()
        try:
            result, mid = client.unsubscribe(current_topic)
            if result == mqtt.MQTT_ERR_SUCCESS:
                logging.info(f"Unsubscribed from topic: {current_topic}")
                current_topic = None
                return jsonify({'status': 'unsubscribed'})
            else:
                raise Exception(
                    f"Unsubscription failed with result code {result}")
        except Exception as e:
            logging.error(f"Unsubscription error: {e}")
            return jsonify({'status': 'error', 'message': str(e)})
    else:
        return jsonify({
            'status': 'error',
            'message': 'No topic to unsubscribe'
        })


@app.route('/data')
def data():
    return jsonify(tracked_data)


if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=mqtt_connect)
    mqtt_thread.start()
    app.run(host='0.0.0.0', debug=True)
