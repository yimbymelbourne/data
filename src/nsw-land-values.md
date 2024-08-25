---
title: NSW land values
sql:
  lvs: data/nsw_land_values.parquet
---

# NSW land values

Data links:
- [Bulk land value information](https://www.valuergeneral.nsw.gov.au/land_value_summaries/lv.php)
- [Schema guide](https://www.nsw.gov.au/sites/default/files/noindex/2024-06/Land_Value_Information_User_Guide_Sml.pdf)

I'm only taking a limited subset of the entire schema, excluding previous valuations other than the latest, and high cardinality columns like address or property description.

```js
// Arrow table
const landValues = FileAttachment("data/nsw_land_values.parquet").parquet();

view(Inputs.table(landValues));
```

```sql
SELECT COUNT(*) FROM lvs
```

```js
// ChatGPT generated this, don't trust it
const NSW_ZONE_CODE_TO_NAME = {
    "A": "Residential",
    "AGB": "Agribusiness",
    "B": "Commercial",
    "B1": "Neighbourhood Centre",
    "B2": "Local Centre",
    "B3": "Commercial Core",
    "B4": "Mixed Use",
    "B5": "Business Development",
    "B6": "Enterprise Corridor",
    "B7": "Business Park",
    "C": "Conservation",
    "C1": "National Parks and Nature Reserves",
    "C2": "Environmental Conservation",
    "C3": "Environmental Management",
    "C4": "Environmental Living",
    "E": "Employment",
    "E1": "National Parks and Nature Reserves",
    "E2": "Environmental Conservation",
    "E3": "Environmental Management",
    "E4": "Environmental Living",
    "E5": "Commercial Core",
    "EM": "Enterprise",
    "ENT": "Enterprise Corridor",
    "ENZ": "Environmental Zone",
    "I": "Industrial",
    "IN1": "General Industrial",
    "IN2": "Light Industrial",
    "MU": "Mixed Use",
    "MU1": "Mixed Use",
    "O": "Open Space",
    "P": "Public Infrastructure",
    "R": "Recreation",
    "R1": "General Residential",
    "R2": "Low Density Residential",
    "R3": "Medium Density Residential",
    "R4": "High Density Residential",
    "R5": "Large Lot Residential",
    "RAZ": "Recreational Activities Zone",
    "RE1": "Public Recreation",
    "RE2": "Private Recreation",
    "REZ": "Recreation Zone",
    "RP": "Roads and Park Zone",
    "RU1": "Primary Production",
    "RU2": "Rural Landscape",
    "RU3": "Forestry",
    "RU4": "Primary Production Small Lots",
    "RU5": "Village",
    "RU6": "Transition",
    "S": "Special Uses",
    "SP1": "Special Activities",
    "SP2": "Infrastructure",
    "SP3": "Tourist",
    "SP4": "Recreational",
    "SP5": "Special Uses",
    "UD": "Urban Development",
    "UR": "Urban Release",
    "W1": "Natural Waterways",
    "W2": "Recreational Waterways",
    "W3": "Working Waterways",
    "W4": "Water Recreation Zone",
    "Z": "General Purpose Zoning"
};
```

```js
Plot.plot({
  width,
  marks: [
    Plot.boxX(landValues, {
      x: "LAND VALUE 1",
      y: "ZONE CODE",
      sort: { y: "x" }
    })
  ],
  x: {
    type: "log"
  }
})
```