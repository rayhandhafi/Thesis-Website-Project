// MQTT connection settings
const brokerUrl = 'wss://34.30.152.206:8000/mqtt'; // HiveMQ public broker WebSocket URL
const clientId = 'web_client_' + Math.random().toString(16).substr(2, 8); // Generate a random client ID for the web client

const options = {
    keepalive: 60,
    clientId: clientId,
    protocolId: 'MQTT',
    protocolVersion: 4,
    clean: true,
    reconnectPeriod: 1000,
    connectTimeout: 30 * 1000,
    username: 'admin',
    password: 'hivemq',
    will: {
        topic: 'WillMsg',
        payload: 'Connection Closed abnormally..!',
        qos: 0,
        retain: false
    }
};

// Connect to the MQTT broker
const client = mqtt.connect(brokerUrl, options);

client.on('connect', () => {
    console.log('Connected to HiveMQ MQTT Broker');
});

client.on('message', (topic, message) => {
    console.log('Received message:', topic, message.toString());
    // Handle the incoming message here
    updateDashboard(message.toString()); // Function to handle the message and update the dashboard
});

client.on('error', (error) => {
    console.error('MQTT error:', error);
});

client.on('close', () => {
    console.log('MQTT connection closed');
});

// Function to dynamically subscribe to a topic based on the entered code
function subscribeToDeviceTopic(deviceCode) {
    const topic = `device/${deviceCode}/data`; // Example topic format
    client.subscribe(topic, { qos: 0 }, (error) => {
        if (error) {
            console.error('Subscribe error:', error);
        } else {
            console.log(`Subscribed to topic: ${topic}`);
        }
    });
}

// Function to publish a message to a topic
function publishMessage(topic, message) {
    client.publish(topic, message, { qos: 0, retain: false }, (error) => {
        if (error) {
            console.error('Publish error:', error);
        } else {
            console.log('Message published:', message);
        }
    });
}

// Function to update the dashboard with received message
function updateDashboard(message) {
    try {
        const data = JSON.parse(message);
        const name = data.name;
        const temp = data.temp;
        const lat = data.lat;
        const lng = data.lng;

        document.getElementById('deviceName').textContent = name;
        document.getElementById('deviceTemp').textContent = temp;

        // Update the map with the new coordinates
        const newPosition = { lat: lat, lng: lng };
        const mapOptions = {
            center: newPosition,
            zoom: 12
        };
        const map = new google.maps.Map(document.getElementById('map'), mapOptions);

        const marker = new google.maps.Marker({
            position: newPosition,
            map: map,
            title: "Device Location"
        });

        // Show the device info section
        document.getElementById('noDevice').style.display = 'none';
        document.getElementById('deviceInfo').style.display = 'block';

    } catch (error) {
        console.error('Error parsing message:', error);
    }
}

// Example function to simulate adding a device
function addDevice() {
    const deviceCode = document.getElementById('deviceCode').value;
    if (deviceCode) {
        // Subscribe to the topic for the entered device code
        subscribeToDeviceTopic(deviceCode);
        openSuccessModal();
    }
}

// Modify the submitDeviceCode function to use addDevice
function submitDeviceCode() {
    addDevice();
}
