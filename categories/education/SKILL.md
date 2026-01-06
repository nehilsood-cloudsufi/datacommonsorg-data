---
name: education
description: Handle datasets related to educational statistics, school enrollment, student demographics, STEM degrees, bachelor's/master's/doctorate degrees by field, teacher data, HBCU enrollment, and civil rights education data.
keywords:
  - education
  - school
  - student
  - enrollment
  - degree
  - graduation
  - teacher
  - university
  - college
  - stem
  - bachelor
  - master
  - doctorate
  - hbcu
input_column_patterns:
  - Total
  - Male
  - Female
  - White
  - Black
  - Hispanic
  - Asian
  - Asian/Pacific Islander
  - Pacific Islander
  - American Indian/Alaska Native
  - Two or more races
  - Nonresident
  - Certificates below the associate's degree level
  - Associate's degrees
  - Bachelor's degrees
  - Master's degrees
  - Doctor's degrees
academic_year_mapping:
  - "2012-13": 2012
  - "2013-14": 2013
  - "2014-15": 2014
  - "2024-25": 2024
output_variable_patterns:
  - Count_Person_BachelorOfScienceOrTechnologyOrEngineeringOrMathematics_EducationalAttainmentCollegeGraduate
  - Count_Person_EducationalAttainmentBachelorsDegree
  - Count_Person_EducationalAttainmentMastersDegree
  - Count_Person_EducationalAttainmentDoctorateDegree
degree_major_property:
  - bachelorsDegreeMajor: Science__Technology__Engineering__Mathematics
educational_attainment_levels:
  - CollegeGraduate
  - BachelorsDegree
  - MastersDegree
  - DoctorateDegree
stratification_dimensions:
  - gender
  - race
  - ethnicity
  - bachelorsDegreeMajor
source_patterns:
  - nces
  - ncses
  - crdc
  - oecd
  - hbcu
countries:
  - USA
  - South Korea
  - Mongolia
  - Global
  - OECD
---

# Education Skill

This skill processes datasets containing educational statistics and academic data.

## What This Skill Handles

- **School enrollment**: Student enrollment counts by level, demographics
- **Degrees conferred**: Bachelor's, master's, doctorate degrees by field
- **STEM education**: Science, technology, engineering, math degree data
- **Teacher statistics**: Teacher counts, demographics
- **Academic achievement**: Graduation rates, completion rates
- **School demographics**: Student body by race, gender, disability, LEP status
- **HBCU data**: Historically Black Colleges and Universities enrollment
- **Civil rights data**: CRDC - educational equity indicators

## Real Input Column Patterns (from NCES STEM pvmap)

Demographic columns:
- `Total`, `Male`, `Female`
- `White`, `Black`, `Hispanic`, `Asian`, `Asian/Pacific Islander`
- `Pacific Islander`, `American Indian/Alaska Native`, `Two or more races`
- `Nonresident`

Degree level columns:
- `Certificates below the associate's degree level`
- `Associate's degrees`
- `Bachelor's degrees`
- `Master's degrees`
- `Doctor's degrees`

Academic year mapping: `2012-13` → `2012`, `2013-14` → `2013`, etc.

## Output Variable Patterns (DCID)

STEM degrees example:
```
dcid:Count_Person_BachelorOfScienceOrTechnologyOrEngineeringOrMathematics_EducationalAttainmentCollegeGraduate
```

Properties used:
- `educationalAttainment`: Person
- `measuredProperty`: count
- `bachelorsDegreeMajor`: Science__Technology__Engineering__Mathematics
- `gender`: Male, Female
- `race/ethnicity`: Various categories

## Stratification Dimensions

Education data stratified by:
- `-race,-ethnicity,-bachelorsDegreeMajor` (denominators in variable names)
- Gender (Male/Female)
- Race/Ethnicity categories
- Field of study

## Standard Output Columns

```
observationAbout, observationDate, value, variableMeasured, unit, scalingFactor, measurementMethod, observationPeriod
```

Example output:
```
country/USA, 2011, 556696, dcid:Count_Person_BachelorOfScienceOrTechnologyOrEngineeringOrMathematics_EducationalAttainmentCollegeGraduate
```

## Source Identifiers

- `nces` - National Center for Education Statistics
- `ncses` - National Center for Science and Engineering Statistics
- `crdc` - Civil Rights Data Collection
- `hbcu` - Historically Black Colleges and Universities
- `oecd` - OECD regional education

## Geographic Coverage

11 datasets covering USA (NCES, NCSES, CRDC, Urban Schools), South Korea, Mongolia, and OECD regional data.
