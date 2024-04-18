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
    // value: "B",
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
    .setView([-37.8136, 144.9631], 13);

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
        console.log(feature.properties)
        console.log(takeMax(feature.properties))
        const color = distancePlot.scale("color").apply(takeMax(feature.properties));
        console.log(color)

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

