var map, marker;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8
    });
    marker = new google.maps.Marker({
        position: { lat: -34.397, lng: 150.644 },
        map: map
    });
}

function updateMap(data) {
    var latLng = new google.maps.LatLng(data.latitude, data.longitude);
    marker.setPosition(latLng);
    map.setCenter(latLng);
    document.getElementById('temperature').innerText = data.temperature;
    document.getElementById('humidity').innerText = data.humidity;
}

function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => updateMap(data));
}

setInterval(fetchData, 5000);
