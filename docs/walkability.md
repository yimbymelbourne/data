---
title: Walkability
---

# Walkability

```js
const final_sal_parquet = FileAttachment("data/final_sal.parquet").parquet();
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
      tip: { channels: { name: "geography_name" }}
    })
  ]
})
```