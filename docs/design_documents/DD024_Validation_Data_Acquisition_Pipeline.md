# DD024: Validation Data Acquisition Pipeline

**Status:** Proposed (Phase A — Infrastructure)
**Author:** OpenWorm Core Team
**Date:** 2026-02-21
**Supersedes:** None
**Related:** [DD010](DD010_Validation_Framework.md) (Validation Framework), [DD008](DD008_Data_Integration_Pipeline.md) (Data Integration Pipeline), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (Connectome Data Access), [DD013](DD013_Simulation_Stack_Architecture.md) (Simulation Stack), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Movement Analysis Toolbox)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **What does this produce?** | Version-controlled repository of all experimental datasets needed for [DD010](DD010_Validation_Framework.md) validation across tiers 1-4 and all subsystem DDs |
| **Success metric** | Every [DD010](DD010_Validation_Framework.md) validation test can run against locally cached, versioned data without requiring external API calls at runtime |
| **Repository** | `openworm/validation-data` (new repo) — issues labeled `dd024` |
| **Config toggle** | `validation.data_path: /opt/openworm/validation/data/` in `openworm.yml` |
| **Build & test** | `docker compose run shell python scripts/verify_validation_data.py` — checks all datasets present, checksums match |
| **Visualize** | N/A (data infrastructure, not a model) |
| **CI gate** | Docker build fails if any required dataset is missing or has incorrect checksum |

---

## TL;DR

Every subsystem DD ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md)-[DD019](DD019_Closed_Loop_Touch_Response.md)) specifies validation targets that depend on published experimental data, but no DD owns the systematic acquisition, formatting, and version control of that data. This DD fills that gap. It catalogs every dataset referenced by [DD010](DD010_Validation_Framework.md)'s four validation tiers, defines how each is acquired (API, supplement download, manual digitization), what format it is stored in, and where it lives in the `openworm/validation-data` repository. This is Phase A infrastructure — without clean, versioned validation data, no validation tier can function.

---

## Goal & Success Criteria

| Criterion | Target |
|-----------|--------|
| **Primary:** Dataset completeness | Every [DD010](DD010_Validation_Framework.md) validation test has its required experimental data committed to `openworm/validation-data` |
| **Secondary:** Format standardization | All datasets in machine-readable formats (CSV, NumPy, WCON, NeuroML) with README metadata |
| **Tertiary:** Reproducibility | Checksums recorded; any contributor can verify data integrity with a single command |
| **Quaternary:** Licensing compliance | Every dataset has a LICENSE file documenting redistribution rights and original DOI |

---

## Deliverables

| Artifact | Path (in `openworm/validation-data`) | Format |
|----------|--------------------------------------|--------|
| Repository with all datasets | `openworm/validation-data` | Git repo |
| Data manifest | `manifest.json` | JSON: dataset_id, source, DOI, license, checksum, format, DD_consumer |
| Verification script | `scripts/verify_validation_data.py` | Python |
| Per-dataset README | `{category}/{dataset}/README.md` | Markdown with provenance |
| Docker data volume | Baked into [DD013](DD013_Simulation_Stack_Architecture.md) Docker `validation` stage | Directory tree at `/opt/openworm/validation/data/` |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Repository** | `openworm/validation-data` (new — to be created) |
| **Issue label** | `dd024` |
| **Milestone** | Phase A: Infrastructure Bootstrap |
| **Branch convention** | `dd024/dataset-name` (e.g., `dd024/randi2023-functional-connectivity`) |

---

## Complete Dataset Inventory

### Tier 1: Single-Cell Electrophysiology

