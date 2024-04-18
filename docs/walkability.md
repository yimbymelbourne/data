---
title: Walkability
sql: 
  walkability_by_node: "data/walkability_by_node.parquet"
  walkability_by_SA1: "data/walkability_by_SA1.parquet"
---

# Walkability

```js
const walkability_by_node = FileAttachment("data/walkability_by_node.parquet").parquet();
const walkability_by_SA1 = FileAttachment("data/walkability_by_SA1.parquet").parquet();

const walkability_by_node_geojson = FileAttachment("data/walkability_by_node.geojson").json();
const walkability_by_SA1_geojson = FileAttachment("data/walkability_by_SA1.geojson").json()
const walkability_by_SAL_geojson = FileAttachment("data/walkability_by_SAL.geojson").json()
```

## Walkability by SA1


```js
async function plotMetrics({ x, y, fill }) {
  return Plot.plot({
    grid: true,
    color: {
      legend: true,
      scheme: "turbo",
    },
    marks: [
      Plot.dot(walkability_by_SA1, {
        x,
        y,
        fill,
        tip: { channels: { name: "geography_name" } },
      }),
    ],
  });
}
```

```js
// adapted from https://uwdata.github.io/mosaic/examples/splom.html
const $brush = vg.Selection.single();

const independentVariables = [
  "restaurant - within 1km",
  "grocery or supermarket - within 1km",
  "cafe - within 1km",
  "bar or pub - within 1km",
]

const dependentVariables = [
  "median_rent_weekly",
  "pct_households_wo_cars",
  "pct_houses",
  "pct_owner_occupiers",
  "pct_apartments",
]


const makeFacet = (x, y) => {
  return vg.plot(
    // https://uwdata.github.io/mosaic/api/vgplot/attributes.html
    vg.frame({stroke: "#ccc"}),
    vg.dot(
      vg.from("walkability_by_SA1"),
      {x, y, fill: "median_rent_weekly", r: 2}
    ),
    vg.intervalXY({as: $brush}),
    vg.highlight({by: $brush, opacity: 0.1}),
    vg.xLabelAnchor("center"),
    vg.yLabelAnchor("center"),
  )
}

const plotSA1Splom = () => vg.vconcat(
  ...dependentVariables.map(d => vg.hconcat(...independentVariables.map(i => makeFacet(i, d)))
))
```

```js
function plotSA1WeeklyRentLegend() {
  const rent = Plot.dotX(walkability_by_SA1, {
    x: 0,
    fill: "median_rent_weekly",
  }).plot()
  return Plot.legend({
    color: rent.scale("color"),
    label: "Median rent, weekly ($)"
  })
}
```

<div>
${plotSA1WeeklyRentLegend()}
${plotMetrics({
  x: "bar or pub - within 500m",
  y: "park area - within 500m",
  fill: "median_rent_weekly",
})}
</div>

<div>
${plotMetrics({
  x: "median_rent_weekly",
  y: "cafe - within 500m",
  fill: "average_household_size"
})}
</div>

<div>
${plotMetrics({
  x: "child care - within 2km",
  y: "pct_owner_occupiers",
  fill: "median_age" })}
</div>

<div>
${plotMetrics({
  x: "pct_households_wo_cars",
  y: "restaurant - within 1km",
  fill: "pct_apartments",
})}
</div>

<div>
${plotSA1WeeklyRentLegend()}
${plotSA1Splom()}
</div>


## Walkability by node

```sql id=[nodesHead] display
SELECT * FROM walkability_by_node LIMIT 10
```

```js
view({...nodesHead})
view(Object.keys(nodesHead))
const closestKeys = Object.keys(nodesHead).filter(d => d.includes("closest"))
view(closestKeys)
```

```js
const consideredKeys = view(
  Inputs.checkbox(closestKeys, {
    sort: true,
    unique: true,
    value: "museum - closest",
    label: "Choose amenities you care about:"
  })
);
```

