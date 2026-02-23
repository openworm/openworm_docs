# DD001 Draft GitHub Issues

**Epic:** DD001 — Neural Circuit Architecture and Multi-Level Framework

**Generated from:** [DD001: Neural Circuit Architecture](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/)

**Methodology:** [DD015 §2.2 — DD Issue Generator](https://docs.openworm.org/design_documents/DD015_AI_Contributor_Model/#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 28 issues (ai-workable: 17 / human-expert: 11 | L1: 9, L2: 12, L3: 7)

---

## Phase 1: Validation Infrastructure

Target: Scripts and baselines needed to measure neural circuit quality and detect regressions.

---

### Issue 1: Create `scripts/extract_trajectory.py`

- **Title:** `[DD001] Create extract_trajectory.py — WCON trajectory from c302/NEURON output`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — How to Build & Test](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#how-to-build-test) (Step 3) and [DD001 — Deliverables](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#deliverables) (WCON row)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/extract_trajectory.py` (new)
    - `tests/test_extract_trajectory.py` (new)
- **Test Commands:**
    - `jnml LEMS_c302_C1_Muscles.xml -nogui`
    - `python3 scripts/extract_trajectory.py --input . --output trajectory.wcon`
- **Acceptance Criteria:**
    - [ ] Reads c302/NEURON simulation output (calcium `.dat` files for 96 muscle cells)
    - [ ] Computes per-muscle activation from calcium concentration time series
    - [ ] Maps 96 muscle activations to body posture using the 4-quadrant muscle geometry (MDR, MVR, MVL, MDL)
    - [ ] Exports a 49-point worm centerline trajectory in WCON 1.0 format
    - [ ] Output validates against WCON JSON schema
    - [ ] Compatible with `open-worm-analysis-toolbox` for DD010 Tier 3 validation
    - [ ] Unit tests with synthetic muscle calcium data
- **Sponsor Summary Hint:** The neural circuit simulation produces calcium signals for 96 muscle cells. This script converts those signals into a worm body trajectory — essentially asking "if these muscles contracted this way, how would the worm move?" The output (WCON format) can be compared against real worm videos to validate the simulation.

---

### Issue 2: Create `scripts/check_regression.py`

- **Title:** `[DD001] Create check_regression.py — validation score regression detector`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD001 — How to Build & Test](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#how-to-build-test) (Step 5) and [DD001 — Quality Criteria](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#quality-criteria) (criterion 5)
- **Depends On:** None
- **Files to Modify:**
    - `scripts/check_regression.py` (new)
    - `tests/test_check_regression.py` (new)
    - `baseline/validation_baseline.json` (new — baseline scores)
- **Test Commands:**
    - `python3 scripts/check_regression.py validation_report.json baseline/validation_baseline.json`
    - `pytest tests/test_check_regression.py`
- **Acceptance Criteria:**
    - [ ] Reads a validation report JSON (output from `compare_kinematics.py`) and a baseline JSON
    - [ ] Compares 5 key metrics: speed, wavelength, frequency, amplitude, crawling/swimming classification
    - [ ] Flags REGRESSION if any metric degrades >15% from baseline
    - [ ] Prints per-metric comparison table (current vs. baseline vs. threshold)
    - [ ] Returns exit code 0 if no regression, non-zero if regression detected
    - [ ] Unit tests with synthetic reports (passing, regressing, improving)
- **Sponsor Summary Hint:** A guard-rail script that prevents accidental damage to the simulation's accuracy. Before any code change lands, this checks: "does the virtual worm still move like a real worm?" If the answer is "worse than before," the change is flagged. Like a quality control checkpoint on a production line.

---

### Issue 3: Create NeuroML validation CI gate

- **Title:** `[DD001] Create GitHub Actions CI gate for jnml -validate on all NeuroML files`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** ci-cd
- **DD Section to Read:** [DD001 — Quality Criteria](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#quality-criteria) (criterion 1: NeuroML compliance) and [DD001 — CI gate](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#quick-action-reference)
- **Depends On:** None
- **Files to Modify:**
    - `.github/workflows/validate.yml` (new or modify existing)
- **Test Commands:**
    - Push to branch and verify CI runs NeuroML validation
- **Acceptance Criteria:**
    - [ ] CI runs `jnml -validate` on all `.nml` and `.xml` files in `channel_models/`, `synapse_models/`, and `examples/generated/`
    - [ ] Fails the PR check if any file is invalid NeuroML 2
    - [ ] Installs pyNeuroML/jnml in CI (pip install pyNeuroML)
    - [ ] Completes in <5 minutes
    - [ ] Runs on `pull_request` to `main` and `dev*` branches
- **Sponsor Summary Hint:** NeuroML is the standard file format for neural models — like a grammar for describing neurons and synapses. This CI gate automatically checks that every code change produces valid NeuroML files. If someone breaks the grammar (missing units, wrong element names), the PR is blocked before human review.

---

### Issue 4: Generate Schafer lab kinematic baseline from WCON data

- **Title:** `[DD001] Generate kinematic baseline metrics from Schafer lab N2 WCON data`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, worm-biology
- **DD Section to Read:** [DD001 — Goal & Success Criteria](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#goal-success-criteria) (±15% of Schafer lab) and [DD010](https://docs.openworm.org/design_documents/DD010_Validation_Framework/) (Tier 3)
- **Depends On:** None
- **Files to Modify:**
    - `baseline/schafer_baseline_metrics.json` (new)
    - `scripts/generate_baseline.py` (new)
- **Test Commands:**
    - `python3 scripts/generate_baseline.py --input schafer_n2_data/ --output baseline/schafer_baseline_metrics.json`
- **Acceptance Criteria:**
    - [ ] Downloads or locates Schafer lab N2 wild-type WCON data (from open-worm-analysis-toolbox or Zenodo)
    - [ ] Computes 5 key metrics: forward speed, body wavelength, undulation frequency, body amplitude, crawling/swimming gait classification
    - [ ] Saves metrics with mean ± std to JSON file
    - [ ] Documents data provenance (which dataset, which animals, which conditions)
    - [ ] ±15% thresholds computed and stored alongside baseline values
    - [ ] Baseline committed to repo as reference for `check_regression.py`
- **Sponsor Summary Hint:** To know if our virtual worm moves correctly, we need ground truth from real worms. The Schafer lab at Cambridge recorded thousands of wild-type N2 worms with precise tracking. This issue extracts the key movement metrics from that data — the "answer key" that our simulation must match within 15%.

---

### Issue 5: Audit c302 simulation output files and document format

- **Title:** `[DD001] Audit and document c302/NEURON simulation output file formats`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Integration Contract — Outputs](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#inputs--outputs) and [DD001 — Coupling Bridge Ownership](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#coupling-bridge-ownership)
- **Depends On:** None
- **Files to Modify:**
    - `docs/output_formats.md` (new — in c302 repo)
- **Test Commands:**
    - N/A (documentation/audit task)
- **Acceptance Criteria:**
    - [ ] Run a Level C1 simulation and catalog every output file produced
    - [ ] Document: file name pattern, format (tab-separated, CSV, etc.), column headers, units
    - [ ] Document: `*_calcium.dat` format (which columns = which muscles/neurons)
    - [ ] Document: `*_voltages.dat` format
    - [ ] Document: which files `sibernetic_c302.py` reads (the coupling bridge)
    - [ ] Identify any undocumented output files
    - [ ] Post findings as `docs/output_formats.md`
- **Sponsor Summary Hint:** The neural simulation produces dozens of output files containing voltage traces, calcium concentrations, and synaptic currents for 302 neurons and 96 muscles. But nobody has documented what's in each file. This audit maps every output file so downstream tools (body physics coupling, validation, visualization) know exactly what to read and how.

---

## Phase 2: Data Pipeline & Integration

Target: Connectome data loading, OME-Zarr export, and coupling interface scripts.

---

### Issue 6: Implement OME-Zarr export for neural voltage and calcium data

- **Title:** `[DD001] Implement OME-Zarr export for neural/voltage, neural/calcium, neural/positions`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD001 — Deliverables](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#deliverables) (OME-Zarr rows) and [DD014](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/) (OME-Zarr schema)
- **Depends On:** Issue 5 (output format documentation)
- **Files to Modify:**
    - `scripts/export_zarr.py` (new)
- **Test Commands:**
    - `python3 scripts/export_zarr.py --input . --output neural.zarr`
    - `python3 -c "import zarr; z = zarr.open('neural.zarr'); print(z['neural/voltage'].shape, z['neural/calcium'].shape, z['neural/positions'].shape)"`
- **Acceptance Criteria:**
    - [ ] Reads c302/NEURON `.dat` output files (voltage and calcium time series)
    - [ ] Exports `neural/voltage/`: shape (n_timesteps, 302), dtype float32, units mV
    - [ ] Exports `neural/calcium/`: shape (n_timesteps, 302), dtype float32, units mol/cm³
    - [ ] Exports `neural/positions/`: shape (302, 3), dtype float32, units µm (static neuron coordinates)
    - [ ] Neuron positions sourced from WormAtlas or Long et al. 2009 3D atlas
    - [ ] Zarr store readable by DD014 viewer
    - [ ] Includes OME-Zarr metadata (axes labels, neuron name mapping)
- **Sponsor Summary Hint:** OME-Zarr is the universal data bus connecting simulation to visualization. This script converts c302's raw text output into a structured Zarr store that the DD014 3D viewer can read. You'll see 302 neurons at their real 3D positions in the worm, colored by how active they are — like a real-time fMRI of a virtual worm brain.

---

### Issue 7: Verify connectome dataset switching via `openworm.yml`

- **Title:** `[DD001] Verify connectome dataset switching: Cook2019, Witvliet2021, Varshney2011`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Integration Contract — Configuration](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#configuration) (`neural.connectome_dataset`) and [DD020](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/) (ConnectomeToolbox)
- **Depends On:** DD013 Issue 9 (config loading)
- **Files to Modify:**
    - `c302/` network generation code (verify dataset parameterization)
    - `tests/test_connectome_switching.py` (new)
- **Test Commands:**
    - `python3 -c "from c302 import generate; generate('C1', 'FW', connectome='Cook2019')"`
    - `python3 -c "from c302 import generate; generate('C1', 'FW', connectome='Witvliet2021')"`
    - `pytest tests/test_connectome_switching.py`
- **Acceptance Criteria:**
    - [ ] c302 network generation accepts a `connectome_dataset` parameter
    - [ ] Cook2019 produces 302 neurons with Cook et al. synapse counts
    - [ ] Witvliet2021 produces 302 neurons with Witvliet developmental synapse counts
    - [ ] Varshney2011 produces 302 neurons with original Varshney synapse counts
    - [ ] `openworm.yml` `neural.connectome_dataset` maps to c302's connectome parameter
    - [ ] Each dataset produces valid NeuroML (`jnml -validate` passes)
    - [ ] Test verifies synapse count differences between datasets
- **Sponsor Summary Hint:** The worm's wiring diagram (connectome) has been mapped by multiple research groups with slightly different methods and results. Cook2019 is the most complete, but Witvliet2021 shows how connections change during development. This issue makes it easy to switch between datasets via a config option — like swapping circuit boards to see how the worm's brain differs across measurements.

---

### Issue 8: Verify all c302 levels generate valid networks

- **Title:** `[DD001] Verify Levels A, B, C, C1, C2, D all generate valid NeuroML networks`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Architecture Levels](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#architecture-levels)
- **Depends On:** None
- **Files to Modify:**
    - `tests/test_all_levels.py` (new)
- **Test Commands:**
    - `pytest tests/test_all_levels.py -v`
- **Acceptance Criteria:**
    - [ ] Test generates a network at each level (A, B, C, C1, C2, D) with the FW reference
    - [ ] Each generated network passes `jnml -validate`
    - [ ] Each network contains 302 neurons (or expected subset)
    - [ ] Level A uses IafCell, Level B uses IafActivityCell, Level C/C1 uses GenericCell, Level D uses multicompartment
    - [ ] Level C1 uses graded synapses, Level C uses event-driven synapses
    - [ ] Test documents which levels currently fail (if any) with clear error messages
- **Sponsor Summary Hint:** c302 offers 6 levels of biological detail — from simple (Level A) to complex (Level D). Like zoom levels on a microscope, each shows more detail but costs more compute. This test verifies all levels still work, catching bitrot in less-used levels before someone needs them.

---

### Issue 9: Document `sibernetic_c302.py` coupling bridge

- **Title:** `[DD001] Document sibernetic_c302.py coupling bridge interface (DD001→DD002→DD003)`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, docs
- **DD Section to Read:** [DD001 — Coupling Bridge Ownership](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#coupling-bridge-ownership) and [DD001 — Integration Contract — Coupling Dependencies](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#coupling-dependencies)
- **Depends On:** Issue 5 (output format audit)
- **Files to Modify:**
    - `docs/coupling_bridge.md` (new — in Sibernetic repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Documents the full data flow: c302 calcium output → `sibernetic_c302.py` → Sibernetic muscle activation
    - [ ] Documents: which c302 output files are read, column mapping, units
    - [ ] Documents: how calcium values are converted to Sibernetic muscle activation coefficients
    - [ ] Documents: timing — when does coupling happen, how often, what's the lag
    - [ ] Documents: the 96-muscle mapping between c302 muscle names and Sibernetic particle indices
    - [ ] Documents: what breaks if either side changes format (the coupling contract)
    - [ ] Identifies fragile assumptions or hardcoded values that should be parameterized
- **Sponsor Summary Hint:** The coupling bridge is the critical handoff between brain and body — c302 computes which muscles the brain wants to contract, and `sibernetic_c302.py` translates that into physical forces on the body. This is the most fragile interface in the entire simulation. Documenting it prevents accidental breakage when either the neural or body physics code changes.

---

## Phase 3: Extended Ion Channel Library

Target: Expand from 4 generic channels to 14+ neuron-class-specific channels, leveraging BAAIWorm NMODL files.

---

### Issue 10: Survey BAAIWorm NMODL channel files for reuse

- **Title:** `[DD001] Survey BAAIWorm repo NMODL channel files for conversion to NeuroML`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (code reuse plan)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a summary comment on the issue)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Clone BAAIWorm repo (`github.com/Jessie940611/BAAIWorm`)
    - [ ] Locate and catalog all NMODL channel files in `eworm/` directory
    - [ ] For each of the 14 channels in DD001's target library table: find the corresponding NMODL file, note filename and path
    - [ ] Assess: does pyNeuroML's NMODL→NeuroML converter handle these files? Test on 2-3 channels
    - [ ] Document: which channels convert cleanly, which need manual intervention
    - [ ] Document: license compatibility (Apache 2.0 → OpenWorm MIT)
    - [ ] Estimate: total effort for full library conversion
    - [ ] Post findings as issue comment
- **Sponsor Summary Hint:** Zhao et al.'s BAAIWorm contains 14 ion channel models in NMODL format (a NEURON-specific language). We need them in NeuroML format (the cross-simulator standard). This survey checks whether automatic conversion tools work, or if we need manual translation. If conversion works, it saves weeks of channel modeling effort.

---

### Issue 11: Convert BAAIWorm EGL-19 (Cav1 L-type) channel to NeuroML

- **Title:** `[DD001] Convert BAAIWorm EGL-19 (Cav1 L-type Ca²⁺) channel from NMODL to NeuroML`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (EGL-19 row, HIGH priority)
- **Depends On:** Issue 10 (survey)
- **Files to Modify:**
    - `channel_models/egl19_cav1.channel.nml` (new)
    - `tests/test_egl19_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/egl19_cav1.channel.nml`
    - `pytest tests/test_egl19_channel.py`
- **Acceptance Criteria:**
    - [ ] EGL-19 channel defined in valid NeuroML 2 XML
    - [ ] Passes `jnml -validate`
    - [ ] I-V curve matches BAAIWorm NMODL version within ±5% (test with voltage clamp protocol)
    - [ ] Activation and inactivation kinetics (V_half, slope, tau) documented with literature source
    - [ ] Can be inserted into a GenericCell definition alongside existing channels
    - [ ] Unit test compares NeuroML channel output against NMODL reference
- **Sponsor Summary Hint:** EGL-19 is the primary L-type calcium channel in *C. elegans* — it's critical for muscle contraction and many neuronal functions. Mutations cause egg-laying defects (hence the name: egg-laying defective). Converting it from NMODL to NeuroML gives our model a biologically accurate calcium channel instead of the generic placeholder currently used.

---

### Issue 12: Convert BAAIWorm SLO-1 (BK Ca²⁺-activated K⁺) channel to NeuroML

- **Title:** `[DD001] Convert BAAIWorm SLO-1 (BK Ca²⁺-activated K⁺) channel from NMODL to NeuroML`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (SLO-1 row, HIGH priority)
- **Depends On:** Issue 10 (survey)
- **Files to Modify:**
    - `channel_models/slo1_bk.channel.nml` (new)
    - `tests/test_slo1_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/slo1_bk.channel.nml`
    - `pytest tests/test_slo1_channel.py`
- **Acceptance Criteria:**
    - [ ] SLO-1 BK channel defined in valid NeuroML 2 XML
    - [ ] Calcium-dependent gating correctly modeled (conductance depends on both V and [Ca²⁺]ᵢ)
    - [ ] I-V curve matches BAAIWorm NMODL version within ±5%
    - [ ] Activation kinetics documented with literature source
    - [ ] Unit test compares NeuroML channel output against NMODL reference
- **Sponsor Summary Hint:** SLO-1 is a "big potassium" (BK) channel that opens when it senses both voltage AND calcium inside the cell. It's the molecular brake that prevents neurons from getting too excited. SLO-1 mutant worms are sluggish and uncoordinated. This channel is critical for realistic repolarization kinetics.

---

### Issue 13: Convert remaining HIGH-priority channels (KVS-1, EGL-36) to NeuroML

- **Title:** `[DD001] Convert BAAIWorm KVS-1 (Kv Shaker) and EGL-36 (ERG) channels to NeuroML`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (KVS-1 and EGL-36 rows, HIGH priority)
- **Depends On:** Issue 10 (survey)
- **Files to Modify:**
    - `channel_models/kvs1_shaker.channel.nml` (new)
    - `channel_models/egl36_erg.channel.nml` (new)
    - `tests/test_kvs1_channel.py` (new)
    - `tests/test_egl36_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/kvs1_shaker.channel.nml`
    - `jnml -validate channel_models/egl36_erg.channel.nml`
    - `pytest tests/test_kvs1_channel.py tests/test_egl36_channel.py`
- **Acceptance Criteria:**
    - [ ] Both channels defined in valid NeuroML 2 XML
    - [ ] KVS-1: Shaker-type voltage-gated K⁺ channel with fast activation kinetics
    - [ ] EGL-36: ERG-type K⁺ channel with characteristic slow inactivation recovery
    - [ ] I-V curves match BAAIWorm NMODL versions within ±5%
    - [ ] All kinetics documented with literature sources
    - [ ] Unit tests compare NeuroML outputs against NMODL references
- **Sponsor Summary Hint:** KVS-1 (Shaker) and EGL-36 (ERG) are potassium channels that shape the electrical personality of neurons. KVS-1 fires rapidly, setting the speed limit on neural responses. EGL-36 recovers slowly from inactivation, creating a refractory period. Both are HIGH priority because they strongly influence neuron firing patterns.

---

### Issue 14: Convert MEDIUM-priority channels (batch) to NeuroML

- **Title:** `[DD001] Convert BAAIWorm MEDIUM-priority channels (CCA-1, EGL-2, KQT-3, SLO-2, KCNL, IRK, NCA) to NeuroML`
- **Labels:** `DD001`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (MEDIUM priority rows)
- **Depends On:** Issues 11-13 (HIGH priority channels establish the conversion workflow)
- **Files to Modify:**
    - `channel_models/cca1_cav3.channel.nml` (new)
    - `channel_models/egl2_eag.channel.nml` (new)
    - `channel_models/kqt3_kcnq.channel.nml` (new)
    - `channel_models/slo2_sk.channel.nml` (new)
    - `channel_models/kcnl2_sk.channel.nml` (new)
    - `channel_models/irk_kir.channel.nml` (new)
    - `channel_models/nca_na.channel.nml` (new)
    - `tests/test_medium_channels.py` (new)
- **Test Commands:**
    - `for f in channel_models/*.nml; do jnml -validate $f; done`
    - `pytest tests/test_medium_channels.py`
- **Acceptance Criteria:**
    - [ ] All 7 MEDIUM-priority channels defined in valid NeuroML 2 XML
    - [ ] Each passes `jnml -validate`
    - [ ] I-V curves match BAAIWorm NMODL versions within ±5%
    - [ ] All kinetics documented with literature sources
    - [ ] Total channel library: 4 existing + 4 HIGH + 7 MEDIUM = 15 channels
- **Sponsor Summary Hint:** This batch converts the remaining 7 ion channel types — including T-type calcium (CCA-1), EAG potassium (EGL-2), inward rectifier (IRK), and sodium leak (NCA). Together with the existing 4 and the HIGH-priority 4, this gives us the full 15-channel library needed to differentiate all 128 neuron classes. Each channel type gives neurons a different "personality" — fast vs. slow, excitable vs. quiet, rhythmic vs. tonic.

---

### Issue 15: Create channel library test suite with voltage-clamp protocols

- **Title:** `[DD001] Create comprehensive channel library test suite with standard voltage-clamp protocols`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) and [DD001 — Quality Criteria](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#quality-criteria) (criterion 3: biophysical units)
- **Depends On:** Issues 11-14 (channel conversions)
- **Files to Modify:**
    - `tests/test_channel_library.py` (new)
    - `tests/protocols/` (new — voltage clamp protocol files)
- **Test Commands:**
    - `pytest tests/test_channel_library.py -v`
- **Acceptance Criteria:**
    - [ ] Standard voltage-clamp protocol: step from -80mV to -60,-40,-20,0,+20,+40 mV
    - [ ] For each channel: measure peak current, steady-state current, activation time constant
    - [ ] Compare against published electrophysiology data where available
    - [ ] Generate I-V curve plots for each channel (saved as PNG test artifacts)
    - [ ] Verify units are correct (conductance in nS, voltage in mV, time in ms)
    - [ ] Detect common errors: reversed polarity, wrong magnitude, unrealistic kinetics
    - [ ] All 15 channels pass the test suite
- **Sponsor Summary Hint:** A voltage-clamp test is the standard way to characterize an ion channel — you hold the cell at a fixed voltage and measure how much current flows. This test suite applies the same protocol to every channel in our library and checks the results against published measurements. Like calibrating 15 different instruments against their spec sheets.

---

## Phase 4: Synaptic Optimization

Target: Per-synapse conductance optimization using differentiable simulation and neurotransmitter identity constraints.

---

### Issue 16: Implement neurotransmitter identity constraints for synapse polarity

- **Title:** `[DD001] Implement neurotransmitter identity constraints from Wang et al. 2024 for synapse polarity`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, neuroscience
- **DD Section to Read:** [DD001 — Synaptic Weight and Polarity Optimization](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#synaptic-weight-and-polarity-optimization) (neurotransmitter identity constraints)
- **Depends On:** None
- **Files to Modify:**
    - `c302/data/neurotransmitter_identities.csv` (new)
    - `c302/synapse_constraints.py` (new)
- **Test Commands:**
    - `python3 -c "from c302 import synapse_constraints; sc = synapse_constraints.load(); print(sc.get_polarity('AVAL', 'AVAR'))"`
    - `pytest tests/test_synapse_constraints.py`
- **Acceptance Criteria:**
    - [ ] Load Wang et al. 2024 neurotransmitter classifications for all connectome neurons
    - [ ] Map neurotransmitter type to synapse polarity: glutamatergic → excitatory, GABAergic → inhibitory, cholinergic → excitatory (with exceptions)
    - [ ] Provide a Python API: `get_polarity(pre, post)` returns +1 (excitatory) or -1 (inhibitory)
    - [ ] Flag synapses where polarity is ambiguous or unknown
    - [ ] Data stored in version-controlled CSV with provenance
    - [ ] Unit tests verify known polarity assignments (e.g., DD/VD GABAergic → inhibitory)
- **Sponsor Summary Hint:** When the brain optimizer fits synapse strengths to match real brain data, it shouldn't be free to make up whether a synapse is excitatory or inhibitory. Wang et al. 2024 experimentally determined which neurotransmitter each neuron uses — glutamate, GABA, or acetylcholine. This constrains the optimizer to respect biology: GABAergic neurons MUST make inhibitory synapses. Like telling the AI "you can adjust the volume, but not whether the speaker plays music or noise."

---

### Issue 17: Add `neural.synapse_optimization` config toggle

- **Title:** `[DD001] Add neural.synapse_optimization config toggle to openworm.yml`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302` + `openworm/OpenWorm`
- **Required Capabilities:** python, yaml
- **DD Section to Read:** [DD001 — Synaptic Weight and Polarity Optimization](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#synaptic-weight-and-polarity-optimization) (Configuration section)
- **Depends On:** DD013 Issue 1 (openworm.yml schema)
- **Files to Modify:**
    - `openworm.yml` (add `neural.synapse_optimization: false`)
    - c302 network generation (read optimization flag)
- **Test Commands:**
    - `python3 -c "from c302 import generate; generate('C1', 'FW', synapse_optimization=False)"`
    - `python3 -c "from c302 import generate; generate('C1', 'FW', synapse_optimization=True)"`
- **Acceptance Criteria:**
    - [ ] `neural.synapse_optimization: false` → uses uniform g_syn = 0.09 nS (backward compatible)
    - [ ] `neural.synapse_optimization: true` → loads per-synapse fitted values from `data/optimized_weights.json`
    - [ ] Placeholder `optimized_weights.json` with uniform weights (actual optimization is a separate issue)
    - [ ] Config documented with DD cross-reference to DD017 (differentiable backend)
    - [ ] Both modes produce valid NeuroML
- **Sponsor Summary Hint:** Currently all synapses in the model have the same strength (0.09 nS) — like every connection in the brain being equally strong. In reality, some connections are powerful and some are whisper-quiet. This toggle switches between the simple uniform model and an optimized model where each synapse has its own fitted strength. The optimization itself is a separate task (requires DD017 differentiable backend).

---

### Issue 18: Implement Randi 2023 functional connectivity target matrix

- **Title:** `[DD001] Load Randi 2023 functional connectivity matrix as optimization target`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroscience
- **DD Section to Read:** [DD001 — Synaptic Weight and Polarity Optimization](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#synaptic-weight-and-polarity-optimization) (full 302-neuron optimization) and Reference 14 (Kato et al. 2015 PCA validation)
- **Depends On:** None
- **Files to Modify:**
    - `c302/data/randi2023_functional_connectivity.py` (new)
    - `tests/test_randi_data.py` (new)
- **Test Commands:**
    - `python3 -c "from c302.data import randi2023_functional_connectivity as rfc; m = rfc.load_correlation_matrix(); print(m.shape)"`
    - `pytest tests/test_randi_data.py`
- **Acceptance Criteria:**
    - [ ] Load Randi et al. 2023 calcium correlation matrix via `wormneuroatlas` package
    - [ ] Matrix shape: (N_neurons, N_neurons) where N = number of identified neurons in the dataset
    - [ ] Map neuron IDs from Randi nomenclature to c302 neuron names
    - [ ] Handle missing neurons gracefully (not all 302 are in the imaging data)
    - [ ] Provide utility: `compare_to_simulation(sim_calcium_matrix)` → Pearson correlation
    - [ ] Unit tests verify matrix is symmetric, diagonal is 1.0, shape is correct
- **Sponsor Summary Hint:** Randi et al. (2023) recorded the activity of nearly every neuron in the worm's brain simultaneously — a complete functional map of which neurons tend to fire together. This is the target our model must match. When we optimize synapse strengths, we're trying to reproduce this real-world pattern of correlated neural activity in our simulation.

---

## Phase 5: Level D Multicompartmental Development

Target: Multicompartmental neuron models for neurons where single-compartment approximation is insufficient.

---

### Issue 19: Convert BAAIWorm SWC morphologies to NeuroML for 5 representative neurons

- **Title:** `[DD001] Convert BAAIWorm SWC morphologies to NeuroML for AWC, AIY, AVA, RIM, VD5`
- **Labels:** `DD001`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, neuroanatomy
- **DD Section to Read:** [DD001 — Level D Multicompartmental](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#level-d-multicompartmental-cable-equation-models-expanded-roadmap) (Stage 1, step 2)
- **Depends On:** Issue 10 (BAAIWorm survey)
- **Files to Modify:**
    - `morphologies/AWC.cell.nml` (new)
    - `morphologies/AIY.cell.nml` (new)
    - `morphologies/AVA.cell.nml` (new)
    - `morphologies/RIM.cell.nml` (new)
    - `morphologies/VD5.cell.nml` (new)
- **Test Commands:**
    - `for f in morphologies/*.nml; do jnml -validate $f; done`
- **Acceptance Criteria:**
    - [ ] 5 multicompartmental NeuroML cell definitions with `<morphology>` elements
    - [ ] Segments < 2 µm length (adequate spatial resolution for cable equation)
    - [ ] Segment groups defined: soma, axon, dendrite (where applicable)
    - [ ] Source morphology documented: BAAIWorm SWC or Witvliet EM reconstruction
    - [ ] All pass `jnml -validate`
    - [ ] Can be loaded by NEURON simulator (via pyNeuroML export)
    - [ ] Soma diameter matches known values (WormAtlas)
- **Sponsor Summary Hint:** Most neurons in our model are treated as a single point — like a ping-pong ball. But some neurons (like RIA, AWC) have complex branching structures where signals propagate along neurites, creating spatial patterns of activity within a single cell. SWC is a standard format for neuron shapes from electron microscopy. This converts 5 key neuron shapes into NeuroML so we can simulate signal propagation along their branches.

---

### Issue 20: Build Level D proof-of-concept: AWC multicompartmental model

- **Title:** `[DD001] Build Level D proof-of-concept: AWC sensory neuron with multicompartmental morphology`
- **Labels:** `DD001`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Level D Multicompartmental](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#level-d-multicompartmental-cable-equation-models-expanded-roadmap) (Stage 1, steps 3-4) and Reference 16 (Nicoletti et al. 2019 AWCon model)
- **Depends On:** Issue 19 (AWC morphology), Issues 11-14 (extended channel library)
- **Files to Modify:**
    - `c302/c302_MultiComp_AWC.py` (new — or extend existing Level D template)
    - `tests/test_awc_multicomp.py` (new)
- **Test Commands:**
    - `jnml -validate morphologies/AWC.cell.nml`
    - `jnml LEMS_AWC_test.xml -nogui`
    - `pytest tests/test_awc_multicomp.py`
- **Acceptance Criteria:**
    - [ ] AWC multicompartmental model with morphology from Issue 19
    - [ ] Per-segment channel densities assigned from extended channel library
    - [ ] Passive parameters (axial resistance, membrane capacitance) fitted to match AWC electrophysiology
    - [ ] Reproduces published AWC responses (Nicoletti et al. 2019) within ±15%
    - [ ] Simulates in NEURON via pyNeuroML export
    - [ ] Can coexist with Level C1 single-compartment neurons in the same network
    - [ ] Documents which experimental data was used for fitting
- **Sponsor Summary Hint:** AWC is one of the worm's key sensory neurons — it detects odors and triggers chemotaxis (moving toward food). Nicoletti et al. (2019) built a detailed model of AWC with multiple ion channels distributed along its branches. This issue recreates that model in NeuroML format, proving that Level D multicompartmental neurons work within our framework. It's the proof of concept for eventually upgrading all 302 neurons.

---

## Phase 6: Documentation & Contributor Support

Target: Enable new contributors to understand and modify the neural circuit model.

---

### Issue 21: Create c302 architecture overview for contributors

- **Title:** `[DD001] Create c302 architecture overview documentation for contributors`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD001 — Technical Approach](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#technical-approach) and [DD001 — Implementation References](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#implementation-references)
- **Depends On:** None
- **Files to Modify:**
    - `docs/architecture.md` (new — in c302 repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Explains: what c302 is, what it produces, who uses its output
    - [ ] File map: which Python scripts generate which levels
    - [ ] Data flow: connectome data → c302 Python → NeuroML XML → NEURON simulation → output files
    - [ ] Level comparison: table showing what each level adds (copied from DD001 but with code pointers)
    - [ ] Channel library: which channels exist, where their definitions live
    - [ ] Coupling interface: how c302 output feeds into `sibernetic_c302.py`
    - [ ] Aimed at L2 contributors (familiar with neuroscience but new to codebase)
- **Sponsor Summary Hint:** The map before the territory. c302 is a complex system — Python scripts that generate XML files that NEURON simulates. This guide explains the architecture so new contributors can find what they need. Like a building blueprint showing where the electrical, plumbing, and HVAC systems run.

---

### Issue 22: Create c302 CONTRIBUTING.md

- **Title:** `[DD001] Create CONTRIBUTING.md with neural circuit development workflow`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD001 — Quality Criteria](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#quality-criteria) and [DD001 — How to Build & Test](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#how-to-build-test)
- **Depends On:** None
- **Files to Modify:**
    - `CONTRIBUTING.md` (new — in c302 repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Prerequisites: Python, pyNeuroML, NEURON, ConnectomeToolbox
    - [ ] Build instructions: how to generate a network at each level
    - [ ] Testing workflow: `jnml -validate` → simulation → validation → regression check
    - [ ] PR checklist from DD001 Quality Criteria (all 5 criteria)
    - [ ] Branch naming: `dd001/description`
    - [ ] How to add a new ion channel (step-by-step)
    - [ ] How to modify synapse parameters (and what tests to run)
    - [ ] Warning: do NOT modify connectome topology without explicit justification
- **Sponsor Summary Hint:** The entry point for neural circuit contributors. Explains how to build, test, and validate changes. The most important rule: never change which neurons connect to which (the wiring diagram is fixed by biology). You CAN change how strong those connections are, what channels neurons express, and how synapses behave — but always test against the movement validation afterward.

---

### Issue 23: Document c302 level comparison with runnable examples

- **Title:** `[DD001] Document c302 levels A-D with runnable comparison examples`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, docs
- **DD Section to Read:** [DD001 — Architecture Levels](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#architecture-levels)
- **Depends On:** Issue 8 (verify all levels work)
- **Files to Modify:**
    - `docs/level_comparison.md` (new — in c302 repo)
    - `examples/compare_levels.py` (new)
- **Test Commands:**
    - `python3 examples/compare_levels.py`
- **Acceptance Criteria:**
    - [ ] Table comparing all levels: cell type, synapse type, channels, compute cost, use case
    - [ ] For each level: a minimal runnable example (10 neurons, 5ms simulation)
    - [ ] `compare_levels.py`: generates and simulates a small network at each level, plots voltage traces
    - [ ] Shows the key difference: Level A spikes (wrong), Level C1 is graded (correct for *C. elegans*)
    - [ ] Explains when to use each level (testing → production → research)
    - [ ] Includes expected output screenshots
- **Sponsor Summary Hint:** A visual guide showing "what does each level look like?" Level A produces sharp spikes (biologically wrong for this worm), while Level C1 produces smooth graded voltage changes (biologically correct). The comparison script lets anyone see the difference in seconds. This helps contributors and sponsors understand why Level C1 is the default.

---

### Issue 24: Create Jupyter notebook: explore the neural circuit

- **Title:** `[DD001] Create Jupyter notebook for interactive neural circuit exploration`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Validated Forward Locomotion Circuit](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#validated-forward-locomotion-circuit-gleeson-et-al-2018) and [DD001 — How to Visualize](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#how-to-visualize)
- **Depends On:** None
- **Files to Modify:**
    - `notebooks/explore_neural_circuit.ipynb` (new)
- **Test Commands:**
    - `jupyter nbconvert --execute notebooks/explore_neural_circuit.ipynb`
- **Acceptance Criteria:**
    - [ ] Generates a Level C1 network for the forward locomotion reference (FW)
    - [ ] Lists all 302 neurons with their classification (sensory, inter, motor)
    - [ ] Visualizes the forward locomotion subcircuit (AVB → B-type → muscles, cross-inhibition)
    - [ ] Runs a short simulation (5ms) and plots voltage traces for key neurons (AVBL, DB1, VB1, DD1, VD1)
    - [ ] Plots muscle calcium traces showing alternating dorsoventral activation
    - [ ] Includes markdown explaining the circuit biology at undergraduate level
    - [ ] Runs to completion without errors
- **Sponsor Summary Hint:** An interactive guided tour of the virtual worm's brain. You generate the 302-neuron circuit, zoom into the forward locomotion pathway, and watch how command neurons (AVB) activate motor neurons (DB, VB) that drive muscles — while inhibitory neurons (DD, VD) create the alternating dorsal/ventral pattern needed for undulatory crawling. All in a Jupyter notebook you can modify and re-run.

---

### Issue 25: Audit existing c302 test suite and document coverage

- **Title:** `[DD001] Audit existing c302 test suite and document test coverage`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD001 — Quality Criteria](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#quality-criteria) (criterion 3)
- **Depends On:** None
- **Files to Modify:**
    - `docs/test_coverage.md` (new — in c302 repo)
- **Test Commands:**
    - `pytest tests/ -v --tb=short`
- **Acceptance Criteria:**
    - [ ] Inventory all existing tests (unit, integration, validation)
    - [ ] Document: which tests exist, what they test, which level they cover
    - [ ] Run all tests and report pass/fail status on current main branch
    - [ ] Identify gaps: which DD001 Quality Criteria are not covered
    - [ ] Identify: are there tests for each level (A, B, C, C1, C2, D)?
    - [ ] Recommend: priority test additions to improve coverage
    - [ ] Post findings as `docs/test_coverage.md`
- **Sponsor Summary Hint:** Before adding new tests, we need to know what exists. c302 has been in development since 2014 — there are tests scattered across files, some passing, some broken, some testing obsolete features. This audit catalogs everything and identifies where the gaps are. You can't improve what you don't measure.

---

## Infrastructure (Cross-Phase)

---

### Issue 26: Verify `wormneuroatlas` integration with c302

- **Title:** `[DD001] Verify wormneuroatlas package integration with c302 for functional connectivity data`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD001 — Existing Code Resources](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#existing-code-resources) (wormneuroatlas section) and [DD020](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/)
- **Depends On:** None
- **Files to Modify:**
    - `tests/test_wormneuroatlas.py` (new)
- **Test Commands:**
    - `pip install wormneuroatlas`
    - `pytest tests/test_wormneuroatlas.py`
- **Acceptance Criteria:**
    - [ ] `pip install wormneuroatlas` succeeds in the Docker/CI environment
    - [ ] Can load Randi 2023 functional connectivity data via the package API
    - [ ] Can load CeNGEN gene expression data via the package API
    - [ ] Neuron naming matches between `wormneuroatlas` and c302 (or mapping documented)
    - [ ] Test verifies: load connectivity, load expression, cross-reference neuron names
    - [ ] Document any API versioning or compatibility issues
- **Sponsor Summary Hint:** `wormneuroatlas` is a Python package that provides unified access to connectome data, gene expression (CeNGEN), and functional connectivity (Randi 2023). This verifies it works in our environment and that neuron names match between the atlas and our model — a critical prerequisite for both synaptic optimization and cell-type specialization.

---

### Issue 27: Add `neural.spatial_synapses` config toggle for Level D

- **Title:** `[DD001] Add neural.spatial_synapses config toggle for spatially resolved synapse placement`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302` + `openworm/OpenWorm`
- **Required Capabilities:** python, yaml
- **DD Section to Read:** [DD001 — Spatially Resolved Synapse Placement](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#spatially-resolved-synapse-placement-phase-2-with-level-d)
- **Depends On:** DD013 Issue 1 (openworm.yml schema)
- **Files to Modify:**
    - `openworm.yml` (add `neural.spatial_synapses: false`)
- **Test Commands:**
    - `python3 -c "import yaml; c = yaml.safe_load(open('openworm.yml')); print(c['neural']['spatial_synapses'])"`
- **Acceptance Criteria:**
    - [ ] `neural.spatial_synapses: false` → synapses are abstract neuron-to-neuron (current behavior)
    - [ ] `neural.spatial_synapses: true` → placeholder for spatially placed synapses (requires Level D)
    - [ ] Config validation: `spatial_synapses: true` requires `level: D` (error otherwise)
    - [ ] Documented with DD cross-reference
- **Sponsor Summary Hint:** In the simple model, a synapse is just "neuron A connects to neuron B." In the detailed Level D model, synapses have specific locations along the neurite — and location matters because it determines how signals combine. This config toggle enables spatial synapse placement when Level D is active. The actual placement algorithm is a separate issue.

---

### Issue 28: Create c302 changelog documenting framework evolution

- **Title:** `[DD001] Create annotated changelog documenting c302's evolution`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** git, docs
- **DD Section to Read:** [DD001 — References](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#references) (Gleeson et al. 2018) and [DD001 — Architecture Levels](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#architecture-levels)
- **Depends On:** None
- **Files to Modify:**
    - `CHANGELOG.md` (new — in c302 repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Lists major milestones: Level A creation, Level C/C1, graded synapses, Sibernetic coupling
    - [ ] Maps milestones to publications (Gleeson et al. 2018, etc.)
    - [ ] Notes key branch points and tags (`ow-0.9.7`, etc.)
    - [ ] Documents current active branches
    - [ ] Notes when Johnson & Mailler muscle model was added
    - [ ] Documents the relationship between c302 and CElegansNeuroML repos
- **Sponsor Summary Hint:** c302 has been in development since ~2014, evolving from simple integrate-and-fire models to sophisticated Hodgkin-Huxley conductance-based neurons. A changelog helps new contributors understand what exists and how it got there — preventing them from reinventing solutions that were already tried (and sometimes abandoned for good reasons).

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 28 |
| **ai-workable** | 17 |
| **human-expert** | 11 |
| **L1** | 9 |
| **L2** | 12 |
| **L3** | 7 |

| Phase | Issues | Target |
|-------|--------|--------|
| **1: Validation Infrastructure** | 1–5 | Scripts and baselines to measure quality |
| **2: Data Pipeline & Integration** | 6–9 | OME-Zarr export, connectome switching, coupling docs |
| **3: Ion Channel Library** | 10–15 | 14 channels from BAAIWorm → NeuroML |
| **4: Synaptic Optimization** | 16–18 | Neurotransmitter constraints, weight fitting prep |
| **5: Level D Development** | 19–20 | Multicompartmental proof-of-concept |
| **6: Documentation** | 21–25 | Architecture docs, contributing guide, notebooks |
| **Infrastructure** | 26–28 | wormneuroatlas, config toggles, changelog |

### Dependency Graph (Critical Path)

```
Issue 3 (NeuroML CI) — independent (deploy immediately)

Issue 5 (output format audit)
  ├→ Issue 6 (OME-Zarr export)
  └→ Issue 9 (coupling bridge docs)

Issue 1 (extract_trajectory.py)
  └→ Issue 4 (Schafer baseline) → Issue 2 (check_regression.py)

Issue 10 (BAAIWorm survey)
  ├→ Issue 11 (EGL-19 channel)  ─┐
  ├→ Issue 12 (SLO-1 channel)   ├→ Issue 14 (MEDIUM channels)
  └→ Issue 13 (KVS-1, EGL-36)  ─┘    └→ Issue 15 (channel test suite)
  └→ Issue 19 (SWC morphologies)
       └→ Issue 20 (AWC Level D proof-of-concept)

Issue 16 (neurotransmitter constraints) — independent
Issue 17 (synapse_optimization config) — depends on DD013 Issue 1
Issue 18 (Randi 2023 matrix) — independent

Issue 7 (connectome switching) — depends on DD013 Issue 9
Issue 8 (level verification) → Issue 23 (level comparison docs)
Issue 27 (spatial_synapses config) — depends on DD013 Issue 1

Issues 21, 22, 24, 25, 26, 28 (docs/infra) — independent
```
