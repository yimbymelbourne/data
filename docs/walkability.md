---
title: Walkability
sql: 
  walkability_by_SA1: "data/walkability_by_SA1.parquet"
  walkability_by_node: "data/walkability_by_node.parquet"
---

# Walkability

```js
const walkability_by_node = FileAttachment("data/walkability_by_node.parquet").parquet();
const walkability_by_SAL = FileAttachment("data/walkability_by_SAL.geojson").json();
const walkability_by_SA1 = FileAttachment("data/walkability_by_SA1.parquet").parquet();
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

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
${plotSA1WeeklyRentLegend()}
${plotMetrics({
  x: "bar or pub - within 500m",
  y: "park area - within 500m",
  fill: "median_rent_weekly",
})}
</div>

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMetrics({
  x: "median_rent_weekly",
  y: "cafe - within 500m",
  fill: "average_household_size"
})}
</div>

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMetrics({
  x: "child care - within 2km",
  y: "pct_owner_occupiers",
  fill: "median_age" })}
</div>

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMetrics({
  x: "pct_households_wo_cars",
  y: "restaurant - within 1km",
  fill: "pct_apartments",
})}
</div>

<div class="card">
<h2>SPLOM</h2>
<h3>TODO</h3>
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

view(Plot.plot({
    aspectRatio: 1,
    color: {
      domain: [0, 5000],
      legend: true,
      scheme: "turbo",
      label: "Max distance"
    },
    marks: [
      Plot.dot(walkability_by_node, { 
        x: "x", 
        y: "y", 
        fill: takeMax, 
        opacity: 0.8,
        tip: true
      }),
    ],
  }))
```

```js
function plotMapScatter({ fill, reverse }) {
  return Plot.plot({
    aspectRatio: 1,
    color: {
      legend: true,
      reverse,
      scheme: "turbo",
    },
    marks: [
      Plot.dot(walkability_by_node, { 
        x: "x", 
        y: "y", 
        fill, 
        opacity: 0.8
      }),
    ],
  });
}
```

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMapScatter({
  fill: "library - closest",
  reverse: true
})}
</div>

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMapScatter({
  fill: "cafe - closest",
  reverse: true
})}
</div>

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMapScatter({
  fill: "grocery or supermarket - within 1km"
})}
</div>

## Walkability by SAL

```js
function plotWeeklyRents() {
  return Plot.plot({
    grid: true,
    aspectRatio: 1,
    color: {
      legend: true,
      label: "Median rent, weekly ($)",
      scheme: "turbo",
    },
    marks: [
      Plot.geo(walkability_by_SAL, {
        fill: (d) => d.properties.median_rent_weekly,
        tip: { channels: { name: (d) => d.properties.geography_name } },
      }),
    ],
  });
}

const weeklyRentPlot = plotWeeklyRents();
```

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
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
  div.style = "height: 400px;";

  const map = L.map(div)
    .setView([-37.8136, 144.9631], 13);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png")
    .addTo(map);

  L.geoJSON(walkability_by_SAL, {
     onEachFeature: function (feature, layer) {
        // sync colors between plots
        const color = weeklyRentPlot.scale("color").apply(feature.properties.median_rent_weekly);
        layer.setStyle({ color }); 
    }
  }).addTo(map);

  return div;
}
```

<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
${plotWeeklyRentSALLegend()}
${leafletWeeklyRents()}
</div>

