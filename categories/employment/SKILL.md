---
name: employment
description: Handle datasets related to employment statistics, labor force participation, unemployment rates, job counts by industry, workforce demographics, occupational data, salary information, and labor market indicators.
keywords:
  - employment
  - unemployment
  - labor
  - labour
  - job
  - workforce
  - worker
  - occupation
  - salary
  - payroll
  - nonfarm
  - industry
input_column_patterns:
  - CEU0000000001
  - CES0000000001
  - CEU0500000001
  - CES0500000001
  - CEU0600000001
  - CES0600000001
  - CEU1000000001
  - CES1000000001
  - CES2000000001
  - CES3000000001
  - employment
  - employed
  - unemployment
  - unemployed
  - labor_force
  - workforce
  - payroll
  - nonfarm
  - occupation
  - industry
  - sector
  - salary
  - earnings
output_variable_patterns:
  - Count_Person_Employed
  - Count_Person_Employed_TotalNonfarm
  - Count_Person_Employed_TotalPrivate
  - Count_Person_Employed_GoodsProducing
  - Count_Person_Employed_MiningAndLogging
  - Count_Person_Employed_Construction
  - Count_Person_Employed_Manufacturing
measurement_methods:
  - BLSSeasonallyUnadjusted
  - BLSSeasonallyAdjusted
industry_codes:
  - NAICS/000000
  - NAICS/21
  - NAICS/23
  - JOLTS_000000
scaling:
  - "#Multiply,1000"
source_patterns:
  - bls
  - ces
  - nces
  - ncses
countries:
  - USA
  - South Korea
  - Mongolia
---

# Employment Skill

This skill processes datasets containing labor market and employment information.

## What This Skill Handles

- **Employment counts**: Number of employed persons, employment-to-population ratio
- **Unemployment**: Unemployment rate, unemployment claims, jobless statistics
- **Labor force**: Labor force participation, working-age population
- **Jobs by industry**: Employment by NAICS industry codes
- **Payroll data**: Nonfarm payrolls, job openings, job gains/losses
- **Occupational data**: Employment by occupation
- **Salary and earnings**: Median salary, average earnings by occupation
- **Workforce demographics**: Employment by age, gender, race, education level

## Real Input Column Patterns (from BLS pvmap files)

BLS Current Employment Statistics use coded columns:
- `CEU0000000001`, `CES0000000001` - All employees, total nonfarm
- `CEU0500000001`, `CES0500000001` - All employees, total private
- `CEU0600000001`, `CES0600000001` - All employees, goods-producing
- `CEU1000000001`, `CES1000000001` - All employees, mining and logging
- `CES2000000001` - All employees, construction
- `CES3000000001` - All employees, manufacturing

General patterns:
- `employment`, `employed`, `employment_rate`
- `unemployment`, `unemployed`, `jobless`
- `labor_force`, `workforce`, `payroll`, `nonfarm`
- `occupation`, `industry`, `sector`
- `salary`, `earnings`, `wage`

## Industry Mapping (NAICS Codes)

Employment data mapped to NAICS industry codes:
- `NAICS/000000` - Total
- `NAICS/21` - Mining
- `NAICS/23` - Construction
- `JOLTS_000000` - Job Openings and Labor Turnover Survey

## Measurement Methods

- `BLSSeasonallyUnadjusted` - Raw data
- `BLSSeasonallyAdjusted` - Seasonally adjusted

## Scaling

Values often in thousands: `#Multiply,1000`

## Standard Output Columns

```
observationAbout, observationDate, value, variableMeasured, observationPeriod, measurementMethod
```

Example output:
```
country/USA, 2015-01, 138491000, dcid:Count_Person_Employed_TotalNonfarm, P1M, BLSSeasonallyUnadjusted
```

## Geographic Coverage

7 datasets covering USA (BLS national and state level, NCES, NCSES), South Korea, and Mongolia.
