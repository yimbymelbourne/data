---
title: Walkability
---

# Walkability

First, let's load Tom's "final"  cleaned data set from https://github.com/tpisel/walkability/blob/master/data/final/final_sal.feather. We can use the Arquero data frame library to load it because it supports Apache Arrow. 

```js
const final_sal_feather = FileAttachment("final_sal.feather");
```

```js
aq.fromArrow(final_sal_feather)
```

Hmm, okay, so it doesn't support the _Feather_ format. That sucks.

I'll just convert it in Python.

```python
import pyarrow.feather as feather
import pyarrow.parquet as pq

feather_table = feather.read_table('final_sal.feather')
pq.write_table(feather_table, 'final_sal.parquet')
```

```js
const final_sal_parquet = FileAttachment("./data/final_sal.parquet").parquet();
```

Let's try and reconstruct the parks and pubs visualization from https://github.com/tpisel/walkability/blob/master/plots/parks%20and%20pubs.png 

<img src="https://github.com/tpisel/walkability/blob/master/plots/parks%20and%20pubs.png?raw=true" />

```js
Plot.plot({
  grid: true,
  color: {
    legend: true,
    scheme: "plasma"
  },
  marks: [
    Plot.dot(final_sal_parquet, {x: "bar or pub - within 500m", y: "park area - within 500m", fill: "median_rent_weekly", tip: true })
  ]
})
```
