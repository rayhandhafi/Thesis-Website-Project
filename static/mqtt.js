var fetchInterval;

function openAddDeviceModal() {
    document.getElementById('addDeviceModal').style.display = 'block';
}

function closeAddDeviceModal() {
    document.getElementById('addDeviceModal').style.display = 'none';
}

function closeSuccessModal() {
    document.getElementById('successModal').style.display = 'none';
    document.getElementById('no-device').style.display = 'none';
    document.getElementById('map').style.display = 'block';
    document.getElementById('disconnect-btn').style.display = 'block';
}

function submitDeviceCode() {
    var deviceCode = document.getElementById('deviceCode').value;
    fetch('/subscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: deviceCode })
    }).then(response => response.json())
    .then(data => {
        if (data.status === 'subscribed') {
            console.log('Subscription successful:', data);
            closeAddDeviceModal();
            document.getElementById('successModal').style.display = 'block';
            fetchData();  // Ensure to fetch data immediately after subscription
            initMap();  // Reinitialize map if needed
            startFetchingData();  // Start fetching data at intervals
        } else {
            console.error('Subscription failed:', data.message);
            alert('Subscription failed: ' + data.message);
        }
    }).catch(error => {
        console.error('Error during subscription:', error);
    });
}

function disconnectDevice() {
    fetch('/unsubscribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(data => {
        if (data.status === 'unsubscribed') {
            console.log('Unsubscription successful:', data);
            document.getElementById('map').style.display = 'none';
            document.getElementById('disconnect-btn').style.display = 'none';
            document.getElementById('no-device').style.display = 'block';
            stopFetchingData();  // Ensure data fetching is stopped when disconnected
        } else {
            console.error('Unsubscription failed:', data.message);
            alert('Unsubscription failed: ' + data.message);
        }
    }).catch(error => {
        console.error('Error during unsubscription:', error);
    });
}

function startFetchingData() {
    fetchInterval = setInterval(fetchData, 5000);
}

function stopFetchingData() {
    if (fetchInterval) {
        clearInterval(fetchInterval);
    }
}

function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => updateMap(data))
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}
