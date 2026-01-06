---
name: infrastructure
description: Handle datasets related to internet connectivity and digital access from NTIA Internet Use Survey, including household internet usage, broadband adoption, and digital divide indicators.
keywords:
  - infrastructure
  - internet
  - broadband
  - connectivity
  - digital
  - telecommunications
  - online
  - access
  - household
input_column_patterns:
  - internetAnywhere
  - internetAtHome
  - noInternetAtHome
  - adultInternetUser
  - ispBundle
  - householderAge
  - householderRace
  - householderGender
  - householderEducationalAttainment
  - householderWorkStatus
output_variable_patterns:
  - isInternetUser
  - internetUsageLocation
  - internetSubscriptionType
  - hasComputer
  - computerUsageLocation
property_mappings:
  isInternetUser:
    - "True"
    - "False"
  internetUsageLocation:
    - AnyLocation
    - Home
    - School
    - Work
  internetSubscriptionType:
    - InternetBundle
  hasComputer:
    - "True"
    - "False"
  computerUsageLocation:
    - Home
population_types:
  - Household
  - Person
demographic_stratification:
  - householderAge
  - householderRace
  - householderGender
  - householderEducationalAttainment
  - householderWorkStatus
armed_forces_status:
  - Civilian
  - Active-Duty Military
institutionalization:
  - USC_NonInstitutionalized
survey_dates:
  - Nov 1994
  - Oct 1997
  - Dec 1998
  - Aug 2000
  - Sep 2001
  - Oct 2003
  - Oct 2007
  - Oct 2009
  - Oct 2010
  - Jul 2011
  - Oct 2012
  - Jul 2013
  - Jul 2015
  - Nov 2017
  - Nov 2019
  - Nov 2021
  - Nov 2023
source_patterns:
  - ntia
countries:
  - USA
---

# Infrastructure Skill

This skill processes datasets containing infrastructure and digital connectivity information.

## What This Skill Handles

- **Internet access**: Household internet usage, internet users by demographics
- **Broadband adoption**: Internet subscription types, bundled services
- **Digital divide**: Access disparities by age, race, education, employment
- **Computer access**: Computer ownership and usage location
- **Telecommunications**: Digital connectivity trends over time

## Real Input Column Patterns (from NTIA pvmap)

Internet usage columns:
- `internetAnywhere` - Internet use from any location
- `internetAtHome` - Internet use at home
- `noInternetAtHome` - No internet access at home
- `adultInternetUser` - Adult internet users
- `ispBundle` - Internet service bundle subscriptions

Householder demographic columns:
- `householderAge` - Age of householder
- `householderRace` - Race of householder
- `householderGender` - Gender of householder
- `householderEducationalAttainment` - Education level
- `householderWorkStatus` - Employment status

## Output Property Mappings

Internet usage properties:
- `isInternetUser`: True, False
- `internetUsageLocation`: AnyLocation, Home, School, Work
- `internetSubscriptionType`: InternetBundle
- `hasComputer`: True, False
- `computerUsageLocation`: Home

Population types:
- `Household` - Household-level data
- `Person` - Individual-level data

## Demographic Stratification

Data stratified by:
- `householderAge` - Age groups
- `householderRace` - Racial categories
- `householderGender` - Male/Female
- `householderEducationalAttainment` - Education levels
- `householderWorkStatus` - Employment status (Civilian, Active-Duty Military)
- `institutionalization`: USC_NonInstitutionalized

## Survey Timeline

Biennial surveys spanning decades:
- Historical: Nov 1994, Oct 1997, Dec 1998, Aug 2000
- 2000s: Sep 2001, Oct 2003, Oct 2007, Oct 2009, Oct 2010
- 2010s: Jul 2011, Oct 2012, Jul 2013, Jul 2015, Nov 2017, Nov 2019
- 2020s: Nov 2021, Nov 2023

## Standard Output Columns

```
observationAbout, observationDate, variableMeasured, value, unit, scalingFactor
```

## Source Identifiers

- `ntia` - National Telecommunications and Information Administration (US Commerce Department)

## Geographic Coverage

1 dataset covering USA: NTIA Internet Use Survey with national and state-level data on internet usage and digital access.
