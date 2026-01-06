---
name: demographics
description: Handle datasets related to population statistics, census data, birth rates, death rates, age distributions, gender distributions, race/ethnicity breakdowns, migration patterns, household composition, and demographic indicators across countries and regions.
keywords:
  - population
  - census
  - birth
  - death
  - mortality
  - fertility
  - age group
  - gender
  - sex
  - race
  - ethnicity
  - hispanic
  - household
  - family
  - urban
  - rural
  - life expectancy
  - demographic
input_column_patterns:
  - TOT_POP
  - TOT_MALE
  - TOT_FEMALE
  - WA_MALE
  - WA_FEMALE
  - BA_MALE
  - BA_FEMALE
  - IA_MALE
  - IA_FEMALE
  - AA_MALE
  - AA_FEMALE
  - H_MALE
  - H_FEMALE
  - NH_MALE
  - NH_FEMALE
  - NHWA_MALE
  - NHWA_FEMALE
  - WAC_MALE
  - WAC_FEMALE
  - TOM_MALE
  - TOM_FEMALE
  - AGE
  - YEAR
  - population
  - pop_count
  - birth_rate
  - death_rate
output_variable_patterns:
  - Count_Person
  - Count_Person_Male
  - Count_Person_Female
  - Count_Person_WhiteAlone
  - Count_Person_BlackOrAfricanAmericanAlone
  - Count_Person_AsianAlone
  - Count_Person_HispanicOrLatino
measurement_methods:
  - CensusPEPSurvey_Race2000Onwards
source_patterns:
  - census
  - pep
  - nfhs
  - undata
countries:
  - USA
  - India
  - Ireland
  - Singapore
  - South Korea
  - New Zealand
  - Mongolia
  - UAE
  - Kenya
  - Rwanda
  - Ethiopia
  - Mexico
  - Switzerland
  - Global
---

# Demographics Skill

This skill processes datasets containing population and demographic information.

## What This Skill Handles

- **Population counts**: Total population, population estimates, population projections
- **Census data**: National and subnational census statistics
- **Vital statistics**: Birth rates, death rates, fertility rates, mortality rates
- **Age distributions**: Population by age groups, median age
- **Gender/Sex breakdowns**: Male/female population counts and ratios
- **Race and ethnicity**: Population by racial and ethnic categories
- **Geographic distributions**: Urban vs rural, regional population
- **Household data**: Household size, family composition

## Real Input Column Patterns (from pvmap files)

A dataset likely belongs to this skill if it contains columns like:
- `TOT_POP`, `TOT_MALE`, `TOT_FEMALE` - Total population by sex
- `WA_MALE`, `WA_FEMALE` - White Alone population
- `BA_MALE`, `BA_FEMALE` - Black/African American population
- `IA_MALE`, `IA_FEMALE` - American Indian/Alaska Native
- `AA_MALE`, `AA_FEMALE` - Asian Alone
- `H_MALE`, `H_FEMALE` - Hispanic population
- `NH_MALE`, `NH_FEMALE` - Non-Hispanic population
- `NHWA_MALE`, `NHWA_FEMALE` - Non-Hispanic White
- `TOM_MALE`, `TOM_FEMALE` - Two Or More Races
- `AGE`, `YEAR` - Age groups and time periods

## Output Variable Format (DCID)

Variables are mapped to Data Commons identifiers:
- `dcid:Count_Person`
- `dcid:Count_Person_Male`
- `dcid:Count_Person_Female`
- `dcid:Count_Person_Male_WhiteAlone`

## Standard Output Columns

```
observationAbout, observationDate, value, variableMeasured, measurementMethod
```

Example output:
```
country/USA, 2024, 336673595, dcid:Count_Person, CensusPEPSurvey_Race2000Onwards
```

## Geographic Coverage

15 datasets covering USA, India, Ireland, Singapore, South Korea, New Zealand, Mongolia, UAE, Kenya, Rwanda, Ethiopia, Mexico, Switzerland (Zurich), and global/UN data.