| Dataset | Source Publication | Neurons Covered | Format Needed | Acquisition Method | Consumer DD | Priority |
|---------|-------------------|-----------------|---------------|-------------------|-------------|----------|
| Touch neuron patch-clamp (V_rest, R_in, I-V) | Goodman et al. 1998, *Neuron* 20:763-772 | ALM, AVM, PLM (~6 neurons) | CSV: neuron, protocol, V/I traces | Digitize from paper figures or request from authors | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | High |
| AVA interneuron recordings | Lockery lab (unpublished / personal communication) | AVA | CSV: time, V, I | Request from Lockery lab | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | High |
| ASH nociceptor electrophysiology | Hilliard et al. 2002 | ASH | CSV: time, V, I, stimulus | Digitize from paper | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Medium |
| AWC olfactory neuron recordings | Chalasani et al. 2007, *Nature* 450:63-70 | AWC | CSV: time, V, I, odor | Digitize from paper | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Medium |
| RIA compartmentalized calcium | Hendricks et al. 2012, *Nature* 487:99-103 | RIA | CSV: time, Ca_proximal, Ca_distal | Supplement or digitize | [DD001](DD001_Neural_Circuit_Architecture.md) (Level E) | Medium |
| AWA calcium action potentials | Liu et al. 2018, *Cell* 175:57-70 | AWA | CSV: time, V, Ca | Supplement data | [DD001](DD001_Neural_Circuit_Architecture.md) (Level E) | Medium |
| MEC-4 channel kinetics | O'Hagan et al. 2005, *Nat Neurosci* 8:43-50 | Touch receptor | CSV: strain, current, activation/inactivation curves | Digitize from paper | [DD019](DD019_Closed_Loop_Touch_Response.md) | High |
| Pharyngeal muscle plateau potentials | Raizen & Avery 1994, *Neuron* 12:483-495 | pm3-pm8 | CSV: time, V (intracellular recording) | Digitize from paper figures | [DD007](DD007_Pharyngeal_System_Architecture.md) | Medium |

### Tier 2: Functional Connectivity

| Dataset | Source Publication | Scale | Format Needed | Acquisition Method | Consumer DD | Priority |
|---------|-------------------|-------|---------------|-------------------|-------------|----------|
| Whole-brain functional connectivity (wild-type) | Randi et al. 2023, *Nature* 623:406-414 | 302x302 correlation matrix | NumPy `.npy` | **Already available via `wormneuroatlas` API** — extract and cache locally | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD010](DD010_Validation_Framework.md) | **Critical** |
| Whole-brain functional connectivity (unc-31 mutant) | Randi et al. 2023 (same paper, supplemental) | 302x302 | NumPy `.npy` | Via `wormneuroatlas` API (`strain="unc31"`) | [DD010](DD010_Validation_Framework.md) (Tier 4) | High |
| Signal propagation atlas | Randi et al. 2023 | Directed functional connectivity | NumPy `.npy` | Via `wormneuroatlas` API | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | High |
| Whole-brain activity during behavioral states | Atanas et al. 2022, *bioRxiv* | Time series per neuron during dwelling/roaming | HDF5 or CSV | Download from supplement / request | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD010](DD010_Validation_Framework.md) | Medium |

### Tier 3: Behavioral Kinematics

