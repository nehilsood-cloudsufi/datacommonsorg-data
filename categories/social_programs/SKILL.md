---
name: social_programs
description: Handle datasets related to Brazil government social programs including food basket distribution to specific populations (indigenous, quilombola, fishing, extractive families) and rural development programs.
keywords:
  - social program
  - welfare
  - assistance
  - aid
  - benefit
  - food distribution
  - food basket
  - rural development
  - beneficiary
  - indigenous
  - quilombola
input_column_patterns:
  - food_basket
  - distribution
  - beneficiary
  - recipient
  - family
  - assistance
  - aid
  - program
population_types:
  - ExtractiveFamily
  - FishingFamily
  - IndigenousFamily
  - GypsyFamily
  - QuilombolaFamily
  - RecycledMaterialCollectorFamily
  - SettledFamilies
  - EmergencyCare
pvmap_file_patterns:
  - FoodBasket_ExtractiveFamily_pvmap.csv
  - FoodBasket_FishingFamily_pvmap.csv
  - FoodBasket_IndigenousFamily_pvmap.csv
  - FoodBasket_GypsyFamily_processed_csv.csv
  - FoodBasket_RecycledMaterialCollectorFamily_pvmap.csv
  - FoodBasket_EmergencyCare_pvmap.csv
  - FoodDistributionAct_FoodBasketByPartners_pvmap.csv
  - MunicipalFoodBasket_*_pvmap.csv
metadata_characteristics:
  number_decimal: ","
  number_separator: " "
  schemaless: 1
place_resolution:
  - Brazil_Places_Resolved.csv
source_patterns:
  - visdata
countries:
  - Brazil
---

# Social Programs Skill

This skill processes datasets containing Brazil government social program and welfare information.

## What This Skill Handles

- **Food assistance**: Food basket distribution to specific population groups
- **Rural development**: Agricultural support, rural productive activities
- **Welfare benefits**: Social welfare payments, public assistance
- **Beneficiary data**: Program recipients by demographics, eligibility
- **Targeted programs**: Programs for vulnerable populations

## Real Population Types (from pvmap files)

Programs target specific vulnerable populations:
- `ExtractiveFamily` - Extractive/forest communities
- `FishingFamily` - Fishing communities
- `IndigenousFamily` - Indigenous populations
- `GypsyFamily` - Roma/Gypsy communities
- `QuilombolaFamily` - Quilombola (Afro-Brazilian) communities
- `RecycledMaterialCollectorFamily` - Waste collectors
- `SettledFamilies` - Settled/resettled families
- `EmergencyCare` - Emergency assistance recipients

## Real pvmap File Patterns

Dataset files follow naming convention:
- `FoodBasket_ExtractiveFamily_pvmap.csv`
- `FoodBasket_FishingFamily_pvmap.csv`
- `FoodBasket_IndigenousFamily_pvmap.csv`
- `FoodBasket_GypsyFamily_processed_csv.csv`
- `FoodBasket_RecycledMaterialCollectorFamily_pvmap.csv`
- `FoodBasket_EmergencyCare_pvmap.csv`
- `FoodDistributionAct_FoodBasketByPartners_pvmap.csv`
- `MunicipalFoodBasket_*_pvmap.csv` variants

## Metadata Characteristics

Brazilian number formatting:
- `number_decimal: ","` (comma as decimal separator)
- `number_separator: " "` (space as thousands separator)
- `schemaless: 1` (special processing flag)

Place resolution via: `Brazil_Places_Resolved.csv`

## Standard Output Columns

```
observationAbout, observationDate, value, variableMeasured, unit, scalingFactor
```

## Source Identifiers

- `visdata` - Brazilian social programs database (VISDATA)

## Geographic Coverage

2 datasets covering Brazil: Food Basket Distribution Program and Rural Development Program (both from VISDATA), with data at country and state levels.

## Distinction from Economics

While economics covers income/poverty indicators, social_programs focuses on:
- Specific government intervention programs
- Aid distribution to identified vulnerable populations
- Program-specific beneficiary counts
- Food security and rural development initiatives
