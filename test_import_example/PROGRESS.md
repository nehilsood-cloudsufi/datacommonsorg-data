# Agentic Import Tool - Example Workflows

This document tracks the progress of running the Agentic Import Tool on multiple datasets to compare Gemini vs Claude performance.

---

## Directory Structure

```
test_import_example/
├── PROGRESS.md                     # This file
├── .datacommons/                   # LLM run logs and attempts
│   └── runs/
│       ├── claude_*               # Claude CLI run logs
│       └── gemini_*               # Gemini CLI run logs
│
├── worldbank/                     # World Bank Population Dataset
│   ├── input/
│   │   ├── world_population.csv   # Full dataset (496 rows)
│   │   └── sample_data.csv        # Sampled data (30 rows)
│   ├── output_gemini/             # Gemini PV map generation output
│   │   ├── output_pvmap.csv
│   │   ├── output_metadata.csv
│   │   ├── output.csv
│   │   └── output.tmcf
│   ├── output_claude/             # Claude PV map generation output
│   │   ├── output_pvmap.csv
│   │   ├── output_metadata.csv
│   │   ├── output.csv
│   │   └── output.tmcf
│   └── final_output/              # Final processed data
│       ├── output.csv
│       └── output.tmcf
│
└── undata/                        # UNdata City Population Dataset
    ├── input/
    │   ├── UNData_input.csv       # Full dataset (48 rows)
    │   ├── sample_data.csv        # Sampled data (30 rows)
    │   ├── expected_output.csv    # Ground truth output
    │   └── expected_output.tmcf   # Ground truth TMCF
    ├── output_gemini/             # Gemini PV map generation (FAILED - quota)
    │   ├── output_pvmap.csv       # Incomplete/invalid
    │   ├── output_metadata.csv
    │   ├── output.csv
    │   └── output.tmcf
    ├── output_claude/             # Claude PV map generation
    │   ├── output_pvmap.csv
    │   ├── output_metadata.csv
    │   ├── output.csv
    │   └── output.tmcf
    └── final_output/              # Final processed data (Claude)
        ├── output.csv             # 49 observations
        └── output.tmcf
```

---

# Dataset 1: World Bank Population

**Goal**: Import World Bank Population data into Data Commons format.

**Dataset**: World Bank Population (SP.POP.TOTL indicator)
- Source: World Bank API
- Time Range: 2020-2023
- Coverage: All countries and regions
- Rows: 496

## Workflow Summary

| Step | Command | Status |
|------|---------|--------|
| 1. Download | Python script | Completed |
| 2. Sample | `data_sampler.py --sampler_output_rows=30` | Completed |
| 3a. Gemini PV Map | `pvmap_generator.py --llm_cli=gemini` | Completed (7 iterations) |
| 3b. Claude PV Map | `pvmap_generator.py --llm_cli=claude` | Completed (7 iterations) |
| 4. Process Full | `stat_var_processor.py` | Completed |

## Results Comparison

| Aspect | Gemini | Claude |
|--------|--------|--------|
| **Iterations** | 7 | 7 |
| **Place DCID** | `country/{code}` | `worldBank/{code}` |
| **Output Rows** | 496 | 496 |
| **StatVar** | Count_Person | Count_Person |

---

# Dataset 2: UNdata City Population

**Goal**: Import UNdata city population data with gender breakdowns.

**Dataset**: UNdata City Population (Mariehamn, Aland Islands)
- Source: UNdata
- Time Range: 2007-2023
- Coverage: Single city (MARIEHAMN)
- Rows: 48 (with Male/Female/Both Sexes breakdown)

## Workflow Summary

| Step | Command | Status |
|------|---------|--------|
| 1. Copy | cp from statvar_imports/undata | Completed |
| 2. Sample | `data_sampler.py --sampler_output_rows=30` | Completed |
| 3a. Gemini PV Map | `pvmap_generator.py --llm_cli=gemini` | FAILED (API quota) |
| 3b. Claude PV Map | `pvmap_generator.py --llm_cli=claude` | Completed (6 iterations) |
| 4. Process Full | `stat_var_processor.py` | Completed |