| Dataset | Source Publication | Content | Format Needed | Acquisition Method | Consumer DD | Priority |
|---------|-------------------|---------|---------------|-------------------|-------------|----------|
| N2 wild-type locomotion baseline | Schafer lab / Yemini et al. 2013, *Nat Methods* 10:877-879 | Speed, wavelength, frequency, amplitude | WCON (Worm Tracker Commons) | Download from [wormbase.org/tools/tracker](https://www.wormbase.org/) or Open Worm Movement Database | [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD003](DD003_Body_Physics_Architecture.md), [DD010](DD010_Validation_Framework.md) | **Critical** |
| unc-2 (Cav2) mutant locomotion | Schafer lab | Reduced speed, altered gait | WCON | Same source as above | [DD010](DD010_Validation_Framework.md) (Tier 4) | High |
| N2 behavioral phenotype statistics | Yemini et al. 2013 | Population means, CVs for ~700 features | CSV from supplement | Download supplementary data | [DD010](DD010_Validation_Framework.md) (±15% threshold grounding) | High |
| Defecation cycle periods | Thomas 1990, *Genetics* 124:855-872 | ~50s period, posterior-to-anterior wave | CSV: animal_id, cycle_start, cycle_end, period | Digitize from Table 1 | [DD009](DD009_Intestinal_Oscillator_Model.md) | High |
| Pharyngeal pumping EPG | Raizen & Avery 1994, *Neuron* 12:483-495 | 3-4 Hz pumping frequency, EPG waveform | CSV: time, voltage | Digitize from figures | [DD007](DD007_Pharyngeal_System_Architecture.md) | Medium |
| Egg-laying bout statistics | Collins et al. 2016, *eLife* 5:e21126 | Inactive/active bout durations, eggs per bout | CSV from supplement | Download supplement | [DD018](DD018_Egg_Laying_System_Architecture.md) | Medium |
| Touch response latency | [Chalfie et al. 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985), *J Neurosci* 5:956-964 | Reversal onset 300-800 ms | CSV: stimulus_type, latency | Digitize from paper | [DD019](DD019_Closed_Loop_Touch_Response.md) | High |
| Foraging behavior decomposition | Flavell et al. 2020, *Genetics* 216:315-332 | Dwelling/roaming state durations, transition rates | CSV: state, duration, transition_probability | Digitize from paper or request | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Medium |

### Tier 4: Causal / Interventional

| Dataset | Source Publication | Intervention | Expected Phenotype | Format Needed | Consumer DD | Priority |
|---------|-------------------|-------------|-------------------|---------------|-------------|----------|
| Touch neuron ablation | [Chalfie et al. 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985) | Laser ablation of ALM, AVM, PLM | Loss of gentle touch response | CSV: ablated_neurons, stimulus, response | [DD019](DD019_Closed_Loop_Touch_Response.md), [DD010](DD010_Validation_Framework.md) | High |
| Pharyngeal neuron ablation | Avery & Horvitz 1989, *Neuron* 3:473-485 | Laser killing of pharyngeal neurons | Pumping persists (semi-autonomous) | CSV: ablated_neurons, pumping_frequency | [DD007](DD007_Pharyngeal_System_Architecture.md), [DD010](DD010_Validation_Framework.md) | Medium |
| Neuropeptide knockouts (FLP, NLP) | Li et al. 1999; Rogers et al. 2003 | Gene deletion | Altered locomotion | CSV: genotype, speed, reversal_rate | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD010](DD010_Validation_Framework.md) | High |
| unc-103 loss-of-function | Collins & Koelle 2013, *J Neurosci* 33:761-775 | ERG channel removal from vm2 | Constitutive egg-laying | CSV: genotype, egg_count, bout_pattern | [DD018](DD018_Egg_Laying_System_Architecture.md), [DD010](DD010_Validation_Framework.md) | Medium |
| egl-1 loss-of-function | Trent et al. 1983, *Genetics* 104:619-647 | HSN cell death | Egg-laying defective | CSV: genotype, phenotype_class | [DD018](DD018_Egg_Laying_System_Architecture.md), [DD010](DD010_Validation_Framework.md) | Medium |
| Optogenetic single-neuron activation | Leifer et al. 2011, *Nat Methods* 8:147-152 | Light activation of specific neurons | Stimulus-specific behavioral response | CSV: neuron, stimulus, behavior | [DD010](DD010_Validation_Framework.md) | Low (Phase 3+) |

### Connectome & Molecular (Supporting)

