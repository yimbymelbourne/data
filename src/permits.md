---
title: Permit analysis
---

# Permit analysis

```js
import {DuckDBClient} from "npm:@observablehq/duckdb";
const db = await DuckDBClient.of({base: FileAttachment("data/permit_data.db")});


const cleanedPermitData = await FileAttachment("data/cleaned_permit_data.csv").csv();

const tidy = cleanedPermitData.flatMap((d) => {
  return [
    {
      ...d,
      type: "total_dwelling_applications",
      dwellings: d.total_dwelling_applications
    },
    {
      ...d,
      type: "council_approved_dwellings",
      dwellings: d.council_approved_dwellings
    },
    {
      ...d,
      type: "council_rejected_dwellings",
      dwellings: d.council_rejected_dwellings
    },
    {
      ...d,
      type: "council_refused_vcat_approved_dwellings",
      dwellings: d.council_refused_vcat_approved_dwellings
    }
  ];
})
```


```js
Plot.plot({
  width,
  marginLeft: 100,
  marginBottom: 130,
  x: {
    tickRotate: 90
  },
  color: {
    legend: true
  },
  marks: [
    Plot.barY(
      tidy.filter((d) => d.type === "total_dwelling_applications"),
      {
        x: "planningScheme",
        y: "dwellings",
        stroke: "type",
        sort: { x: "y", reverse: true, limit: 20 }
      }
    ),
    Plot.barY(
      tidy.filter((d) => d.type !== "total_dwelling_applications"),
      {
        x: "planningScheme",
        y: "dwellings",
        fill: "type",
        sort: { x: "y", reverse: true, limit: 20 }
      }
    ),
    Plot.ruleY([0])
  ]
})
```

```js
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
const permits = await db.sql`SELECT * FROM base.permit LIMIT 50`;
// view(Inputs.table(permits));
```

```js
// for each final outcome and each number of new dwellings, count the number of each combination
const counts = await db.sql`
SELECT numberOfNewDwellings, lower(finalOutcome) as finalOutcome, count(*) as count
FROM base.permit 
WHERE numberOfNewDwellings IS NOT NULL 
  AND numberOfNewDwellings > 0
  AND finalOutcome IS NOT NULL 
  AND finalOutcome != ''
GROUP BY numberOfNewDwellings, lower(finalOutcome)`

// view(Inputs.table(counts));

// now groupby number of dwellings again, and then calculate (permit issued / (permit issued + no permit issued))
const issuedRates = Object.values(_.groupBy(counts.toArray(), (d) => d.numberOfNewDwellings)).map(d => {
  const noPermitIssued = d.find(e => e.finalOutcome === "no permit issued")?.count || 0;
  const permitIssued = d.find(e => e.finalOutcome === "permit issued")?.count || 0;

  return {
    numberOfNewDwellings: d[0].numberOfNewDwellings,
    "issuedRate": permitIssued / (permitIssued + noPermitIssued),
  };
});
// view(Inputs.table(issuedRates))
```


```js
// for each final outcome and each number of new dwellings, count the number of each combination
const costs = await db.sql`
SELECT 
  CAST(
    REPLACE(
      REPLACE(estimatedCostOfWorks, '$', ''), 
      ',', 
      ''
    ) AS NUMERIC
  ) as estimatedCostOfWorks,
  LOWER(finalOutcome) as finalOutcome
FROM base.permit 
WHERE 
  estimatedCostOfWorks IS NOT NULL 
  AND finalOutcome IS NOT NULL 
  AND finalOutcome != ''`

// view(Inputs.table(costs));
```

```js
// Plot.plot({
//   width: 1000,
//   marginLeft: 100, 
//   marginRight: 100,
//   marginBottom: 100,
//   grid: true,
//   x: {
//     // 500k, 1M, 2M, etc.
//     tickRotate: 45,
//     tickFormat: d => d3.format("$,")(d),
//     label: "Estimated costs of works",
//   },
//   y: { 
//     label: "Permit issued?",
//     type: "log",
//     clamp: true
//   },
//   color: {
//     legend: true
//   },
//   title: "Permit issuance rate by estimated costs of works",
//   marks: [
//     Plot.rectY(costs, Plot.binX({y: "count" }, {x: "estimatedCostOfWorks", fy: "finalOutcome", fill: "finalOutcome"  }))
//   ],
// })
```