## Ground Truth vs Claude Comparison

### Data Match: 100% IDENTICAL

| Metric | Ground Truth | Claude |
|--------|--------------|--------|
| **Observations** | 49 | 49 |
| **Place DCID** | `wikidataId/Q48329` | `wikidataId/Q48329` |
| **StatVars** | Count_Person, Count_Person_Male, Count_Person_Female | Same |
| **Years** | 2007-2023 | 2007-2023 |

### PV Map Comparison

| Feature | Ground Truth | Claude |
|---------|--------------|--------|
| **Lines** | 93 | 18 |
| **Place Resolution** | Dynamic `{CityName} {Country}` | Hardcoded `wikidataId/Q48329` |
| **Gender Mapping** | `gender,Male` | `gender,dcs:Male` |
| **Data Filter** | `#Filter,int(value) > 1` | None |
| **Aggregation** | `#Aggregate,max` | None |
| **City Exclusions** | 78 cities | None |
| **measurementMethod** | `UNData` | `dcs:UNDataEstimateDeJure` |

### TMCF Comparison

**Ground Truth**:
```
Node: E:UNData.tmcf->E0
observationAbout: C:UNData.tmcf->observationAbout
observationDate: C:UNData.tmcf->observationDate
value: C:UNData.tmcf->value
variableMeasured: C:UNData.tmcf->variableMeasured
unit: C:UNData.tmcf->unit
scalingFactor: C:UNData.tmcf->scalingFactor
typeOf: dcs:StatVarObservation
#Aggregate: max
measurementMethod: UNData
```

**Claude**:
```
Node: E:output->E0
observationDate: C:output->observationDate
value: C:output->value
variableMeasured: C:output->variableMeasured
measurementMethod: dcs:UNDataEstimateDeJure
observationPeriod: P1Y
observationAbout: wikidataId/Q48329
typeOf: dcs:StatVarObservation
```

### Evaluation

**Claude Strengths**:
1. Correctly identified WikidataId (Q48329) for Mariehamn
2. Generated correct gender-based StatVars
3. Added `observationPeriod: P1Y` (appropriate for yearly data)
4. Simpler, cleaner PV map (18 lines vs 93)

**Claude Weaknesses**:
1. Hardcoded place DCID - won't work for multi-city datasets
2. Missing `#Aggregate` for duplicate handling
3. Missing `#Filter` for data quality
4. No city-specific exclusion rules

**Conclusion**: For this single-city test dataset, Claude's output is functionally equivalent to Ground Truth (100% data match). Ground Truth's approach is more production-ready for multi-city datasets.

---

# Commands Reference

## Sample Data
```bash
python tools/statvar_importer/data_sampler.py \
  --sampler_input="input.csv" \
  --sampler_output="sample.csv" \
  --sampler_output_rows=30
```

## Generate PV Map (Gemini)
```bash
python tools/agentic_import/pvmap_generator.py \
  --input_data="sample.csv" \
  --output_path="output/output" \
  --llm_cli="gemini" \
  --gemini_cli="gemini --model gemini-2.5-flash" \
  --skip_confirmation
```

## Generate PV Map (Claude)
```bash
python tools/agentic_import/pvmap_generator.py \
  --input_data="sample.csv" \
  --output_path="output/output" \
  --llm_cli="claude" \
  --skip_confirmation
```

## Process Full Dataset
```bash
python tools/statvar_importer/stat_var_processor.py \
  --input_data="full_data.csv" \
  --pv_map="output_pvmap.csv" \
  --config_file="output_metadata.csv" \
  --generate_statvar_name=True \
  --output_path="final/output"
```

---

# Debugging

**Log Locations**:
- LLM CLI logs: `.datacommons/runs/*/llm_cli.log`
- Processor logs: `.datacommons/processor.log`
- Per-attempt logs: `.datacommons/runs/*/attempt_*/processor.log`

**View Generated Prompt**:
```bash
cat .datacommons/runs/claude_*/generate_pvmap_prompt.md
```