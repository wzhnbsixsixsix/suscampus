import '../sustainableCampus/templates/geoLocTestStyles.css';
import Map from '../jsLibraries/ol/Map.js';
import OSM from '../jsLibraries/ol/source/OSM.js';
import TileLayer from '../jsLibraries/ol/layer/Tile.js';
import View from '../jsLibraries/ol/View.js';

function findLocOnMap()  {
    const status = document.querySelector("#status");
    const mapView = document.querySelector("#map-view");

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        status.textContent = "Location Found:";
        mapView.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
        mapView.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
    }

    function error() {
        status.textContent = "Unable to find location."
    }

    if ("geolocation" in navigator) {
        status.textContent = "Finding location..."
        navigator.geolocation.getCurrentPosition(success, error)
    } else {
        status.textContent = "Geolocation not supported by your browser."
    }
}

document.querySelector("#find-loc").addEventListener("click", findLocOnMap)

const map = new Map({
    target: 'map',
    layers: [
        new TileLayer({
            source: new OSM(),
        }),
    ],
    view: new View({
        center: [0, 0],
        zoom: 2,
    }),
});