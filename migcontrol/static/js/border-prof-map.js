// profmap.js

// Styling for circular markers
const markerColor = '#8B0000'; // Dark red
const markerOpacity = 0.8;
const markerRadius = 3;

// Styling for clusters (additional styling for cluster icon in style sheet)
const clusterMaxRadius = 20;        // How close markers must be to cluster
const clusterSpiderfyMultiplier = 1.3;
const clusterLineColor = '#222';
const clusterLineWeight = 1.5;
const clusterLineOpacity = 0.5;

const clusterIconSize = L.point(30, 30);
const clusterIconClass = 'custom-cluster-icon';

// Set limits of bounding box of the map (here: world bounds)
const southWest = L.latLng(-90, -180);
const northEast = L.latLng(90, 180);
const bounds = L.latLngBounds(southWest, northEast);


// Initialize the map
var map = L.map('map', {
    maxZoom: 9
}).setView([40, 15], zoomLevel);


// Add Esri tiles to the map
const esriLayer = L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}',
    {
        attribution: 'Tiles © Esri — Source: USGS, Esri, TANA, DeLorme, and NPS',
        maxZoom: 9,
        noWrap: false
    }
).addTo(map);

// Fallback to OSM if Esri fails
esriLayer.on('tileerror', function () {
    map.removeLayer(esriLayer);

    L.tileLayer('https://cartodb-basemaps-a.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors & CARTO',
        maxZoom: 18
    }).addTo(map);
});

// Apply max bounds to prevent endless panning
map.setMaxBounds(bounds);


// Create a marker cluster group
var markers = L.markerClusterGroup({
    iconCreateFunction: function(cluster) {
        var count = cluster.getChildCount();
        return L.divIcon({
            html: '<div class="custom-cluster-icon">' + count + '</div>',
            className: clusterIconClass,
            iconSize: clusterIconSize
        });
    },
    showCoverageOnHover: false,
    spiderLegPolylineOptions: {
        weight: clusterLineWeight,
        color: clusterLineColor,
        opacity: clusterLineOpacity
    },
    spiderfyDistanceMultiplier: clusterSpiderfyMultiplier,
    maxClusterRadius: clusterMaxRadius // Determines how close markers need to be to be clustered
});

// Create a circular marker for each profiteer
function createMarkers(profiteers) {
    profiteers.forEach(function(profiteer) {
        // Skip invalid coordinates
        if (
            !profiteer.coords ||
            profiteer.coords.length !== 2 ||
            typeof profiteer.coords[0] !== 'number' ||
            typeof profiteer.coords[1] !== 'number' ||
            profiteer.coords[0] < -90 || profiteer.coords[0] > 90 ||
            profiteer.coords[1] < -180 || profiteer.coords[1] > 180
        ) return;

        // Create a circular marker for others
        const marker = L.circleMarker(profiteer.coords, {
            color: markerColor,
            fillColor: markerColor,
            fillOpacity: markerOpacity,
            radius: markerRadius
        });

        // Bind a popup with name, location etc.
        marker.bindPopup(`
            <b>${profiteer.name}</b><br>
            Address: <i>${profiteer.address}</i><br>
            Status: <i>${profiteer.status}</i><br>
            <a href="${profiteer.link}" target="_blank">More details</a>
        `);

        // Add marker to the cluster group
        markers.addLayer(marker);
    });
}

createMarkers(profiteers, 'Profiteers');

// Add marker cluster group to the map
map.addLayer(markers);
