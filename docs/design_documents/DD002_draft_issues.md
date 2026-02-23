# DD002 Draft GitHub Issues

**Epic:** DD002 — Muscle Model Architecture and Calcium-Force Coupling

**Generated from:** [DD002: Muscle Model Architecture](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/)

**Methodology:** [DD015 §2.2 — DD Issue Generator](https://docs.openworm.org/design_documents/DD015_AI_Contributor_Model/#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 18 issues (ai-workable: 13 / human-expert: 5 | L1: 9, L2: 6, L3: 3)

**Note:** DD002's `GenericMuscleCell` template and `sibernetic_c302.py` coupling script are already implemented. These issues cover missing validation scripts, output pipeline, bug fixes, documentation, and research for future muscle-type differentiation. Significant working code already exists across multiple OpenWorm repos (`c302`, `muscle_model`, `sibernetic`, `CE_locomotion`) that can be directly imported, adapted, or used as templates — each issue below includes an **"Existing Code to Reuse"** section pointing contributors to the right starting point rather than writing from scratch. Where applicable, **"DD013 Stack Notes"** describe how each script integrates into the DD013 simulation stack (Docker containers, `docker compose run`, CI gates).

**Roadmap Context:** The "Groups" below organize issues thematically within this DD — they are **not** the same as the [DD Phase Roadmap](DD_PHASE_ROADMAP.md) phases (Phase 0/A/1/2/3/4). DD002 is a **Phase 0** DD (existing, working). Groups 1–3 primarily support Roadmap Phase A (infrastructure and bug fixes). Group 4 (research) feeds Roadmap Phase 1 (cell-type specialization via DD005). Group 5 (docs) can be addressed at any roadmap phase.

---

## Group 1: Validation Scripts

Target: Create the two scripts listed as `[TO BE CREATED]` in DD002, plus unit tests and parameter auditing.

---

### Issue 1: Refactor `c302_MuscleTest.py` plotting into standalone `plot_muscle_activation.py`

- **Title:** `[DD002] Refactor c302_MuscleTest.py plotting into standalone plot_muscle_activation.py`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, matplotlib
- **DD Section to Read:** [DD002 — How to Build & Test](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#how-to-build-test) (Step 4) and [DD002 — How to Visualize](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#how-to-visualize)
- **Existing Code to Reuse:**
    - `openworm/c302` → `c302/c302_MuscleTest.py` — already stimulates all 96 muscles and plots calcium dynamics; **extract** the plotting logic into a standalone script that reads `.dat` files instead of running inline (reuse strategy: **adapt**)
    - `openworm/c302` → `c302/c302_Muscles.py` — shows data generation pattern and `.dat` output format (reuse strategy: **reference**)
    - `openworm/sibernetic` → `plot_positions.py` — plotting template for simulation output (reuse strategy: **reference**)
    - `c302.__init__.get_muscle_names()` — import directly for muscle enumeration and quadrant grouping (reuse strategy: **import directly**)
- **DD013 Stack Notes:** Script should be runnable inside the Docker container (`docker compose run shell`). Output to `./output/` volume mount.
- **Depends On:** None
- **Files to Modify:**
    - `scripts/plot_muscle_activation.py` (new — adapts from `c302_MuscleTest.py` plotting logic)
- **Test Commands:**
    - `python CElegans.py C1Muscles && jnml LEMS_c302_C1_Muscles.xml -nogui`
    - `python scripts/plot_muscle_activation.py LEMS_c302_C1_Muscles_muscles.dat`
- **Acceptance Criteria:**
    - [ ] Reads LEMS muscle output `.dat` file (tab-separated, first column = time)
    - [ ] Extracts intracellular calcium concentration per muscle
    - [ ] Computes activation coefficient: `activation = min(1.0, [Ca²⁺]ᵢ / 4e-7)`
    - [ ] Plots activation time series for all 95 muscles (4 subplots by quadrant: MDR, MVR, MVL, MDL)
    - [ ] Plots heatmap: muscles (y-axis) vs. time (x-axis), warm colormap [0,1]
    - [ ] Saves figures to `output/` directory (PNG or PDF)
    - [ ] Prints summary: min/max/mean activation, number of muscles with peak > 0.3
    - [ ] Works as standalone script (no c302 import dependency beyond data file)
    - [ ] Adapts plotting logic from `c302_MuscleTest.py` rather than writing from scratch
- **Sponsor Summary Hint:** This script turns raw simulation numbers into pictures of muscle activity. Each of the worm's 95 body wall muscles contracts when calcium flows in — this script shows you which muscles are contracting, when, and how strongly. It's like watching an MRI of muscle activity: a heatmap where red means "contracting" and blue means "relaxed." DD002 lists this script as needed but never created. Most of the plotting logic already exists in `c302_MuscleTest.py` — this issue extracts it into a reusable standalone script.

---

### Issue 2: Adapt `muscle_model` validation code into `validate_muscle_calcium.py`

- **Title:** `[DD002] Adapt muscle_model validation code into validate_muscle_calcium.py — calcium dynamics and activation range checker`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, numpy
- **DD Section to Read:** [DD002 — How to Build & Test](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#how-to-build-test) (Step 5) and [DD002 — Green Light Criteria](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#green-light-criteria)
- **Existing Code to Reuse:**
    - `openworm/muscle_model` → `BoyleCohen2008/PythonSupport/Main_Version/compareToNeuroML2.py` — already validates calcium dynamics against the published Boyle-Cohen model; **adapt** its validation logic for this script (reuse strategy: **adapt**)
    - `openworm/muscle_model` → `BoyleCohen2008/PythonSupport/Main_Version/input_vars.py` — published parameter values for comparison targets (reuse strategy: **reference**)
    - `openworm/sibernetic` → `src/main_sim.py` — 4e-7 Ca²⁺ threshold is hardcoded here; reference for expected scaling (reuse strategy: **reference**)
    - `openworm/c302` → `c302/c302_MuscleTest.py` — comprehensive test that can generate validation data (reuse strategy: **reference**)
- **DD013 Stack Notes:** Should be callable from `docker compose run quick-test` pipeline. Exit code 0/1 for CI gate.
- **Depends On:** None
- **Files to Modify:**
    - `scripts/validate_muscle_calcium.py` (new — adapts validation logic from `muscle_model/compareToNeuroML2.py`)
    - `tests/test_validate_muscle_calcium.py` (new)
- **Test Commands:**
    - `python scripts/validate_muscle_calcium.py LEMS_c302_C1_Muscles_muscles.dat`
    - `pytest tests/test_validate_muscle_calcium.py`
- **Acceptance Criteria:**
    - [ ] Reads LEMS muscle output and extracts calcium and voltage traces
    - [ ] Checks activation range: all values in [0, 1]
    - [ ] Checks peak activation during neural drive > 0.3 (warning if < 0.5)
    - [ ] Estimates calcium decay time constant and checks ~12 ms (Boyle & Cohen 2008)
    - [ ] Checks voltage range: no values below -60 mV, no values above +20 mV
    - [ ] Prints PASS/FAIL for each criterion with diagnostic details
    - [ ] Returns exit code 0 on all-pass, non-zero on any failure
    - [ ] Unit tests with synthetic data (clean data → PASS, out-of-range data → FAIL)
    - [ ] Adapts validation approach from `muscle_model/compareToNeuroML2.py`
- **Sponsor Summary Hint:** The muscle model converts electrical signals into calcium, and calcium into contraction force. This script is a health check — it verifies the calcium dynamics look physically realistic: are contractions in the right range? Does calcium decay at the right speed (~12 ms)? Are voltages staying in biologically plausible bounds? The `muscle_model` repo already has validation code comparing NeuroML against published equations — this issue adapts that approach into a general-purpose validation script. It's listed as a DD002 deliverable but was never created.

---

### Issue 3: Convert `c302_IClampMuscle.py` and `c302_MuscleTest.py` into pytest suite

- **Title:** `[DD002] Convert c302_IClampMuscle.py and c302_MuscleTest.py into pytest suite for GenericMuscleCell validation`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD002 — Quality Criteria](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#quality-criteria) (criteria 3-5) and [DD002 — Implementation References — Muscle Cell Template](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#muscle-cell-template)
- **Existing Code to Reuse:**
    - `openworm/c302` → `c302/c302_IClampMuscle.py` — already tests a single muscle (MDR01) with current clamp injection; **convert** to pytest assertions (reuse strategy: **adapt**)
    - `openworm/c302` → `c302/c302_MuscleTest.py` — already validates all muscles with calcium dynamics; **convert** to pytest assertions (reuse strategy: **adapt**)
    - `openworm/muscle_model` → `NeuroML2/SingleCompMuscle.cell.nml` — reference for expected channel structure (4 channels, morphology) (reuse strategy: **reference**)
    - `openworm/c302` → `c302/custom_muscle_components.xml` — the actual channel definitions (k_fast_muscle, k_slow_muscle, ca_boyle_muscle) to validate against (reuse strategy: **reference**)
    - `openworm/c302` → `c302/parameters_C.py` (or `parameters_D.py`) — actual conductance density values used in simulation (reuse strategy: **reference**)
- **Depends On:** None
- **Files to Modify:**
    - `tests/test_muscle_cell.py` (new — converts `c302_IClampMuscle.py` and `c302_MuscleTest.py` logic into pytest)
- **Test Commands:**
    - `pytest tests/test_muscle_cell.py -v`
- **Acceptance Criteria:**
    - [ ] Validates GenericMuscleCell is valid NeuroML 2 (`jnml -validate`)
    - [ ] Verifies all 4 channels present: leak, K_slow, K_fast, Ca_boyle
    - [ ] Verifies muscle conductance densities match DD002 spec (leak: 5e-7, K_slow: 0.0006, K_fast: 0.0001, Ca_boyle: 0.0007 S/cm²)
    - [ ] Verifies conductance densities are 10-1000x smaller than neuron equivalents (DD002 Quality Criterion 5)
    - [ ] Verifies membrane capacitance = 1 µF/cm² and initial voltage = -45 mV
    - [ ] Verifies 95 muscle cells are generated (not 96 — see MVL24 issue)
    - [ ] Verifies all 4 quadrants present (MDR, MVR, MVL, MDL) with correct counts
    - [ ] Tests can run without NEURON installed (NeuroML XML inspection only)
    - [ ] Test logic adapted from existing `c302_IClampMuscle.py` and `c302_MuscleTest.py` scripts
- **Sponsor Summary Hint:** Unit tests that verify the muscle cell "recipe" is correct. Each muscle cell has 4 ion channels (leak, two potassium, one calcium) with specific conductance densities tuned to produce slow, sustained contractions rather than sharp spikes. The c302 repo already has two scripts (`c302_IClampMuscle.py` for single-muscle testing, `c302_MuscleTest.py` for all-muscle validation) — this issue converts their logic into a proper pytest suite that can run in CI.

---

### Issue 4: Extend `muscle_model/compareToNeuroML2.py` into full parameter audit

- **Title:** `[DD002] Extend muscle_model/compareToNeuroML2.py into full conductance density audit against Boyle & Cohen 2008 and DD002 spec`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD002 — Technical Approach — Muscle Cells](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#muscle-cells-use-the-same-hodgkin-huxley-framework-as-neurons) and [Boyle & Cohen 2008](https://doi.org/10.1016/j.biosystems.2008.05.025)
- **Existing Code to Reuse:**
    - `openworm/muscle_model` → `BoyleCohen2008/PythonSupport/Main_Version/compareToNeuroML2.py` — **THIS IS THE AUDIT TOOL**. Already compares NeuroML values against Boyle & Cohen 2008 equations; **extend** to output a full comparison table (reuse strategy: **adapt**)
    - `openworm/muscle_model` → `BoyleCohen2008/PythonSupport/Main_Version/input_vars.py` — published Boyle-Cohen parameter values as Python constants (reuse strategy: **reference**)
    - `openworm/muscle_model` → `NeuroML2/SingleCompMuscle.cell.nml` — reference values: leak 0.0193, K_slow 0.436, K_fast 0.400, Ca_boyle 0.220 mS/cm² (reuse strategy: **reference**)
    - `openworm/c302` → `c302/parameters_C.py` and `c302/parameters_D.py` — the actual conductance values in the simulation code (reuse strategy: **reference**)
    - **Unit note:** The `muscle_model` repo values (mS/cm²) differ in units from DD002 spec (S/cm²). The audit should explicitly reconcile these unit differences.
- **Depends On:** None
- **Files to Modify:**
    - None (audit task — output is a summary posted on the issue, extending the `compareToNeuroML2.py` approach)
- **Test Commands:**
    - N/A (audit task)
- **Acceptance Criteria:**
    - [ ] For each of the 4 channels (leak, K_slow, K_fast, Ca_boyle), find the conductance value in `c302_Muscles.py`
    - [ ] Compare against DD002 spec values and Boyle & Cohen 2008 Table 1
    - [ ] Document: file path, line number, variable name, actual value, expected value
    - [ ] Check calcium dynamics parameters: rho (0.000238), tau_Ca (11.5943 ms)
    - [ ] Check activation formula: `min(1.0, [Ca²⁺]ᵢ / 4e-7)`
    - [ ] Check max_muscle_force = 4000 in `sibernetic_c302.py`
    - [ ] Reconcile unit differences between `muscle_model` values (mS/cm²) and DD002 spec values (S/cm²)
    - [ ] Post findings as issue comment with comparison table
    - [ ] If discrepancies found, file follow-up issues for fixes
    - [ ] Uses `compareToNeuroML2.py` as starting point for the audit methodology
- **Sponsor Summary Hint:** A parameter audit — checking that the numbers in the code match the numbers in the scientific paper. The `muscle_model` repo already has `compareToNeuroML2.py` that does exactly this kind of validation for the standalone muscle model. This issue extends that approach to audit the c302 muscle parameters comprehensively. If parameters drifted during development (a common issue in long-running projects), the simulation's muscle behavior could be subtly wrong. This audit catches silent parameter drift.

---

## Group 2: Output Pipeline & Integration

Target: OME-Zarr export, config validation, and integration testing for DD002's interfaces with DD001 and DD003.

---

### Issue 5: Implement OME-Zarr export for muscle activation and calcium time series

- **Title:** `[DD002] Implement OME-Zarr export for muscle/activation/ and muscle/calcium/`
- **Labels:** `DD002`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, zarr
- **DD Section to Read:** [DD002 — Deliverables](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#deliverables) (OME-Zarr rows) and [DD014 — OME-Zarr Schema](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/)
- **Existing Code to Reuse:**
    - `openworm/sibernetic` → `src/main_sim.py` — documents the 96-element muscle array format: `[MDR_0...MDR_23, MVR_0...MVR_23, MVL_0...MVL_23, MDL_0...MDL_23]` (reuse strategy: **reference**)
    - `c302.__init__.get_muscle_names()` — canonical muscle ordering for array indices (reuse strategy: **import directly**)
    - No existing OME-Zarr code in any OpenWorm repo — this is genuinely new work, but data format is well-documented in the references above
- **DD013 Stack Notes:** Export script should be runnable inside the Docker container. Output to shared `./output/` volume. Should be callable from `docker compose run shell` and eventually integrated into post-simulation pipeline.
- **Depends On:** None
- **Files to Modify:**
    - `scripts/export_muscle_zarr.py` (new)
    - `tests/test_export_muscle_zarr.py` (new)
- **Test Commands:**
    - `python scripts/export_muscle_zarr.py LEMS_c302_C1_Muscles_muscles.dat --output output/openworm.zarr`
    - `python -c "import zarr; z = zarr.open('output/openworm.zarr'); print(z['muscle/activation'].shape, z['muscle/calcium'].shape)"`
    - `pytest tests/test_export_muscle_zarr.py`
- **Acceptance Criteria:**
    - [ ] Reads LEMS muscle output and extracts per-muscle calcium time series
    - [ ] Computes activation coefficients: `min(1.0, [Ca²⁺]ᵢ / 4e-7)` per muscle per timestep
    - [ ] Exports `muscle/activation/` array: shape (n_timesteps, 95), dtype float32, dimensionless [0,1]
    - [ ] Exports `muscle/calcium/` array: shape (n_timesteps, 95), dtype float32, units mol/cm³
    - [ ] Includes OME-Zarr metadata (axes labels: time, muscle_id; units)
    - [ ] Muscle IDs ordered by quadrant and row number (MDR01...MDR24, MVR01...MVR24, MVL01...MVL23, MDL01...MDL24)
    - [ ] Zarr store readable by DD014 viewer
    - [ ] Unit tests verify shapes, dtypes, value ranges, and metadata
- **Sponsor Summary Hint:** OME-Zarr is the data format that connects the muscle simulation to the 3D viewer (DD014). This script converts the raw simulation output into a structured data store containing two "movies" — muscle activation (how hard each muscle is contracting) and muscle calcium (the ion concentration driving contraction). The viewer reads this to show a heatmap of the worm's 95 muscles over time.

---

### Issue 6: Add muscle config section validation to openworm.yml

- **Title:** `[DD002] Add muscle config section validation and cross-constraint checking`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, yaml
- **DD Section to Read:** [DD002 — Integration Contract — Configuration](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#configuration) and [DD013 §1](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#1-simulation-configuration-system-openwormyml)
- **Existing Code to Reuse:**
    - `openworm/OpenWorm` → `.openworm.yml` — current minimal config file to validate against (reuse strategy: **reference**)
    - DD013 specifies the full `openworm.yml` schema (see DD013 §1) — use this as the validation spec (reuse strategy: **reference**)
    - `openworm/sibernetic` → `sibernetic_c302.py` — currently reads no config; this issue's work enables Issue 10 (reuse strategy: **reference**)
- **DD013 Stack Notes:** Validation script should be callable from `docker compose run quick-test` as a pre-simulation check. Exit code 0/1 for CI gate. Must run before any simulation step.
- **Depends On:** DD013 Issue 1 (openworm.yml config schema), DD013 Issue 2 (validation script)
- **Files to Modify:**
    - `scripts/validate_config.py` (extend — add muscle section rules)
    - `tests/test_config.py` (extend — add muscle validation tests)
- **Test Commands:**
    - `python scripts/validate_config.py openworm.yml`
    - `pytest tests/test_config.py -k muscle`
- **Acceptance Criteria:**
    - [ ] Validates `muscle.enabled` is boolean
    - [ ] Validates `muscle.calcium_coupling` is boolean
    - [ ] Validates `muscle.max_muscle_force` is a positive float
    - [ ] Validates `muscle.max_ca` is a positive float (physically reasonable range: 1e-8 to 1e-5 mol)
    - [ ] Enforces cross-constraint: `muscle.enabled: true` requires `neural.enabled: true`
    - [ ] Enforces cross-constraint: `muscle.calcium_coupling: true` requires `muscle.enabled: true`
    - [ ] Warns if `max_muscle_force` deviates more than 2x from default (4000)
    - [ ] Unit tests cover valid config, missing keys, invalid types, cross-constraint violations
- **Sponsor Summary Hint:** The muscle section in `openworm.yml` has 4 parameters that control how muscles behave. This adds validation rules — a safety net that catches mistakes like turning on muscles without turning on the neural circuit (muscles need neurons to tell them when to contract). It also catches typos like setting force to -4000 or calcium to a nonsensical value.

---

### Issue 7: Create DD002→DD003 calcium interface integration test

- **Title:** `[DD002] Create integration test verifying muscle calcium → Sibernetic activation pipeline`
- **Labels:** `DD002`, `ai-workable`, `L2`
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, docker
- **DD Section to Read:** [DD002 — Integration Contract — Outputs](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#inputs--outputs) and [DD002 — Coupling Bridge Ownership](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#coupling-bridge-ownership)
- **Existing Code to Reuse:**
    - `openworm/sibernetic` → `sibernetic_c302.py` — **THE file to test**. This IS the coupling bridge between c302/NEURON and Sibernetic (reuse strategy: **reference — test target**)
    - `openworm/sibernetic` → `src/main_sim.py` → `C302NRNSimulation` class — live NEURON integration mode that extracts `cai` (calcium) from soma; documents the coupling data flow (reuse strategy: **reference**)
    - `openworm/CE_locomotion` → `Worm.cpp` → `Step()` — reference for the correct coupling sequence (neural→NMJ→muscle→body); use as gold standard for testing the correct order of operations (reuse strategy: **reference**)
    - `openworm/c302` → `c302/c302_Muscles.py` — generates the test network the integration test should use (reuse strategy: **reference**)
- **DD013 Stack Notes:** Test should use `docker compose run quick-test` infrastructure. Short simulation (1-2s sim time). Must be runnable in CI without GPU (mock Sibernetic physics if needed).
- **Depends On:** Issue 2 (validate_muscle_calcium.py)
- **Files to Modify:**
    - `tests/test_dd002_dd003_integration.py` (new)
- **Test Commands:**
    - `docker compose run quick-test`
    - `pytest tests/test_dd002_dd003_integration.py -v`
- **Acceptance Criteria:**
    - [ ] Runs a short coupled simulation (c302 muscles + Sibernetic, 1-2 seconds sim time)
    - [ ] Verifies `sibernetic_c302.py` reads muscle [Ca²⁺]ᵢ from NEURON state
    - [ ] Verifies activation coefficients are computed correctly: `min(1.0, [Ca²⁺]ᵢ / max_ca)`
    - [ ] Verifies activation values written to Sibernetic are in [0, 1] range
    - [ ] Verifies at least some muscles have non-zero activation (coupling is working)
    - [ ] Verifies coupling timestep matches config (`dt_coupling = 0.005 ms`)
    - [ ] Test uses Docker (`docker compose run quick-test`) or can mock the file interface
    - [ ] Reports which muscle IDs are active and their peak activation values
- **Sponsor Summary Hint:** The critical handoff: muscle calcium from the neural simulation (c302/NEURON) must flow correctly into the body physics engine (Sibernetic) via the coupling script. This test verifies the entire pipeline — neurons fire, muscles accumulate calcium, calcium converts to a contraction coefficient, and that coefficient reaches Sibernetic. If this pipeline breaks, the virtual worm is paralyzed.

---

### Issue 8: Extend `c302_TargetMuscle.py` into systematic NMJ connectivity validator

- **Title:** `[DD002] Extend c302_TargetMuscle.py into systematic NMJ connectivity validator against Cook et al. 2019`
- **Labels:** `DD002`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroscience, connectomics
- **DD Section to Read:** [DD002 — Neural-to-Muscle Coupling](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#neural-to-muscle-coupling) and [DD020](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/) (cect API)
- **Existing Code to Reuse:**
    - `openworm/c302` → `c302/c302_TargetMuscle.py` — already queries which neurons synapse onto a given muscle; **extend** to iterate over all muscles and produce a systematic comparison (reuse strategy: **adapt**)
    - `openworm/CE_locomotion` → `NervousSystem.cpp` — NMJ weight constants per motor neuron class: `NMJ_DA`, `NMJ_DB`, `NMJ_DD`, `NMJ_VA`, `NMJ_VB`, `NMJ_VD` (reuse strategy: **reference**)
    - ConnectomeToolbox (`cect`) API — `from cect import connectome_data` for Cook et al. 2019 adult hermaphrodite NMJ data (reuse strategy: **import directly**)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/validate_nmj_connectivity.py` (new — extends `c302_TargetMuscle.py` approach to all muscles)
- **Test Commands:**
    - `python scripts/validate_nmj_connectivity.py`
- **Acceptance Criteria:**
    - [ ] Extract NMJ connectivity from c302 muscle network (which motor neurons innervate which muscles)
    - [ ] Extract NMJ connectivity from cect/ConnectomeToolbox (Cook et al. 2019 adult hermaphrodite)
    - [ ] Compare: for each muscle, list motor neurons in c302 vs. Cook et al. 2019
    - [ ] Report: number of matching connections, missing connections, extra connections
    - [ ] Flag any muscles with zero innervation in c302 but known innervation in Cook et al.
    - [ ] Flag NMJ conductance values: are 0.5-1.0 nS values consistent across all NMJs?
    - [ ] Post comparison table as issue comment
    - [ ] File follow-up issues for any significant discrepancies
    - [ ] Builds on `c302_TargetMuscle.py` query approach rather than reimplementing NMJ lookup
- **Sponsor Summary Hint:** Motor neurons connect to muscles via neuromuscular junctions (NMJs) — the biological "wires" that tell muscles when to contract. Cook et al. (2019) mapped every NMJ connection in the real worm using electron microscopy. The c302 repo already has `c302_TargetMuscle.py` that queries NMJ connections for a single muscle — this issue extends that into a systematic validator across all 95 muscles against the ground truth connectome. This requires domain expertise to interpret which discrepancies matter biologically.

---

## Group 3: Bug Fixes & Improvements

Target: Fix known issues and improve muscle model configurability.

---

### Issue 9: Patch `get_muscle_names()` to return 95 muscles — fix MVL24 phantom

- **Title:** `[DD002] Patch get_muscle_names() in c302/__init__.py to return 95 muscles — fix MVL24 phantom`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD002 — Known Issues — Issue 3: MVL24](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#issue-3-mvl24-muscle-does-not-exist)
- **Existing Code to Reuse:**
    - `openworm/c302` → `c302/__init__.py` → `get_muscle_names()` — returns all 96 muscle names; **this function must be patched** to return 95 (excluding MVL24) (reuse strategy: **modify in place**)
    - `openworm/c302` → `c302/c302_Muscles.py` — muscle generation loop that creates MVL24; must be updated to skip it (reuse strategy: **modify in place**)
    - `CElegansNeuroML/CElegans/generatedNeuroML2/muscles.csv` — row to remove (reuse strategy: **modify in place**)
    - `c302.__init__.is_muscle(cell_name)` — verify this still works after the fix (reuse strategy: **reference**)
- **Depends On:** Issue 3 (unit tests — to verify fix doesn't break anything)
- **Files to Modify:**
    - `c302/__init__.py` (modify `get_muscle_names()` to exclude MVL24)
    - `c302/c302_Muscles.py` (modify muscle generation)
    - `CElegansNeuroML/CElegans/generatedNeuroML2/muscles.csv` (update to 95 rows)
- **Test Commands:**
    - `python CElegans.py C1Muscles`
    - `jnml -validate LEMS_c302_C1_Muscles.xml`
    - `pytest tests/test_muscle_cell.py`
- **Acceptance Criteria:**
    - [ ] MVL24 is either removed or has all conductances set to zero
    - [ ] `muscles.csv` contains exactly 95 rows (not 96)
    - [ ] Quadrant counts: MDR=24, MVR=24, MVL=23, MDL=24 (total=95)
    - [ ] `get_muscle_names()` returns exactly 95 names
    - [ ] NeuroML validation passes (`jnml -validate`)
    - [ ] Simulation runs without error after fix
    - [ ] Existing unit tests still pass
    - [ ] If MVL24 is removed (preferred), update any hardcoded references to 96 muscles
    - [ ] If MVL24 is zeroed (fallback), add comment explaining why
- **Sponsor Summary Hint:** The real worm has 95 body wall muscles, but the simulation has 96 — an extra phantom muscle called MVL24 that doesn't exist in nature. The fix is surgical: patch `get_muscle_names()` in `c302/__init__.py` to exclude MVL24, update the muscle generation loop, and remove the row from `muscles.csv`. This is a minor biological inaccuracy that should be fixed to prevent confusion and ensure muscle-count-dependent analyses are correct.

---

### Issue 10: Propagate muscle config parameters from openworm.yml to sibernetic_c302.py

- **Title:** `[DD002] Propagate muscle.max_muscle_force and muscle.max_ca from openworm.yml to coupling script`
- **Labels:** `DD002`, `ai-workable`, `L2`
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python
- **DD Section to Read:** [DD002 — Integration Contract — Configuration](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#configuration) and [DD013 §1](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#1-simulation-configuration-system-openwormyml)
- **Existing Code to Reuse:**
    - `openworm/sibernetic` → `sibernetic_c302.py` — **THE file to modify**. Currently hardcodes `max_force` and `max_ca`; replace hardcoded values with config loading (reuse strategy: **modify in place**)
    - `openworm/sibernetic` → `src/main_sim.py` — 4e-7 hardcoded at the Ca²⁺ scaling line; must also read from config (reuse strategy: **modify in place**)
    - `openworm/OpenWorm` → `master_openworm.py` — orchestrator that launches `sibernetic_c302.py`; needs to pass config path (reuse strategy: **modify in place**)
    - DD013 §1 `openworm.yml` schema — defines `muscle.max_muscle_force` and `muscle.max_ca` fields (reuse strategy: **reference**)
- **DD013 Stack Notes:** Config must flow through the full chain: `openworm.yml` → `master_openworm.py` → `sibernetic_c302.py` → NEURON/Sibernetic. Config file path should be a Docker volume mount or environment variable.
- **Depends On:** DD013 Issue 1 (openworm.yml schema), DD013 Issue 9 (config loading in master_openworm.py)
- **Files to Modify:**
    - `sibernetic_c302.py` (read config instead of hardcoded values)
    - `tests/test_coupling_config.py` (new)
- **Test Commands:**
    - `python -c "import yaml; c = yaml.safe_load(open('openworm.yml')); print(c['muscle'])"`
    - `pytest tests/test_coupling_config.py`
- **Acceptance Criteria:**
    - [ ] `sibernetic_c302.py` reads `muscle.max_muscle_force` from `openworm.yml` (default: 4000)
    - [ ] `sibernetic_c302.py` reads `muscle.max_ca` from `openworm.yml` (default: 4e-7)
    - [ ] Activation formula uses config value: `min(1.0, ca / config['muscle']['max_ca'])`
    - [ ] Force formula uses config value: `activation * config['muscle']['max_muscle_force']`
    - [ ] Falls back to hardcoded defaults if config not available (backward compatible)
    - [ ] Unit tests verify config loading and fallback behavior
    - [ ] Changing config values in openworm.yml changes simulation behavior (no restart of NEURON needed)
- **Sponsor Summary Hint:** Currently the muscle coupling script has key parameters hardcoded (max force = 4000, max calcium = 4e-7). This moves them to the central config file (`openworm.yml`) so contributors can tune muscle strength and calcium sensitivity without editing code. Think of it like moving a knob from inside the engine to the dashboard.

---

### Issue 11: Verify and document calcium-to-activation edge cases

- **Title:** `[DD002] Verify calcium-to-activation formula handles edge cases correctly`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD002 — Calcium-to-Force Coupling](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#calcium-to-force-coupling-the-bridge-to-sibernetic)
- **Existing Code to Reuse:**
    - `openworm/sibernetic` → `src/main_sim.py` — the actual activation formula implementation to test; locate the `min(1.0, ca / max_ca)` line (reuse strategy: **reference — test target**)
    - `openworm/sibernetic` → `sibernetic_c302.py` — where the formula is applied in production (reuse strategy: **reference — test target**)
    - `openworm/CE_locomotion` → `Muscles.cpp` — alternative (simpler) muscle dynamics using first-order low-pass filter; useful comparison for expected behavior at edge cases (reuse strategy: **reference**)
- **Depends On:** None
- **Files to Modify:**
    - `tests/test_activation_edge_cases.py` (new)
- **Test Commands:**
    - `pytest tests/test_activation_edge_cases.py -v`
- **Acceptance Criteria:**
    - [ ] Tests activation formula: `activation = min(1.0, [Ca²⁺]ᵢ / max_ca)`
    - [ ] Verifies: [Ca²⁺]ᵢ = 0 → activation = 0
    - [ ] Verifies: [Ca²⁺]ᵢ = max_ca → activation = 1.0
    - [ ] Verifies: [Ca²⁺]ᵢ > max_ca → activation = 1.0 (clamped, not > 1)
    - [ ] Verifies: negative [Ca²⁺]ᵢ (numerical artifact) → activation clamped to 0 (not negative)
    - [ ] Verifies: very small [Ca²⁺]ᵢ (1e-20) → activation ≈ 0 (not NaN, not underflow)
    - [ ] Documents any negative-calcium clamping in code comments
    - [ ] If negative calcium is possible, add `max(0, ca)` guard and document why
- **Sponsor Summary Hint:** The activation formula converts calcium concentration to a contraction coefficient [0, 1]. But what happens at the edges? What if calcium goes negative (a numerical glitch)? What if it exceeds the maximum? What about extremely tiny values? This issue verifies the formula is robust — no NaN values, no negative contractions, no activation above 100%. Defensive programming for the most critical equation in the muscle model.

---

### Issue 12: Audit NMJ conductance range across all motor neuron–muscle pairs

- **Title:** `[DD002] Audit NMJ conductance values (0.5-1.0 nS) across all motor neuron–muscle pairs`
- **Labels:** `DD002`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroscience
- **DD Section to Read:** [DD002 — Neural-to-Muscle Coupling](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#neural-to-muscle-coupling) and [DD001 — Integration Contract](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/)
- **Existing Code to Reuse:**
    - `openworm/c302` → `c302/parameters_C.py` → `neuron_to_muscle_chem_exc_syn_gbase`, `neuron_to_muscle_chem_inh_syn_gbase` — the actual synapse conductance values used in the simulation (reuse strategy: **reference**)
    - `openworm/c302` → `c302/c302_TargetMuscle.py` — queries NMJ connections for a given muscle; use to enumerate all connections (reuse strategy: **adapt**)
    - `openworm/CE_locomotion` → `NervousSystem.cpp` — NMJ weight constants per motor neuron class (`NMJ_DA`, `NMJ_DB`, `NMJ_DD`, `NMJ_VA`, `NMJ_VB`, `NMJ_VD`); comparison reference (reuse strategy: **reference**)
- **Depends On:** None
- **Files to Modify:**
    - None (audit task — output is a summary posted on the issue)
- **Test Commands:**
    - N/A (audit task)
- **Acceptance Criteria:**
    - [ ] Extract all NMJ synapse conductance values from c302 muscle network LEMS/NeuroML files
    - [ ] Verify all NMJ conductances are in the 0.5-1.0 nS range specified in DD002
    - [ ] Compare NMJ conductance (0.5-1.0 nS) vs. inter-neuron synapse conductance (0.09 nS) — confirm ratio is ~5-11x
    - [ ] Check if any motor neuron classes (VA, VB, DA, DB, DD, VD, AS) have systematically different NMJ weights
    - [ ] Report distribution: histogram of NMJ conductance values across all ~350 NMJ connections
    - [ ] Identify outliers (any NMJ conductance < 0.3 nS or > 2.0 nS)
    - [ ] Post findings as issue comment with comparison table and histogram
    - [ ] Assess whether uniform conductance is appropriate or if motor-neuron-class-specific values would be more realistic
- **Sponsor Summary Hint:** Each motor neuron connects to its target muscle via a neuromuscular junction (NMJ) with a specific "volume" setting — the conductance. DD002 says all NMJs should be 0.5-1.0 nS (about 5-10x louder than neuron-to-neuron connections). But are they actually set correctly in the code? Do different motor neuron types (e.g., the ones for forward vs. backward locomotion) need different conductance values? This audit requires neuroscience expertise to interpret the results.

---

## Group 4: Research & Advanced Features

Target: Investigate muscle-type differentiation, multi-compartment modeling, and alternative mechanical models for future phases.

---

### Issue 13: Survey CeNGEN transcriptomic data for muscle-type-specific channel expression

- **Title:** `[DD002] Survey CeNGEN data for muscle-type-specific ion channel expression profiles`
- **Labels:** `DD002`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, bioinformatics, neuroscience
- **DD Section to Read:** [DD002 — Migration Path — Muscle-Type Diversity](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#if-muscle-type-diversity-is-required-phase-3) and [DD005](https://docs.openworm.org/design_documents/DD005_Cell_Type_Differentiation_Strategy/) (Cell-Type Specialization)
- **Existing Code to Reuse:**
    - `openworm/wormneuroatlas` repo — Python package for accessing CeNGEN single-cell RNA-seq data; use as the primary data access interface (reuse strategy: **import directly**)
    - `openworm/c302` → `c302/parameters_D.py` — current channel→gene mapping (which genes map to which model channels); use as the mapping to validate against (reuse strategy: **reference**)
    - `openworm/muscle_model` → `NeuroML2/*.channel.nml` — the channel definitions that would need gene-specific conductances if differentiation is warranted (reuse strategy: **reference**)
    - `openworm/JohnsonMailler_MuscleModel` → `NeuroML2/CaPool.nml` — alternative Ca²⁺ pool dynamics as reference for different channel implementations (reuse strategy: **reference**)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a report)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Query CeNGEN single-cell RNA-seq database for body wall muscle cells
    - [ ] Extract expression levels for DD002's 4 channel genes: leak (best candidate), K_slow (kvs-1? egl-2?), K_fast (shk-1?), Ca_boyle (egl-19? unc-2?)
    - [ ] Determine which WormBase gene IDs correspond to each DD002 channel type
    - [ ] Compare expression across body wall muscles vs. pharyngeal muscles vs. vulval muscles
    - [ ] Assess: do body wall muscles in different quadrants (MDR/MVR/MVL/MDL) show differential channel expression?
    - [ ] Summarize: which muscle types might need distinct conductance profiles?
    - [ ] Post report as issue comment with data tables and citations
    - [ ] If differentiation is warranted, draft a follow-up issue for Phase 3 implementation
- **Sponsor Summary Hint:** The current model uses one generic muscle cell type for all 95 body wall muscles. But real worms might have subtle differences — do muscles near the head express different ion channels than muscles near the tail? CeNGEN is a massive dataset of gene expression in individual C. elegans cells. This research mines that data to determine whether we need different "recipes" for different muscles, or whether the single generic model is biologically justified.

---

### Issue 14: Prototype multi-compartment muscle cell model

- **Title:** `[DD002] Prototype multi-compartment muscle cell to evaluate voltage non-uniformity`
- **Labels:** `DD002`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, neuroscience, computational-modeling
- **DD Section to Read:** [DD002 — Known Issues — Issue 1: Single Muscle Compartment](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#issue-1-single-muscle-compartment)
- **Existing Code to Reuse:**
    - `openworm/muscle_model` → `NeuroML2/SingleCompMuscle.cell.nml` — **starting point**: the complete single-compartment muscle cell with 4 channels and morphology; extend to multi-compartment (reuse strategy: **adapt**)
    - `openworm/c302` → `c302/custom_muscle_components.xml` — channel definitions (k_fast_muscle, k_slow_muscle, ca_boyle_muscle) to include in multi-compartment version (reuse strategy: **import/include**)
    - `openworm/CE_locomotion` → `WormBody.h` — body segment dimensions (50 segments); use for determining realistic compartment sizes for the ~60 µm muscle spindle (reuse strategy: **reference**)
- **Depends On:** None
- **Files to Modify:**
    - `c302/prototypes/multi_compartment_muscle.py` (new — experimental)
- **Test Commands:**
    - `python c302/prototypes/multi_compartment_muscle.py`
    - `jnml -validate MultiCompartmentMuscle.nml`
- **Acceptance Criteria:**
    - [ ] Create a prototype muscle cell with 4-8 compartments along spindle axis (~60 µm length)
    - [ ] Use same channel densities as GenericMuscleCell (DD002 spec)
    - [ ] Add axial resistance between compartments (estimate from muscle cell dimensions)
    - [ ] Run single-cell simulation: inject current at one end, measure voltage at both ends
    - [ ] Quantify voltage attenuation: is voltage uniform (single-compartment is fine) or non-uniform (multi-compartment is needed)?
    - [ ] Report: compute time increase per muscle cell (current: 1 compartment → prototype: N compartments)
    - [ ] Assess feasibility: N compartments × 95 muscles × simulation duration → practical?
    - [ ] Post findings with go/no-go recommendation for multi-compartment adoption
    - [ ] Starts from `SingleCompMuscle.cell.nml` rather than building from scratch
- **Sponsor Summary Hint:** Each muscle is currently modeled as a single point — the voltage is the same everywhere in the cell. But real muscles are spindle-shaped, ~60 µm long. If one end of the muscle is stimulated by a motor neuron, does the other end "know"? This prototype starts from the existing `SingleCompMuscle.cell.nml` in the `muscle_model` repo and extends it to 4-8 compartments. It tests whether voltage spreads uniformly (single-compartment is fine, saving enormous computation) or attenuates (we'd need multi-compartment, at 4-8x the computational cost per muscle).

---

### Issue 15: Evaluate Hill-type crossbridge mechanics feasibility

- **Title:** `[DD002] Evaluate Hill-type crossbridge mechanics for specialized muscles (egg-laying, defecation)`
- **Labels:** `DD002`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** physics, biomechanics, neuroscience
- **DD Section to Read:** [DD002 — Alternatives Considered — Hill-Type Muscle Model](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#1-hill-type-muscle-model-with-crossbridge-dynamics) and [DD002 — Migration Path](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#migration-path)
- **Existing Code to Reuse:**
    - `openworm/JohnsonMailler_MuscleModel` — **THE alternative muscle model** to evaluate. Has different Ca²⁺ dynamics (EGL_19/L-type Ca²⁺, SHK_1/K⁺) from Boyle-Cohen; compare channel repertoire and dynamics (reuse strategy: **reference**)
    - `openworm/muscle_model` → `BoyleCohen2008/` — baseline Boyle-Cohen model to compare against (reuse strategy: **reference**)
    - `openworm/CE_locomotion` → `Muscles.cpp` — simplest coupling model (first-order low-pass filter: `dV/dt = (V_input - V_muscle) / T_muscle`); lower bound for muscle dynamics complexity (reuse strategy: **reference**)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a feasibility report)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Review literature on C. elegans muscle mechanics: tetanic contraction (egg-laying), rapid twitches (defecation), isometric force-length curves
    - [ ] Identify which muscle types may require crossbridge dynamics (vulval, uterine, anal depressor, intestinal)
    - [ ] Assess parameter availability: are actin-myosin binding rates, length-tension curves measured for C. elegans?
    - [ ] Estimate computational cost: 6+ additional state variables per muscle × N specialized muscles
    - [ ] Compare against DD002's linear activation model: when does linear fail?
    - [ ] Compare Boyle-Cohen, JohnsonMailler, and CE_locomotion muscle dynamics approaches
    - [ ] Propose LEMS ComponentType extension approach (per DD002 Migration Path)
    - [ ] Post feasibility report with go/no-go recommendation per muscle type
    - [ ] If Hill-type is warranted for any muscle type, draft DD amendment for Phase 3
- **Sponsor Summary Hint:** DD002's muscle model uses a simple linear formula: more calcium = more force. This works for locomotion (Boyle & Cohen 2008 showed body wall muscles are "simple actuators"). But what about specialized muscles — the vulval muscles that lay eggs, the anal depressor muscle that contracts during defecation, the pharyngeal muscles that pump food? These might need a richer mechanical model (Hill-type) with actin-myosin crossbridge dynamics. Three different muscle model implementations exist across OpenWorm repos (`muscle_model`, `JohnsonMailler_MuscleModel`, `CE_locomotion`) — this research compares them to determine which muscles, if any, need upgrading.

---

## Group 5: Documentation & Maintenance

Target: Comprehensive documentation enabling contributors to understand and modify the muscle model.

---

### Issue 16: Create muscle model contributor guide

- **Title:** `[DD002] Create muscle model contributor guide for c302 developers`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD002 — Quality Criteria](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#quality-criteria), [DD002 — Testing Procedure](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#testing-procedure), and [DD002 — Boundaries](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#boundaries-explicitly-out-of-scope)
- **Existing Code to Reuse:**
    - `openworm/c302` → `c302/c302_Muscles.py`, `c302/c302_MuscleTest.py`, `c302/c302_IClampMuscle.py`, `c302/c302_MusclesSine.py` — document these as the "getting started" workflow; show contributors the progression from single-muscle test → all-muscle test → oscillatory stimulation (reuse strategy: **document as resources**)
    - `openworm/muscle_model` repo — document as the biophysical reference implementation for Boyle-Cohen muscle (reuse strategy: **document as resource**)
    - `openworm/c302` → `c302/parameters_C.py` through `parameters_D.py` — document the parameter level system (A/B/C/D) and when to use each (reuse strategy: **document as resource**)
    - The contributor guide should **map all existing code resources** so contributors know what's already built before starting new work
- **Depends On:** None
- **Files to Modify:**
    - `docs/muscle_model_guide.md` (new — in c302 repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Overview: what the muscle model does, what it produces, who uses its output
    - [ ] File map: `c302_Muscles.py` (templates), `muscles.csv` (cell list), `sibernetic_c302.py` (coupling)
    - [ ] Existing code inventory: catalog all muscle-related scripts in c302, muscle_model, and CE_locomotion repos
    - [ ] Contributor workflow: generate muscle network → validate NeuroML → run simulation → check outputs
    - [ ] Quality criteria: 5 rules from DD002 (calcium interface, movement validation, NeuroML 2, units, muscle-neuron distinction)
    - [ ] Common mistakes: copying neuron parameters to muscles, changing calcium variable name without updating `sibernetic_c302.py`
    - [ ] References to DD002 for specification, DD003 for body physics coupling, DD014 for visualization
    - [ ] Aimed at L2 contributors (familiar with Python but new to muscle physiology)
- **Sponsor Summary Hint:** A "getting started" guide for anyone wanting to improve the muscle model. Explains which files to edit, what tests to run, and what mistakes to avoid (like accidentally copying neuron parameters to muscles — which would make muscles twitch like neurons instead of contracting smoothly). Crucially, this guide catalogs all existing code across repos so contributors reuse what's already built. DD002 is the specification; this is the practical "how to contribute" companion.

---

### Issue 17: Document NMJ connectivity and muscle quadrant mapping

- **Title:** `[DD002] Document muscle quadrant layout and NMJ connectivity diagram`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD002 — Context & Background](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#context-background), [DD002 — Muscle List](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#muscle-list-95-cells), and [DD002 — Neural-to-Muscle Coupling](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#neural-to-muscle-coupling)
- **Existing Code to Reuse:**
    - `openworm/c302` → `c302/__init__.py` → `get_muscle_names()` — canonical naming convention (MDR01-24, MVR01-24, MVL01-23, MDL01-24); document this as the authoritative source (reuse strategy: **document as resource**)
    - `openworm/sibernetic` → `src/main_sim.py` — 96-element array layout `[MDR_0...MDR_23, MVR_0...MVR_23, MVL_0...MVL_23, MDL_0...MDL_23]`; document the index mapping (reuse strategy: **document as resource**)
    - `openworm/CE_locomotion` → `Worm.cpp` — NMJ wiring showing which motor classes (DA, DB, DD, VA, VB, VD, AS) innervate dorsal vs. ventral quadrants (reuse strategy: **document as resource**)
    - `openworm/CE_locomotion` → `WormBody.h` — 50-segment body layout for anterior-posterior positioning (reuse strategy: **document as resource**)
- **Depends On:** None
- **Files to Modify:**
    - `docs/muscle_quadrant_mapping.md` (new — in c302 repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Diagram: 4 quadrants (MDR, MVR, MVL, MDL) arranged around body cross-section
    - [ ] Table: all 95 muscles with quadrant, row number (1-24), anterior-posterior position
    - [ ] Explanation: why MDL has 24, MVL has 23 (no MVL24)
    - [ ] Diagram: motor neuron classes (VA, VB, DA, DB, DD, VD, AS) and which quadrants they innervate
    - [ ] Explanation: excitatory (VA/VB/DA/DB/AS) vs. inhibitory (DD/VD) motor neurons
    - [ ] Explanation: dorsal vs. ventral muscle coordination for undulatory locomotion
    - [ ] Index mapping: c302 muscle names → Sibernetic array indices (from `main_sim.py`)
    - [ ] Cross-references to DD003 (elastic particle mapping in Sibernetic) and WormAtlas
    - [ ] Visual enough for L1 contributors to understand muscle anatomy at a glance
- **Sponsor Summary Hint:** The worm's 95 body wall muscles wrap around the body in 4 strips (quadrants). During forward crawling, dorsal and ventral muscles activate in alternating waves — like a crowd doing "the wave" in a stadium. This document maps out which muscles are where, which motor neurons control them, and how that creates coordinated movement. It includes the critical index mapping between c302 muscle names and Sibernetic array positions. It's the anatomical atlas for anyone working on the muscle system.

---

### Issue 18: Document sibernetic_c302.py coupling script architecture

- **Title:** `[DD002] Document sibernetic_c302.py coupling script: data flow, timing, and variable mapping`
- **Labels:** `DD002`, `ai-workable`, `L2`
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, docs
- **DD Section to Read:** [DD002 — Coupling to Sibernetic](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#coupling-to-sibernetic) and [DD002 — Coupling Bridge Ownership](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#coupling-bridge-ownership)
- **Existing Code to Reuse:**
    - `openworm/sibernetic` → `sibernetic_c302.py` — **THE file to document** (8.6 KB); the entire coupling bridge between c302/NEURON and Sibernetic (reuse strategy: **document as primary subject**)
    - `openworm/sibernetic` → `src/main_sim.py` — coupling modes (synthetic waves, file-based, live NEURON) and data flow (17.9 KB); documents three different ways coupling can work (reuse strategy: **document as primary subject**)
    - `openworm/CE_locomotion` → `Worm.cpp` → `Step()` — cleanest reference for correct coupling sequence: body physics → stretch receptors → neural compute → NMJ translation → muscle dynamics → body activation (reuse strategy: **document as reference architecture**)
    - `openworm/OpenWorm` → `master_openworm.py` — how the orchestrator invokes the coupling; Steps 4-5 (analysis/validation) are unimplemented stubs (reuse strategy: **document as context**)
- **Depends On:** None
- **Files to Modify:**
    - `docs/coupling_script_architecture.md` (new — in Sibernetic repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Data flow diagram: NEURON muscle state → `sibernetic_c302.py` → Sibernetic muscle activation
    - [ ] Variable mapping: which NEURON variable (`ca_internal`) maps to which Sibernetic input
    - [ ] Timing diagram: coupling timestep (dt_coupling = 0.005 ms), when reads/writes happen
    - [ ] Activation formula walkthrough: `min(1.0, [Ca²⁺]ᵢ / max_ca)` with units and typical values
    - [ ] Force injection: how Sibernetic converts activation [0,1] to elastic particle forces (max_force = 4000)
    - [ ] Muscle ID mapping: c302 muscle names → Sibernetic muscle indices
    - [ ] Coupling modes: document all three modes from `main_sim.py` (synthetic, file-based, live NEURON)
    - [ ] Change impact analysis: what breaks if you change each parameter (from DD002 Coupling Bridge Ownership section)
    - [ ] Coordination notes: who must agree before changing the coupling interface
    - [ ] Cross-references to DD002 (muscle model), DD003 (body physics), DD013 (simulation stack)
    - [ ] Reference `CE_locomotion/Worm.cpp::Step()` as gold standard for coupling sequence
- **Sponsor Summary Hint:** The coupling script is the bridge between two very different worlds: the electrical simulation (NEURON, millisecond timescale, voltages in millivolts) and the mechanical simulation (Sibernetic, microsecond timescale, forces in arbitrary units). This document explains exactly how data flows across that bridge — what gets read, what gets computed, what gets written, and when. It references the `CE_locomotion` implementation as the gold standard for coupling sequence. It's the most critical integration point in the entire worm simulation, and currently the least documented.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 18 |
| **ai-workable** | 13 |
| **human-expert** | 5 |
| **L1** | 9 |
| **L2** | 6 |
| **L3** | 3 |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Validation Scripts** | 1–4 | Adapt existing scripts into validation tools, unit tests, parameter audit |
| **2: Output Pipeline & Integration** | 5–8 | OME-Zarr export, config validation, interface testing |
| **3: Bug Fixes & Improvements** | 9–12 | MVL24 fix, config propagation, edge cases, NMJ audit |
| **4: Research & Advanced** | 13–15 | Transcriptomics survey, multi-compartment, Hill-type |
| **5: Documentation** | 16–18 | Contributor guide, anatomy mapping, coupling architecture |

### Code Reuse Summary

| Issue | Reframe Level | Primary Source Code | Reuse Strategy |
|-------|--------------|-------------------|----------------|
| 1 | Aggressively reframed | `c302/c302_MuscleTest.py` | Extract plotting logic into standalone script |
| 2 | Aggressively reframed | `muscle_model/.../compareToNeuroML2.py` | Adapt validation code |
| 3 | Aggressively reframed | `c302/c302_IClampMuscle.py`, `c302/c302_MuscleTest.py` | Convert to pytest suite |
| 4 | Aggressively reframed | `muscle_model/.../compareToNeuroML2.py`, `input_vars.py` | Extend audit methodology |
| 5 | Genuinely new | (no existing Zarr code) | New work; data format documented |
| 6 | Genuinely new | (no existing config validation) | New work; schema from DD013 |
| 7 | Genuinely new | `sibernetic/sibernetic_c302.py` (test target) | New test for existing pipeline |
| 8 | Aggressively reframed | `c302/c302_TargetMuscle.py`, cect API | Extend single-muscle query to all muscles |
| 9 | Aggressively reframed | `c302/__init__.py` → `get_muscle_names()` | Patch function in place |
| 10 | Modify existing | `sibernetic/sibernetic_c302.py` | Replace hardcoded values with config |
| 11 | New tests | `sibernetic/src/main_sim.py` (test target) | New tests for existing formula |
| 12 | Analysis | `c302/parameters_C.py`, `c302_TargetMuscle.py` | Audit using existing query tools |
| 13–15 | Research | Various repos | Reference only |
| 16–18 | Documentation | All repos | Catalog existing code |

### Cross-References

| Related DD | Related Issues |
|------------|---------------|
| DD001 (Neural Circuit) | Issues 8, 12 (NMJ connectivity and conductance) |
| DD003 (Body Physics) | Issues 7, 10, 18 (calcium interface, config, coupling) |
| DD005 (Cell-Type Specialization) | Issue 13 (CeNGEN transcriptomics for muscle types) |
| DD007 (Pharyngeal System) | Issue 15 (specialized muscle mechanics) |
| DD010 (Validation Framework) | Issues 1, 2, 7 (validation scripts and integration testing) |
| DD013 (Simulation Stack) | Issues 6, 10 (config schema and propagation) |
| DD014 (Dynamic Visualization) | Issue 5 (OME-Zarr export for viewer) |
| DD020 (Connectome Data Access) | Issue 8 (cect API for NMJ validation) |
| DD003 Draft Issues (Issue 18) | Issue 17 (complementary: c302-side NMJ mapping vs. Sibernetic-side particle mapping) |

### Dependency Graph

```
Issue 1 (plot_muscle_activation.py) — independent
Issue 2 (validate_muscle_calcium.py) — independent
Issue 3 (unit tests) ─────────────────→ Issue 9 (MVL24 fix — tests verify fix)
Issue 4 (parameter audit) — independent

Issue 5 (OME-Zarr export) — independent
Issue 6 (config validation) — depends on DD013 Issues 1, 2
Issue 7 (DD002→DD003 integration test) — depends on Issue 2
Issue 8 (NMJ connectivity validation) — independent

Issue 9 (MVL24 fix) — depends on Issue 3
Issue 10 (config propagation) — depends on DD013 Issues 1, 9
Issue 11 (edge cases) — independent
Issue 12 (NMJ conductance audit) — independent

Issues 13–15 (research) — independent
Issues 16–18 (documentation) — independent
```
