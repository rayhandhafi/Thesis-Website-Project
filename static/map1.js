function openAddDeviceModal() {
  document.getElementById('addDeviceModal').style.display = 'block';
}

function closeAddDeviceModal() {
  document.getElementById('addDeviceModal').style.display = 'none';
}

function openSuccessModal() {
  document.getElementById('successModal').style.display = 'block';
}

function closeSuccessModal() {
  document.getElementById('successModal').style.display = 'none';
  document.getElementById('addDeviceModal').style.display = 'none';
}

function submitDeviceCode() {
  addDevice();
}

function initMap() {
  const mapOptions = {
      center: { lat: -6.9175, lng: 107.6191 },
      zoom: 12
  };
  const map = new google.maps.Map(document.getElementById('map'), mapOptions);

  const marker = new google.maps.Marker({
      position: { lat: -6.9175, lng: 107.6191 },
      map: map,
      title: "Device Location"
  });
}


/*function initMap() {
  const bandung = { lat: -6.914744, lng: 107.609810 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: bandung,
  });
  const contentString =
    '<div id="content">' +
    '<div id="siteNotice">' +
    '<h1 id="firstHeading" class="firstHeading">Satria Winekas Herlambang</h1>' +
    '<div id="bodyContent">' +
    '<p><b>Satria</b>, anak dari <b>Nama Ortu Satria</b>, merupakan anggota dari <b>POTADS Jawa Barat</b></p> ' + "<p><b>Kondisi Anak</b></p>"+
    '<p>Temperature: 28.7 C</p>' +
    "</div>" +
    "</div>";
  const infowindow = new google.maps.InfoWindow({
    content: contentString,
    ariaLabel: "Bandung",
  });
  const marker = new google.maps.Marker({
    position: bandung,
    map,
    title: "Satria",
    label: "S",
  });

  marker.addListener("click", () => {
    infowindow.open({
      anchor: marker,
      map,
    });
  });
}

window.initMap = initMap;*/