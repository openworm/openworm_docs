# DD010: Validation Framework and Quantitative Benchmarks

**Status:** Accepted  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-14  
**Supersedes:** None  
**Related:** All other DDs (validation applies to all models), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Movement Analysis Toolbox — Tier 3 validation tool)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 1](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3) |
| **Layer** | Validation — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3) |
| **What does this produce?** | Three-tier validation reports: Tier 1 (single-cell electrophysiology), Tier 2 (functional connectivity correlation), Tier 3 (behavioral kinematics via `open-worm-analysis-toolbox` — see [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) |
| **Success metric** | Tier 2: correlation-of-correlations r > 0.5 vs. [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4); Tier 3: 5 kinematic metrics within ±15% of Schafer lab data |
| **Repository** | Validation scripts in `openworm/OpenWorm` meta-repo; Tier 3 tool: [`openworm/open-worm-analysis-toolbox`](https://github.com/openworm/open-worm-analysis-toolbox) ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) |
| **Config toggle** | `validation.run_after_simulation: true`, `validation.tier2_functional_connectivity: true`, `validation.tier3_behavioral: true` in `openworm.yml` |
| **Build & test** | `docker compose run validate` — runs all enabled tiers, produces `output/validation_report.json` |
| **Visualize** | Validation overlay in [DD014](DD014_Dynamic_Visualization_Architecture.md) viewer: `validation/overlay/` OME-Zarr group shows per-metric pass/fail |
| **CI gate** | Tier 2 blocks PR merge (r < 0.5 = fail); Tier 3 blocks merge to main (>15% deviation = fail) |

---

## Context

OpenWorm's core philosophy, articulated in Sarma et al. 2016 "Unit Testing, Model Validation, and Biological Simulation" (*F1000Research*), is that **model validation is a form of testing**. Just as software has unit tests, integration tests, and system tests, biological models must be validated at multiple levels:

- **Single-cell level:** Electrophysiology (voltage, conductance, kinetics)
- **Circuit level:** Functional connectivity (calcium correlations)
- **Behavioral level:** Movement kinematics, pumping, defecation

A simulation that produces movement but fails electrophysiology validation has **passed the behavioral test but failed the mechanistic test**. Both matter.

---

## Decision

### Three-Tier Validation Hierarchy

| Tier | What Is Validated | Validation Data | Acceptance Criteria | Blocking? |
|------|------------------|-----------------|-------------------|-----------|
| **Tier 1: Unit (Single Cell)** | Membrane voltage, conductances, calcium dynamics | Goodman lab patch-clamp, Randi et al. single-neuron Ca imaging | Quantitative match within 20% | No (warning) |
| **Tier 2: Integration (Circuit)** | Functional connectivity, network dynamics | [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) whole-brain pairwise correlations | Correlation coefficient > 0.5 vs. experimental | Yes (blocks merge) |
| **Tier 3: System (Behavior)** | Movement kinematics, pumping, defecation | Schafer lab WCON, Raizen EPG, Thomas defecation assays | Statistical match via open-worm-analysis-toolbox | Yes (blocks merge) |

**Blocking:** A PR that degrades Tier 2 or Tier 3 validation scores cannot be merged without explicit founder approval + justification.

### Tier 1: Single-Cell Validation (Unit Tests)

**For each neuron class with published electrophysiology:**

Run the cell model in isolation (no synaptic inputs, no network effects) with standard voltage-clamp or current-clamp protocols. Compare:

| Property | Measurement | Typical Acceptance Range |
|----------|-------------|-------------------------|
| Resting potential (V_rest) | No current injection | ± 5 mV |
| Input resistance (R_in) | Small current step | ± 30% |
| I-V curve | Voltage ramp | Pearson r > 0.8 |
| Spike threshold | Depolarizing current | ± 10 mV (if applicable) |
| Calcium influx | Depolarization-evoked | ± 40% (noisy measurement) |

**Example (AVA neuron validation):**
```bash
# Run isolated AVA model
python c302/test_single_cell.py --cell AVACell --protocol voltage_clamp

# Compare to Lockery lab data
python scripts/validate_single_cell_electrophys.py \
    --simulated AVA_voltage_clamp.csv \
    --experimental data/AVA_lockery_vclamp.csv \
    --output validation_report_AVA.html
```

**Outcome:** Report file showing parameter-by-parameter comparison. If >2 parameters fail (exceed acceptance range), flag for review.

### Tier 2: Circuit-Level Validation (Integration Tests)

**Primary target:** [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity matrix (pairwise calcium signal correlations for all 302 neurons during spontaneous activity).

**Validation procedure:**

1. Run c302 simulation for 60 seconds (spontaneous activity, no stimulus)
2. Extract calcium time series for all neurons
3. Compute pairwise Pearson correlations → 302×302 matrix
4. Compare to Randi et al. experimental 302×302 matrix
5. Metric: **Correlation of correlations** (Pearson r between simulated and experimental matrices, flattened to vectors)

**Acceptance criterion:**

- **r > 0.5** between simulated and experimental functional connectivity
- At least 70% of neuron pairs have correlation sign agreement (both positive, both negative, or both near-zero)

**Testing command:**
```bash
# Run functional connectivity validation
python scripts/validate_functional_connectivity.py \
    --model c302_C1_Differentiated \
    --duration 60 \
    --experimental_data data/randi2023_functional_connectivity.npy \
    --output func_conn_validation.json

# Check if acceptance criteria pass
python scripts/check_validation_criteria.py func_conn_validation.json
```

**Blocking:** If this test fails (r < 0.5), the PR cannot merge to `main`.

### Tier 3: Behavioral Validation (System Tests)

**Primary tool:** `open-worm-analysis-toolbox` (see **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** for toolbox revival plan, WCON format specification, API contract, and version pinning) — compares simulated movement trajectories to Schafer lab experimental data in WCON format.

**Validated metrics:**

1. **Speed:** Mean forward velocity (µm/s)
2. **Wavelength:** Body bend wavelength (µm)
3. **Frequency:** Undulation frequency (Hz)
4. **Amplitude:** Body bend amplitude (degrees)
5. **Crawl/swim classification:** Behavioral mode based on gait

**Acceptance criteria (from Palyanov et al. validation):**

- All 5 metrics within **±15% of experimental mean**
- Movement trajectory visually resembles real worm (qualitative check)

**Testing command:**
```bash
# Run behavioral validation suite
cd open-worm-analysis-toolbox/
python validate_movement.py \
    --simulated ../c302/output/worm_trajectory.wcon \
    --experimental data/schafer_baseline_N2.wcon \
    --output validation_report.json

# Check pass/fail
python check_acceptance.py validation_report.json --tolerance 0.15
```

**Additional behavioral tests:**

1. **Pharyngeal pumping:** 3-4 Hz ([DD007](DD007_Pharyngeal_System_Architecture.md))
2. **Defecation cycle:** 50 ± 10 seconds period ([DD009](DD009_Intestinal_Oscillator_Model.md))
3. **Reversal initiation:** Response to aversive stimulus (<1 second latency)

**Blocking:** If movement validation degrades by >15%, the PR is blocked.

---

## Alternatives Considered

### 1. No Quantitative Validation (Visual Inspection Only)

**Rejected:** "It looks right" is subjective. Quantitative metrics enable regression detection and objective comparison between models.

### 2. Single Validation Level (Behavior Only)

**Rejected:** A model can produce correct movement for the wrong reasons (parameter compensation). Multi-level validation (electrophysiology + connectivity + behavior) ensures mechanistic correctness.

### 3. Strict Thresholds (Must Match Exactly)

**Rejected:** Biological data have measurement noise and animal-to-animal variability. ±15-20% tolerance accounts for this. Exact matches are neither achievable nor necessary.

---

## Quality Criteria

1. **Automated Test Suite:** All validation tests must be runnable via CI/CD without manual intervention.

2. **Regression Detection:** Every PR that modifies cell models, connectome, or physics must run the validation suite. Report before/after comparison.

3. **Versioned Experimental Data:** Validation datasets must be versioned and archived (e.g., `data/randi2023_v1.0/`). Do not overwrite.

4. **Pass/Fail Criteria Documented:** Each test must have explicit acceptance criteria (e.g., "r > 0.5," "period = 50 ± 10 s") in the test script, not tribal knowledge.

---

## Integration Contract

### Inputs (What This Subsystem Consumes)

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| Neuron calcium time series | [DD001](DD001_Neural_Circuit_Architecture.md) | Per-neuron [Ca²⁺] over time | Tab-separated `*_calcium.dat` | mol/cm³ |
| Single-cell electrophysiology | [DD001](DD001_Neural_Circuit_Architecture.md) | V, I_Ca, I_K per cell | Tab-separated from NEURON | mV, nA |
| Movement trajectory | [DD003](DD003_Body_Physics_Architecture.md) | Body centroid + posture over time | WCON file | µm, frames |
| Pharyngeal pumping state | [DD007](DD007_Pharyngeal_System_Architecture.md) | Per-section contraction time series | Tab-separated | binary or [0,1] |
| Defecation motor program | [DD009](DD009_Intestinal_Oscillator_Model.md) | pBoc/aBoc/Exp timestamps | Event log | ms |
| Experimental data (electrophysiology) | [DD008](DD008_Data_Integration_Pipeline.md) / published papers | Patch-clamp recordings | CSV | mV, nA |
| Experimental data (functional connectivity) | [DD008](DD008_Data_Integration_Pipeline.md) / [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) | 302×302 correlation matrix | NumPy `.npy` | dimensionless |
| Experimental data (kinematics) | [DD008](DD008_Data_Integration_Pipeline.md) / Schafer lab | Movement trajectories | WCON | µm |
| Experimental data (defecation) | [DD008](DD008_Data_Integration_Pipeline.md) / [Thomas 1990](https://doi.org/10.1093/genetics/124.4.855) | Defecation cycle periods | CSV | seconds |
| Experimental data (pumping) | [DD008](DD008_Data_Integration_Pipeline.md) / [Raizen 1994](https://doi.org/10.1016/0896-6273(94)90207-0) | EPG recordings | CSV | mV |

### Outputs (What This Subsystem Produces)

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Tier 1 validation report | [DD012](DD012_Design_Document_RFC_Process.md) (PR review) | Per-cell pass/fail + metrics | JSON | mixed |
| Tier 2 validation report | [DD012](DD012_Design_Document_RFC_Process.md) (PR review), [DD013](DD013_Simulation_Stack_Architecture.md) (CI gate) | Correlation-of-correlations score | JSON | dimensionless (r value) |
| Tier 3 validation report | [DD012](DD012_Design_Document_RFC_Process.md) (PR review), [DD013](DD013_Simulation_Stack_Architecture.md) (CI gate) | Per-metric pass/fail (speed, wavelength, frequency, amplitude, gait) | JSON | mixed |
| Regression alert | [DD013](DD013_Simulation_Stack_Architecture.md) (CI pipeline) | Pass/fail + diff from baseline | JSON + exit code | boolean |
| Validation dashboard | Mad-Worm-Scientist (daily digest) | Summary metrics for all tiers | JSON | mixed |
| Validation overlay data (for viewer) | **[DD014](DD014_Dynamic_Visualization_Architecture.md)** (visualization) | Per-metric pass/fail + experimental comparison traces | OME-Zarr: `validation/overlay/` (tier results + reference data) | mixed |

### CI/CD Ownership Split ([DD010](DD010_Validation_Framework.md) vs. [DD013](DD013_Simulation_Stack_Architecture.md))

**[DD010](DD010_Validation_Framework.md) defines WHAT to validate.** [DD013](DD013_Simulation_Stack_Architecture.md) defines HOW to run it in Docker and CI.

| Responsibility | Owned By |
|---------------|----------|
| Validation metrics, acceptance criteria, test scripts | [DD010](DD010_Validation_Framework.md) |
| Docker compose services (`quick-test`, `validate`) | [DD013](DD013_Simulation_Stack_Architecture.md) |
| CI/CD pipeline (GitHub Actions workflow) | [DD013](DD013_Simulation_Stack_Architecture.md) |
| Validation data packaging in Docker image | [DD010](DD010_Validation_Framework.md) + [DD013](DD013_Simulation_Stack_Architecture.md) (shared) |
| Pass/fail decision logic (blocking PRs) | [DD010](DD010_Validation_Framework.md) (criteria) + [DD013](DD013_Simulation_Stack_Architecture.md) (enforcement) |

**Reconciliation:** The `docker compose run validate` service ([DD013](DD013_Simulation_Stack_Architecture.md)) runs the validation scripts defined by [DD010](DD010_Validation_Framework.md). The scripts produce JSON reports. [DD013](DD013_Simulation_Stack_Architecture.md)'s CI pipeline reads those reports and applies [DD010](DD010_Validation_Framework.md)'s acceptance criteria to determine pass/fail.

### Configuration (`openworm.yml` Section)

```yaml
validation:
  run_after_simulation: false         # Set true for CI; false for interactive use
  tier1_electrophysiology: false      # Single-cell validation (requires specific cell models)
  tier2_functional_connectivity: false  # Circuit-level (requires 60s sim)
  tier3_behavioral: false             # Movement kinematics (requires ~5s sim)
  tier3_pumping: false                # Pharyngeal pumping (requires pharynx.enabled + ~5s sim)
  tier3_defecation: false             # Defecation cycle (requires intestine.enabled + ~200s sim)
  acceptance_criteria:
    tier2_min_correlation: 0.5        # Minimum r for functional connectivity
    tier3_max_deviation: 0.15         # Maximum deviation from experimental mean (±15%)
    tier3_pumping_range: [3.0, 4.0]   # Hz
    tier3_defecation_range: [40, 60]  # seconds
```

**Default vs. CI configuration:**

```yaml
# configs/validation_full.yml (used by CI)
validation:
  run_after_simulation: true
  tier2_functional_connectivity: true
  tier3_behavioral: true
```

### Docker Build

- **Repository:** `openworm/open-worm-analysis-toolbox` (movement validation, see [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) + `openworm/tracker-commons` (WCON spec, see [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) + validation scripts in `openworm/OpenWorm` meta-repo
- **Docker stage:** `validation` in multi-stage Dockerfile
- **`versions.lock` keys:** `open_worm_analysis_toolbox`, `tracker_commons` (both managed per [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md))
- **Build dependencies:** `pip install open-worm-analysis-toolbox` + validation data files

### Validation Data Location

All validation datasets are **baked into the Docker image at build time** (not downloaded at runtime):

```
/opt/openworm/validation/data/
├── electrophysiology/
│   ├── goodman1998_touch_neurons.csv
│   ├── lockery_AVA_recordings.csv
│   └── README.md (sources, DOIs, licenses)
├── functional_connectivity/
│   ├── randi2023_full_matrix.npy
│   ├── randi2023_metadata.json
│   └── README.md
├── kinematics/
│   ├── schafer_N2_baseline.wcon
│   ├── schafer_unc2_mutant.wcon
│   └── README.md
└── behavioral/
    ├── thomas1990_defecation.csv
    ├── raizen1994_pumping_EPG.csv
    └── README.md
```

**Licensing requirement:** All validation data must be openly accessible (CC-BY or equivalent). Each directory includes a README with source DOIs and licenses.

### Code Reuse: wormneuroatlas for Tier 2 Validation

**Repository:** `openworm/wormneuroatlas` (pushed 2025-10-22, maintained)
**Installation:** `pip install wormneuroatlas`

**[Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity is already accessible via API:**

```python
from wormneuroatlas import NeuroAtlas

atlas = NeuroAtlas()
experimental_fc = atlas.get_signal_propagation_atlas(strain="wt")
# Returns: 302×302 correlation matrix (exactly what Tier 2 needs)

# Use in validation
simulated_fc = compute_pairwise_correlations(simulation_calcium_traces)
correlation_of_correlations = np.corrcoef(
    experimental_fc.flatten(),
    simulated_fc.flatten()
)[0, 1]

# DD010 Tier 2 acceptance: r > 0.5
assert correlation_of_correlations > 0.5, "Tier 2 FAILED"
```

**No manual download from Nature supplement needed.** The wormneuroatlas package handles data access, versioning, and neuron ID normalization.

**Testing:**
```bash
pip install wormneuroatlas
python -c "from wormneuroatlas import NeuroAtlas; fc = NeuroAtlas().get_signal_propagation_atlas(strain='wt'); print(f'Randi 2023 data: {fc.shape}')"
# Expected: (302, 302) or similar
```

**Action Items:**

- [ ] Add `wormneuroatlas` to [DD013](DD013_Simulation_Stack_Architecture.md) Docker validation stage
- [ ] Pin version in `versions.lock`
- [ ] Update Tier 2 validation scripts to use wormneuroatlas API
- [ ] Also available: unc-31 mutant functional connectivity via `strain="unc31"`

**Estimated Time Savings:** 15-20 hours (no manual data extraction, API is production-ready)

---

### `open-worm-analysis-toolbox` Revival ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md))

This repo is **dormant** (last commit Jan 2020). **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Movement Analysis Toolbox and WCON Policy)** owns the full revival plan, including:

- 8-task revival roadmap with owners, effort estimates, and dependencies (~33 hours total)
- Python 3.12 compatibility, dependency updates, test suite fixes
- WCON 1.0 format pinning from `tracker-commons`
- Docker `validation` stage and `versions.lock` entries
- API contract for `NormalizedWorm` and `WormFeatures` classes
- Relationship to Tierpsy Tracker (modern successor)

**See [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) for the complete revival plan.** This is a Phase A ([DD013](DD013_Simulation_Stack_Architecture.md) roadmap) task. Without a working analysis toolbox, Tier 3 validation is impossible.

Note: The archived predecessor repo `openworm/movement_validation` should not be used — it was superseded by the analysis toolbox.

### Integration Test

```bash
# Step 1: Verify validation tools install
docker compose run shell python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
print('Analysis toolbox loaded successfully')
"

# Step 2: Verify validation data is present
docker compose run shell ls /opt/openworm/validation/data/
# Must show: electrophysiology/, functional_connectivity/, kinematics/, behavioral/

# Step 3: Run validation suite (after simulation)
docker compose run validate
# Verify: output/validation_report.json exists
# Verify: report contains tier2 and tier3 sections
# Verify: CI exit code = 0 if all tiers pass, non-zero if any blocking tier fails

# Step 4: Test regression detection
# Modify a parameter known to degrade locomotion
# Run validation
# Verify: Tier 3 fails with specific metric(s) identified
```

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Neural output format | [DD001](DD001_Neural_Circuit_Architecture.md) | If calcium time series format changes, Tier 1 and Tier 2 validators can't read data |
| Movement output format | [DD003](DD003_Body_Physics_Architecture.md) | If WCON format or particle output changes, Tier 3 movement validator breaks |
| Pharyngeal output format | [DD007](DD007_Pharyngeal_System_Architecture.md) | If pumping state format changes, pumping validation breaks |
| Intestinal output format | [DD009](DD009_Intestinal_Oscillator_Model.md) | If defecation event format changes, defecation validation breaks |
| Experimental data (OWMeta) | [DD008](DD008_Data_Integration_Pipeline.md) | If data provenance or versioning changes, validation baselines may shift |
| Docker compose services | [DD013](DD013_Simulation_Stack_Architecture.md) | If `validate` service configuration changes, validation pipeline breaks |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| CI pipeline (blocking gates) | [DD013](DD013_Simulation_Stack_Architecture.md) | If acceptance criteria change, CI may pass/fail differently |
| PR review (Mind-of-a-Worm) | [DD012](DD012_Design_Document_RFC_Process.md) | Mind-of-a-Worm references [DD010](DD010_Validation_Framework.md) criteria when checking PR compliance |
| Founder digest (Mad-Worm-Scientist) | AI Agents | If validation report format changes, Mad-Worm-Scientist can't parse regression alerts |
| All subsystem DDs | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD009](DD009_Intestinal_Oscillator_Model.md) | If a tier's acceptance criteria tighten, previously-passing subsystems may now fail |

---

## Implementation References

### Open-Worm-Analysis-Toolbox

**Repository:**
```
https://github.com/openworm/open-worm-analysis-toolbox
```

> **Note:** The predecessor repo `openworm/movement_validation` is **archived** and should not be used. The analysis toolbox is the current, canonical implementation. See [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) for full repository landscape and revival plan.

**Key modules:**

- `movement_validation/` — Statistical feature extraction from WCON files
- `comparison/` — Compare simulated vs. real
- `wcon_parser/` — WCON format handling

**Usage:**
```python
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures

# Load experimental data
exp_worm = NormalizedWorm.from_schafer_file("schafer_N2_baseline.wcon")
exp_features = WormFeatures(exp_worm)

# Load simulated data
sim_worm = NormalizedWorm.from_simulation("c302_output.wcon")
sim_features = WormFeatures(sim_worm)

# Compare
comparison = exp_features.compare(sim_features)
print(comparison.summary())  # Pass/fail report
```

### Validation Data Repository

```
openworm/validation_data/
├── electrophysiology/
│   ├── goodman1998_touch_neurons.csv
│   ├── lockery_AVA_recordings.csv
│   └── ...
├── functional_connectivity/
│   ├── randi2023_full_matrix.npy
│   ├── randi2023_metadata.json
│   └── ...
├── kinematics/
│   ├── schafer_N2_baseline.wcon
│   ├── schafer_unc2_mutant.wcon  # Calcium channel mutant
│   └── ...
└── behavioral/
    ├── thomas1990_defecation.csv
    ├── raizen1994_pumping_EPG.csv
    └── ...
```

**Licensing:** All validation data must be openly accessible (CC-BY or equivalent). Cite original publications.

---

## Migration Path

### From Manual Validation to Automated CI

**Current state:** Validation is run manually before major releases.

**Target state (Phase 1):** GitHub Actions CI runs validation suite on every PR to `main`.

**Implementation:**
```yaml
# .github/workflows/validation.yml
name: Model Validation
on: [pull_request]
jobs:
  tier2_functional_connectivity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate c302 network
        run: python c302/CElegans.py C1Differentiated
      - name: Run simulation
        run: jnml LEMS_c302_C1_Differentiated.xml -nogui
      - name: Validate vs. Randi 2023
        run: python scripts/validate_functional_connectivity.py
      - name: Check acceptance
        run: python scripts/check_criteria.py --min_correlation 0.5

  tier3_behavioral:
    runs-on: ubuntu-latest
    steps:
      - name: Run movement validation
        run: cd open-worm-analysis-toolbox && python validate_movement.py
      - name: Check acceptance
        run: python scripts/check_criteria.py --max_deviation 0.15
```

---

## Boundaries (Out of Scope)

1. **Developmental validation:** Validating stage-specific models (L1, dauer, male) is Phase 6 work.
2. **Genetic variation:** Validating against natural isolates (Ben-David eQTLs) is Phase 6+ work.
3. **Pharmacological validation:** Drug effects (aldicarb, levamisole) are future work.

---

## References

1. **Sarma GP, Ghayoomie V, Jacobs T, et al. (2016).** "Unit testing, model validation, and biological simulation." *F1000Research* 5:1946.
2. **Randi F et al. (2023).** "Neural signal propagation atlas." *Nature* 623:406-414.
3. **Yemini E, Jucikas T, Grundy LJ, et al. (2013).** "A database of *Caenorhabditis elegans* behavioral phenotypes." *Nature Methods* 10:877-879.

---

**Approved by:** OpenWorm Steering
**Implementation Status:** Partial

- **Tier 1** (single-cell electrophysiology): Scripts exist but not automated (non-blocking currently)
- **Tier 2** (functional connectivity): [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) data needs ingestion into [DD008](DD008_Data_Integration_Pipeline.md)/DD020 (blocking)
- **Tier 3** (behavioral kinematics): **BLOCKED** — `open-worm-analysis-toolbox` is dormant (last commit Jan 2020, broken on Python 3.12)

**See [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Movement Analysis Toolbox and WCON Policy)** for the complete toolbox revival plan (8 tasks, ~33 hours). Tier 3 validation cannot run until the toolbox is revived and installable on Python 3.12.

**Next Actions:**

1. **URGENT:** Prioritize [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) toolbox revival as Phase A work (parallel with [DD013](DD013_Simulation_Stack_Architecture.md))
2. Appoint Validation L4 Maintainer to own revival (see ClickUp task 868hjdzqy)
3. After revival: Ingest [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) data for Tier 2 validation
4. After [DD013](DD013_Simulation_Stack_Architecture.md): Implement Steps 4-5 in `master_openworm.py` (validation pipeline)
5. Set up GitHub Actions CI with Tier 2+3 blocking gates
