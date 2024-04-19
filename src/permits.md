---
title: Distance map
---

# Permit analysis

```js
const db = await FileAttachment("data/permit_data.db").sqlite();
// columnNames = [
//   0: "pparsID"
//   1: "planningScheme"
//   2: "applicationType"
//   3: "dateApplicationReceived"
//   4: "dateOfRAOutcome"
//   5: "dateOfFinalOutcome"
//   6: "responsibleAuthorityOutcome"
//   7: "finalOutcome"
//   8: "applicationCategory"
//   9: "currentLandUse"
//   10: "proposedLandUse"
//   11: "estimatedCostOfWorks"
//   12: "fees"
//   13: "submissions"
//   14: "publicNotice"
//   15: "referralIssued"
//   16: "furtherInformationRequested"
//   17: "vicSmart"
//   18: "sixtyDayTimeframe"
//   19: "vicSmartTimeframe"
//   20: "vcatGroundsForAppeal"
//   21: "vcatLodgementDate"
//   22: "vcatOutcomeDate"
//   23: "vcatOutcome"
//   24: "numberOfNewLots"
//   25: "numberOfNewDwellings"
// ]
const permits = await db.sql`SELECT * FROM permit LIMIT 50`;
view(Inputs.table(permits));
```

```js
// for each final outcome and each number of new dwellings, count the number of each combination
const counts = await db.sql`
SELECT numberOfNewDwellings, lower(finalOutcome) as finalOutcome, count(*) as count
FROM permit 
WHERE numberOfNewDwellings IS NOT NULL 
  AND numberOfNewDwellings > 0
  AND finalOutcome IS NOT NULL 
  AND finalOutcome != ''
GROUP BY numberOfNewDwellings, lower(finalOutcome)`

view(Inputs.table(counts));

// now groupby number of dwellings again, and then calculate (permit issued / (permit issued + no permit issued))
const issuedRates = Object.values(_.groupBy(counts, (d) => d.numberOfNewDwellings)).map(d => {
  const noPermitIssued = d.find(e => e.finalOutcome === "no permit issued")?.count || 0;
  const permitIssued = d.find(e => e.finalOutcome === "permit issued")?.count || 0;

  return {
    numberOfNewDwellings: d[0].numberOfNewDwellings,
    "issuedRate": permitIssued / (permitIssued + noPermitIssued),
  };
});
view(Inputs.table(issuedRates))
```

```js
Plot.plot({
  x: { 
    label: "Number of new dwellings",
    domain: [0, 3500] 
  },
  y: { 
    label: "Permit issued rate" 
  },
  title: "Permit issuance rate by number of new dwellings",
  marks: [
    Plot.linearRegressionY(issuedRates, { 
      x: "numberOfNewDwellings", 
      y: "issuedRate" 
    }),
    Plot.dot(issuedRates, { 
      x: "numberOfNewDwellings", 
      y: "issuedRate" 
    }),
  ],
})
```

```js
// for each final outcome and each number of new dwellings, count the number of each combination
const costs = await db.sql`
SELECT estimatedCostOfWorks, lower(finalOutcome) as finalOutcome
FROM permit 
WHERE estimatedCostOfWorks IS NOT NULL 
  AND finalOutcome IS NOT NULL 
  AND finalOutcome != ''`

// estimated costs of works are formatted like this: $-16,900,000.00
// we need to parse them into numbers
costs.forEach(d => {
  d.estimatedCostOfWorks = Number(d.estimatedCostOfWorks.replaceAll("$", "").replaceAll(",", ""));
})

view(Inputs.table(costs));
```

```js
Plot.plot({
  width: 1000,
  marginLeft: 100, 
  marginRight: 100,
  marginBottom: 100,
  grid: true,
  x: {
    // 500k, 1M, 2M, etc.
    tickRotate: 45,
    tickFormat: d => d3.format("$,")(d),
    label: "Estimated costs of works",
  },
  y: { 
    label: "Permit issued?",
    type: "log",
    clamp: true
  },
  color: {
    legend: true
  },
  title: "Permit issuance rate by estimated costs of works",
  marks: [
    Plot.rectY(costs, Plot.binX({y: "count" }, {x: "estimatedCostOfWorks", fy: "finalOutcome", fill: "finalOutcome"  }))
  ],
})
```