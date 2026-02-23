# DD001 Draft GitHub Issues

**Epic:** DD001 — Neural Circuit Architecture and Multi-Level Framework

**Generated from:** [DD001: Neural Circuit Architecture](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/)

**Methodology:** [DD015 §2.2 — DD Issue Generator](https://docs.openworm.org/design_documents/DD015_AI_Contributor_Model/#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 21 issues (ai-workable: 10 / human-expert: 11 | L1: 5, L2: 9, L3: 7)

**Note:** DD001's "How to Build & Test" section references kinematic validation scripts (`check_regression.py`, Schafer baseline generation) at Steps 5-6. Those scripts are **thin wrappers around `open-worm-analysis-toolbox`**, which DD021 owns. They have been moved to [DD021 Draft Issues](DD021_draft_issues.md) (Issues 1-2) where they belong as Phase A validation infrastructure. DD001 is a **consumer** of that validation pipeline, not the owner.

**Roadmap Context:** The "Groups" below organize issues thematically within this DD — they are **not** the same as the [DD Phase Roadmap](DD_PHASE_ROADMAP.md) phases (Phase 0/A/1/2/3/4). DD001 is a **Phase 0** DD (existing, working). Groups 1–2 primarily support Roadmap Phase A (infrastructure). Group 3 (ion channels) feeds Roadmap Phase 1 (cell-type specialization via DD005). Groups 4–5 (synaptic optimization, Level D) align with Roadmap Phase 2. Group 6 and Infrastructure issues can be addressed at any roadmap phase.

---

## Group 1: Validation Infrastructure

Target: Scripts and baselines needed to measure neural circuit quality — trajectory extraction tools (ported from existing C++ implementations) and output format documentation. Kinematic regression detection is handled by [DD021](DD021_draft_issues.md).

---

### Issue 1: Port Boyle-Cohen 2D body model as `scripts/boyle_berri_cohen_trajectory.py`

- **Title:** `[DD001] Port Boyle-Cohen 2D body model into boyle_berri_cohen_trajectory.py — fast trajectory screening tool`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, physics
- **DD Section to Read:** [DD001 — How to Build & Test](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#how-to-build-test) (Step 3a) and [DD001 — Deliverables](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#deliverables) (WCON row)
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
- **Target Repo:** `openworm/Sibernetic`
- **Required Capabilities:** python, physics
- **DD Section to Read:** [DD001 — How to Build & Test](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#how-to-build-test) (Step 3b) and [DD001 — Deliverables](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#deliverables) (WCON row)
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
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Integration Contract — Outputs](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#inputs--outputs) and [DD001 — Coupling Bridge Ownership](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#coupling-bridge-ownership)
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

## Group 2: Data Pipeline & Integration

Target: OME-Zarr export and coupling interface documentation.

---

### Issue 4: Implement OME-Zarr export for neural voltage and calcium data

- **Title:** `[DD001] Implement OME-Zarr export for neural/voltage, neural/calcium, neural/positions`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD001 — Deliverables](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#deliverables) (OME-Zarr rows) and [DD014](https://docs.openworm.org/design_documents/DD014_Dynamic_Visualization_Architecture/) (OME-Zarr schema)
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

## Group 3: Extended Ion Channel Library

Target: Expand from 4 generic channels to 14+ neuron-class-specific channels, leveraging existing NeuroML2 models from Nicoletti et al. and NMODL files from BAAIWorm.

---

### Issue 5: Survey existing ion channel implementations across all OpenWorm repos

- **Title:** `[DD001] Survey existing NeuroML2 and NMODL ion channel implementations across all OpenWorm and related repos`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (code reuse plan)
- **Depends On:** None
- **Existing Code to Reuse (THIS IS THE CODE TO SURVEY):**
    - [`openworm/NicolettiEtAl2019_NeuronModels/NeuroML2/`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **31 ion channels already in NeuroML2**: AWCon (16 channels: shal, kvs1, shak, kqt3, egl2, kir, unc2, egl19, cca, bk, slo1, bk2, slo2, sk, nca, leak) and RMD (15 channels: bk, bk2, cca, egl19, egl36, kir, leak, nca, shak, shal, sk, slo1, slo2, unc2). Includes `GenerateNeuroML.py` and Ca dynamics model. **Validated against original XPP models.**
    - [`openworm/NicolettiEtAl2024_MN_IN/`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — **22 NMODL files** for motor neurons (VA5, VB6, VD5) and interneurons (AVAL, AVAR, AIY, RIM). Includes voltage-clamp and current-clamp simulation scripts. **6 channels partially converted to NeuroML2** (AIY subset: egl19, egl2, shk1, shl1, unc2, leak).
    - [`Jessie940611/BAAIWorm/eworm/components/mechanism/modfile/`](https://github.com/Jessie940611/BAAIWorm) — **17+ NMODL files** covering all DD001 target channels. Also contains per-neuron conductance parameters (`eworm/components/param/cell/*.json` — one JSON per neuron with max conductance for each channel), ion channel validation scripts (`eworm/ion_channel_tune/`), and calcium correlation data (`eworm/components/cb2022_data/`). All channels cite Nicoletti et al. 2019 as source.
    - [`openworm/ChannelWorm2/NML2_models/`](https://github.com/openworm/ChannelWorm2) — **4 NeuroML2 channels** (EGL-19, SHK-1, SHL-1, SLO-2) with annotated PDFs of equations. Uses Boyle & Cohen 2008 parameters (different from Nicoletti). Also has **200+ raw electrophysiology JSON files** with digitized I-V curves for C. elegans channels, and a parameter fitting pipeline (`parameter_fitting/`).
    - [`openworm/CElegansNeuroML/CElegans/generatedNeuroML2/`](https://github.com/openworm/CElegansNeuroML) — Generic `LeakConductance.channel.nml` only, but has 11 synapse types (Acetylcholine, GABA, Glutamate, etc.) and all 302 neuron morphologies as multicompartmental NeuroML2.
- **Approach:** **Survey, catalog, and produce a reconciliation matrix** — not just BAAIWorm, but ALL existing channel implementations. The key output is: which channels already exist in NeuroML2 (and can be adopted immediately), which exist only as NMODL (and need conversion), and where parameter discrepancies exist between sources.
- **Files to Modify:**
    - None (research issue — output is a summary comment on the issue)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Catalog all existing NeuroML2 channel files across: NicolettiEtAl2019, NicolettiEtAl2024, ChannelWorm2, CElegansNeuroML
    - [ ] Catalog all existing NMODL channel files across: BAAIWorm, NicolettiEtAl2024
    - [ ] For each of the 14 channels in DD001's target library table: identify ALL existing implementations (NeuroML2 and/or NMODL), note repository, file path, and parameter source
    - [ ] Produce a reconciliation matrix: where parameters differ between sources (e.g., ChannelWorm2 EGL-19 uses Boyle & Cohen 2008 parameters vs. Nicoletti 2019 parameters), flag for expert review
    - [ ] Assess: do the existing NicolettiEtAl2019 NeuroML2 channels pass `jnml -validate`? Test all 31
    - [ ] Document: license compatibility across repos (Apache 2.0 / MIT)
    - [ ] Recommend: for each channel, which existing implementation to adopt as canonical
    - [ ] Post findings as issue comment
- **Sponsor Summary Hint:** Before converting anything, let's catalog what already exists. Multiple OpenWorm and related repos already contain ion channel models — 31 channels in NeuroML2 from Nicoletti 2019 alone. This survey maps every existing implementation, flags parameter discrepancies between sources, and recommends which to adopt. It could save weeks of conversion work.

---

### Issue 6: Validate and adopt EGL-19 (Cav1 L-type) NeuroML2 channel into c302

- **Title:** `[DD001] Validate and adopt existing EGL-19 (Cav1 L-type Ca²⁺) NeuroML2 channel into c302 channel library`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (EGL-19 row, HIGH priority)
- **Depends On:** Issue 5 (survey)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/AWCon_egl19.channel.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **EGL-19 already exists in validated NeuroML2.** Part of the AWCon 16-channel model. Validated against XPP original.
    - [`NicolettiEtAl2024_MN_IN/NeuroML/egl19.channel.nml`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — Another NeuroML2 version (AIY subset conversion)
    - [`NicolettiEtAl2024_MN_IN/egl19.mod`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — NMODL reference
    - [`ChannelWorm2/NML2_models/EGL-19.channel.nml`](https://github.com/openworm/ChannelWorm2) — Older NeuroML2 version using Boyle & Cohen 2008 parameters (different from Nicoletti)
    - `ChannelWorm2/raw_data/JSON/` — Digitized experimental I-V curves for validation
- **Approach:** **Validate and adopt** the existing NicolettiEtAl2019 NeuroML2 channel. Reconcile parameters against the NicolettiEtAl2024 and ChannelWorm2 versions. Validate against experimental I-V data from ChannelWorm2. Do NOT convert from NMODL — the NeuroML2 already exists.
- **Files to Modify:**
    - `channel_models/egl19_cav1.channel.nml` (adopted from NicolettiEtAl2019, possibly reconciled)
    - `tests/test_egl19_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/egl19_cav1.channel.nml`
    - `pytest tests/test_egl19_channel.py`
- **Acceptance Criteria:**
    - [ ] EGL-19 channel adopted from existing NicolettiEtAl2019 NeuroML2 — not reimplemented
    - [ ] Parameters reconciled against NicolettiEtAl2024 and ChannelWorm2 versions; discrepancies documented
    - [ ] Passes `jnml -validate`
    - [ ] I-V curve matches NMODL reference within ±5% (test with voltage clamp protocol)
    - [ ] Validated against ChannelWorm2 experimental I-V data where available
    - [ ] Activation and inactivation kinetics (V_half, slope, tau) documented with literature source
    - [ ] Can be inserted into a GenericCell definition alongside existing channels
    - [ ] Unit test compares NeuroML channel output against NMODL reference
- **Sponsor Summary Hint:** EGL-19 is the primary L-type calcium channel in *C. elegans* — and it already exists in NeuroML2 format from Nicoletti et al. 2019. This issue validates that existing model against experimental data and integrates it into c302's channel library. Adoption, not reinvention.

---

### Issue 7: Validate and adopt SLO-1 (BK Ca²⁺-activated K⁺) NeuroML2 channel into c302

- **Title:** `[DD001] Validate and adopt existing SLO-1 (BK Ca²⁺-activated K⁺) NeuroML2 channel into c302 channel library`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (SLO-1 row, HIGH priority)
- **Depends On:** Issue 5 (survey)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/AWCon_slo1.channel.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **SLO-1 already exists in validated NeuroML2.** Calcium-dependent gating modeled. Part of AWCon model.
    - [`NicolettiEtAl2024_MN_IN/slo1egl19.mod`, `slo1unc2.mod`, `slo1iso.mod`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — Three SLO-1 variants coupled to different calcium sources (EGL-19, UNC-2, isolated)
    - [`BAAIWorm/eworm/components/mechanism/modfile/slo1_egl19.mod`, `slo1_unc2.mod`](https://github.com/Jessie940611/BAAIWorm) — BAAIWorm NMODL versions
- **Approach:** **Validate and adopt** the existing NicolettiEtAl2019 NeuroML2 channel. Note that BAAIWorm and NicolettiEtAl2024 have calcium-source-specific variants (SLO-1 coupled to EGL-19 vs UNC-2) — determine if the c302 library needs separate variants or a unified model.
- **Files to Modify:**
    - `channel_models/slo1_bk.channel.nml` (adopted from NicolettiEtAl2019)
    - `tests/test_slo1_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/slo1_bk.channel.nml`
    - `pytest tests/test_slo1_channel.py`
- **Acceptance Criteria:**
    - [ ] SLO-1 BK channel adopted from existing NicolettiEtAl2019 NeuroML2 — not reimplemented
    - [ ] Calcium-dependent gating correctly modeled (conductance depends on both V and [Ca²⁺]ᵢ)
    - [ ] Decision documented: single unified SLO-1 or separate EGL-19/UNC-2/iso variants per NicolettiEtAl2024
    - [ ] I-V curve matches NMODL reference within ±5%
    - [ ] Activation kinetics documented with literature source
    - [ ] Unit test compares NeuroML channel output against NMODL reference
- **Sponsor Summary Hint:** SLO-1 is a "big potassium" (BK) channel that opens when it senses both voltage AND calcium inside the cell. It already exists in NeuroML2 from Nicoletti et al. 2019. This issue validates and adopts it, with a decision on whether to carry the calcium-source-specific variants from the newer Nicoletti 2024 models.

---

### Issue 8: Validate and adopt KVS-1 and EGL-36 NeuroML2 channels into c302

- **Title:** `[DD001] Validate and adopt existing KVS-1 (Kv Shaker) and EGL-36 (ERG) NeuroML2 channels into c302 library`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (KVS-1 and EGL-36 rows, HIGH priority)
- **Depends On:** Issue 5 (survey)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/AWCon_kvs1.channel.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **KVS-1 already exists in validated NeuroML2** (AWCon model)
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/RMD_egl36.channel.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **EGL-36 already exists in validated NeuroML2** (RMD model)
    - [`NicolettiEtAl2024_MN_IN/kvs1.mod`, `egl36.mod`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — NMODL references
    - `ChannelWorm2/raw_data/JSON/` — Experimental I-V data for KVS-1 and EGL-36
- **Approach:** **Validate and adopt** the existing NeuroML2 channels from NicolettiEtAl2019. Both channels already exist — reconcile and integrate.
- **Files to Modify:**
    - `channel_models/kvs1_shaker.channel.nml` (adopted)
    - `channel_models/egl36_erg.channel.nml` (adopted)
    - `tests/test_kvs1_channel.py` (new)
    - `tests/test_egl36_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/kvs1_shaker.channel.nml`
    - `jnml -validate channel_models/egl36_erg.channel.nml`
    - `pytest tests/test_kvs1_channel.py tests/test_egl36_channel.py`
- **Acceptance Criteria:**
    - [ ] Both channels adopted from existing NicolettiEtAl2019 NeuroML2 — not reimplemented
    - [ ] KVS-1: Shaker-type voltage-gated K⁺ channel with fast activation kinetics
    - [ ] EGL-36: ERG-type K⁺ channel with characteristic slow inactivation recovery
    - [ ] I-V curves match NMODL references within ±5%
    - [ ] All kinetics documented with literature sources
    - [ ] Unit tests compare NeuroML outputs against NMODL references
- **Sponsor Summary Hint:** Both KVS-1 and EGL-36 already exist as validated NeuroML2 files from Nicoletti et al. 2019. This issue adopts them into c302's channel library with validation against experimental data and NMODL references.

---

### Issue 9: Adopt or convert remaining MEDIUM-priority channels into c302

- **Title:** `[DD001] Adopt existing NeuroML2 or convert NMODL for MEDIUM-priority channels (CCA-1, EGL-2, KQT-3, SLO-2, KCNL, IRK, NCA)`
- **Labels:** `DD001`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) (MEDIUM priority rows)
- **Depends On:** Issues 7-9 (HIGH priority channels establish the adoption/validation workflow)
- **Existing Code to Reuse:**
    - **Already in NeuroML2 (NicolettiEtAl2019):** CCA-1 (`AWCon_cca.channel.nml`), EGL-2 (`AWCon_egl2.channel.nml`), KQT-3 (`AWCon_kqt3.channel.nml`), SLO-2 (`AWCon_slo2.channel.nml`), SK/KCNL (`AWCon_sk.channel.nml`), IRK/KIR (`AWCon_kir.channel.nml`), NCA (`AWCon_nca.channel.nml`) — **ALL 7 channels already exist in validated NeuroML2**
    - **NMODL references (NicolettiEtAl2024):** `cca1.mod`, `egl2.mod`, `kqt3.mod`, `slo2egl19.mod`/`slo2unc2.mod`/`slo2iso.mod`, `kcnl.mod`, `irk.mod`, `nca.mod`
    - **ChannelWorm2:** `SLO-2.channel.nml` (older NeuroML2 with Boyle & Cohen parameters)
    - **BAAIWorm per-neuron conductances:** `eworm/components/param/cell/*.json` — max conductance values for every channel in every neuron (302 neurons × ~15 channels)
- **Approach:** **Adopt all 7 from NicolettiEtAl2019 NeuroML2** — they already exist and are validated. Reconcile with NicolettiEtAl2024 variants where parameters differ. This should be primarily validation and integration work, not conversion.
- **Files to Modify:**
    - `channel_models/cca1_cav3.channel.nml` (adopted)
    - `channel_models/egl2_eag.channel.nml` (adopted)
    - `channel_models/kqt3_kcnq.channel.nml` (adopted)
    - `channel_models/slo2_sk.channel.nml` (adopted)
    - `channel_models/kcnl2_sk.channel.nml` (adopted)
    - `channel_models/irk_kir.channel.nml` (adopted)
    - `channel_models/nca_na.channel.nml` (adopted)
    - `tests/test_medium_channels.py` (new)
- **Test Commands:**
    - `for f in channel_models/*.nml; do jnml -validate $f; done`
    - `pytest tests/test_medium_channels.py`
- **Acceptance Criteria:**
    - [ ] All 7 channels adopted from existing NicolettiEtAl2019 NeuroML2 — conversion from NMODL only if no NeuroML2 version exists after Issue 5 survey
    - [ ] Each passes `jnml -validate`
    - [ ] I-V curves match NMODL references within ±5%
    - [ ] Parameters reconciled against NicolettiEtAl2024 and ChannelWorm2 where applicable; discrepancies documented
    - [ ] All kinetics documented with literature sources
    - [ ] Total channel library: 4 existing + 4 HIGH + 7 MEDIUM = 15 channels
- **Sponsor Summary Hint:** Here's the plot twist: all 7 MEDIUM-priority channels already exist in NeuroML2 from Nicoletti et al. 2019's AWCon model. This issue validates and adopts them into c302's channel library — turning what looked like weeks of conversion work into a validation and integration task.

---

### Issue 10: Create channel library test suite with voltage-clamp protocols

- **Title:** `[DD001] Create comprehensive channel library test suite with standard voltage-clamp protocols`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#extended-ion-channel-library-phase-1-2) and [DD001 — Quality Criteria](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#quality-criteria) (criterion 3: biophysical units)
- **Depends On:** Issues 6-9 (channel adoptions)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2024_MN_IN/*_vclamp.py`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — Voltage-clamp simulation scripts already exist for VA5, VB6, VD5 neurons. Includes conductance unit conversion utilities (`g_to_Scm2.py`, `g_to_nS.py`).
    - [`BAAIWorm/eworm/ion_channel_tune/`](https://github.com/Jessie940611/BAAIWorm) — Channel validation scripts with result PNG plots for each channel against published I-V curves
    - [`ChannelWorm2/raw_data/JSON/`](https://github.com/openworm/ChannelWorm2) — **200+ digitized experimental I-V curves** across species — use C. elegans-specific data for validation targets
    - `c302/examples/parametersweep/` — Parameter sweep infrastructure with firing rate analysis and heatmap generation
- **Approach:** **Adapt existing voltage-clamp protocols** from NicolettiEtAl2024 and BAAIWorm validation scripts. Use ChannelWorm2's experimental I-V data as validation targets.
- **Files to Modify:**
    - `tests/test_channel_library.py` (new — adapted from existing vclamp scripts)
    - `tests/protocols/` (new — voltage clamp protocol files)
- **Test Commands:**
    - `pytest tests/test_channel_library.py -v`
- **Acceptance Criteria:**
    - [ ] Standard voltage-clamp protocol: step from -80mV to -60,-40,-20,0,+20,+40 mV
    - [ ] For each channel: measure peak current, steady-state current, activation time constant
    - [ ] Compare against published electrophysiology data where available (use ChannelWorm2 JSON data)
    - [ ] Generate I-V curve plots for each channel (saved as PNG test artifacts)
    - [ ] Verify units are correct (conductance in nS, voltage in mV, time in ms)
    - [ ] Detect common errors: reversed polarity, wrong magnitude, unrealistic kinetics
    - [ ] All 15 channels pass the test suite
- **Sponsor Summary Hint:** A voltage-clamp test suite built on existing validation scripts from Nicoletti et al. and BAAIWorm, plus 200+ digitized experimental I-V curves from ChannelWorm2 as ground truth. Calibrating 15 ion channels against their published spec sheets.

---

## Group 4: Synaptic Optimization

Target: Per-synapse conductance optimization using differentiable simulation and neurotransmitter identity constraints.

---

### Issue 11: Consolidate existing neurotransmitter data into synapse polarity constraints

- **Title:** `[DD001] Consolidate existing neurotransmitter identity data from c302, wormneuroatlas, and Wang et al. 2024 into validated synapse polarity constraints`
- **Labels:** `DD001`, `human-expert`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, neuroscience
- **DD Section to Read:** [DD001 — Synaptic Weight and Polarity Optimization](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#synaptic-weight-and-polarity-optimization) (neurotransmitter identity constraints)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`c302/data/GABA.py`](https://github.com/openworm/c302) — GABAergic neuron identity vector (binary, 279 neurons). Already used in c302 network generation.
    - [`c302/data/Bentley_et_al_2016_expression.csv`](https://github.com/openworm/c302) — Comprehensive CSV with neurotransmitter identities (Dopamine, Serotonin, GABA, etc.), neuropeptide expression, and receptor expression per neuron, with evidence citations.
    - [`c302/__init__.py` `generate()` function](https://github.com/openworm/c302) — Already uses `synclass` to set synapse polarity (excitatory vs inhibitory) during network generation.
    - [`wormneuroatlas/SynapseSign.py`](https://github.com/openworm/wormneuroatlas) — Synapse sign predictions from Fenyves et al. 2020, accessible via `NeuroAtlas.get_synapse_sign()`.
    - [`BAAIWorm/eworm/components/cb2022_data/`](https://github.com/Jessie940611/BAAIWorm) — Calcium correlation data used for model fitting
- **Approach:** **Consolidate and validate** existing data sources — c302 already has neurotransmitter data in multiple places (GABA.py, Bentley CSV, synclass in generate()). Merge these with wormneuroatlas SynapseSign data, update with Wang et al. 2024 where it supersedes older sources, and create a single validated constraint module.
- **Files to Modify:**
    - `c302/data/neurotransmitter_identities.csv` (new — consolidated from existing sources)
    - `c302/synapse_constraints.py` (new — wrapping existing polarity logic)
- **Test Commands:**
    - `python3 -c "from c302 import synapse_constraints; sc = synapse_constraints.load(); print(sc.get_polarity('AVAL', 'AVAR'))"`
    - `pytest tests/test_synapse_constraints.py`
- **Acceptance Criteria:**
    - [ ] Consolidates neurotransmitter data from: c302 GABA.py, Bentley et al. 2016 CSV, wormneuroatlas SynapseSign, and Wang et al. 2024
    - [ ] Documents where sources agree and disagree; flags conflicts for expert review
    - [ ] Map neurotransmitter type to synapse polarity: glutamatergic → excitatory, GABAergic → inhibitory, cholinergic → excitatory (with exceptions)
    - [ ] Provide a Python API: `get_polarity(pre, post)` returns +1 (excitatory) or -1 (inhibitory)
    - [ ] Flag synapses where polarity is ambiguous or unknown
    - [ ] Data stored in version-controlled CSV with provenance
    - [ ] Unit tests verify known polarity assignments (e.g., DD/VD GABAergic → inhibitory)
- **Sponsor Summary Hint:** c302 already has neurotransmitter data scattered across multiple files (GABA.py, Bentley CSV, synclass logic) and wormneuroatlas provides synapse sign predictions. This issue consolidates all of it — plus newer Wang et al. 2024 data — into a single validated constraint module, so the synapse optimizer can't violate known biology.

---

### Issue 12: Add `neural.synapse_optimization` config toggle

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

### Issue 13: Create thin adapter for Randi 2023 functional connectivity via wormneuroatlas

- **Title:** `[DD001] Create adapter for Randi 2023 functional connectivity matrix using wormneuroatlas API`
- **Labels:** `DD001`, `ai-workable`, `L2`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroscience
- **DD Section to Read:** [DD001 — Synaptic Weight and Polarity Optimization](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#synaptic-weight-and-polarity-optimization) (full 302-neuron optimization) and Reference 14 (Kato et al. 2015 PCA validation)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`wormneuroatlas`](https://github.com/openworm/wormneuroatlas) — **The Randi 2023 signal propagation atlas is already included** as `funatlas.h5` with a clean Python API: `NeuroAtlas.get_signal_propagation_atlas(strain="wt")`. Supports WT and unc-31 strains. Handles neuron ID conventions and bilateral/dorsoventral merging.
    - [`c302/examples/test/test_WNA.py`](https://github.com/openworm/c302) — Already tests wormneuroatlas integration including gap junctions, chemical synapses, and neurotransmitter sign
    - [`BAAIWorm/eworm/components/cb2022_data/Ca_corr_mat.txt`](https://github.com/Jessie940611/BAAIWorm) — Same underlying Randi data in matrix form, used for BAAIWorm model fitting
- **Approach:** **Thin adapter on wormneuroatlas** — the data loading is essentially a one-liner (`NeuroAtlas.get_signal_propagation_atlas()`). The real work is neuron name mapping to c302 conventions and the `compare_to_simulation()` utility.
- **Files to Modify:**
    - `c302/data/randi2023_functional_connectivity.py` (new — thin adapter)
    - `tests/test_randi_data.py` (new)
- **Test Commands:**
    - `python3 -c "from c302.data import randi2023_functional_connectivity as rfc; m = rfc.load_correlation_matrix(); print(m.shape)"`
    - `pytest tests/test_randi_data.py`
- **Acceptance Criteria:**
    - [ ] Loads Randi 2023 data via `wormneuroatlas.NeuroAtlas.get_signal_propagation_atlas()` — does NOT duplicate the dataset
    - [ ] Maps neuron IDs from wormneuroatlas convention to c302 neuron names
    - [ ] Handle missing neurons gracefully (not all 302 are in the imaging data)
    - [ ] Provide utility: `compare_to_simulation(sim_calcium_matrix)` → Pearson correlation
    - [ ] Unit tests verify matrix is symmetric, diagonal is 1.0, shape is correct
- **Sponsor Summary Hint:** Randi et al. (2023) recorded nearly every neuron in the worm's brain simultaneously — and the data is already in wormneuroatlas with a clean Python API. This issue writes a thin adapter that maps wormneuroatlas neuron names to c302's conventions, plus a comparison utility for optimization. The hard data work is already done.

---

## Group 5: Level D Multicompartmental Development

Target: Multicompartmental neuron models for neurons where single-compartment approximation is insufficient.

---

### Issue 14: Evaluate and refine existing NeuroML2 morphologies for Level D neurons

- **Title:** `[DD001] Evaluate existing CElegansNeuroML morphologies for AWC, AIY, AVA, RIM, VD5 and refine for Level D`
- **Labels:** `DD001`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, neuroanatomy
- **DD Section to Read:** [DD001 — Level D Multicompartmental](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#level-d-multicompartmental-cable-equation-models-expanded-roadmap) (Stage 1, step 2)
- **Depends On:** Issue 5 (channel survey, which also catalogs morphology sources)
- **Existing Code to Reuse:**
    - [`CElegansNeuroML/CElegans/generatedNeuroML2/`](https://github.com/openworm/CElegansNeuroML) — **All 302 neurons already exist as multicompartmental NeuroML2 cells** with realistic 3D morphology (derived from VirtualWorm Blender files). Includes `AWCL.cell.nml`, `AWCR.cell.nml`, `AIYL.cell.nml`, `AIYR.cell.nml`, `AVAL.cell.nml`, `AVAR.cell.nml`, `RIML.cell.nml`, `RIMR.cell.nml`, `VD5.cell.nml` — all 5 target neurons.
    - [`BAAIWorm/eworm/components/model/`](https://github.com/Jessie940611/BAAIWorm) — HOC files for every neuron with multi-compartment morphology and biophysical parameters. Includes per-neuron conductance JSONs specifying which channels are expressed where.
    - [`c302/NeuroML2/`](https://github.com/openworm/c302) — Another copy of all 302 neuron morphologies already in the c302 repo
- **Approach:** **Evaluate existing morphologies, do not recreate.** The NeuroML2 morphologies for all 5 target neurons already exist in two repos. Evaluate whether they meet Level D requirements (segment length < 2µm, segment group annotations). Compare against BAAIWorm HOC files for discrepancies. Refine as needed.
- **Files to Modify:**
    - `morphologies/AWC.cell.nml` (refined from existing CElegansNeuroML, if needed)
    - `morphologies/AIY.cell.nml` (refined)
    - `morphologies/AVA.cell.nml` (refined)
    - `morphologies/RIM.cell.nml` (refined)
    - `morphologies/VD5.cell.nml` (refined)
- **Test Commands:**
    - `for f in morphologies/*.nml; do jnml -validate $f; done`
- **Acceptance Criteria:**
    - [ ] Start from existing CElegansNeuroML morphologies — do NOT recreate from SWC
    - [ ] Compare existing NeuroML2 morphologies against BAAIWorm HOC files; document discrepancies
    - [ ] Segments < 2 µm length (adequate spatial resolution for cable equation); refine if existing segmentation is too coarse
    - [ ] Segment groups defined: soma, axon, dendrite (where applicable)
    - [ ] All pass `jnml -validate`
    - [ ] Can be loaded by NEURON simulator (via pyNeuroML export)
    - [ ] Soma diameter matches known values (WormAtlas)
- **Sponsor Summary Hint:** Here's the surprise: multicompartmental NeuroML2 morphologies for all 302 neurons already exist in CElegansNeuroML and are already copied into c302. This issue evaluates whether those existing morphologies are detailed enough for Level D cable-equation simulation, compares them against BAAIWorm's independently derived morphologies, and refines where needed. Evaluation, not creation.

---

### Issue 15: Integrate existing components into AWC Level D proof-of-concept

- **Title:** `[DD001] Integrate existing Nicoletti AWCon channels + CElegansNeuroML morphology into c302 Level D AWC proof-of-concept`
- **Labels:** `DD001`, `human-expert`, `L3`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Level D Multicompartmental](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#level-d-multicompartmental-cable-equation-models-expanded-roadmap) (Stage 1, steps 3-4) and Reference 16 (Nicoletti et al. 2019 AWCon model)
- **Depends On:** Issue 14 (AWC morphology evaluation), Issues 6-9 (adopted channel library)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/AWCon.cell.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **Complete AWCon single-compartment model with ALL 16 channels in NeuroML2**, validated against XPP original. Includes `CaDynamics.nml` for calcium concentration dynamics and `GenerateNeuroML.py` for programmatic cell generation.
    - [`CElegansNeuroML/CElegans/generatedNeuroML2/AWCL.cell.nml`](https://github.com/openworm/CElegansNeuroML) — AWC multicompartmental morphology
    - [`c302/parameters_D.py`](https://github.com/openworm/c302) — **Level D framework already exists** with multicompartmental infrastructure, `ChannelDensity` support, `Species` (Ca), and `FixedFactorConcentrationModel`. Currently uses "BlindGuess" placeholder channels (generic leak + k_slow). The framework is ready — just needs real channel models plugged in.
    - [`BAAIWorm/eworm/components/param/cell/`](https://github.com/Jessie940611/BAAIWorm) — Per-neuron JSON with max conductance for each channel — use AWC entry for channel density distribution guidance
- **Approach:** **Integration, not creation.** The channels exist (NicolettiEtAl2019). The morphology exists (CElegansNeuroML). The Level D framework exists (c302 parameters_D.py). This issue combines them: distribute NicolettiEtAl2019's 16 AWCon channel models across the existing AWC morphology, using BAAIWorm's conductance JSONs for distribution guidance, within c302's existing Level D framework.
- **Files to Modify:**
    - `c302/c302_MultiComp_AWC.py` (new — or extend existing Level D template)
    - `tests/test_awc_multicomp.py` (new)
- **Test Commands:**
    - `jnml -validate morphologies/AWC.cell.nml`
    - `jnml LEMS_AWC_test.xml -nogui`
    - `pytest tests/test_awc_multicomp.py`
- **Acceptance Criteria:**
    - [ ] AWC multicompartmental model built by combining existing NicolettiEtAl2019 channels with existing CElegansNeuroML morphology — not reimplemented
    - [ ] Per-segment channel densities assigned from adopted channel library (Issues 6-9), guided by BAAIWorm conductance data
    - [ ] Passive parameters (axial resistance, membrane capacitance) fitted to match AWC electrophysiology
    - [ ] Reproduces published AWC responses (Nicoletti et al. 2019) within ±15%
    - [ ] Simulates in NEURON via pyNeuroML export
    - [ ] Can coexist with Level C1 single-compartment neurons in the same network
    - [ ] Documents which existing components were combined and any modifications made
- **Sponsor Summary Hint:** The channels exist (16 in NeuroML2 from Nicoletti). The morphology exists (CElegansNeuroML). The Level D framework exists (c302 parameters_D.py with placeholder channels). This issue plugs real channels into a real morphology in an existing framework — proving that Level D multicompartmental neurons work. Three existing codebases, one integration task.

---

## Group 6: Documentation & Contributor Support

Target: Enable new contributors to understand and modify the neural circuit model.

---

### Issue 16: Create c302 architecture overview for contributors

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

### Issue 17: Create c302 CONTRIBUTING.md

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

### Issue 18: Document c302 level comparison with runnable examples

- **Title:** `[DD001] Document c302 levels A-D with runnable comparison examples`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, docs
- **DD Section to Read:** [DD001 — Architecture Levels](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#architecture-levels)
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

### Issue 19: Audit existing c302 test suite and document coverage

- **Title:** `[DD001] Audit existing c302 test suite and document test coverage`
- **Labels:** `DD001`, `ai-workable`, `L1`
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD001 — Quality Criteria](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/#quality-criteria) (criterion 3)
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

## Infrastructure (Cross-Group)

---

### Issue 20: Add `neural.spatial_synapses` config toggle for Level D

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

### Issue 21: Create c302 changelog documenting framework evolution

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
| **Total Issues** | 23 |
| **ai-workable** | 12 |
| **human-expert** | 11 |
| **L1** | 5 |
| **L2** | 11 |
| **L3** | 7 |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Validation Infrastructure** | 1–3 | Trajectory tools (ported from existing C++), output format audit. Kinematic regression detection moved to [DD021](DD021_draft_issues.md). |
| **2: Data Pipeline** | 4 | OME-Zarr export |
| **3: Ion Channel Library** | 5–10 | Survey + adopt/validate 14 channels from existing NeuroML2 and NMODL |
| **4: Synaptic Optimization** | 11–13 | Consolidate neurotransmitter data, weight fitting prep |
| **5: Level D Development** | 14–15 | Evaluate existing morphologies, integrate AWC proof-of-concept |
| **6: Documentation** | 16–19 | Architecture docs, contributing guide, level comparison |
| **Infrastructure** | 20–21 | Config toggles, changelog |

### Cross-References

| Related DD | Relationship |
|------------|-------------|
| **[DD021](DD021_draft_issues.md) (Movement Toolbox)** | **Kinematic validation scripts moved there** — DD021 Issues 1-2 (`check_regression.py`, Schafer baseline) were originally DD001 Issues 3-4. DD001 is a consumer of DD021's validation pipeline. |
| DD002 (Muscle Model) | DD002 Issue 18 documents `sibernetic_c302.py` coupling bridge |
| DD003 (Body Physics) | Issue 2 (extract_trajectory.py) |
| DD010 (Validation Framework) | Issues 1, 2 produce WCON consumed by DD010 Tier 3 |
| DD013 (Simulation Stack) | Issues 12, 20 (config toggles depend on openworm.yml schema); DD013 Issue 24 covers c302 notebook |
| DD014 (Dynamic Visualization) | Issue 4 (OME-Zarr export for viewer) |
| DD017 (Hybrid ML) | Issue 12 (synapse optimization toggle, actual optimization via DD017) |
| DD020 (Connectome Data Access) | Issue 11 (neurotransmitter data consolidation) |

### Dependency Graph (Critical Path)

```
Issue 3 (output format audit)
  └→ Issue 4 (OME-Zarr export)

Issue 1 (boyle_berri_cohen_trajectory.py — port existing C++) — independent, fast path
Issue 2 (extract_trajectory.py — adapt Sibernetic generate_wcon.py) — depends on DD003
  ├→ [both Issue 1 and Issue 2 produce WCON for DD021 regression checking]

Issue 5 (channel survey across ALL repos — reconciliation matrix)
  ├→ Issue 6 (adopt EGL-19 from NicolettiEtAl2019)   ─┐
  ├→ Issue 7 (adopt SLO-1 from NicolettiEtAl2019)     ├→ Issue 9 (adopt MEDIUM channels)
  └→ Issue 8 (adopt KVS-1, EGL-36)                    ─┘    └→ Issue 10 (channel test suite)
  └→ Issue 14 (evaluate existing morphologies)
       └→ Issue 15 (AWC Level D integration — channels + morphology + framework)

Issue 11 (consolidate neurotransmitter constraints) — independent
Issue 12 (synapse_optimization config) — depends on DD013 Issue 1
Issue 13 (Randi 2023 adapter via wormneuroatlas) — independent

Issue 20 (spatial_synapses config) — depends on DD013 Issue 1

Issues 16, 17, 18, 19, 21 (docs/infra) — independent

Kinematic validation (check_regression.py, Schafer baseline) → see DD021 Issues 1-2
```
