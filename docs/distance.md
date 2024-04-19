---
title: Distance map

sql: 
  walkability_by_node: "data/walkability_by_node.parquet"
---

# Distance

A Melbourne specific clone of [close.city](https://close.city/).


```js
const walkability_by_node_geojson = FileAttachment("data/walkability_by_node.geojson").json();
const walkability_by_SA1_geojson = FileAttachment("data/walkability_by_SA1.geojson").json()
```

<div class="card" style="margin: 0 -1rem;">

<figure style="max-width: none; position: relative;">
  <div id="container" style="border-radius: 8px; overflow: hidden; background: rgb(18, 35, 48); height: 800px; margin: 1rem 0; "></div>
  <div style="position: absolute; top: 1rem; right: 1rem; filter: drop-shadow(0 0 4px rgba(0,0,0,.5));">${plotWeeklyRentLegend()}</div>
  <div style="position: absolute; top: 4rem; right: 1rem; filter: drop-shadow(0 0 4px rgba(0,0,0,.5));">${plotDistanceLegend()}</div>
  <figcaption>Data: <a href="">TODO</a></figcaption>
</figure>

</div>


```sql id=[nodesHead] display
SELECT * FROM walkability_by_node LIMIT 10
```

```js
view({...nodesHead})
view(Object.keys(walkability_by_node_geojson.features[0].properties))
const closestKeys = Object.keys(nodesHead).filter(d => d.includes("closest"))
view(closestKeys)
```

```js
const consideredKeys = view(
  Inputs.checkbox(closestKeys, {
    sort: true,
    unique: true,
    value: ["restaurant - closest", "grocery or supermarket - closest", "cafe - closest", "bar or pub - closest", "park area - closest", "school - closest", "child care - closest", "medical facility - closest"],
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
const DISTANCE_LEGEND_LABEL = "Max distance to a desired amenity (m)";

const distancePlot = Plot.plot({
    grid: true,
    aspectRatio: 1,
    width: 1000,
    color: {
      domain: [0, 5000],
      legend: true,
      scheme: "turbo",
      label: DISTANCE_LEGEND_LABEL
    },
    marks: [
      Plot.geo(walkability_by_node_geojson, {
        fill: (d) => takeMax(d.properties),
        tip: true
      }),
    ],
  })

view(distancePlot)

function plotDistanceLegend() {
  return Plot.legend({
    color: distancePlot.scale("color"),
    label: DISTANCE_LEGEND_LABEL
  })
}
```

```js
const WEEKLY_RENT_LEGEND_LABEL = "Median rent, weekly ($)";

const weeklyRentPlot  = Plot.plot({
    grid: true,
    aspectRatio: 1,
    width: 1000,
    color: {
      domain: [0, 1200],
      legend: true,
      label: WEEKLY_RENT_LEGEND_LABEL,
      scheme: "plasma",
    },
    marks: [
      Plot.geo(walkability_by_SA1_geojson, {
        fill: (d) => d.properties.median_rent_weekly,
        tip: { channels: { name: (d) => d.properties.geography_name } },
      }),
    ],
  })

view(weeklyRentPlot)

function plotWeeklyRentLegend() {
  return Plot.legend({
    color: weeklyRentPlot.scale("color"),
    label: WEEKLY_RENT_LEGEND_LABEL
  })
}
```

```js
import deck from "npm:deck.gl";
import mapboxgl from "npm:mapbox-gl";
import Color from "npm:color-js";
const {DeckGL, AmbientLight, GeoJsonLayer, ColumnLayer, LightingEffect, PointLight} = deck;
```

```js
// https://observablehq.com/@visionscarto/world-atlas-topojson#files
const topo = import.meta.resolve("npm:visionscarto-world-atlas/world/50m.json");
const world = fetch(topo).then((response) => response.json());
const countries = world.then((world) => topojson.feature(world, world.objects.countries));
```


```js
// Melbourne CBD
const DEFAULT_VIEWPORT_LAT_LON = [-37.8136, 144.9631];

const deckInstance = new DeckGL({
  container,
  initialViewState: {
    longitude: DEFAULT_VIEWPORT_LAT_LON[1],
    latitude: DEFAULT_VIEWPORT_LAT_LON[0],
    zoom: 15,
    minZoom: 5,
    maxZoom: 15,
    pitch: 40.5,
    bearing: 0
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
    // Add the node layer as a ColumnLayer
    new ColumnLayer({
      id: "nodes",
      data: [...walkability_by_node_geojson.features],
      radius: 100,
      elevationScale: 0.2,
      opacity: 0.5,
      extruded: true,
      coverage: 1,
      getPosition: (f) => f.geometry.coordinates,
      getElevation: (f) => 5000 - takeMax(f.properties),
      getColor: (f) => {
        const hex = distancePlot.scale("color").apply(takeMax(f.properties));
        const color = Color(hex);
        return [color.red * 255, color.green * 255, color.blue * 255]
      },
    }),
  ]
});

// clean up if this code re-runs
invalidation.then(() => {
  deckInstance.finalize();
  container.innerHTML = "";
});
```