| Dataset | Source | Content | Format Needed | Acquisition Method | Consumer DD | Status |
|---------|--------|---------|---------------|-------------------|-------------|--------|
| Synaptic + gap junction connectome | Cook et al. 2019, *Nature* 571:63-71 | Adjacency matrices | **Already in `cect`** | Via ConnectomeToolbox API | [DD001](DD001_Neural_Circuit_Architecture.md), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | Available |
| Developmental connectomes | Witvliet et al. 2021, *Nature* 596:257-261 | 8 animals L1-adult | **Already in `cect`** | Via ConnectomeToolbox API | [DD001](DD001_Neural_Circuit_Architecture.md), [DD004](DD004_Mechanical_Cell_Identity.md), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | Available |
| Neuropeptidergic connectome | Ripoll-Sanchez et al. 2023, *Neuron* 111:3570-3589 | 31,479 interactions | CSV + **in `cect`** | Supplement Table S1 + ConnectomeToolbox | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | Available |
| CeNGEN L4 expression | Taylor et al. 2021, *Cell* 184:4329-4347 | 128 classes x 20,500 genes | CSV (TPM) via `wormneuroatlas` | API or cengen.org download | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Available |
| WBbt cell ontology | WormBase | 959 somatic cell IDs | OWL/OBO | WormBase download | [DD004](DD004_Mechanical_Cell_Identity.md) | Available |
| 3D nuclear positions | Long et al. 2009, *Nat Methods* 6:667-672 | 357 nuclei at L1 | CSV: cell_name, x, y, z | Supplement | [DD004](DD004_Mechanical_Cell_Identity.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Needs acquisition |
| NeuroPAL neuron ID atlas | Yemini et al. 2021, *Cell* 184:272-288 | Color atlas for all neurons | Reference images + ID mapping | Published with reagents | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Reference only |

---

## Data Format Standards

All datasets in `openworm/validation-data` must follow these conventions:

### File Formats

| Data Type | Format | Justification |
|-----------|--------|---------------|
| Time series (V, Ca, I) | CSV with header row: `time_ms, value, unit` | Universal readability, git-friendly |
| Correlation matrices | NumPy `.npy` with companion `.json` metadata | Efficient for large matrices, metadata preserves neuron ordering |
| Movement trajectories | WCON 1.0 (per [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) | Standard format for *C. elegans* tracking data |
| Behavioral statistics | CSV with header: `genotype, metric, mean, std, n, source_doi` | Machine-readable, self-documenting |
| Intervention/ablation data | CSV with header: `genotype_or_ablation, stimulus, metric, value, n, source_doi` | Uniform causal validation format |
| Expression matrices | CSV (gene x cell class) or via `wormneuroatlas` API cache | Consistent with [DD005](DD005_Cell_Type_Differentiation_Strategy.md) pipeline |

### Metadata Requirements

Every dataset directory must contain a `README.md` with:

```markdown
# Dataset: {name}

**Source:** {author} et al. ({year}), *{journal}* {volume}:{pages}
**DOI:** {doi}
**License:** {license or "Fair use — digitized from published figures"}
**Acquired:** {date}
**Acquired by:** {person or script}

## Description
{What this dataset contains and why it matters for validation}

## Files
| File | Description | Rows | Columns |
|------|-------------|------|---------|
| ... | ... | ... | ... |

## Provenance
{How the data was obtained: API call, supplement download, figure digitization}
{Any transformations applied: unit conversion, column renaming, neuron ID normalization}

## Consumer DDs
{Which DDs use this data and for what validation tier}
```

### Checksums

A root `checksums.sha256` file records the SHA-256 hash of every data file. The verification script checks all hashes on Docker build and on `verify_validation_data.py` execution.

---

## Acquisition Priorities

### Phase A (Weeks 1-4) — Must Have

These datasets are blocking for the two critical validation tiers (Tier 2 and Tier 3):

1. **Randi 2023 functional connectivity** (Tier 2) — Extract from `wormneuroatlas` API, cache as `.npy`. ~2 hours.
2. **Schafer lab N2 baseline WCON** (Tier 3) — Download from Worm Tracker database or WormBase. ~4 hours (format verification).
3. **Yemini 2013 behavioral statistics** (Tier 3 threshold grounding) — Download supplement CSV. ~1 hour.
4. **Thomas 1990 defecation periods** ([DD009](DD009_Intestinal_Oscillator_Model.md) Tier 3) — Digitize Table 1. ~2 hours.
5. **Raizen 1994 pumping frequency** ([DD007](DD007_Pharyngeal_System_Architecture.md) Tier 3) — Digitize from figures. ~3 hours.
6. **O'Hagan 2005 MEC-4 kinetics** ([DD019](DD019_Closed_Loop_Touch_Response.md) Tier 1) — Digitize activation/inactivation curves. ~4 hours.
7. **[Chalfie 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985) touch response** ([DD019](DD019_Closed_Loop_Touch_Response.md) Tier 3 + Tier 4) — Digitize latency data. ~2 hours.

**Estimated total: ~18 hours**

### Phase 1 (Months 1-3) — Should Have

8. **Goodman 1998 touch neuron electrophysiology** (Tier 1) — Digitize I-V curves. ~4 hours.
9. **Collins 2016 egg-laying statistics** ([DD018](DD018_Egg_Laying_System_Architecture.md) Tier 3) — Download supplement. ~2 hours.
10. **Flavell 2020 dwelling/roaming statistics** ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md) Tier 4) — Digitize or request. ~3 hours.
11. **Randi 2023 unc-31 mutant** (Tier 4) — Extract from `wormneuroatlas`. ~1 hour.
12. **Long 2009 3D nuclear positions** ([DD004](DD004_Mechanical_Cell_Identity.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md)) — Download supplement. ~2 hours.
13. **Schafer lab unc-2 mutant WCON** (Tier 4) — Download from tracker database. ~2 hours.

### Phase 2+ — Nice to Have

