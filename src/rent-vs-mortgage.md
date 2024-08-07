# Rent vs Mortgage

```js
import { DuckDBClient } from 'npm:@observablehq/duckdb'

const rates = FileAttachment('data/housing_lending_rates.xlsx').xlsx()
const rents = FileAttachment('data/abs_sa2_rents.csv').csv({ typed: true })
const prices = FileAttachment('data/neoval_sa2_prices.csv').csv({ typed: true })
const db = DuckDBClient.of({
  src_prices: prices,
  src_rents: rents,
})
const plotParams = {
  x: 'monthly_repayment',
  y: 'typical_monthly_rent',
}
const titleCaseFormat = v => v
  .toLowerCase()
  .replace(/ +/g, ' ')
  .replace(/\b[a-z]/g, letter => letter.toUpperCase())
const priceFormat = v => d3.format('$,.0f')(Number(v))
const percentFormat = d3.format('.0%')
const noZeroFormat = fn => v => v === 0 ? '' : fn(v)
```

<div class="caution">
  The rent data (ABS, based on the 2021 census) is old and so this comparision is only vaguely indicative until we source more up to date data.
</div>

```js
const rateCells = [...rates.sheet('Data')]
const descriptionRow = rateCells.findIndex(row => row.A === 'Description')
const rateDescription = 'Lending rates; Housing credit; New loans funded in the month; Owner-occupied; Variable-rate; All institutions'
const [rateColumn] = Object.entries(rateCells[descriptionRow]).find(([column, value]) => value === rateDescription)
const latestInterestRate = rateCells.findLast(row => row.A instanceof Date)
const interestRate = latestInterestRate[rateColumn] / 100
const interestRateAsAt = latestInterestRate.A
```

A comparison of the rents vs mortgage repayments for houses and units in Melbourne.

## Sources and Assumptions

