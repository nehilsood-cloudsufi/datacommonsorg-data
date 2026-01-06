---
name: health
description: Handle datasets related to public health statistics, disease prevalence, health conditions like asthma and diabetes, health insurance coverage, mortality causes, health surveys (BRFSS, NFHS), and epidemiological indicators.
keywords:
  - health
  - disease
  - illness
  - medical
  - hospital
  - insurance
  - healthcare
  - prevalence
  - asthma
  - diabetes
  - chronic
  - brfss
  - vulnerability
input_column_patterns:
  - health
  - healthcare
  - medical
  - disease
  - illness
  - condition
  - diagnosis
  - prevalence
  - incidence
  - insurance
  - insured
  - uninsured
  - coverage
  - asthma
  - diabetes
  - cancer
  - heart_disease
  - mortality
  - death_cause
output_variable_patterns:
  - Count_Person_WithAsthma
  - Percent_Person_WithAsthma
  - SampleSize_Count_Person_WithAsthma
  - StdError_Count_Person_WithAsthma
  - Count_Person_0To4Years_WithAsthma
  - Percent_Person_0To4Years_WithAsthma
age_stratification:
  - 0To4Years
  - 5To9Years
  - 10To14Years
  - 15To19Years
  - 20To24Years
measurement_indicators:
  - unit: Percent
  - scalingFactor: 100
  - SampleSize
  - StdError
source_patterns:
  - cdc
  - nchs
  - brfss
  - sahie
  - nfhs
  - nss
data_url_patterns:
  - cdc.gov/asthma/brfss
countries:
  - USA
  - India
  - South Korea
  - Mongolia
---

# Health Skill

This skill processes datasets containing health and medical information.

## What This Skill Handles

- **Disease prevalence**: Rates of specific diseases (asthma, diabetes, etc.)
- **Health insurance**: Coverage rates, uninsured population (SAHIE data)
- **Mortality and causes**: Deaths by cause, disease-specific mortality
- **Health surveys**: BRFSS, NFHS, and other population health surveys
- **Chronic conditions**: Prevalence of chronic diseases, risk factors
- **Social determinants**: Social vulnerability index (SVI), health disparities
- **Sample statistics**: Sample sizes, standard errors for health estimates

## Real Input Column Patterns (from pvmap files)

A dataset likely belongs to this skill if it contains:
- `health`, `healthcare`, `medical`
- `disease`, `illness`, `condition`, `diagnosis`
- `prevalence`, `incidence`, `rate`
- `insurance`, `insured`, `uninsured`, `coverage`
- `asthma`, `diabetes`, `cancer`, `heart_disease`
- `mortality`, `death_cause`, `cause_of_death`

## Output Variable Patterns (DCID)

BRFSS Asthma example patterns:
- `dcid:Count_Person_0To4Years_WithAsthma`
- `dcid:Percent_Person_0To4Years_WithAsthma`
- `dcid:SampleSize_Count_Person_0To4Years_WithAsthma`
- `dcid:StdError_Count_Person_0To4Years_WithAsthma`

Age stratification: `0To4Years`, `5To9Years`, `10To14Years`, etc.

## Measurement Indicators

Health datasets typically include:
- `unit: Percent` for prevalence rates
- `scalingFactor` for percentage calculations
- `SampleSize` - survey sample size
- `StdError` - standard error estimates

## Standard Output Columns

```
observationAbout, observationDate, variableMeasured, value, unit, scalingFactor
```

Example output:
```
dcid:country/USA, 2021, dcid:Percent_Person_0To4Years_WithAsthma, 4.9, Percent,
dcid:country/USA, 2021, dcid:SampleSize_Count_Person_0To4Years_WithAsthma, 10645, ,
```

## Source Identifiers

- `cdc` - Centers for Disease Control
- `nchs` - National Center for Health Statistics
- `brfss` - Behavioral Risk Factor Surveillance System
- `sahie` - Small Area Health Insurance Estimates
- `nfhs` - India National Family Health Survey
- `nss` - India National Sample Survey

## Geographic Coverage

7 datasets covering USA (CDC, Census SAHIE, BRFSS), India (NFHS, NSS), South Korea, and Mongolia.
