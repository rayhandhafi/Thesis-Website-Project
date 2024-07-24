function openAddDeviceModal() {
    document.getElementById('addDeviceModal').style.display = 'block';
}

function closeAddDeviceModal() {
    document.getElementById('addDeviceModal').style.display = 'none';
}

function closeSuccessModal() {
    document.getElementById('successModal').style.display = 'none';
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
        console.log(data);
        document.getElementById('addDeviceModal').style.display = 'none';
        document.getElementById('successModal').style.display = 'block';
        document.querySelector('.no-device').style.display = 'none';
        document.getElementById('map').style.display = 'block';
        document.getElementById('info').style.display = 'block';
        fetchData();
        initMap();
    }).catch((error) => {
        console.error('Error:', error);
    });
}
