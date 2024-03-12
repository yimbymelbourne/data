---
title: Walkability
sql:
  walkability_by_node: "data/walkability_by_node.parquet"
  walkability_by_SAL: "data/walkability_by_SAL.parquet"
---

# Walkability

```js
const db = await DuckDBClient.of({
  walkability_by_node: FileAttachment("data/walkability_by_node.parquet"),
  walkability_by_SAL: FileAttachment("data/walkability_by_SAL.parquet"),
  walkability_by_SA1: FileAttachment("data/walka bility_by_SA1.parquet")
});
```

```js
// spatial only works under version 1.28.1-dev106.0
// right now, it's pinned to 1.28.0 for unknown reasons:
// https://github.com/observablehq/framework/blob/0b40787072ee245a54dbafc9a0d24d9a97ae2c17/src/javascript/imports.ts#L346
// when it's inevitibly bumped, the following commands will start working
await db.query('INSTALL spatial');
await db.query('LOAD spatial');

const walkability_by_SAL = await db.query(`
  SELECT ST_AsGeoJSON(ST_GeomFromWKB(geometry)) as geojson, *
  FROM walkability_by_SAL
`);

const walkability_by_SAL_feature_collection = {
  type: "FeatureCollection",
  features: walkability_by_SAL.map(({ geojson, ...properties }) => ({
    type: "Feature",
    geometry: JSON.parse(geojson),
    properties,
  })),
};
```

## Walkability by SA1

```js
async function plotMetrics({ x, y, fill }) {
  const columns = ["geography_name", x, y, fill]
  const columnsCsv = columns.map((col) => `"${col}"`).join(", ") + ",";
  const walkability_by_SA1 = await db.query(`SELECT ${columnsCsv} FROM walkability_by_SA1`);

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


## Walkability by node

```sql
SELECT * FROM walkability_by_node LIMIT 10
```

```js
async function plotMapScatter({ fill, reverse }) {
  const walkability_by_node = await db.query(`
    SELECT x, y, "${fill}" as "${fill}"
    FROM walkability_by_node
  `);

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

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${await plotMapScatter({
  fill: "library - closest",
  reverse: true
})}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${await plotMapScatter({
  fill: "cafe - closest",
  reverse: true
})}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${await plotMapScatter({
  fill: "grocery or supermarket - within 1km"
})}
</div>

## Walkability by SAL

```sql
SELECT * FROM walkability_by_SAL LIMIT 10
```

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
      Plot.geo(walkability_by_SAL_feature_collection, {
        fill: (d) => d.properties.median_rent_weekly,
        tip: { channels: { name: (d) => d.properties.geography_name } },
      }),
    ],
  });
}

const weeklyRentPlot = plotWeeklyRents();
```

<div class="card" style="max-width: 640px;">
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

  L.geoJSON(walkability_by_SAL_feature_collection, {
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
${plotWeeklyRentLegend()}
${leafletWeeklyRents()}
</div>

