import Feature from './node_modules/ol/Feature.js';
import Geolocation from './node_modules/ol/Geolocation.js';
import Map from './node_modules/ol/Map.js';
import View from './node_modules/ol/View.js';
import Point from './node_modules/ol/geom/Point.js';
import TileLayer from './node_modules/ol/layer/Tile.js';
import VectorLayer from './node_modules/ol/layer/Vector.js';
import OSM from './node_modules/ol/source/OSM.js';
import VectorSource from './node_modules/ol/source/Vector.js';
import CircleStyle from './node_modules/ol/style/Circle.js';
import Fill from './node_modules/ol/style/Fill.js';
import Stroke from './node_modules/ol/style/Stroke.js';
import Style from './node_modules/ol/style/Style.js';
import RegularShape from "./node_modules/ol/style/RegularShape.js";

// currently this is almost all an example from the OpenLayers site to figure out how the location tracking should work
// will be rewritten once the process is figured out so that it can be used for our purposes

const view = new View({
    center: [0, 0],
    zoom: 2,
});

const map = new Map({
    layers: [
        new TileLayer({
            source: new OSM(),
        }),
    ],
    target: 'map',
    view: view,
});

const geolocation = new Geolocation({
    // enableHighAccuracy must be set to true to have the heading value.
    trackingOptions: {
        enableHighAccuracy: true,
    },
    projection: view.getProjection(),
});

function el(id) {
    return document.getElementById(id);
}

// sets the geolocation object's Tracking to be in the same state as the 'track' checkbox (automatically updates)
el('track').addEventListener('change', function () {
    geolocation.setTracking(this.checked);
});

// update the HTML page when the position changes.
geolocation.on('change', function () {
    el('accuracy').innerText = geolocation.getAccuracy() + ' [m]';
    el('altitude').innerText = geolocation.getAltitude() + ' [m]';
    el('altitudeAccuracy').innerText = geolocation.getAltitudeAccuracy() + ' [m]';
    el('heading').innerText = geolocation.getHeading() + ' [rad]';
    el('speed').innerText = geolocation.getSpeed() + ' [m/s]';
});

// handle geolocation error.
geolocation.on('error', function (error) {
    const info = document.getElementById('info');
    info.innerHTML = error.message;
    info.style.display = '';
});

// no idea what exactly this does, might have to look at Feature in the ol library
const accuracyFeature = new Feature();
geolocation.on('change:accuracyGeometry', function () {
    accuracyFeature.setGeometry(geolocation.getAccuracyGeometry());
});

// controls how the user's position is visually represented on the map
const positionFeature = new Feature();
positionFeature.setStyle(
    new Style({
        image: new CircleStyle({
            radius: 6,
            fill: new Fill({
                color: '#3399CC',
            }),
            stroke: new Stroke({
                color: '#fff',
                width: 2,
            }),
        }),
    }),
);

// changes the position of the position indicator on the map (above) to match when the user's position updates
// ternary operator catches the possibility that the coordinates are invalid/empty, I think
geolocation.on('change:position', function () {
    const coordinates = geolocation.getPosition();
    positionFeature.setGeometry(coordinates ? new Point(coordinates) : null);
});

new VectorLayer({
    map: map,
    source: new VectorSource({
        features: [accuracyFeature, positionFeature],
    }),
});

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

function createMarker() {
    // first need to get all the user's input from the input fields when the button is pressed:
    // currently assumes all user input is valid
    let xPos = el("xcoord").value;
    let yPos = el("ycoord").value;
    // below are dropdowns; have to convert their choice into appropriate format here.
    let shape = el("shape").value;
    let color = el("color").value;

    let markerShape;
    let markerColor;

    // converts chosen color to hex value
    switch (color) {
        case "red":
            markerColor = '#FF0000';
            break;
        case "green":
            markerColor = '#00FF00';
            break;
        case "blue":
            markerColor = '#0000FF';
            break;
        case "yellow":
            markerColor = '#FFFF00';
            break;
    }

    // creates the object for the marker's shape, using the shape and color specified by the user
    switch (shape) {
        case "circle":
            markerShape = new CircleStyle({
                radius: 6,
                fill: new Fill({
                    color: markerColor,
                }),
                stroke: new Stroke({
                    color: '#fff',
                    width: 2,
                })
            });
            break;
        case "square":
            markerShape = new RegularShape({
                fill: new Fill({
                    color: markerColor,
                }),
                stroke: new Stroke({
                    color: '#fff',
                    width: 2,
                }),
                points: 4,
                radius: 6,
                angle: Math.PI / 4,
            });
            break;
        case "triangle":
            markerShape = new RegularShape({
                fill: new Fill({
                    color: markerColor,
                }),
                stroke: new Stroke({
                    color: '#fff',
                    width: 2,
                }),
                points: 3,
                radius: 10,
                rotation: Math.PI / 4,
                angle: 0,
            });
            break;
    }

    // creates the marker
    const marker = new Feature();
    marker.setStyle(
        new Style({image: markerShape,}),
    );

    // places the marker on the map
    marker.setGeometry([xPos, yPos]);
}

document.querySelector("#find-loc").addEventListener("click", findLocOnMap);

const addMarkerButton = document.querySelector("#create-marker");
if (addMarkerButton) {
    addMarkerButton.addEventListener("click", createMarker);
    console.log("Marker Added."); // should probably add more detailed logging in the function itself.
} else {
    console.log("Add marker button not found.");
}