14. **Hendricks 2012 RIA compartmentalized calcium** — For [DD001](DD001_Neural_Circuit_Architecture.md) Level E validation.
15. **Liu 2018 AWA calcium data** — For [DD001](DD001_Neural_Circuit_Architecture.md) Level E validation.
16. **Atanas 2022 whole-brain behavioral states** — For [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) state transition validation.
17. **Optogenetic perturbation data** (Leifer, Randi) — As published datasets become available.
18. **Hilliard 2002 ASH, Chalasani 2007 AWC** — For [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration training set expansion.

---

## How to Build & Test

### Adding a New Dataset

```bash
# 1. Create dataset directory
mkdir -p data/tier3_behavioral/thomas1990_defecation/

# 2. Add data files
cp digitized_data.csv data/tier3_behavioral/thomas1990_defecation/defecation_periods.csv

# 3. Write README.md with provenance
# (follow template above)

# 4. Update manifest
python scripts/update_manifest.py \
    --dataset thomas1990_defecation \
    --doi "10.1534/genetics.124.4.855" \
    --consumer-dds DD009,DD010 \
    --tier 3

# 5. Update checksums
python scripts/update_checksums.py

# 6. Verify everything
python scripts/verify_validation_data.py
# Green light: all datasets present, all checksums match, all READMEs exist
```

### Verification Script

```python
# scripts/verify_validation_data.py
# Checks:
# 1. All datasets listed in manifest.json exist on disk
# 2. SHA-256 checksums match
# 3. Every dataset directory has a README.md
# 4. CSV files are parseable with expected columns
# 5. NumPy files have expected shapes
# 6. WCON files pass basic format validation
# Exit code 0 = all checks pass; non-zero = failure with specific error
```

---

## Relationship to Existing Data Infrastructure

### ConnectomeToolbox (`cect`) — [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)

`cect` already provides programmatic access to connectome datasets (Cook 2019, Witvliet 2021, Ripoll-Sanchez 2023). [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) does NOT duplicate this. Instead:

- Connectome data remains in `cect` (the canonical API)
- [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) stores *validation* data (experimental recordings, behavioral measurements) that `cect` does not cover
- For Randi 2023 functional connectivity, [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) caches the output of `wormneuroatlas` API calls as static files to avoid runtime dependencies

### OWMeta ([DD008](DD008_Data_Integration_Pipeline.md))

OWMeta is the semantic knowledge graph for *C. elegans* biological facts. [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) complements it:

- OWMeta stores structured biological knowledge (cell types, gene functions, anatomical relationships)
- [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) stores quantitative experimental recordings used specifically for model validation
- In Phase 3+, OWMeta may ingest [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) data as validation-specific data types

### Docker Integration ([DD013](DD013_Simulation_Stack_Architecture.md))

[DD024](DD024_Validation_Data_Acquisition_Pipeline.md) data is baked into the Docker `validation` stage at build time:

```dockerfile
# In DD013 multi-stage Dockerfile
FROM validation-base AS validation
COPY --from=openworm/validation-data:v1.0 /data /opt/openworm/validation/data/
RUN python scripts/verify_validation_data.py
```

Data is NOT downloaded at runtime — all validation data is pre-packaged for reproducibility and offline CI.

---

## Boundaries (Out of Scope)

1. **Raw imaging data:** We store derived/processed data (correlation matrices, extracted features, digitized traces), not raw calcium imaging volumes or EM stacks. Raw data is too large for Git and available from original authors.

2. **Proprietary or restricted data:** Only openly redistributable data (CC-BY, CC0, or fair-use digitization from published figures) is included. Data requiring DTA or institutional agreement is documented in the manifest but not stored.

3. **Simulation output data:** [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) stores *experimental* data for validation. Simulated reference outputs (baseline scores, expected trajectories) are generated by [DD010](DD010_Validation_Framework.md)/[DD013](DD013_Simulation_Stack_Architecture.md) CI pipeline, not pre-stored.

4. **Data analysis scripts:** Scripts that *use* validation data (correlation computation, feature extraction) live in their respective DD repositories ([DD010](DD010_Validation_Framework.md), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)). [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) only stores data and verification scripts.

---

## Configuration

```yaml
# openworm.yml section
validation:
  data_path: /opt/openworm/validation/data/   # Docker default
  data_version: "v1.0"                         # Tag in openworm/validation-data
  verify_checksums: true                        # Verify on Docker build
```

---

## References

