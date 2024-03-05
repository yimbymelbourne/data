---
title: Walkability
---

# Walkability

```js
import * as duckdb from "npm:@duckdb/duckdb-wasm";

const db = await DuckDBClient.of();
const walkability_by_node = FileAttachment("data/walkability_by_node.parquet").parquet();
const walkability_by_SAL = FileAttachment("data/walkability_by_SAL.geojson").json();

// TODO(mjbo): Try this again when duckdb-wasm gets a version bump
// db.query('INSTALL spatial').then(x => db.query('LOAD spatial'))
```

```js
async function plotMetrics({ x, y, fill }) {
  const columns = ["geography_name", x, y, fill]
  const columnsCsv = columns.map((col) => `"${col}"`).join(", ") + ",";
  const walkability_by_SA1 = await db.query(`SELECT ${columnsCsv} FROM read_parquet('https://tompisel.com/data/walkability_by_SA1.parquet')`);

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


<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMetrics({
  x: "bar or pub - within 500m",
  y: "park area - within 500m",
  fill: "median_rent_weekly",
})}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMetrics({
  x: "median_rent_weekly",
  y: "cafe - within 500m",
  fill: "average_household_size"
})}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMetrics({
  x: "child care - within 2km",
  y: "pct_owner_occupiers",
  fill: "median_age" })}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMetrics({
  x: "pct_households_wo_cars",
  y: "restaurant - within 1km",
  fill: "pct_apartments",
})}
</div>


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
        opacity: 0.8,
        tip: { channels: { name: "geography_name" } } 
      }),
    ],
  });
}
```

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMapScatter({
  fill: "library - closest",
  reverse: true
})}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMapScatter({
  fill: "cafe - closest",
  reverse: true
})}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${plotMapScatter({
  fill: "grocery or supermarket - within 1km"
})}
</div>

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
```

```js
const weeklyRentPlot = plotWeeklyRents()
```

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${weeklyRentPlot}
</div>


```js
import * as L from "npm:leaflet";

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

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${Plot.legend({ color: weeklyRentPlot.scale("color"), label: "Median rent, weekly ($)"})}
${leafletWeeklyRents()}
</div>

