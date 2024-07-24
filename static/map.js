var map, marker, infoWindow;

function initMap() {
    try {
        const initialPosition = { lat: -6.914744, lng: 107.609810 };
        map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: initialPosition,
        });

        marker = new google.maps.Marker({
            position: initialPosition,
            map: map,
            title: "Satria",
            label: "S",
        });

        infoWindow = new google.maps.InfoWindow();

        marker.addListener("click", () => {
            infoWindow.open(map, marker);
        });

        // Fetch initial data
        fetchData();
        // Set interval to fetch data every 5 seconds
        startFetchingData();
    } catch (error) {
        console.error('Error initializing map:', error);
    }
}

function updateMap(data) {
    if (!data || !data.latitude || !data.longitude || data.latitude === 0 || data.longitude === 0) {
        console.error('Invalid data:', data);
        data = {
            latitude: -6.914744,
            longitude: 107.609810,
            temperature: 25,
            humidity: 50
        };
    }

    console.log('Updating map with data:', data);

    const latLng = new google.maps.LatLng(data.latitude, data.longitude);
    marker.setPosition(latLng);
    map.setCenter(latLng);

    const contentString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        '<h1 id="firstHeading" class="firstHeading">Satria Winekas Herlambang</h1>' +
        '<div id="bodyContent">' +
        '<p><b>Satria</b>, anak dari <b>Nama Ortu Satria</b>, merupakan anggota dari <b>POTADS Jawa Barat</b></p>' +
        '<p><b>Kondisi Anak</b></p>' +
        `<p>Temperature: ${data.temperature}°C</p>` +
        `<p>Humidity: ${data.humidity}%</p>` +
        '</div>' +
        '</div>';

    console.log('Setting InfoWindow content:', contentString);
    infoWindow.setContent(contentString);
}