```js
function takeMax(node) {
  // extract the values using the considered keys from the node
  const consideredValues = consideredKeys.map(key => node[key]).map(d => d || 5000);
  // console.log(consideredValues)

  return Math.max(...consideredValues);
}
```

```js
const distancePlot = Plot.plot({
    grid: true,
    aspectRatio: 1,
    width: 1000,
    color: {
      domain: [0, 5000],
      legend: true,
      scheme: "turbo",
      label: "Max distance"
    },
    marks: [
      Plot.geo(walkability_by_node_geojson, {
        fill: (d) => takeMax(d.properties),
        tip: true
      }),
    ],
  })

view(distancePlot)
```

## Walkability by SA1 again

```js
Plot.plot({
    grid: true,
    aspectRatio: 1,
    width: 1000,
    color: {
      domain: [0, 1200],
      legend: true,
      label: "Median rent, weekly ($)",
      scheme: "plasma",
    },
    marks: [
      Plot.geo(walkability_by_SA1_geojson, {
        fill: (d) => d.properties.median_rent_weekly,
        tip: { channels: { name: (d) => d.properties.geography_name } },
      }),
    ],
  })
```

## Walkability by SAL

```js
function plotWeeklyRents() {
  return Plot.plot({
    grid: true,
    aspectRatio: 1,
    width: 1000,
    color: {
      domain: [0, 1200],
      legend: true,
      label: "Median rent, weekly ($)",
      scheme: "plasma",
    },
    marks: [
      Plot.geo(walkability_by_SAL_geojson, {
        fill: (d) => d.properties.median_rent_weekly,
        tip: { channels: { name: (d) => d.properties.geography_name } },
      }),
    ],
  });
}

const weeklyRentPlot = plotWeeklyRents();
```

<div>
${weeklyRentPlot}
</div>

```js
const DEFAULT_VIEWPORT_LAT_LON = [-37.8136, 144.9631];
```

```js
import * as L from "npm:leaflet";

function plotWeeklyRentSALLegend() {
  return Plot.legend({
    color: weeklyRentPlot.scale("color"),
    label: "Median rent, weekly ($)"
  })
}

function leafletWeeklyRents() {
  const div = display(document.createElement("div"));
  div.style = "height: 800px;";

  const map = L.map(div)
    .setView(DEFAULT_VIEWPORT_LAT_LON, 13);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png")
    .addTo(map);

  L.geoJSON(walkability_by_SA1_geojson, {
     onEachFeature: function (feature, layer) {
        // sync colors between plots
        const color = weeklyRentPlot.scale("color").apply(feature.properties.median_rent_weekly);
        layer.setStyle({ color }); 
    }
  }).addTo(map);

  L.geoJSON(walkability_by_node_geojson, {
     pointToLayer: function (feature, latlng) {
        // sync colors between plots
        const color = distancePlot.scale("color").apply(takeMax(feature.properties));

        const geojsonMarkerOptions = {
            radius: 8,
            fillColor: color,
            color: color,
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        };

        return L.circleMarker(latlng, geojsonMarkerOptions);
    }
  }).addTo(map);

  return div;
}
```

<div>
${plotWeeklyRentSALLegend()}
${leafletWeeklyRents()}
</div>

## deck.gl

```js
import deck from "npm:deck.gl";
import mapboxgl from "npm:mapbox-gl";
import Color from "npm:color-js";
const {DeckGL, AmbientLight, GeoJsonLayer, HexagonLayer, LightingEffect, PointLight} = deck;
```


```js
const COLOR_RANGE = [
  [1, 152, 189],
  [73, 227, 206],
  [216, 254, 181],
  [254, 237, 177],
  [254, 173, 84],
  [209, 55, 78]
];

const colorLegend = Plot.plot({
  margin: 0,
  marginTop: 20,
  width: 180,
  height: 35,
  style: "color: white;",
  x: {padding: 0, axis: null},
  marks: [
    Plot.cellX(COLOR_RANGE, {fill: ([r, g, b]) => `rgb(${r},${g},${b})`, inset: 0.5}),
    Plot.text(["Fewer"], {frameAnchor: "top-left", dy: -12}),
    Plot.text(["More"], {frameAnchor: "top-right", dy: -12})
  ]
});
```

