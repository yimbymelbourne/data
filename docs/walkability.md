---
title: Walkability
---

# Walkability

```js
const final_sal_parquet = FileAttachment("data/final_sal.parquet").parquet()
const final_sat_geojson = FileAttachment("data/final_sal.geojson").json();
```

Let's try and reconstruct the parks and pubs visualization from
https://github.com/tpisel/walkability/blob/master/plots/parks%20and%20pubs.png

<img src="https://github.com/tpisel/walkability/blob/master/plots/parks%20and%20pubs.png?raw=true" />

```js
Plot.plot({
  grid: true,
  color: {
    legend: true,
    scheme: "plasma",
  },
  marks: [
    Plot.dot(final_sal_parquet, { 
      x: "bar or pub - within 500m", 
      y: "park area - within 500m", 
      fill: "median_rent_weekly", 
      tip: { channels: { name: "geography_name" } },
    }),
  ],
})
```


```js
import * as L from "npm:leaflet";

const div = display(document.createElement("div"));
div.style = "height: 400px;";

const map = L.map(div)
  .setView([-37.8136, 144.9631], 13);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png")
  .addTo(map);

const style = {
    "color": "#ff7800",
    "weight": 5,
    "opacity": 0.65
};

// TODO: Figure out why nothings appearing.
L.geoJSON(final_sat_geojson).addTo(map, {
    style
});
```