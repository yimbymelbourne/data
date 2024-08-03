---
title: Walkability
sql:
  # walkability_by_node: "data/walkability_by_node.parquet"
  walkability_by_SA1: "data/walkability_by_SA1.parquet"
---

# Walkability

```js
// const walkability_by_node = FileAttachment("data/walkability_by_node.parquet").parquet();
const walkability_by_SA1 = FileAttachment(
  "data/walkability_by_SA1.parquet"
).parquet()
```

## Walkability by SA1 njsdjkflbnvgjkdsfbkls

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
  })
}
```

```js
// adapted from https://uwdata.github.io/mosaic/examples/splom.html
const $brush = vg.Selection.single()

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
    vg.frame({ stroke: "#ccc" }),
    vg.dot(vg.from("walkability_by_SA1"), {
      x,
      y,
      fill: "median_rent_weekly",
      r: 2,
    }),
    vg.intervalXY({ as: $brush }),
    vg.highlight({ by: $brush, opacity: 0.1 }),
    vg.xLabelAnchor("center"),
    vg.yLabelAnchor("center")
  )
}

const plotSA1Splom = () =>
  vg.vconcat(
    ...dependentVariables.map((d) =>
      vg.hconcat(...independentVariables.map((i) => makeFacet(i, d)))
    )
  )
```

```js
function plotSA1WeeklyRentLegend() {
  const rent = Plot.dotX(walkability_by_SA1, {
    x: 0,
    fill: "median_rent_weekly",
  }).plot()
  return Plot.legend({
    color: rent.scale("color"),
    label: "Median rent, weekly ($)",
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
