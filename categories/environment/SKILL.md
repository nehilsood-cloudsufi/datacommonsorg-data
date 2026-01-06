---
name: environment
description: Handle datasets related to environmental data including Brazil wildfire events from INPE, FEMA flood insurance claims, OECD wastewater treatment, and sustainability financial incentives.
keywords:
  - environment
  - fire
  - wildfire
  - flood
  - disaster
  - climate
  - forest
  - pollution
  - waste
  - sustainability
  - emission
input_column_patterns:
  - Year
  - Janeiro
  - Fevereiro
  - Marco
  - Abril
  - Maio
  - Junho
  - Julho
  - Agosto
  - Setembro
  - Outubro
  - Novembro
  - Dezembro
  - Acre
  - Alagoas
  - Amapa
  - Amazonas
  - Bahia
  - Ceara
  - flood
  - claim
  - payment
  - wastewater
  - emission
output_variable_patterns:
  - Count_FireEvent
month_mapping_portuguese:
  Janeiro: "01"
  Fevereiro: "02"
  Marco: "03"
  Abril: "04"
  Maio: "05"
  Junho: "06"
  Julho: "07"
  Agosto: "08"
  Setembro: "09"
  Outubro: "10"
  Novembro: "11"
  Dezembro: "12"
observation_periods:
  - P1M
  - P1Y
aggregation:
  - "#Aggregate,sum"
brazilian_states:
  - Acre
  - Alagoas
  - Amapa
  - Amazonas
  - Bahia
  - Ceara
  - Distrito Federal
  - Espirito Santo
  - Goias
  - Maranhao
  - Mato Grosso
  - Mato Grosso do Sul
  - Minas Gerais
  - Para
  - Paraiba
  - Parana
  - Pernambuco
  - Piaui
  - Rio de Janeiro
  - Rio Grande do Norte
  - Rio Grande do Sul
  - Rondonia
  - Roraima
  - Santa Catarina
  - Sao Paulo
  - Sergipe
  - Tocantins
source_patterns:
  - inpe
  - fema
  - oecd
  - terrabrasilis
data_url_patterns:
  - terrabrasilis.dpi.inpe.br/queimadas
countries:
  - USA
  - Brazil
  - Global
  - OECD
---

# Environment Skill

This skill processes datasets containing environmental and sustainability information.

## What This Skill Handles

- **Wildfires**: Brazil INPE fire event counts from TerraBrasilis
- **Floods**: FEMA National Flood Insurance claims and payments
- **Waste management**: OECD wastewater treatment data
- **Sustainability**: Google sustainability financial incentives

## Real Input Column Patterns (from INPE Fire pvmap)

Year and month columns (Portuguese):
- `Year` - Observation year
- `Janeiro` (January) through `Dezembro` (December) - Monthly fire counts

Brazilian state columns:
- `Acre`, `Alagoas`, `Amapa`, `Amazonas`, `Bahia`, `Ceara`
- `Distrito Federal`, `Espirito Santo`, `Goias`, `Maranhao`
- `Mato Grosso`, `Mato Grosso do Sul`, `Minas Gerais`, `Para`
- `Paraiba`, `Parana`, `Pernambuco`, `Piaui`, `Rio de Janeiro`
- `Rio Grande do Norte`, `Rio Grande do Sul`, `Rondonia`, `Roraima`
- `Santa Catarina`, `Sao Paulo`, `Sergipe`, `Tocantins`

## Portuguese Month Mapping

```
Janeiro → 01, Fevereiro → 02, Marco → 03, Abril → 04
Maio → 05, Junho → 06, Julho → 07, Agosto → 08
Setembro → 09, Outubro → 10, Novembro → 11, Dezembro → 12
```

## Output Variable Patterns (DCID)

- `variableMeasured`: `Count_FireEvent`
- Aggregation: `#Aggregate,sum` for monthly totals

## Observation Periods

- `P1M` - Monthly data
- `P1Y` - Annual data (aggregated)

## Standard Output Columns

```
observationAbout, observationDate, value, observationPeriod, variableMeasured
```

Example INPE output:
```
dcid:country/BRA, 1998-06, 734, P1M, Count_FireEvent
dcid:wikidataId/Q40780, 1998-06, 3, P1M, Count_FireEvent  (Acre state)
dcid:country/BRA, 1998-07, 3088, P1M, Count_FireEvent
```

## Geographic Identifiers

- Brazil country: `country/BRA`
- Brazilian states: WikidataIds (e.g., `wikidataId/Q40780` for Acre)
- USA states/counties: `geoId/XX` or `geoId/XXXXX`

## Source Identifiers

- `inpe` - Brazil's Instituto Nacional de Pesquisas Espaciais
- `terrabrasilis` - TerraBrasilis database
- `fema` - Federal Emergency Management Agency
- `oecd` - OECD environmental data

## Geographic Coverage

4 datasets covering Brazil (INPE fire data), USA (FEMA flood insurance), and global sources (OECD wastewater, Google sustainability).