The following sources are used
* [**Neoval property price data**](https://neoval.io/) as at ${prices.at(0).date.toLocaleString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })}
* **ABS rent data** from the 2021 census
* [**RBA interest rates**](https://www.rba.gov.au/statistics/tables/xls/f06hist.xlsx), with the latest data from ${interestRateAsAt.toLocaleString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })})

The analysis only includes SA2s from the greater Melbourne region (although it would be easy to extend nationally given appropriate rent data).

Repayments are calculated on the assumption of a 20% deposit and a 30 year mortgage using the RBA rate of ${d3.format('.2%')(interestRate)} (the interest rate for *${rateDescription}*, which seemed the most appropriate to use for the situation of a renter becoming a home owner at the present point in time).

```js
const monthlyInterestRate = interestRate / 12
const data = db.query(`
  with
    rent as (
      with
        base as (
          select
            sa2_code_2021 as sa2_code,
            property_type,
            median_band as weekly_median_band,
            str_split(median_band, '-') AS band_parts,
          from src_rents
        ),

        step as (
          select
            *,
            band_parts[1]::float as band_lower,
            band_parts[2]::float as band_upper,
          from base
        )

      select
        * exclude (band_parts),
        (band_lower + band_upper) / 2 as typical_weekly_rent,
        (band_lower + band_upper) / 2 / 7 * 365 / 12 as typical_monthly_rent,
      from step
    ),

    repayment as (
      select
        *,
        geometric_mean as typical_price,
        round(geometric_mean * 0.8) as typical_loan, -- 80% LVR
        -- See https://stackoverflow.com/questions/17194957/replicate-pmt-function-in-sql-use-column-values-as-inputs
        -- Verified vs PMT in Google Sheets
        (
          (geometric_mean * 0.8) -- 80% LVR
          / (power(1 + ${monthlyInterestRate}, 30 * 12) - 1)
          * (${monthlyInterestRate} * power(1 + ${monthlyInterestRate}, 30 * 12))
        ) as monthly_repayment,
      from src_prices
    ),

    comparison as (
        select
          repayment.sa2_code,
          repayment.sa2_name,
          repayment.sua_name,
          repayment.gcc_name,

          repayment.property_type,
          repayment.typical_price,
          repayment.typical_loan,
          repayment.monthly_repayment,

          rent.typical_monthly_rent,

          round(rent.typical_monthly_rent / repayment.monthly_repayment, 2) as rent_to_repayment_ratio,
          round(repayment.monthly_repayment / rent.typical_monthly_rent, 2) as repayment_to_rent_ratio,
        from
          rent
          inner join repayment using (sa2_code, property_type)
    )

    select *,
    from comparison
`)
const comparisonDb = DuckDBClient.of({ data })
```

## Aggregate Ratios

```js
const metrics = (await comparisonDb.query(`
  select
    count(distinct sa2_code) as n_sa2s,
    count(distinct
      case
        when repayment_to_rent_ratio < 1 then sa2_code
        else null
      end
    ) as n_rent_cheaper_than_mortgage,
    median(repayment_to_rent_ratio) as median_repayment_to_rent_ratio,
    median(
      case
        when property_type = 'HOUSE' then repayment_to_rent_ratio
          else null
      end
    ) as median_house_repayment_to_rent_ratio,
    median(
      case
        when property_type = 'UNIT' then repayment_to_rent_ratio
          else null
      end
    ) as median_unit_repayment_to_rent_ratio,
  from data
`)).get(0)
```

Of ${metrics.n_sa2s} SA2s considered, there ${metrics.n_rent_cheaper_than_mortgage === 1 ? 'is' : 'are'} ${metrics.n_rent_cheaper_than_mortgage === 0 ? 'no' : metrics.n_rent_cheaper_than_mortgage} SA2s where typical rents are higher than typical mortgage repayments for units or houses.

Units typically have a ${metrics.median_unit_repayment_to_rent_ratio < metrics.median_house_repayment_to_rent_ratio ? 'lower' : 'higher'} repayment to rent ratio than houses with the median ratio for units being ${percentFormat(metrics.median_unit_repayment_to_rent_ratio)} vs ${percentFormat(metrics.median_house_repayment_to_rent_ratio)} for houses (a median of ${percentFormat(metrics.median_repayment_to_rent_ratio)} across all types) - and that's before taking into account the other costs of ownership (rates, insurance, maintenance, etc).

<div class="card">

```js
Plot.plot({
  marginRight: 50,
  color: {
    domain: [0, 3],
    scheme: 'reds',
    type: 'linear',
  },
  y: {
    grid: true,
    label: '# SA2s',
  },
  x: {
    domain: [0, 9],
    label: 'Mortgage % of Rent',
    tickFormat: noZeroFormat(percentFormat),
  },
  fy: {
    label: 'Property Type',
  },
  facet: {
    data,
    padding: 0,
    y: 'property_type',
  },
  marks: [
    Plot.rectY(data, Plot.binX(
      { y: 'count' },
      {
        fill: 'repayment_to_rent_ratio',
        thresholds: 80,
        tip: true,
        x: 'repayment_to_rent_ratio',
      },
    )),
    Plot.ruleY([0]),
    Plot.ruleX([0], { x: 1, stroke: 'green' }),
    Plot.tip(['Mortgage = rent'], { x: 1, y: 70, anchor: 'left' }),
  ],
})
```

</div>
<div class="card">


```js
Plot.plot({
  marginLeft: 70,
  y: {
    label: 'Property Type',
  },
  x: {
    domain: [0, 9],
    label: 'Mortgage % of Rent',
    tickFormat: noZeroFormat(percentFormat),
  },
  fy: {
    padding: 0,
    label: 'Property Type',
  },
  facet: {
    data,
    y: 'property_type',
  },
  marks: [
    Plot.ruleX([0]),
    Plot.boxX(data, { fill: 'property_type', x: 'repayment_to_rent_ratio' }),
  ],
})
```

</div>

## Detailed Distribution

```js
// We want to anchor the domains at zero, so need to figure out the maximum ourselves
const maxes = (await (await DuckDBClient.of({ data })).query(`
  select
    max(monthly_repayment) as max_repayment,
    max(typical_monthly_rent) as max_rent,
  from data
`)).get(0)
const round = v => Math.ceil(v / 2000) * 2000
const maxRepaymentDomain = round(maxes.max_repayment)
const maxRentDomain = round(maxes.max_rent)

const repaymentFormat = v => d3.formatPrefix('$.2~s', Math.max(maxRepaymentDomain, maxRentDomain))(Number(v))
```

<div class="card">

```js
Plot.plot({
  marginRight: 50,
  color: {
    domain: [0, 3],
    scheme: 'reds',
    type: 'linear',
  },
  x: {
    domain: [0, maxRepaymentDomain],
    label: 'Mortgage / month',
    tickFormat: repaymentFormat,
  },
  y: {
    domain: [0, maxRentDomain],
    label: 'Rent / month',
    tickFormat: repaymentFormat,
  },
  fy: {
    label: 'Property Type',
  },
  facet: {
    data,
    y: 'property_type',
  },
  marks: [
    Plot.dot(data, {
      fill: 'repayment_to_rent_ratio',
      fy: 'property_type',
      ...plotParams,
    }),
    Plot.tip(data, Plot.pointer({
      ...plotParams,
      title: d => `${titleCaseFormat(d.sa2_name)} / Mortgage ${percentFormat(d.repayment_to_rent_ratio)} of rent`
    })),
    Plot.ruleY([0]),
    Plot.link({ length: 1 }, {
      x1: 0,
      y1: 0,
      x2: maxRentDomain,
      y2: maxRentDomain,
    }),
    Plot.tip(['Mortgage = rent'], { x: maxRentDomain, y: maxRentDomain, anchor: 'left' }),
  ],
})
```

</div>

## SA2 Details

The specific details for all SA2s included can be checked below.

```js
const search = view(Inputs.search(data))
```

<div class="card" style="padding: 0">

```js
Inputs.table(search, {
  width: '100%',
  height: 800,
  align: {
    typical_price: 'right',
    typical_loan: 'right',
    monthly_repayment: 'right',
    typical_monthly_rent: 'right',
    rent_to_repayment_ratio: 'right',
    repayment_to_rent_ratio: 'right',
  },
  format: {
    sa2_code: x => `${x}`,
    sa2_name: titleCaseFormat,
    sua_name: titleCaseFormat,
    gcc_name: titleCaseFormat,
    typical_price: priceFormat,
    typical_loan: priceFormat,
    monthly_repayment: priceFormat,
    typical_monthly_rent: priceFormat,
    rent_to_repayment_ratio: percentFormat,
    repayment_to_rent_ratio: percentFormat,
  },
  header: {
    sa2_code: 'SA2 Code',
    sa2_name: 'SA2 Name',
    sua_name: 'SUA',
    gcc_name: 'GCC',
    property_type: 'Type',
    typical_price: 'Property $',
    typical_loan: '80% Loan',
    monthly_repayment: 'Mortgage',
    typical_monthly_rent: 'Rent',
    rent_to_repayment_ratio: 'Rent / Repayment Ratio',
    repayment_to_rent_ratio: 'Repayment / Rent Ratio',
  },
})
```

</div>
