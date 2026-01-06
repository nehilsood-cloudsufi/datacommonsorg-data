---
name: economics
description: Handle datasets related to economic indicators including GDP, income levels, poverty rates, consumer prices, inflation, commodity prices, interest rates, exchange rates, retail sales, minimum wage, and financial market data.
keywords:
  - gdp
  - gross domestic product
  - income
  - poverty
  - price
  - cpi
  - consumer price index
  - inflation
  - commodity
  - interest rate
  - exchange rate
  - currency
  - retail sales
  - wage
  - minimum wage
  - economic
  - financial
input_column_patterns:
  - gdp
  - gross_domestic_product
  - income
  - median_income
  - household_income
  - per_capita_income
  - poverty
  - poverty_rate
  - below_poverty
  - price
  - cpi
  - ppi
  - inflation
  - price_index
  - commodity
  - oil_price
  - gold_price
  - wheat_price
  - interest_rate
  - fed_rate
  - policy_rate
  - yield
  - exchange_rate
  - currency
  - forex
  - retail_sales
  - sales
  - trade
  - wage
  - minimum_wage
  - earnings
  - compensation
output_variable_patterns:
  - ConsumerPriceIndex
  - GrossDomesticProduct
  - MedianIncome
  - PovertyRate
  - InterestRate
  - ExchangeRate
  - RetailSales
  - MinimumWage
metadata_indicators:
  - header_rows: 5
  - aggregate_duplicate_svobs: last
  - number_decimal
  - number_separator
  - scalingFactor
source_patterns:
  - bls
  - bea
  - rbi
  - world_bank
  - oecd
  - bis
  - fao
  - sidra
  - ibge
  - saipe
countries:
  - USA
  - Brazil
  - India
  - Global
  - OECD
---

# Economics Skill

This skill processes datasets containing economic and financial indicators.

## What This Skill Handles

- **GDP and output**: Gross domestic product, economic growth, production indices
- **Income and poverty**: Household income, median income, poverty rates, SAIPE data
- **Prices and inflation**: Consumer Price Index (CPI), Producer Price Index, inflation rates
- **Commodity markets**: Commodity prices (oil, gold, wheat, agricultural)
- **Interest rates**: Federal funds rate, central bank rates, treasury yields
- **Exchange rates**: Currency exchange rates, foreign exchange data
- **Retail and trade**: Retail sales, trade balances
- **Wages**: Minimum wage, average wages, wage growth

## Real Input Column Patterns (from pvmap files)

A dataset likely belongs to this skill if it contains columns like:
- `gdp`, `gross_domestic_product`, `economic_output`
- `income`, `median_income`, `household_income`, `per_capita_income`
- `poverty`, `poverty_rate`, `below_poverty`
- `price`, `cpi`, `ppi`, `inflation`, `price_index`
- `commodity`, `oil_price`, `gold_price`, `wheat_price`
- `interest_rate`, `fed_rate`, `policy_rate`, `yield`
- `exchange_rate`, `currency`, `forex`
- `retail_sales`, `sales`, `trade`
- `wage`, `minimum_wage`, `earnings`

## Metadata Characteristics

Economics datasets often have:
- Multiple header rows (`header_rows: 5`)
- Duplicate observation handling (`aggregate_duplicate_svobs: last`)
- Number formatting specifications (`number_decimal`, `number_separator`)
- Scaling factors for units (`scalingFactor`)
- Time period specifications (`observationPeriod: P1M` for monthly)

## Standard Output Columns

```
observationAbout, observationDate, value, variableMeasured, unit, scalingFactor, measurementMethod, observationPeriod
```

## Source Abbreviations

Match datasets with these source identifiers:
- `bls` - Bureau of Labor Statistics
- `bea` - Bureau of Economic Analysis
- `rbi` - Reserve Bank of India
- `oecd` - OECD
- `bis` - Bank for International Settlements
- `fao` - Food and Agriculture Organization
- `sidra`, `ibge` - Brazil statistics
- `saipe` - Small Area Income and Poverty Estimates

## Geographic Coverage

15 datasets covering USA (BLS, BEA, Federal Reserve, Census), Brazil (SIDRA/IBGE), India (RBI), and global sources (World Bank, OECD, BIS, FAO).
