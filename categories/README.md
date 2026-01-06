# Data Categories

This folder contains datasets organized by category for use with Anthropic Skills.

## Categories Overview

| Category | Description | Dataset Count |
|----------|-------------|---------------|
| [demographics](./demographics/) | Population, census, births, deaths, demographic indicators | 15 |
| [economics](./economics/) | GDP, income, prices, commodities, exchange rates | 15 |
| [employment](./employment/) | Labor force, unemployment, workforce statistics | 7 |
| [health](./health/) | Disease prevalence, insurance, public health | 7 |
| [education](./education/) | Schools, enrollment, degrees, academic data | 11 |
| [crime_safety](./crime_safety/) | Crime statistics, traffic fatalities | 2 |
| [environment](./environment/) | Fires, floods, climate, sustainability | 4 |
| [social_programs](./social_programs/) | Government programs, welfare, food distribution | 2 |
| [infrastructure](./infrastructure/) | Internet, roads, power, connectivity | 1 |

**Total Datasets: 64**

## Geographic Coverage

- **USA**: Demographics, Economics, Employment, Health, Education, Crime/Safety, Environment, Infrastructure
- **Brazil**: Demographics (via Economics), Environment, Social Programs
- **India**: Demographics, Economics, Health
- **South Korea**: Demographics, Employment, Health, Education
- **Mongolia**: Demographics, Employment, Health, Education
- **Ireland**: Demographics
- **Singapore**: Demographics
- **New Zealand**: Demographics
- **Switzerland (Zurich)**: Demographics
- **UAE**: Demographics
- **Kenya**: Demographics
- **Rwanda**: Demographics
- **Ethiopia**: Demographics
- **Mexico**: Demographics
- **Global/OECD**: Economics, Education, Environment

## Usage for Anthropic Skills

Each category folder can be used as a separate skill. The folder structure:

```
categories/
├── skill_registry.json    <- Master registry for programmatic skill matching
├── demographics/          <- Skill: demographics
│   ├── SKILL.md           <- Skill metadata (name, description, keywords, triggers)
│   ├── README.md
│   └── [dataset folders]
├── economics/             <- Skill: economics
│   ├── SKILL.md
│   ├── README.md
│   └── [dataset folders]
├── employment/            <- Skill: employment
│   ├── SKILL.md
│   ├── README.md
│   └── [dataset folders]
├── health/                <- Skill: health
│   ├── SKILL.md
│   ├── README.md
│   └── [dataset folders]
├── education/             <- Skill: education
│   ├── SKILL.md
│   ├── README.md
│   └── [dataset folders]
├── crime_safety/          <- Skill: crime_safety
│   ├── SKILL.md
│   ├── README.md
│   └── [dataset folders]
├── environment/           <- Skill: environment
│   ├── SKILL.md
│   ├── README.md
│   └── [dataset folders]
├── social_programs/       <- Skill: social_programs
│   ├── SKILL.md
│   ├── README.md
│   └── [dataset folders]
└── infrastructure/        <- Skill: infrastructure
    ├── SKILL.md
    ├── README.md
    └── [dataset folders]
```

## Skill Metadata Format

Each category contains a `SKILL.md` file following Anthropic's agent skills format:

```yaml
---
name: skill_name
description: What the skill handles
keywords:
  - keyword1
  - keyword2
triggers:
  - trigger phrase 1
  - trigger phrase 2
countries:
  - Country1
  - Country2
---

# Skill Content

Instructions and details about the skill...
```

## Skill Selection

Use `skill_registry.json` for programmatic skill matching. It contains:
- `keywords`: Terms that indicate relevance to this skill
- `column_patterns`: Column/variable names commonly found in datasets of this type
- `source_patterns`: Data source identifiers (e.g., "bls", "census", "cdc")
- `countries`: Geographic coverage

Example matching logic:
1. Check if dataset columns match any `column_patterns`
2. Check if dataset source matches any `source_patterns`
3. Check if dataset description contains any `keywords`
4. Score and select the best matching skill

## Data Sources

- US Census Bureau
- US Bureau of Labor Statistics (BLS)
- US Bureau of Economic Analysis (BEA)
- US CDC (Centers for Disease Control)
- US NCES (National Center for Education Statistics)
- FBI Crime Data Explorer
- NHTSA (National Highway Traffic Safety Administration)
- FEMA (Federal Emergency Management Agency)
- World Bank
- OECD
- UN Data
- India NDAP / RBI / NFHS
- Brazil IBGE / INPE
- Various national statistics offices (Ireland, Singapore, South Korea, New Zealand, Mongolia, UAE, etc.)
