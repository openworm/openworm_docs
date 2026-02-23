# DD002 Draft GitHub Issues

**Epic:** DD002 — Muscle Model Architecture and Calcium-Force Coupling

**Generated from:** [DD002: Muscle Model Architecture](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/)

**Methodology:** [DD015 §2.2 — DD Issue Generator](https://docs.openworm.org/design_documents/DD015_AI_Contributor_Model/#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 18 issues (ai-workable: 13 / human-expert: 5 | L1: 9, L2: 6, L3: 3)

**Note:** DD002's `GenericMuscleCell` template and `sibernetic_c302.py` coupling script are already implemented. These issues cover missing validation scripts, output pipeline, bug fixes, documentation, and research for future muscle-type differentiation.

---

## Phase 1: Validation Scripts

Target: Create the two scripts listed as `[TO BE CREATED]` in DD002, plus unit tests and parameter auditing.

---

### Issue 1: Create `scripts/plot_muscle_activation.py`

- **Title:** `[DD002] Create plot_muscle_activation.py — muscle activation visualization`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, matplotlib
- **DD Section to Read:** [DD002 — How to Build & Test](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#how-to-build-test) (Step 4) and [DD002 — How to Visualize](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#how-to-visualize)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/plot_muscle_activation.py` (new)
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
- **Sponsor Summary Hint:** This script turns raw simulation numbers into pictures of muscle activity. Each of the worm's 95 body wall muscles contracts when calcium flows in — this script shows you which muscles are contracting, when, and how strongly. It's like watching an MRI of muscle activity: a heatmap where red means "contracting" and blue means "relaxed." DD002 lists this script as needed but never created.

---

### Issue 2: Create `scripts/validate_muscle_calcium.py`

- **Title:** `[DD002] Create validate_muscle_calcium.py — calcium dynamics and activation range checker`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, numpy
- **DD Section to Read:** [DD002 — How to Build & Test](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#how-to-build-test) (Step 5) and [DD002 — Green Light Criteria](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#green-light-criteria)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/validate_muscle_calcium.py` (new)
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
- **Sponsor Summary Hint:** The muscle model converts electrical signals into calcium, and calcium into contraction force. This script is a health check — it verifies the calcium dynamics look physically realistic: are contractions in the right range? Does calcium decay at the right speed (~12 ms)? Are voltages staying in biologically plausible bounds? It's listed as a DD002 deliverable but was never created.

---

### Issue 3: Create unit tests for GenericMuscleCell NeuroML template

- **Title:** `[DD002] Create unit tests for GenericMuscleCell NeuroML template validation`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD002 — Quality Criteria](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#quality-criteria) (criteria 3-5) and [DD002 — Implementation References — Muscle Cell Template](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#muscle-cell-template)
- **Depends On:** None
- **Files to Modify:**
    - `tests/test_muscle_cell.py` (new)
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
- **Sponsor Summary Hint:** Unit tests that verify the muscle cell "recipe" is correct. Each muscle cell has 4 ion channels (leak, two potassium, one calcium) with specific conductance densities tuned to produce slow, sustained contractions rather than sharp spikes. These tests check that the recipe matches the Boyle & Cohen 2008 paper — like verifying a recipe's ingredient list before cooking.

---

### Issue 4: Audit muscle conductance densities against Boyle & Cohen 2008

- **Title:** `[DD002] Audit muscle conductance densities in c302 code against Boyle & Cohen 2008 and DD002 spec`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD002 — Technical Approach — Muscle Cells](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#muscle-cells-use-the-same-hodgkin-huxley-framework-as-neurons) and [Boyle & Cohen 2008](https://doi.org/10.1016/j.biosystems.2008.05.025)
- **Depends On:** None
- **Files to Modify:**
    - None (audit task — output is a summary posted on the issue)
- **Test Commands:**
    - N/A (audit task)
- **Acceptance Criteria:**
    - [ ] For each of the 4 channels (leak, K_slow, K_fast, Ca_boyle), find the conductance value in `c302_Muscles.py`
    - [ ] Compare against DD002 spec values and Boyle & Cohen 2008 Table 1
    - [ ] Document: file path, line number, variable name, actual value, expected value
    - [ ] Check calcium dynamics parameters: rho (0.000238), tau_Ca (11.5943 ms)
    - [ ] Check activation formula: `min(1.0, [Ca²⁺]ᵢ / 4e-7)`
    - [ ] Check max_muscle_force = 4000 in `sibernetic_c302.py`
    - [ ] Post findings as issue comment with comparison table
    - [ ] If discrepancies found, file follow-up issues for fixes
- **Sponsor Summary Hint:** A parameter audit — checking that the numbers in the code match the numbers in the scientific paper. Muscle channels have very specific conductance values from Boyle & Cohen (2008). If these drifted during development (a common issue in long-running projects), the simulation's muscle behavior could be subtly wrong. This audit catches silent parameter drift.

---

## Phase 2: Output Pipeline & Integration

Target: OME-Zarr export, config validation, and integration testing for DD002's interfaces with DD001 and DD003.

---

### Issue 5: Implement OME-Zarr export for muscle activation and calcium time series

- **Title:** `[DD002] Implement OME-Zarr export for muscle/activation/ and muscle/calcium/`
- **Labels:** `DD002`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, zarr
- **DD Section to Read:** [DD002 — Deliverables](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#deliverables) (OME-Zarr rows) and [DD014 — OME-Zarr Schema](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/)
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

### Issue 8: Validate NMJ connectivity mapping against Cook et al. 2019

- **Title:** `[DD002] Validate neuromuscular junction connectivity against Cook et al. 2019 connectome`
- **Labels:** `DD002`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroscience, connectomics
- **DD Section to Read:** [DD002 — Neural-to-Muscle Coupling](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#neural-to-muscle-coupling) and [DD020](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/) (cect API)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/validate_nmj_connectivity.py` (new)
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
- **Sponsor Summary Hint:** Motor neurons connect to muscles via neuromuscular junctions (NMJs) — the biological "wires" that tell muscles when to contract. Cook et al. (2019) mapped every NMJ connection in the real worm using electron microscopy. This issue compares our simulation's wiring against that ground truth. Missing connections mean some muscles might not contract when they should; extra connections mean false signals. This requires domain expertise to interpret which discrepancies matter biologically.

---

## Phase 3: Bug Fixes & Improvements

Target: Fix known issues and improve muscle model configurability.

---

### Issue 9: Fix MVL24 phantom muscle (95 vs 96 mismatch)

- **Title:** `[DD002] Fix MVL24 phantom muscle — set conductances to zero or remove`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD002 — Known Issues — Issue 3: MVL24](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#issue-3-mvl24-muscle-does-not-exist)
- **Depends On:** Issue 3 (unit tests — to verify fix doesn't break anything)
- **Files to Modify:**
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
    - [ ] NeuroML validation passes (`jnml -validate`)
    - [ ] Simulation runs without error after fix
    - [ ] Existing unit tests still pass
    - [ ] If MVL24 is removed (preferred), update any hardcoded references to 96 muscles
    - [ ] If MVL24 is zeroed (fallback), add comment explaining why
- **Sponsor Summary Hint:** The real worm has 95 body wall muscles, but the simulation has 96 — an extra phantom muscle called MVL24 that doesn't exist in nature. It was added for code symmetry (4 quadrants × 24 rows = 96, but the real worm is missing one). This is a minor biological inaccuracy that should be fixed to prevent confusion and ensure muscle-count-dependent analyses are correct.

---

### Issue 10: Propagate muscle config parameters from openworm.yml to sibernetic_c302.py

- **Title:** `[DD002] Propagate muscle.max_muscle_force and muscle.max_ca from openworm.yml to coupling script`
- **Labels:** `DD002`, `ai-workable`, `L2`
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python
- **DD Section to Read:** [DD002 — Integration Contract — Configuration](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#configuration) and [DD013 §1](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#1-simulation-configuration-system-openwormyml)
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

## Phase 4: Research & Advanced Features

Target: Investigate muscle-type differentiation, multi-compartment modeling, and alternative mechanical models for future phases.

---

### Issue 13: Survey CeNGEN transcriptomic data for muscle-type-specific channel expression

- **Title:** `[DD002] Survey CeNGEN data for muscle-type-specific ion channel expression profiles`
- **Labels:** `DD002`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, bioinformatics, neuroscience
- **DD Section to Read:** [DD002 — Migration Path — Muscle-Type Diversity](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#if-muscle-type-diversity-is-required-phase-3) and [DD005](https://docs.openworm.org/design_documents/DD005_Cell_Type_Differentiation_Strategy/) (Cell-Type Specialization)
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
- **Sponsor Summary Hint:** Each muscle is currently modeled as a single point — the voltage is the same everywhere in the cell. But real muscles are spindle-shaped, ~60 µm long. If one end of the muscle is stimulated by a motor neuron, does the other end "know"? This prototype tests whether voltage spreads uniformly (single-compartment is fine, saving enormous computation) or attenuates (we'd need multi-compartment, at 4-8x the computational cost per muscle). This is the kind of fundamental modeling question that determines architecture.

---

### Issue 15: Evaluate Hill-type crossbridge mechanics feasibility

- **Title:** `[DD002] Evaluate Hill-type crossbridge mechanics for specialized muscles (egg-laying, defecation)`
- **Labels:** `DD002`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** physics, biomechanics, neuroscience
- **DD Section to Read:** [DD002 — Alternatives Considered — Hill-Type Muscle Model](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#1-hill-type-muscle-model-with-crossbridge-dynamics) and [DD002 — Migration Path](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#migration-path)
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
    - [ ] Propose LEMS ComponentType extension approach (per DD002 Migration Path)
    - [ ] Post feasibility report with go/no-go recommendation per muscle type
    - [ ] If Hill-type is warranted for any muscle type, draft DD amendment for Phase 3
- **Sponsor Summary Hint:** DD002's muscle model uses a simple linear formula: more calcium = more force. This works for locomotion (Boyle & Cohen 2008 showed body wall muscles are "simple actuators"). But what about specialized muscles — the vulval muscles that lay eggs, the anal depressor muscle that contracts during defecation, the pharyngeal muscles that pump food? These might need a richer mechanical model (Hill-type) with actin-myosin crossbridge dynamics. This research determines which muscles, if any, need upgrading.

---

## Phase 5: Documentation & Maintenance

Target: Comprehensive documentation enabling contributors to understand and modify the muscle model.

---

### Issue 16: Create muscle model contributor guide

- **Title:** `[DD002] Create muscle model contributor guide for c302 developers`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD002 — Quality Criteria](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#quality-criteria), [DD002 — Testing Procedure](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#testing-procedure), and [DD002 — Boundaries](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#boundaries-explicitly-out-of-scope)
- **Depends On:** None
- **Files to Modify:**
    - `docs/muscle_model_guide.md` (new — in c302 repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Overview: what the muscle model does, what it produces, who uses its output
    - [ ] File map: `c302_Muscles.py` (templates), `muscles.csv` (cell list), `sibernetic_c302.py` (coupling)
    - [ ] Contributor workflow: generate muscle network → validate NeuroML → run simulation → check outputs
    - [ ] Quality criteria: 5 rules from DD002 (calcium interface, movement validation, NeuroML 2, units, muscle-neuron distinction)
    - [ ] Common mistakes: copying neuron parameters to muscles, changing calcium variable name without updating `sibernetic_c302.py`
    - [ ] References to DD002 for specification, DD003 for body physics coupling, DD014 for visualization
    - [ ] Aimed at L2 contributors (familiar with Python but new to muscle physiology)
- **Sponsor Summary Hint:** A "getting started" guide for anyone wanting to improve the muscle model. Explains which files to edit, what tests to run, and what mistakes to avoid (like accidentally copying neuron parameters to muscles — which would make muscles twitch like neurons instead of contracting smoothly). DD002 is the specification; this is the practical "how to contribute" companion.

---

### Issue 17: Document NMJ connectivity and muscle quadrant mapping

- **Title:** `[DD002] Document muscle quadrant layout and NMJ connectivity diagram`
- **Labels:** `DD002`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD002 — Context & Background](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#context-background), [DD002 — Muscle List](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#muscle-list-95-cells), and [DD002 — Neural-to-Muscle Coupling](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#neural-to-muscle-coupling)
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
    - [ ] Cross-references to DD003 (elastic particle mapping in Sibernetic) and WormAtlas
    - [ ] Visual enough for L1 contributors to understand muscle anatomy at a glance
- **Sponsor Summary Hint:** The worm's 95 body wall muscles wrap around the body in 4 strips (quadrants). During forward crawling, dorsal and ventral muscles activate in alternating waves — like a crowd doing "the wave" in a stadium. This document maps out which muscles are where, which motor neurons control them, and how that creates coordinated movement. It's the anatomical atlas for anyone working on the muscle system.

---

### Issue 18: Document sibernetic_c302.py coupling script architecture

- **Title:** `[DD002] Document sibernetic_c302.py coupling script: data flow, timing, and variable mapping`
- **Labels:** `DD002`, `ai-workable`, `L2`
- **Target Repo:** `openworm/sibernetic`
- **Required Capabilities:** python, docs
- **DD Section to Read:** [DD002 — Coupling to Sibernetic](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#coupling-to-sibernetic) and [DD002 — Coupling Bridge Ownership](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/#coupling-bridge-ownership)
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
    - [ ] Change impact analysis: what breaks if you change each parameter (from DD002 Coupling Bridge Ownership section)
    - [ ] Coordination notes: who must agree before changing the coupling interface
    - [ ] Cross-references to DD002 (muscle model), DD003 (body physics), DD013 (simulation stack)
- **Sponsor Summary Hint:** The coupling script is the bridge between two very different worlds: the electrical simulation (NEURON, millisecond timescale, voltages in millivolts) and the mechanical simulation (Sibernetic, microsecond timescale, forces in arbitrary units). This document explains exactly how data flows across that bridge — what gets read, what gets computed, what gets written, and when. It's the most critical integration point in the entire worm simulation, and currently the least documented.

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

| Phase | Issues | Target |
|-------|--------|--------|
| **1: Validation Scripts** | 1–4 | Create missing scripts, unit tests, parameter audit |
| **2: Output Pipeline & Integration** | 5–8 | OME-Zarr export, config validation, interface testing |
| **3: Bug Fixes & Improvements** | 9–12 | MVL24 fix, config propagation, edge cases, NMJ audit |
| **4: Research & Advanced** | 13–15 | Transcriptomics survey, multi-compartment, Hill-type |
| **5: Documentation** | 16–18 | Contributor guide, anatomy mapping, coupling architecture |

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
| DD003 Draft Issues (Issue 19) | Issue 17 (complementary: c302-side NMJ mapping vs. Sibernetic-side particle mapping) |

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
