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

// currently much the geolocation handling is an example from the OpenLayers site to figure out how the location tracking should work
// will be rewritten when implementing to the main webpage

// the center and zoom will be changed when location tracking is enabled to focus on the user's position
const view = new View({
    center: [0, 0],
    zoom: 12,
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
// it might make the circle around the user's marker, showing the possible inaccuracy of their position?
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
    // updates the view's centre to the user's new position:
    const newPos = positionFeature.getGeometry().getCoordinates();
    console.log("centering view on: " + newPos);
    mapView.setCenter(newPos);
});

let userFeatures = [accuracyFeature, positionFeature];
let markerSource = new VectorSource();

map.addLayer( new VectorLayer({
                source: new VectorSource({
                    features: userFeatures,
                }),
            }));

map.addLayer(new VectorLayer({
                source: markerSource,
            }));


// gets the view property of the map, which we can use to set the center and zoom
const mapView = map.getView();

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

function createMarker(event) {
    console.log("Adding new marker...");
    // first need to get all the user's input from the input fields when the button is pressed:
    // currently assumes all user input is valid
    console.log("Getting marker specifications from the form...")
    let markerInfo = event.formData;

    // for debugging
    for (const [key, value] of markerInfo) {
        console.log(`${key}: ${value}`);
    }

    let markerShape;
    let markerColor;

    // converts chosen color to hex value
    console.log("Setting color...");
    console.log("color from form: " + markerInfo.get('color'));
    switch (markerInfo.get('color')) {
        case "red":
            console.log("case: red");
            markerColor = '#FF0000';
            break;
        case "green":
            console.log("case: green");
            markerColor = '#00FF00';
            break;
        case "blue":
            console.log("case: blue");
            markerColor = '#0000FF';
            break;
        case "yellow":
            console.log("case: yellow");
            markerColor = '#FFFF00';
            break;
    }

    // creates the object for the marker's shape, using the shape and color specified by the user
    console.log("Setting shape...");
    console.log("shape from form: " + markerInfo.get('shape'));
    switch (markerInfo.get('shape')) {
        case "circle":
            console.log("case: circle");
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
            console.log("case: square");
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
            console.log("case: triangle");
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
    console.log("Making marker object...");
    console.log("Shape and color:");
    console.log(markerShape);
    console.log(markerColor);
    const marker = new Feature();
    marker.setStyle(
        new Style({image: markerShape,}),
    );
    console.log(marker);

    console.log("Adding marker to vector layer...");
    markerSource.addFeature(marker);

    // places the marker on the map
    console.log("Placing marker on map...");
    marker.setGeometry(new Point([markerInfo["xcoord"], markerInfo["ycoord"]]));
    console.log("Re-rendering map to show marker...");
    map.render(); // re-renders the map to show the marker
}

document.querySelector("#find-loc").addEventListener("click", findLocOnMap);

const markerData = document.getElementById("add-marker-form");

markerData.addEventListener("submit",(event) => {
    event.preventDefault();
    new FormData(markerData); // this causes the formdata event for the next eventListener
});
markerData.addEventListener("formdata", (event) => createMarker(event));