```js
// https://observablehq.com/@visionscarto/world-atlas-topojson#files
const topo = import.meta.resolve("npm:visionscarto-world-atlas/world/50m.json");
const world = fetch(topo).then((response) => response.json());
const countries = world.then((world) => topojson.feature(world, world.objects.countries));
```

<div class="card" style="margin: 0 -1rem;">

<figure style="max-width: none; position: relative;">
  <div id="container" style="border-radius: 8px; overflow: hidden; background: rgb(18, 35, 48); height: 800px; margin: 1rem 0; "></div>
  <div style="position: absolute; top: 1rem; right: 1rem; filter: drop-shadow(0 0 4px rgba(0,0,0,.5));">${plotWeeklyRentSALLegend()}</div>
  <div style="position: absolute; top: 4rem; right: 1rem; filter: drop-shadow(0 0 4px rgba(0,0,0,.5));">${colorLegend}</div>
  <figcaption>Data: <a href="">TODO</a></figcaption>
</figure>

</div>

```js
const deckInstance = new DeckGL({
  container,
  initialViewState: {
    longitude: DEFAULT_VIEWPORT_LAT_LON[1],
    latitude: DEFAULT_VIEWPORT_LAT_LON[0],
    zoom: 13,
    minZoom: 5,
    maxZoom: 15,
    pitch: 40.5,
    bearing: -5
  },
  // getTooltip: ({ object}) => {
  //   if (!object) return null;
  //   const [lng, lat] = object.position;
  //   const count = object.points.length;
  //   return `latitude: ${lat.toFixed(2)}
  //     longitude: ${lng.toFixed(2)}
  //     ${count} collisions`;
  // },
  effects: [
    new LightingEffect({
      ambientLight: new AmbientLight({color: [255, 255, 255], intensity: 1.0}),
      pointLight: new PointLight({color: [255, 255, 255], intensity: 0.8, position: [-0.144528, 49.739968, 80000]}),
      pointLight2: new PointLight({color: [255, 255, 255], intensity: 0.8, position: [-3.807751, 54.104682, 8000]})
    })
  ],
  controller: true,
  map: mapboxgl,
  mapboxApiAccessToken: "pk.eyJ1IjoibWF4Ym8iLCJhIjoiY2lsd2JnZDRyMDFxNHZna3MwZDZmN2R0ZCJ9.32XWATCazaiDzdW6bXvBxw",
  mapStyle: "mapbox://styles/mapbox/light-v10",
  layers: [
    // Add the rent layer
    new GeoJsonLayer({
      id: "rent",
      data: walkability_by_SA1_geojson,
      opacity: 0.5,
      stroked: false,
      filled: true,
      wireframe: true,
      getElevation: (f) => f.properties.median_rent_weekly / 10,
      getFillColor: (f) => {
        const hex = weeklyRentPlot.scale("color").apply(f.properties.median_rent_weekly)
        const color = Color(hex);
        return [color.red * 255, color.green * 255, color.blue * 255]
      },
      getLineColor: [255, 255, 255],
    }),
    // Add the node layer as a HexagonLayer
    new HexagonLayer({
      id: "nodes",
      data: [...walkability_by_node_geojson.features],
      radius: 100,
      elevationScale: 10,
      extruded: true,
      colorRange: COLOR_RANGE,
      coverage: 1,
      getPosition: (f) => f.geometry.coordinates,
      getElevation: (f) => takeMax(f.properties),
      elevationAggregation: "MIN",
      getColor: (f) => {
        const hex = distancePlot.scale("color").apply(takeMax(f.properties));
        const color = Color(hex);
        return [color.red * 255, color.green * 255, color.blue * 255]
      },
      colorAggregation: "MIN",
    }),
  ]
});

// clean up if this code re-runs
invalidation.then(() => {
  deckInstance.finalize();
  container.innerHTML = "";
});
```
