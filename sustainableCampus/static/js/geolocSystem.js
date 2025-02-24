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
import Overlay from "./node_modules/ol/Overlay.js";
import Select from './node_modules/ol/interaction/Select.js';
import {click} from "./node_modules/ol/events/condition.js";

// the center and zoom will be changed when location tracking is enabled to focus on the user's position
const view = new View({
    center: [0, 0],
    zoom: 12,
});

const rasterLayer = new TileLayer({
    source: new OSM(),
});

const drawMarkers = new VectorLayer({
    source: new VectorSource({
        features: [],
    })
});

// Creates the overlay used when the user wants to interact with a map marker.
const popContainer = document.getElementById('marker-popup');
const popContent = document.getElementById('marker-popup-content');
const popCloser = document.getElementById('marker-popup-closer');
const markerPopups = new Overlay({
    element: popContainer,
    autoPan: {
        animation: {
            duration: 250,
        },
    },
});

// handles closing the markerPopups
popCloser.onclick = function () {
    markerPopups.setPosition(undefined); // removes popup
    popCloser.blur();
    return false; // otherwise returns a href?
};

const map = new Map({
    layers: [
        rasterLayer,
        drawMarkers,
    ],
    target: 'map',
    view: view,
    overlays: [markerPopups],
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

// update the HTML page when the position changes.
geolocation.on('change', function () {
    el('accuracy').innerText = geolocation.getAccuracy() + ' [m]';
    el('altitude').innerText = geolocation.getAltitude() + ' [m]';
    el('altitudeAccuracy').innerText = geolocation.getAltitudeAccuracy() + ' [m]';
    el('heading').innerText = geolocation.getHeading() + ' [rad]';
    el('speed').innerText = geolocation.getSpeed() + ' [m/s]';
});

// make the circle around the user's marker, showing the possible inaccuracy of their position
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
// ternary operator used to create a new Point at the coordinates of the geolocator, if defined, null otherwise
geolocation.on('change:position', function () {
    const coordinates = geolocation.getPosition();
    positionFeature.setGeometry(coordinates ? new Point(coordinates) : null);
    // updates the view's centre to the user's new position:
    const newPos = positionFeature.getGeometry().getCoordinates();
    console.log("centering view on: " + newPos);
    mapView.setCenter(newPos);
});

let userFeatures = [accuracyFeature, positionFeature];

map.addLayer( new VectorLayer({
                source: new VectorSource({
                    features: userFeatures,
                }),
}));


// gets the view property of the map, which we can use to set the center and zoom
const mapView = map.getView();

function enableGeolocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(success, error)
    } else {
        alert("Geolocation is not supported by your browser.");
    }

    function error() {
        alert("Unable to find location.");
    }
}

function createMarkerFromForm(event) {
    // first need to get all the user's input from the input fields when the button is pressed:
    // currently assumes all user input is valid
    console.log("Getting marker specifications from the form...");
    let markerInfo = event.formData;

    // for debugging
    for (const [key, value] of markerInfo) {
        console.log(`${key}: ${value}`);
    }

    createMarker(markerInfo);
}

function createMarker(data) {
    console.log("Adding new marker...");


    let markerShape;
    let markerColor;

    // converts chosen color to hex value
    console.log("Setting color...");
    console.log("color from form: " + data.get('color'));
    switch (data.get('color')) {
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
    console.log("shape from form: " + data.get('shape'));
    switch (data.get('shape')) {
        case "circle":
            console.log("case: circle");
            markerShape = new CircleStyle({
                radius: 6,
                fill: new Fill({
                    color: markerColor,
                }),
                stroke: new Stroke({
                    color: '#000',
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
                    color: '#000',
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
                    color: '#000',
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
    const marker = new Feature({
        type: "marker",
    });
    marker.setStyle(new Style({
        image: markerShape,
    }));
    console.log(marker);

    console.log("Adding marker to vector layer...");
    drawMarkers.getSource().addFeature(marker);

    // places the marker on the map
    console.log("Placing marker on map...");
    marker.setGeometry(new Point([data.get("xcoord"), data.get("ycoord")]));
}

const markerData = document.getElementById("add-marker-form");

markerData.addEventListener("submit",(event) => {
    event.preventDefault();
    new FormData(markerData); // this causes the formdata event for the next eventListener
});
markerData.addEventListener("formdata", (event) => createMarkerFromForm(event));

// prompt user to enable geolocation
enableGeolocation();

// adding interactions to the map

// allowing selection of features (for markers)

// defines how a selected mark is styled
const selectedMarkerStyle = new Style({
    image: new CircleStyle({
        radius: 6,
        fill: new Fill({
            color: '#FFFFFF',
        }),
        stroke: new Stroke({
            color: '#FF00FF',
            width: 3,
        }),
    })

});

// features on the drawMarkers layer can be selected, which will restyle them (while selected) according to the
// selectedMarkerStyle
const clickSelection = new Select({
    condition: click,
    layers: [drawMarkers],
    style: selectedMarkerStyle,
});
map.addInteraction(clickSelection);
// when a marker is clicked:
clickSelection.on('select', function (e) {
    // add popup on marker
    console.log(e);

    const marker = e.selected[0];
    // avoids a popup appearing when a marker is deselcted by clicking on the map, instead of a marker
    if (marker !== undefined) {
        const markerPos = marker.getGeometry().getCoordinates();
        console.log("popup position: " + markerPos);
        popContent.innerHTML = '<p>Selected Marker at: </p><code>' + markerPos + '</code>';
        markerPopups.setPosition(markerPos);
    }
});
