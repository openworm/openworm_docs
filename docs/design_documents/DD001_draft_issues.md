# DD001 Draft GitHub Issues

**Epic:** DD001 — Neural Circuit Architecture and Multi-Level Framework

**Generated from:** [DD001: Neural Circuit Architecture](DD001_Neural_Circuit_Architecture.md)

**Methodology:** [DD015 §2.2 — DD Issue Generator](DD015_AI_Contributor_Model.md#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 9 issues (ai-workable: 6 / human-expert: 3 | L1: 5, L2: 3, L3: 1)

**Note:** DD001's "How to Build & Test" section references kinematic validation scripts (`check_regression.py`, Schafer baseline generation) at Steps 5-6. Those scripts are **thin wrappers around `open-worm-analysis-toolbox`**, which DD021 owns. They have been moved to [DD021 Draft Issues](DD021_draft_issues.md) (Issues 1-2) where they belong as Phase A validation infrastructure. DD001 is a **consumer** of that validation pipeline, not the owner.

**Roadmap Context:** DD001 is a **Phase 0** DD (existing, working). Its draft issues span multiple roadmap phases:

| Group | Phase | Rationale |
|-------|-------|-----------|
| 1. Validation Infrastructure (Issues 1-3) | **Phase A** | Trajectory extraction tools for automated validation pipeline |
| 2. Data Pipeline (Issue 4) | **Phase A** | OME-Zarr export for DD014 viewer |
| 3. Documentation (Issues 5-8) | **Any** | Can be addressed independently |
| Infrastructure (Issue 9-10) | **Phase A** | Changelog |

**Issues relocated to other DDs:** Ion Channel Library (6 issues) → [DD005 Draft Issues](DD005_draft_issues.md); Synaptic Optimization (3 issues) → [DD017 Draft Issues](DD017_draft_issues.md); Level D Multicompartmental (2 issues) + spatial synapses config → [DD027 Draft Issues](DD027_draft_issues.md).

---

## Group 1: Validation Infrastructure (Phase A)

Target: Scripts and baselines needed to measure neural circuit quality — trajectory extraction tools (ported from existing C++ implementations) and output format documentation. Kinematic regression detection is handled by [DD021](DD021_draft_issues.md).

---

### Issue 1: Port Boyle-Cohen 2D body model as `scripts/boyle_berri_cohen_trajectory.py`

- **Title:** `[DD001] Port Boyle-Cohen 2D body model into boyle_berri_cohen_trajectory.py — fast trajectory screening tool`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, physics
- **DD Section to Read:** [DD001 — How to Build & Test](DD001_Neural_Circuit_Architecture.md#how-to-build-test) (Step 3a) and [DD001 — Deliverables](DD001_Neural_Circuit_Architecture.md#deliverables) (WCON row)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`openworm/CelegansNeuromechanicalGaitModulation/WormSim/Model/worm.cc`](https://github.com/openworm/CelegansNeuromechanicalGaitModulation) — Complete C++ Boyle-Cohen model (48 segments, Sundials IDA solver) with bistable neural circuit, muscle model, stretch receptors, and obstacle avoidance. **Also includes `generate_wcon.py` that already converts simulation CSV output to WCON 1.0 format**, plus `WormView.py` and `WormPlot.py` visualization tools.
    - [`openworm/CE_locomotion/WormBody.cpp`](https://github.com/openworm/CE_locomotion) — Complete C++ implementation (50 segments, custom semi-implicit backward Euler DAE solver) by Randall Beer. Full neuromechanical coupling loop in `Worm.cpp`: body → stretch receptors → nervous system → muscles → body. Includes `load_data.py` for visualization. 3 documented deviations from original BBC code with `BBC_STRICT` toggle.
    - [`openworm/Worm2D/src/CE_locomotion/WormBody.cpp`](https://github.com/openworm/Worm2D) — C++ implementation (50 segments) with c302 integration layer via CPython embedding (`src/neuromlModel/c302ForW2D.cpp`). Shows how to bridge c302's Python neural simulation with the C++ body model.
    - **Paper:** [Boyle, Berri & Cohen 2012](https://doi.org/10.3389/fncom.2012.00010)
- **Approach:** **Port or wrap** the existing C++ body model, do not reimplement from scratch. Two viable paths: (a) Python/NumPy port of `WormBody.cpp` (~200 lines of core math plus DAE solver), treating the C++ as the reference specification; (b) compile `CelegansNeuromechanicalGaitModulation/WormSim/Model/worm.cc` as a subprocess and adapt the existing `generate_wcon.py` for WCON output. Path (a) gives tighter c302 integration; path (b) is faster to ship.
- **DD013 Pipeline Role:** Neural-stage script. Must be callable from `master_openworm.py` with output path from `openworm.yml`. Produces WCON artifact at a well-known path for downstream DD021/DD010 consumption.
- **Files to Modify:**
    - `scripts/boyle_berri_cohen_trajectory.py` (new — port/wrapper of existing C++ implementations)
    - `tests/test_boyle_berri_cohen_trajectory.py` (new)
- **Test Commands:**
    - `jnml LEMS_c302_C1_Muscles.xml -nogui`
    - `python3 scripts/boyle_berri_cohen_trajectory.py --input . --output trajectory.wcon`
    - `pytest tests/test_boyle_berri_cohen_trajectory.py`
- **Acceptance Criteria:**
    - [ ] Reads c302/NEURON muscle calcium `.dat` files (96 muscle cells)
    - [ ] Converts calcium to activation via threshold/low-pass filter (reference: `Muscles.cpp` in CE_locomotion, time constant T_muscle = 0.1)
    - [ ] Runs Boyle-Cohen 2D rod-spring model (48–50 segments, ~150 state variables, anisotropic drag) — ported from or wrapping one of the three existing C++ implementations
    - [ ] Body model output matches the reference C++ implementation within numerical tolerance
    - [ ] Exports 49-point worm centerline in WCON 1.0 format (reference: `generate_wcon.py` in CelegansNeuromechanicalGaitModulation)
    - [ ] Output validates against WCON JSON schema
    - [ ] Compatible with `open-worm-analysis-toolbox` for DD010 Tier 3
    - [ ] Runs in <30 seconds on single CPU (fast enough for CI quick-test)
    - [ ] Unit tests with synthetic calcium data
- **Sponsor Summary Hint:** A fast validation ruler built on proven code. Three OpenWorm repos already implement the Boyle-Cohen 2D body model in C++ — this issue ports one of them to Python and wires it to c302's muscle output. Change a neural parameter → re-run → check if the worm still crawls correctly — all in under 30 seconds, no GPU needed.

---

### Issue 2: Adapt Sibernetic's WCON generator as `scripts/extract_trajectory.py`

- **Title:** `[DD001] Adapt Sibernetic's existing WCON generator into extract_trajectory.py — full-fidelity trajectory extraction`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD001 — How to Build & Test](DD001_Neural_Circuit_Architecture.md#how-to-build-test) (Step 3b) and [DD001 — Deliverables](DD001_Neural_Circuit_Architecture.md#deliverables) (WCON row)
- **Depends On:** DD003 (Sibernetic must produce particle output)
- **Existing Code to Reuse:**
    - [`openworm/sibernetic/wcon/generate_wcon.py`](https://github.com/openworm/sibernetic) — ~300 lines of **working Python** that reads `worm_motion_log.txt` from Sibernetic, generates WCON JSON, validates against `wcon_schema.json`, and computes speed/curvature. Also includes `wcon/__init__.py`, `wcon/wcon_schema.json`, and test WCON files.
    - [`openworm/skeletonExtraction`](https://github.com/openworm/skeletonExtraction) — C++ skeleton extraction from Sibernetic mesh output (3D graphics skeleton for animation, not 2D midline — different purpose but the centerline concept is related)
- **Approach:** **Adapt and extend** the existing `sibernetic/wcon/generate_wcon.py`. The core WCON generation pipeline exists; extend it to handle the full acceptance criteria (49-point centerline from elastic shell particles, 3D→2D projection, schema validation).
- **DD013 Pipeline Role:** Body-stage script. Runs after Sibernetic simulation completes. Output WCON path configured via `openworm.yml`. Must be callable from `master_openworm.py`.
- **Files to Modify:**
    - `scripts/extract_trajectory.py` (new — adapted from existing `wcon/generate_wcon.py`)
    - `tests/test_extract_trajectory.py` (new)
- **Test Commands:**
    - `python3 scripts/extract_trajectory.py --input sibernetic_output/ --output trajectory.wcon`
    - `pytest tests/test_extract_trajectory.py`
- **Acceptance Criteria:**
    - [ ] Built on the existing `sibernetic/wcon/generate_wcon.py` codebase, not from scratch
    - [ ] Reads Sibernetic SPH elastic particle positions from simulation output
    - [ ] Extracts 3D worm centerline (49-point skeleton) from elastic shell particles
    - [ ] Projects to 2D x/y for WCON 1.0 (which is 2D centerline format)
    - [ ] Exports in WCON 1.0 format
    - [ ] Output validates against WCON JSON schema (reuse existing `wcon/wcon_schema.json`)
    - [ ] Compatible with `open-worm-analysis-toolbox` for DD010 Tier 3
    - [ ] Captures full 3D body deformation effects (fluid-structure, pseudocoelomic pressure)
    - [ ] Unit tests with synthetic particle data
- **Sponsor Summary Hint:** Sibernetic already has a working WCON generator — this issue extends it for the full DD001 validation chain. The existing `generate_wcon.py` reads motion logs and produces WCON; this version adds 49-point centerline extraction from the ~100K SPH particle cloud, capturing 3D effects the fast 2D model cannot.

---

### Issue 3: Audit c302 simulation output files and document format

- **Title:** `[DD001] Audit and document c302/NEURON simulation output file formats`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Integration Contract — Outputs](DD001_Neural_Circuit_Architecture.md#inputs--outputs) and [DD001 — Coupling Bridge Ownership](DD001_Neural_Circuit_Architecture.md#coupling-bridge-ownership)
- **Depends On:** None
- **Existing Code to Reuse:**
    - `c302/runAndPlot.py` — Already generates summary images and HTML pages across all configs; shows which output files are produced
    - `c302/c302_info.py` — Generates cell info summaries
    - `c302/examples/summary/README.md` — HTML table of all config × parameter-set combinations
- **Approach:** **Document existing outputs.** Run simulations and catalog what's produced; the outputs exist but are undocumented.
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

## Group 2: Data Pipeline & Integration (Phase A)

Target: OME-Zarr export and coupling interface documentation.

---

### Issue 4: Implement OME-Zarr export for neural voltage and calcium data

- **Title:** `[DD001] Implement OME-Zarr export for neural/voltage, neural/calcium, neural/positions`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD001 — Deliverables](DD001_Neural_Circuit_Architecture.md#deliverables) (OME-Zarr rows) and [DD014](DD014_Dynamic_Visualization_Architecture.md) (OME-Zarr schema)
- **Depends On:** Issue 3 (output format documentation)
- **DD013 Pipeline Role:** Neural-stage post-processing. Produces Zarr store artifact for DD014 visualization stage. Output path from `openworm.yml`.
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

## ~~Group 3: Ion Channel Library~~ → Relocated to [DD005 Draft Issues](DD005_draft_issues.md)

6 issues (survey + adopt/validate 14 channels) relocated to DD005, which drives Phase 1 cell-type specialization. See [DD005 Draft Issues](DD005_draft_issues.md) Issues 1-6.

## ~~Group 4: Synaptic Optimization~~ → Relocated to [DD017 Draft Issues](DD017_draft_issues.md)

3 issues (neurotransmitter constraints, synapse optimization toggle, Randi 2023 adapter) relocated to DD017, which provides the differentiable simulation backend. See [DD017 Draft Issues](DD017_draft_issues.md) Issues 1-3.

## ~~Group 5: Level D Multicompartmental~~ → Relocated to [DD027 Draft Issues](DD027_draft_issues.md)

2 issues (morphology evaluation, AWC proof-of-concept) + 1 infrastructure issue (spatial synapses config) relocated to DD027, which specifies multicompartmental models. See [DD027 Draft Issues](DD027_draft_issues.md) Issues 1-3.

---

## Group 3: Documentation & Contributor Support (Any)

(Renumbered from original Group 6. Issues renumbered 5-8.)

Target: Enable new contributors to understand and modify the neural circuit model.

---

### Issue 5: Create c302 architecture overview for contributors

- **Title:** `[DD001] Create c302 architecture overview documentation for contributors`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD001 — Technical Approach](DD001_Neural_Circuit_Architecture.md#technical-approach) and [DD001 — Implementation References](DD001_Neural_Circuit_Architecture.md#implementation-references)
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

### Issue 6: Create c302 CONTRIBUTING.md

- **Title:** `[DD001] Create CONTRIBUTING.md with neural circuit development workflow`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD001 — Quality Criteria](DD001_Neural_Circuit_Architecture.md#quality-criteria) and [DD001 — How to Build & Test](DD001_Neural_Circuit_Architecture.md#how-to-build-test)
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

### Issue 7: Document c302 level comparison with runnable examples

- **Title:** `[DD001] Document c302 levels A-D with runnable comparison examples`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, docs
- **DD Section to Read:** [DD001 — Architecture Levels](DD001_Neural_Circuit_Architecture.md#architecture-levels)
- **Depends On:** None
- **Existing Code to Reuse:**
    - `c302/runAndPlot.py -all` — Already generates comparison images across all levels/configs with HTML summary
    - `c302/examples/summary/README.md` — Existing HTML table of all config × parameter-set combinations
    - `c302/examples/test/Comparison.ipynb` — Existing Jupyter notebook comparing configurations
    - `test.sh` — Already generates and validates all 9 parameter sets × 8 configs (proves all levels work)
- **Approach:** **Build on existing infrastructure.** The level generation, validation, and comparison plotting already exist in `runAndPlot.py` and `test.sh`. This issue wraps that into a contributor-friendly document with narrative, not a new comparison tool.
- **Files to Modify:**
    - `docs/level_comparison.md` (new — in c302 repo)
    - `examples/compare_levels.py` (new — wrapping existing runAndPlot.py functionality)
- **Test Commands:**
    - `python3 examples/compare_levels.py`
- **Acceptance Criteria:**
    - [ ] Table comparing all levels: cell type, synapse type, channels, compute cost, use case
    - [ ] For each level: a minimal runnable example (10 neurons, 5ms simulation)
    - [ ] `compare_levels.py`: generates and simulates a small network at each level, plots voltage traces (build on existing `runAndPlot.py`)
    - [ ] Shows the key difference: Level A spikes (wrong), Level C1 is graded (correct for *C. elegans*)
    - [ ] Explains when to use each level (testing → production → research)
    - [ ] Includes expected output screenshots
- **Sponsor Summary Hint:** c302 already generates and validates all levels in CI and produces comparison images via `runAndPlot.py`. This issue turns that existing infrastructure into a visual guide showing "what does each level look like?" — so contributors understand why Level C1 is the default.

---

### Issue 8: Audit existing c302 test suite and document coverage

- **Title:** `[DD001] Audit existing c302 test suite and document test coverage`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD001 — Quality Criteria](DD001_Neural_Circuit_Architecture.md#quality-criteria) (criterion 3)
- **Depends On:** None
- **Existing Code to Reuse:**
    - `c302/test.sh` — **~150+ line shell script** running ALL readers, ALL generators, ALL validators, ALL simulators. This IS the test suite — it just needs documentation.
    - `.github/workflows/ci.yml` — OMV tests across Python 3.10/3.13 with jNeuroML, NEURON, and validate engines
    - `.github/workflows/non_omv.yml` — Non-OMV tests on Ubuntu + macOS
    - `examples/*.omt` and `examples/*.mep` — **18+ OMV test/expected-value pairs**
    - `examples/parametersweep/*.py` — Parameter sweep test infrastructure
    - `examples/test/test_WNA.py` — WormNeuroAtlas integration test
- **Approach:** **Document what exists.** The test suite is extensive but undocumented. Run it, catalog it, identify gaps.
- **Files to Modify:**
    - `docs/test_coverage.md` (new — in c302 repo)
- **Test Commands:**
    - `pytest tests/ -v --tb=short`
- **Acceptance Criteria:**
    - [ ] Inventory ALL existing tests: `test.sh`, OMV `.omt`/`.mep` files, CI workflows, parametersweep scripts, `test_WNA.py`
    - [ ] Document: which tests exist, what they test, which level they cover
    - [ ] Run all tests and report pass/fail status on current main branch
    - [ ] Identify gaps: which DD001 Quality Criteria are not covered
    - [ ] Identify: are there tests for each level (A, B, C, C1, C2, D)?
    - [ ] Recommend: priority test additions to improve coverage
    - [ ] Post findings as `docs/test_coverage.md`
- **Sponsor Summary Hint:** c302 has an extensive test suite — `test.sh` runs all 9 parameter sets × 8 configs, CI validates on multiple Python versions and OSes, and 18+ OMV tests check expected values. But nobody has documented what it all covers. This audit catalogs everything and identifies where the gaps are. You can't improve what you don't measure.

---

## Group 4: Infrastructure (Phase A)

---

### Issue 9: Create c302 changelog documenting framework evolution

- **Title:** `[DD001] Create annotated changelog documenting c302's evolution`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** git, docs
- **DD Section to Read:** [DD001 — References](DD001_Neural_Circuit_Architecture.md#references) (Gleeson et al. 2018) and [DD001 — Architecture Levels](DD001_Neural_Circuit_Architecture.md#architecture-levels)
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
| **Total Issues** | 9 |
| **ai-workable** | 6 |
| **human-expert** | 3 |
| **L1** | 5 |
| **L2** | 3 |
| **L3** | 1 |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Validation Infrastructure** | 1–3 | Trajectory tools (ported from existing C++), output format audit. Kinematic regression detection moved to [DD021](DD021_draft_issues.md). |
| **2: Data Pipeline** | 4 | OME-Zarr export |
| **3: Documentation** | 5–8 | Architecture docs, contributing guide, level comparison, test audit |
| **4: Infrastructure** | 9 | Changelog |

**Relocated issues:**

| Destination | Issues Moved | Count |
|------------|-------------|-------|
| [DD005 Draft Issues](DD005_draft_issues.md) | Ion Channel Library (original Issues 5-10) | 6 |
| [DD017 Draft Issues](DD017_draft_issues.md) | Synaptic Optimization (original Issues 11-13) | 3 |
| [DD027 Draft Issues](DD027_draft_issues.md) | Level D Multicompartmental (original Issues 14-15) + spatial synapses config (original Issue 20) | 3 |

### Cross-References

| Related DD | Relationship |
|------------|-------------|
| **[DD005](DD005_draft_issues.md) (Cell-Type Specialization)** | **Ion channel issues relocated there** — 6 issues (original Issues 5-10) |
| **[DD017](DD017_draft_issues.md) (Hybrid ML)** | **Synaptic optimization issues relocated there** — 3 issues (original Issues 11-13) |
| **[DD027](DD027_draft_issues.md) (Multicompartmental)** | **Level D issues relocated there** — 3 issues (original Issues 14-15, 20) |
| **[DD021](DD021_draft_issues.md) (Movement Toolbox)** | Kinematic validation scripts moved there — DD021 Issues 1-2. DD001 is a consumer of DD021's validation pipeline. |
| DD002 (Muscle Model) | DD002 Issue 18 documents `sibernetic_c302.py` coupling bridge |
| DD003 (Body Physics) | Issue 2 (extract_trajectory.py) |
| DD010 (Validation Framework) | Issues 1, 2 produce WCON consumed by DD010 Tier 3 |
| DD013 (Simulation Stack) | DD013 Issue 24 covers c302 notebook |
| DD014 (Dynamic Visualization) | Issue 4 (OME-Zarr export for viewer) |

### Dependency Graph (Critical Path)

```
Issue 3 (output format audit)
  └→ Issue 4 (OME-Zarr export)

Issue 1 (boyle_berri_cohen_trajectory.py — port existing C++) — independent, fast path
Issue 2 (extract_trajectory.py — adapt Sibernetic generate_wcon.py) — depends on DD003
  ├→ [both Issue 1 and Issue 2 produce WCON for DD021 regression checking]

Issues 5, 6, 7, 8 (docs) — independent
Issue 9 (changelog) — independent

Ion channel library → see DD005 Draft Issues
Synaptic optimization → see DD017 Draft Issues
Level D multicompartmental → see DD027 Draft Issues
Kinematic validation → see DD021 Issues 1-2
```
