---
name: crime_safety
description: Handle datasets related to crime statistics from FBI Crime Data Explorer, traffic crash fatalities from NHTSA FARS, criminal offenses by type, arrests, and public safety indicators.
keywords:
  - crime
  - criminal
  - offense
  - arrest
  - police
  - safety
  - accident
  - crash
  - fatality
  - homicide
  - theft
  - robbery
  - assault
  - traffic
input_column_patterns:
  - StateName
  - CityName
  - ViolentCrime
  - MurderAndNonNegligentManslaughter
  - ForcibleRape
  - Robbery
  - AggravatedAssault
  - PropertyCrime
  - Burglary
  - LarcenyTheft
  - MotorVehicleTheft
  - Arson
  - STATE
  - STATENAME
  - ST_CASE
  - COUNTY
  - COUNTYNAME
  - CITY
  - CITYNAME
  - PEDS
  - PERNOTMVIT
  - VE_TOTAL
  - VE_FORMS
  - PVH_INVL
  - PERSONS
  - PERMVIT
  - FATALS
  - YEAR
  - MONTH
  - DAY
  - HOUR
  - TWAY_ID
  - ROUTE
  - RUR_URB
  - LGT_COND
  - WEATHER
  - HARM_EV
output_variable_patterns:
  - Count_CriminalActivities_ViolentCrime
  - Count_CriminalActivities_MurderAndNonNegligentManslaughter
  - Count_CriminalActivities_Robbery
  - Count_CriminalActivities_AggravatedAssault
  - Count_CriminalActivities_PropertyCrime
  - Count_CriminalActivities_Burglary
  - Count_CriminalActivities_LarcenyTheft
  - Count_CriminalActivities_MotorVehicleTheft
  - Count_Person_InvolvedInCrash
  - Count_Person_InvolvedInCrash_NotMotorVehicleOccupant
  - Count_MortalityEvent_VehicleCrashIncident
  - Count_VehicleCrashIncident
crime_type_property:
  - ViolentCrime
  - MurderAndNonNegligentManslaughter
  - ForcibleRape
  - Robbery
  - AggravatedAssault
  - PropertyCrime
  - Burglary
  - LarcenyTheft
  - MotorVehicleTheft
  - Arson
fars_properties:
  - populationType: MortalityEvent
  - causeOfDeath: VehicleCrashIncident
  - vehicleOccupantType: NotMotorVehicleOccupant
  - roadType: InterstateRoad, StateRoute, CountyRoad, LocalStreet
source_patterns:
  - fbi
  - ucr
  - fars
  - nhtsa
countries:
  - USA
---

# Crime and Safety Skill

This skill processes datasets containing crime and public safety information.

## What This Skill Handles

- **Crime statistics**: FBI Crime Data Explorer offense counts
- **Violent crime**: Homicide, assault, robbery, rape statistics
- **Property crime**: Theft, burglary, motor vehicle theft, arson
- **Traffic safety**: NHTSA FARS crash data, traffic fatalities
- **Geographic crime data**: Crime by city, state, county

## Real Input Column Patterns (from FBI pvmap)

FBI Crime Data columns:
- `StateName`, `CityName` - Geographic identifiers
- `ViolentCrime` - Aggregate violent crime
- `MurderAndNonNegligentManslaughter`
- `ForcibleRape`
- `Robbery`
- `AggravatedAssault`
- `PropertyCrime` - Aggregate property crime
- `Burglary`
- `LarcenyTheft`
- `MotorVehicleTheft`
- `Arson`

FARS Crash Data columns:
- `STATE`, `STATENAME`, `COUNTY`, `COUNTYNAME`, `CITY`, `CITYNAME`
- `ST_CASE` - Case identifier
- `PEDS` - Pedestrians involved
- `PERNOTMVIT` - Persons not in motor vehicles
- `VE_TOTAL`, `VE_FORMS` - Vehicle counts
- `PERSONS`, `PERMVIT` - Person counts
- `FATALS` - Fatality count
- `YEAR`, `MONTH`, `DAY`, `HOUR` - Date/time
- `TWAY_ID`, `ROUTE`, `RUR_URB` - Road characteristics
- `LGT_COND`, `WEATHER` - Conditions
- `HARM_EV` - Harmful event type

## Output Variable Patterns (DCID)

FBI Crime:
- `crimeType` property with values: `ViolentCrime`, `MurderAndNonNegligentManslaughter`, `Robbery`, etc.
- `UCR_CombinedCrime` for aggregate totals

FARS:
- `dcid:Count_Person_InvolvedInCrash_NotMotorVehicleOccupant`
- `dcid:Count_MortalityEvent_VehicleCrashIncident` (fatalities)
- `dcid:Count_VehicleCrashIncident` (crash events)

FARS Properties:
- `populationType`: MortalityEvent, Person, VehicleCrashIncident
- `causeOfDeath`: VehicleCrashIncident
- `vehicleOccupantType`: NotMotorVehicleOccupant
- `roadType`: InterstateRoad, StateRoute, CountyRoad, LocalStreet

## Standard Output Columns

```
observationAbout, observationDate, variableMeasured, value, unit, scalingFactor
```

Example FARS output:
```
geoId/01115, 2021-02, dcid:Count_Person_InvolvedInCrash_NotMotorVehicleOccupant, 0, , P1M
country/USA, 2021-02, dcid:Count_Person_InvolvedInCrash_NotMotorVehicleOccupant, 1, , P1M
```

## Source Identifiers

- `fbi` - Federal Bureau of Investigation
- `ucr` - Uniform Crime Reports
- `fars` - Fatality Analysis Reporting System
- `nhtsa` - National Highway Traffic Safety Administration

## Geographic Coverage

2 datasets covering USA: FBI Crime Data Explorer (city-level) and NHTSA FARS (country, state, county level with monthly data).
