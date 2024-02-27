---
title: Walkability
---

# Walkability

```js
const final_sal_parquet = FileAttachment("data/final_sal.parquet").parquet();
const final_sat_geojson = FileAttachment("data/final_sal.geojson").json();
const final_sa1_parquet = FileAttachment("data/final_sa1.parquet").parquet();
// const final_sa1_geojson = FileAttachment("data/final_sa1.geojson").json();
```

```js
function dotPlot({ x, y, fill }) {
  return Plot.plot({
    grid: true,
    color: {
      legend: true,
      scheme: "viridis",
    },
    marks: [
      Plot.dot(final_sa1_parquet, {
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
function geoPlot() {
  return Plot.plot({
    grid: true,
    aspectRatio: 1,
    color: {
      legend: true,
      label: "Median rent, weekly ($)",
      scheme: "viridis",
    },
    marks: [
      Plot.geo(final_sat_geojson, {
        fill: (d) => d.properties.median_rent_weekly,
        tip: { channels: { name: (d) => d.properties.geography_name } },
      }),
    ],
  })
}
```

```js
import * as L from "npm:leaflet";
function leafletMap() {
  const div = display(document.createElement("div"));
  div.style = "height: 400px;";

  const map = L.map(div)
    .setView([-37.8136, 144.9631], 13);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png")
    .addTo(map);

  const style = {
    "color": "#ff7800",
    "weight": 5,
    "opacity": 0.65,
  };

  L.geoJSON(final_sat_geojson).addTo(map, {
    style,
  });
  return div;
}
```

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${dotPlot({
  x: "bar or pub - within 500m",
  y: "park area - within 500m",
  fill: "median_rent_weekly",
})}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${dotPlot({ 
  x: "median_rent_weekly", 
  y: "cafe - within 500m", 
  fill: "average_household_size" 
})}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${dotPlot({ 
  x: "child care - within 2km", 
  y: "pct_owner_occupiers", 
  fill: "median_age" })}
</div>

<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${dotPlot({
  x: "pct_households_wo_cars",
  y: "restaurant - within 1km",
  fill: "pct_apartments",
})}
</div>


<div class="card" style="max-width: 640px;">
<h2>TODO</h2>
<h3>TODO</h3>
${geoPlot()}
</div>

${leafletMap()}
