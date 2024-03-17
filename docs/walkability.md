---
title: Walkability
sql: 
  walkability_by_SA1: "data/walkability_by_SA1.parquet"
---

# Walkability

```js
const walkability_by_node = FileAttachment("data/walkability_by_node.parquet").parquet();
const walkability_by_SAL = FileAttachment("data/walkability_by_SAL.geojson").json();
const walkability_by_SA1 = FileAttachment("data/walkability_by_SA1.parquet").parquet();
```

## Walkability by SA1

```sql
SELECT * FROM walkability_by_SA1 LIMIT 5
```

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
// borrowed from https://uwdata.github.io/mosaic/examples/splom.html
const $brush = vg.Selection.single();
// https://uwdata.github.io/mosaic/api/vgplot/attributes.html
const defaultAttributes = [
  // vg.xTicks(3),
  // vg.yTicks(4),
  // vg.xDomain(vg.Fixed),
  // vg.yDomain(vg.Fixed),
  // vg.colorDomain(vg.Fixed),
  // vg.marginTop(5),
  // vg.marginBottom(10),
  // vg.marginLeft(10),
  // vg.marginRight(5),
  // vg.xAxis(null),
  // vg.yAxis(null),
  vg.xLabelAnchor("center"),
  vg.yLabelAnchor("center"),
  // vg.xTickFormat("s"),
  // vg.yTickFormat("s"),
];

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
    vg.frame({stroke: "#ccc"}),
    vg.dot(
      vg.from("walkability_by_SA1"),
      {x, y, fill: "median_rent_weekly", r: 2}
    ),
    vg.intervalXY({as: $brush}),
    vg.highlight({by: $brush, opacity: 0.1}),
    ...defaultAttributes
  )
}

const plotSA1Splom = () => vg.vconcat(...dependentVariables.map(d =>
  vg.hconcat(...independentVariables.map(i => makeFacet(i, d)))
))
```


<div class="card">
<h2>TODO</h2>
<h3>TODO</h3>
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
${plotSA1Splom()}
</div>


## Walkability by node

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

function plotWeeklyRentLegend() {
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
${plotWeeklyRentLegend()}
${leafletWeeklyRents()}
</div>