1. **Randi F et al. (2023).** "Neural signal propagation atlas of *Caenorhabditis elegans*." *Nature* 623:406-414.
2. **Yemini E et al. (2013).** "A database of *Caenorhabditis elegans* behavioral phenotypes." *Nature Methods* 10:877-879.
3. **Thomas JH (1990).** "Genetic analysis of defecation in *Caenorhabditis elegans*." *Genetics* 124:855-872.
4. **Raizen DM, Avery L (1994).** "Electrical activity and behavior in the pharynx of *Caenorhabditis elegans*." *Neuron* 12:483-495.
5. **O'Hagan R, Chalfie M, Bhatt R (2005).** "The MEC-4 DEG/ENaC channel of *Caenorhabditis elegans* touch receptor neurons transduces mechanical signals." *Nature Neurosci* 8:43-50.
6. **[Chalfie M et al. (1985)](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985).** "The neural circuit for touch sensitivity in *Caenorhabditis elegans*." *J Neurosci* 5:956-964.
7. **Collins KM et al. (2016).** "Activity of the *C. elegans* egg-laying behavior circuit is controlled by competing activation and feedback inhibition." *eLife* 5:e21126.
8. **Flavell SW, Raizen DM, You YJ (2020).** "Behavioral States." *Genetics* 216:315-332.
9. **Goodman MB, Hall DH, Avery L, Bhatt R (1998).** "Active currents regulate sensitivity and dynamic range in *C. elegans* neurons." *Neuron* 20:763-772.
10. **Pearl J, Mackenzie D (2018).** *The Book of Why.* Basic Books. *(Motivates causal/interventional validation data.)*

---

## Integration Contract

### Inputs (What This Subsystem Consumes)

| Input | Source | Description |
|-------|--------|-------------|
| Published papers | PubMed / journal websites | Source material for digitization |
| `wormneuroatlas` API | PyPI package | Randi 2023, CeNGEN programmatic access |
| ConnectomeToolbox (`cect`) | PyPI package | Connectome data (not stored in [DD024](DD024_Validation_Data_Acquisition_Pipeline.md), but referenced) |
| Supplement files | Journal supplement pages | Raw data tables from publications |

### Outputs (What This Subsystem Produces)

| Output | Consumer DD | Description |
|--------|------------|-------------|
| Electrophysiology CSVs | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD007](DD007_Pharyngeal_System_Architecture.md), [DD019](DD019_Closed_Loop_Touch_Response.md) (Tier 1) | Patch-clamp, V-clamp, channel kinetics |
| Functional connectivity matrices | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD010](DD010_Validation_Framework.md) (Tier 2) | Randi 2023 302x302 `.npy` files |
| Behavioral kinematic data | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD003](DD003_Body_Physics_Architecture.md), [DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md), [DD019](DD019_Closed_Loop_Touch_Response.md), [DD010](DD010_Validation_Framework.md) (Tier 3) | WCON files, defecation/pumping CSVs |
| Intervention/perturbation data | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD007](DD007_Pharyngeal_System_Architecture.md), [DD010](DD010_Validation_Framework.md), [DD018](DD018_Egg_Laying_System_Architecture.md), [DD019](DD019_Closed_Loop_Touch_Response.md) (Tier 4) | Ablation, mutant, and knockout phenotype CSVs |
| Docker data volume | [DD013](DD013_Simulation_Stack_Architecture.md) (Docker build) | `/opt/openworm/validation/data/` tree |
| Data manifest | [DD010](DD010_Validation_Framework.md) (validation runner) | `manifest.json` mapping datasets to DDs and tiers |

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Neuron naming convention | [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (ConnectomeToolbox) | If neuron IDs change in `cect`, cached Randi 2023 matrix column labels may break |
| WCON format spec | [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | If WCON version changes, kinematics files may need re-export |
| Docker build pipeline | [DD013](DD013_Simulation_Stack_Architecture.md) | If Docker stage names or paths change, data COPY step breaks |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| All validation tiers | [DD010](DD010_Validation_Framework.md) | If data format or file paths change, validation scripts break |
| CI pipeline | [DD013](DD013_Simulation_Stack_Architecture.md) | If Docker data volume path changes, `docker compose run validate` can't find data |
| All subsystem DDs | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD019](DD019_Closed_Loop_Touch_Response.md) | If a dataset is removed or reformatted, the consuming DD's validation fails |

---

**Approved by:** Pending
**Implementation Status:** Proposed
**Next Actions:**

1. Create `openworm/validation-data` GitHub repository
2. Acquire Phase A datasets (7 datasets, ~18 hours)
3. Write `verify_validation_data.py` script
4. Integrate into [DD013](DD013_Simulation_Stack_Architecture.md) Docker build
5. Announce in next board sync for contributor help with digitization tasks
