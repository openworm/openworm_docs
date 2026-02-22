# OpenWorm Modeling Phase Roadmap
- **Version:** 1.0
- **Created:** 2026-02-19
- **Purpose:** Master timeline for Design Document implementation with visible milestones

---

## Mission, Vision, and Principles

### Mission (from openworm.org)

**"OpenWorm is an open source project dedicated to creating the world's first virtual organism in a computer, a *C. elegans* nematode."**

### Vision

**"Building the first digital life form. Open source."**

### Core Principles

1. **Physical Realism:** "Worms are soft and squishy. So our model has to be too. We are building in the physics of muscles, soft tissues and fluids. Because it matters."

2. **Multi-Scale Integration:** From ion channels (angstroms) to neurons (micrometers) to organs (hundreds of micrometers) to organism behavior (millimeters, seconds to minutes).

3. **Experimental Validation:** Every model must be validated against real *C. elegans* data — electrophysiology, calcium imaging, and behavior. We don't build plausible models; we build **validated** models.

4. **Open Science:** All code, data, and Design Documents are open source. No proprietary IP, no paywalls, no secrets.

5. **Causal Interpretability:** We can trace *why* behavior emerges through the mechanistic causal chain. Every parameter has physical meaning. Black-box ML is used only at boundaries ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)), never replacing the mechanistic core.

### How This Roadmap Serves the Mission

- **The Mission says:** "world's first virtual organism."
- **This Roadmap delivers:** 959-cell whole-organism simulation (Phase 4) with neurons, muscles, pharynx, intestine, hypodermis, reproductive system — validated against experimental data at three scales ([DD010](DD010_Validation_Framework.md) Tier 1-3).

- **The Vision says:** "digital life form."
- **This Roadmap delivers:** Not just anatomy (static 3D models exist), but **dynamic temporal behavior** — pumping, defecating, egg-laying, locomoting, responding to touch — emergent from coupled biophysical subsystems.

- **The Principles say:** "soft and squishy... physics matters."
- **This Roadmap delivers:** SPH body physics ([DD003](DD003_Body_Physics_Architecture.md)), calcium-force muscle coupling ([DD002](DD002_Muscle_Model_Architecture.md)), fluid-structure interaction, mechanical cell identity ([DD004](DD004_Mechanical_Cell_Identity.md)). The worm deforms realistically because the physics is realistic.

---

## Overview

OpenWorm's path from 302 generic neurons to 959 differentiated cells is organized into **7 implementation phases** over ~18-24 months. Each phase has:

1. **Clear scope** (which DDs belong to it)
2. **Visible milestone** (what we can announce when complete)
3. **Timeline estimate** (weeks/months)
4. **Success criteria** (how we know it's done)
5. **Blocking dependencies** (what must be done first)

**The North Star:** By end of Phase 4, OpenWorm simulates a complete adult hermaphrodite *C. elegans* with 959 differentiated cells, validated against experimental data at multiple scales (electrophysiology, neural recordings, behavior), with an interactive 3D viewer anyone can explore in a web browser.

---

## Phase 0: Existing Foundation (Accepted, Working)

**Status:** ✅ **Complete** (but needs containerization work per Phase A)

**Scope:**

| DD | Title | Implementation Status |
|----|-------|---------------------|
| [DD001](DD001_Neural_Circuit_Architecture.md) | Neural Circuit Architecture | ✅ c302 Levels A-D exist, generate NeuroML networks |
| [DD002](DD002_Muscle_Model_Architecture.md) | Muscle Model Architecture | ✅ GenericMuscleCell exists, Ca²⁺→force coupling works |
| [DD003](DD003_Body_Physics_Architecture.md) | Body Physics Architecture | ✅ Sibernetic v1.0+ works (OpenCL backend stable) |
| [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | Connectome Data Access | ✅ `cect` v0.2.7 exists (needs version pinning per [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) |

**What Works Today:**

- 302 identical neurons (Level C1 graded synapses)
- 95 body wall muscles with calcium-force coupling
- ~100K SPH particles (fluid-structure interaction)
- Coupled simulation via `sibernetic_c302.py`
- 15ms simulations produce movement (validated against Schafer lab kinematics)
- ConnectomeToolbox provides [Cook2019](https://doi.org/10.1038/s41586-019-1352-7), Witvliet, Randi, Ripoll-Sanchez data

**What's Missing (addressed in Phase A):**

- No config system (parameters hardcoded in `master_openworm.py`)
- No docker-compose (raw shell scripts)
- No dependency pinning (branch names, not commits)
- No automated validation (Tier 3 toolbox is broken)
- Video pipeline has memory leak (OOMs >2s simulations)

**Milestone:** *(Already achieved)* **"First Whole-Nervous-System Simulation"**

- **What you run:** `python master_openworm.py` — coupled c302 + Sibernetic simulation, 15ms of worm locomotion
- **What you see:** ~100K SPH particles forming a worm shape that bends and propagates undulatory waves. Voltage traces for 302 neurons. Muscle activation patterns.
- **Validated against:** [Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560) Schafer lab kinematic features — locomotion speed, body curvature, wave frequency within ±15% of wild-type N2
- **Published:** [Sarma et al. 2018](https://doi.org/10.1098/rstb.2017.0382), [Gleeson et al. 2018](https://doi.org/10.1098/rstb.2017.0379)

---

## Phase A: Infrastructure Bootstrap (Weeks 1-4)

**Status:** ⚠️ **Proposed** — Must complete before modeling phases proceed

**Scope:**

| DD | Title | Owner | Effort | Blocking |
|----|-------|-------|--------|----------|
| **[DD013](DD013_Simulation_Stack_Architecture.md)** | Simulation Stack Architecture | Integration L4 (TBD) | ~40 hours | **CRITICAL** — All phases need this |
| **[DD008](DD008_Data_Integration_Pipeline.md)** | Data Integration Pipeline (OWMeta) | Data L4 (TBD) | ~30 hours | **Data layer** — Phase 1+ datasets need unified access |
| **[DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** | Movement Toolbox Revival | Validation L4 (TBD) | ~33 hours | **Tier 3 validation** |
| [DD012](DD012_Design_Document_RFC_Process.md) | Design Document RFC Process | Founder | ~8 hours | Governance |
| [DD011](DD011_Contributor_Progression_Model.md) | Contributor Progression Model | Founder | ~8 hours | Governance |
| [DD015](DD015_AI_Contributor_Model.md) | AI-Native Contributor Model | Founder | ~12 hours | Governance (AI agent workflow) |
| **[DD024](DD024_Validation_Data_Acquisition_Pipeline.md)** | Validation Data Acquisition Pipeline | Validation L4 (TBD) | ~18 hours | All validation tiers — data must exist before validation can run |
| **[DD025](DD025_Protein_Foundation_Model_Pipeline.md)** | Foundation Model Channel Kinetics | ML/Structural Bio (TBD) | ~20 hours | Parallel (derisks [DD005](DD005_Cell_Type_Differentiation_Strategy.md)) |

**Key Deliverables:**

1. **`openworm.yml`** config schema ([DD013](DD013_Simulation_Stack_Architecture.md)) — Single source of truth for simulation parameters
2. **Multi-stage Docker** build ([DD013](DD013_Simulation_Stack_Architecture.md)) — Subsystem caching, contributor override (--build-arg)
3. **`docker-compose.yml`** ([DD013](DD013_Simulation_Stack_Architecture.md)) — quick-test, simulation, validate, viewer, shell services
4. **`versions.lock`** ([DD013](DD013_Simulation_Stack_Architecture.md)) — Pin exact commits for c302, Sibernetic, cect, toolbox
5. **Revived analysis toolbox** ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) — Python 3.12 compatible, 5 metrics extractable, WCON parser works
6. **Contributor workflow** ([DD013](DD013_Simulation_Stack_Architecture.md)) — Fork subsystem → build with custom branch → quick-test → validate → PR
7. **OWMeta data bundles** ([DD008](DD008_Data_Integration_Pipeline.md)) — Unified Python API for connectome, CeNGEN, cell positions, neuropeptide data; WBbt ID normalization across all datasets
8. **AI contributor workflow** ([DD015](DD015_AI_Contributor_Model.md)) — Agent registration system, DD→GitHub issue decomposition, AI pre-review pipeline, human final-approval gates
9. **Channel kinetics predictions** ([DD025](DD025_Protein_Foundation_Model_Pipeline.md)) — Cross-validation of foundation model predictions against ~50-100 channels with known kinetics; `channel_kinetics_predictions.csv` ready for [DD005](DD005_Cell_Type_Differentiation_Strategy.md) integration

**Milestone:** 🎉 **"Containerized Stack with Automated Validation"**

- **What you run:** `docker compose run quick-test` (completes in <5 min) — builds the full simulation stack, runs a short simulation, checks for crashes
- **What you see:** Terminal output showing build → simulate → validate pipeline. JSON report with pass/fail on each metric. Video of worm locomotion (no more OOM at >2s).
- **Then try:** `docker compose run validate` — runs Tier 2 (functional connectivity vs. [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4)) + Tier 3 (kinematics vs. [Yemini 2013](https://doi.org/10.1038/nmeth.2560)). Produces `output/validation_report.json` with per-metric scores.
- **Contributor workflow:** Fork a subsystem → `docker compose run quick-test --build-arg C302_BRANCH=my-branch` → see if your change breaks anything → PR with CI green

**Success Criteria:**

- ✅ `docker compose run quick-test` completes in <5 minutes
- ✅ `docker compose run validate` runs Tier 2 functional connectivity + Tier 3 kinematics, produces JSON report
- ✅ `versions.lock` pins c302, Sibernetic, cect, toolbox to exact commits
- ✅ Video pipeline memory leak fixed (can run >2s without OOM)
- ✅ Analysis toolbox installs on Python 3.12, extracts 5 metrics from sample WCON file
- ✅ OWMeta installs, `connect("openworm_data")` returns 302 neurons with WBbt IDs ([DD008](DD008_Data_Integration_Pipeline.md))
- ✅ DD025 cross-validation: predicted kinetics within <30% relative error of measured values for known channels ([DD025](DD025_Protein_Foundation_Model_Pipeline.md))
- ✅ AI contributor registry repo exists, issue auto-generation from DD Integration Contracts demonstrated ([DD015](DD015_AI_Contributor_Model.md))

**Datasets Needed:** See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) for the complete inventory. Key Phase A datasets:

- **Schafer lab N2 baseline kinematics** (WCON format) — Tier 3 validation baseline
- **Randi 2023 functional connectivity** (302×302 correlation matrix) — Tier 2 validation
- **Validation data for digitization** — Thomas 1990, Raizen 1994, O'Hagan 2005, Chalfie 1985
- **DD025 inputs** — Ion channel sequences (WormBase) + known kinetics (~50-100 channels)

**Blocking Dependencies:**

- Recruit Integration L4 Maintainer (owns [DD013](DD013_Simulation_Stack_Architecture.md) implementation)
- Recruit Data L4 Maintainer (owns [DD008](DD008_Data_Integration_Pipeline.md) OWMeta revival)
- Recruit Validation L4 Maintainer (owns [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) revival)

---

## Phase 1: Cell-Type Differentiation (Months 1-3)

**Status:** ⚠️ **Ready to Start** (after Phase A complete)

**Scope:**

| DD | Title | Dependencies | What Changes |
|----|-------|-------------|--------------|
| **[DD005](DD005_Cell_Type_Differentiation_Strategy.md)** | Cell-Type Differentiation Strategy | [DD001](DD001_Neural_Circuit_Architecture.md), [DD008](DD008_Data_Integration_Pipeline.md)/DD020 (CeNGEN) | Replace 302 identical neurons with 128 distinct neuron classes |
| **[DD014](DD014_Dynamic_Visualization_Architecture.md) (Phase 1)** | Post-Hoc Trame Viewer | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD003](DD003_Body_Physics_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Evolve Worm3DViewer from Streamlit to Trame; OME-Zarr export |
| [DD014.1](DD014.1_Visual_Rendering_Specification.md) | Visual Rendering Specification | [DD014](DD014_Dynamic_Visualization_Architecture.md) | Canonical color palette (37 materials), 14 reference mockups, material definitions for all 959 cells |
| **[DD010](DD010_Validation_Framework.md) (Tier 2)** | Functional Connectivity Validation | [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD008](DD008_Data_Integration_Pipeline.md) | Activate Tier 2 blocking gate (r > 0.5 vs. [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4)) |
| [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (integration) | Foundation Model → [DD005](DD005_Cell_Type_Differentiation_Strategy.md) Priors | ML/Structural Bio (TBD) | ~12 hours | Feeds [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration |

**Key Deliverables:**

1. **128 cell-type NeuroML files** (`cells/AVALCell.cell.nml`, etc.) — CeNGEN expression → conductance densities
2. **Calibration parameters CSV** (`data/expression_to_conductance_calibration.csv`) — Fit from ~20 neurons with electrophysiology
3. **Differentiated c302 network** (`LEMS_c302_C1_Differentiated.xml`) — Generated via `python CElegans.py C1Differentiated`
4. **OME-Zarr export pipeline** ([DD014](DD014_Dynamic_Visualization_Architecture.md)) — `master_openworm.py` Step 4b writes `output/openworm.zarr/` with neural/, muscle/, body/ groups
5. **Trame viewer** ([DD014](DD014_Dynamic_Visualization_Architecture.md)) — Replaces Streamlit+stpyvista, supports time animation in browser
6. **Tier 2 validation** ([DD010](DD010_Validation_Framework.md)) — Automated correlation vs. [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4); CI blocks PRs if r < 0.5
7. **Visual rendering spec** ([DD014.1](DD014.1_Visual_Rendering_Specification.md)) — 37-material color palette, activity-state overlays, 14 reference mockups as acceptance tests
8. **WormBrowser enhancement** ([DD014](DD014_Dynamic_Visualization_Architecture.md)) — Click neuron/cell → links to WormAtlas + WormBase on browser.openworm.org (quick win for John White, ~8-16 hrs)

**Milestone:** 🎉 **"Biologically Distinct Neurons"**

- **What you run:** `docker compose run simulation` then `docker compose up viewer` — open `localhost:8501`
- **What you see:** 3D viewer with smooth worm body crawling. Toggle "Neurons" layer — 302 neurons appear, colored by class (128 distinct colors). Click AVAL — inspector panel shows its class-specific voltage and calcium traces, visibly different from ASER or AWCL. Toggle "color by class" mode to see the diversity.
- **Validated against:** [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) whole-brain calcium imaging — simulated functional connectivity correlation improves ≥20% over generic baseline (e.g., r=0.3 → r≥0.36). Side-by-side comparison plot: generic model vs. CeNGEN-parameterized model vs. experimental data.
- **Video:** Time-lapse of simulation with neurons glowing by activity — command interneurons (AVA, AVB) show graded potentials, sensory neurons (ASEL, ASER) show distinct response profiles, motor neurons fire rhythmically driving visible muscle contractions.

**Success Criteria:**

- ✅ All 128 `.cell.nml` files generated without error
- ✅ `jnml -validate` passes for each cell type
- ✅ Tier 2 validation: correlation with [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) improves ≥20% vs. generic baseline
- ✅ Tier 3 validation: kinematic metrics remain within ±15% (no regression)
- ✅ Trame viewer launches via `docker compose up viewer`, shows time-animated worm at localhost:8501
- ✅ OME-Zarr export complete: `neural/`, `muscle/`, `body/` groups all populated

**Datasets Needed:** See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) for the complete inventory. Key Phase 1 datasets:

- **CeNGEN L4 expression** (128 classes × 20,500 genes) — DD005 conductance calibration
- **Electrophysiology training set** (~20 neurons with measured conductances) — DD005 calibration regression
- **Ion channel gene list** (~100 genes) — DD005 gene→channel mapping

**Blocking Dependencies:**

- Phase A complete ([DD013](DD013_Simulation_Stack_Architecture.md) Docker stack, [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) toolbox working)
- CeNGEN data downloaded and validated
- Electrophysiology training set curated (20 neurons with measured conductances)

---

## Phase 2: Slow Modulation + Closed-Loop Sensory (Months 4-6)

**Status:** ⚠️ **Proposed** (ready after Phase 1)

**Scope:**

| DD | Title | Dependencies | What Changes |
|----|-------|-------------|--------------|
| **[DD006](DD006_Neuropeptidergic_Connectome_Integration.md)** | Neuropeptidergic Connectome Integration | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Add 31,479 peptide-receptor interactions as slow modulation layer |
| **[DD019](DD019_Closed_Loop_Touch_Response.md)** | Closed-Loop Touch Response | [DD001](DD001_Neural_Circuit_Architecture.md), [DD003](DD003_Body_Physics_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | MEC-4 mechanotransduction + bidirectional coupling + tap withdrawal |
| [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) | Environmental Modeling & Stimulus Delivery | [DD003](DD003_Body_Physics_Architecture.md), [DD019](DD019_Closed_Loop_Touch_Response.md) | Agar substrate, chemical/thermal gradients, chemotaxis (CI >0.5) + thermotaxis |
| [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) | Proprioceptive Feedback & Motor Coordination | [DD001](DD001_Neural_Circuit_Architecture.md), [DD003](DD003_Body_Physics_Architecture.md), [DD019](DD019_Closed_Loop_Touch_Response.md) | Stretch receptors on B-class motor neurons, wavelength stability ±10% |
| **[DD014](DD014_Dynamic_Visualization_Architecture.md) (Phase 2)** | Interactive Dynamic Viewer | [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 1, [DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD019](DD019_Closed_Loop_Touch_Response.md) | Layer toggle, pharynx/intestine (future), neuropeptide volumetric clouds, validation overlay |
| **[DD001](DD001_Neural_Circuit_Architecture.md) Level D Stage 1** | Multicompartmental Neurons (Proof of Concept) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | 5 representative neurons with 14 ion channel classes, EM morphologies, fitted to electrophysiology |

**Key Deliverables:**

1. **NeuroML peptide extensions** (`lems/PeptideReleaseDynamics.xml`, `lems/PeptideReceptorDynamics.xml`)
2. **Neuropeptidergic adjacency CSV** (31,479 rows: source, target, peptide, receptor, distance, modulation_type)
3. **MEC-4 channel model** (`channel_models/mec4_chan.channel.nml`) — Strain-gated DEG/ENaC channel
4. **Cuticle strain readout** (`sibernetic/coupling/strain_readout.py`) — SPH particles → local strain per touch neuron
5. **Bidirectional coupling** (`sibernetic_c302_closedloop.py`) — Extends existing forward coupling with body→sensory reverse path
6. **Tap stimulus** (`sibernetic/stimuli/tap_stimulus.py`) — Boundary particle displacement, configurable position
7. **Agar substrate + chemical/thermal gradients** ([DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md)) — Steady-state NaCl gradient field, thermal gradient, substrate boundary particles
8. **Stretch receptor channel model** ([DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md)) — Curvature-gated channels on B-class motor neurons (DB, VB), body curvature readout from SPH
9. **Viewer enhancements** ([DD014](DD014_Dynamic_Visualization_Architecture.md)) — Neuropeptide volumetric layer, strain heatmap, reversal event markers, gradient field visualization

**Milestone:** 🎉 **"The Worm Can Feel and Modulate"**

- **What you run:** `docker compose run simulation --config closedloop_touch` then open the viewer
- **Demo 1 — Tap withdrawal:** Worm crawls forward. At t=5s, anterior tap stimulus fires. Watch: touch receptor neurons (ALM, AVM) activate → command interneurons (AVA, AVD) depolarize → motor neurons reverse → worm reverses direction within <1 second, travels backward ≥1 body length, then resumes forward crawling. Compare: `--config openloop` (same tap, no reversal — the worm is deaf).
- **Demo 2 — Neuropeptide knockout:** Run with `neuropeptides.flp_knockout: true`. Watch locomotion pattern change — speed, reversal frequency, body wave amplitude all shift. Compare side-by-side with wild-type. Matches [Li et al. 1999](https://doi.org/10.1111/j.1749-6632.1999.tb07895.x) / [Rogers et al. 2003](https://doi.org/10.1038/nn1140) FLP loss-of-function phenotypes.
- **Validated against:** [Chalfie et al. 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985) tap withdrawal (reversal latency, distance, direction discrimination); [Wicks et al. 1996](https://doi.org/10.1523/JNEUROSCI.16-12-04017.1996) anterior-vs-posterior direction selectivity; ≥3 peptide knockout phenotypes within 30% of experimental measurements.
- **In the viewer:** Neuropeptide volumetric clouds visible as colored mist waxing/waning on seconds timescale. Cuticle strain heatmap shows where the body is being compressed. Reversal events marked on the time scrubber.

**Success Criteria:**

- ✅ Peptide-enabled simulation completes without crash (Tier 3 kinematics not degraded)
- ✅ ≥3 peptide knockout phenotypes reproduced within 30% error ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md) validation)
- ✅ Tap stimulus → reversal onset <1 s, distance ≥1 body length ([DD019](DD019_Closed_Loop_Touch_Response.md) Tier 3)
- ✅ Anterior touch → backward, posterior touch → forward (direction discrimination, [DD019](DD019_Closed_Loop_Touch_Response.md))
- ✅ Closed-loop stable for 30s without NaN/divergence ([DD019](DD019_Closed_Loop_Touch_Response.md) quick-test)
- ✅ Chemotaxis: CI (chemotaxis index) >0.5 on simulated NaCl gradient ([DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md))
- ✅ Thermotaxis: worm navigates to cultivation temperature ±2°C ([DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md))
- ✅ Wavelength stability: ±10% with proprioception enabled (improved from ±15%), >30% degradation when stretch receptors disabled ([DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md))
- ✅ Viewer shows: neuropeptide volumetric clouds, cuticle strain heatmap, reversal event markers, gradient fields

**Datasets Needed:** See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) for the complete inventory. Key Phase 2 datasets:

- **Ripoll-Sanchez 2023 neuropeptide connectome** (31,479 interactions) — DD006 extrasynaptic wiring
- **Touch neuron electrophysiology** (MEC-4 kinetics) — DD019 channel model validation
- **Tap withdrawal behavioral data** (Chalfie 1985, Wicks 1996) — DD019 Tier 3 validation
- **BAAIWorm NMODL + SWC data** — DD001 Level D Stage 1 multicompartmental neurons
- **Chemotaxis and thermotaxis behavioral data** — DD022 Tier 3 validation

**Blocking Dependencies:**

- Phase 1 complete (differentiated neurons are substrate for peptide modulation)
- Ripoll-Sanchez data downloaded and ingested into ConnectomeToolbox/OWMeta
- 3D cell positions extracted (for peptide distance-dependent attenuation)

---

## Phase 3: Organ Systems + Hybrid ML (Months 7-12)

**Status:** ⚠️ **Proposed** (ready after Phase 2)

**Scope:**

| DD | Title | Dependencies | What Adds |
|----|-------|-------------|-----------|
| **[DD007](DD007_Pharyngeal_System_Architecture.md)** | Pharyngeal System Architecture | [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | 63-cell semi-autonomous organ (20 neurons + 20 muscles), 3-4 Hz pumping |
| **[DD009](DD009_Intestinal_Oscillator_Model.md)** | Intestinal Oscillator Model | [DD001](DD001_Neural_Circuit_Architecture.md), [DD004](DD004_Mechanical_Cell_Identity.md) (optional) | 20-cell IP3/Ca oscillator, defecation motor program (50s period) |
| **[DD018](DD018_Egg_Laying_System_Architecture.md)** | Egg-Laying System Architecture | [DD001](DD001_Neural_Circuit_Architecture.md), [DD002](DD002_Muscle_Model_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | 28-cell reproductive circuit (HSN serotonergic, VC cholinergic, 16 sex muscles), two-state pattern |
| **[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)** | Hybrid Mechanistic-ML Framework | [DD001](DD001_Neural_Circuit_Architecture.md)-[DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD010](DD010_Validation_Framework.md) | Differentiable backend (auto parameter fit), SPH surrogate (1000× speedup), learned sensory (Component 3 extracted to [DD025](DD025_Protein_Foundation_Model_Pipeline.md)) |

**Key Deliverables:**

1. **Pharyngeal network** (`LEMS_c302_pharynx.xml`) — 20 neurons + 20 muscles, pumping oscillator module
2. **Intestinal network** (`LEMS_IntestineOscillator.xml`) — 20 cells with IP3R, gap-junction-coupled
3. **Egg-laying network** (`LEMS_c302_EggLaying.xml`) — HSN, VC, vulval/uterine muscles, serotonin/ACh/tyramine synapses
4. **Differentiable worm** (`openworm-ml/differentiable/`) — PyTorch ODE solver, full [DD001](DD001_Neural_Circuit_Architecture.md)+[DD002](DD002_Muscle_Model_Architecture.md)+[DD009](DD009_Intestinal_Oscillator_Model.md) chain
5. **SPH surrogate** (`openworm-ml/surrogate/`) — FNO trained on 500+ SPH runs, <5% trajectory error, 1000× faster
6. **Auto-fitted parameters** — Gradient descent on [DD010](DD010_Validation_Framework.md) validation loss, per-neuron-class conductances

**Milestone:** 🎉 **"From 302 Neurons to 433 Cells — Multi-Organ Simulation"**

- **What you run:** `docker compose run simulation --config full_organism` (runs for ~20 simulated minutes to capture egg-laying cycle). Then open viewer.
- **What you see — 3 organs running simultaneously:**
    - **Pharynx** (toggle layer ON): 63 pharyngeal cells at the head pump rhythmically at 3-4 Hz. Corpus contracts → isthmus peristalsis → terminal bulb grinds. Pharyngeal neurons (MC, M3) fire in sync with the pump cycle. Validated against [Raizen & Avery 1994](https://doi.org/10.1016/0896-6273(94)90207-0) electropharyngeogram recordings.
    - **Intestine** (toggle layer ON): 20 intestinal cells show a calcium wave propagating posterior-to-anterior every ~50 seconds. Cells color from blue→red as [Ca2+] rises. Every wave triggers a visible defecation motor program — body contraction runs anterior-to-posterior. Validated against [Thomas 1990](https://doi.org/10.1093/genetics/124.4.855) (50 ± 10s cycle period).
    - **Egg-laying** (toggle layer ON): HSN neurons fire serotonergic bursts → vulval muscles contract → eggs deposited. Two-state pattern: ~20 min inactive, ~2 min active bout (3-5 eggs). Validated against [Collins et al. 2016](https://doi.org/10.7554/eLife.21126) calcium imaging.
- **Demo — ML surrogate:** `docker compose run surrogate` — same muscle activation input, full SPH takes hours, surrogate completes in <1 minute. Overlay both trajectories: <5% difference. Enables rapid parameter sweeps that were previously impossible.
- **All the while:** Body locomotion continues in background — worm crawls, pharynx pumps, intestine oscillates, eggs are laid. Multiple timescales visible simultaneously (ms for neurons, seconds for pumping, minutes for defecation, tens of minutes for egg-laying).

**Success Criteria:**

- ✅ Pharyngeal pumping frequency: 3-4 Hz ([DD007](DD007_Pharyngeal_System_Architecture.md) Tier 3)
- ✅ Intestinal defecation period: 50 ± 10 s ([DD009](DD009_Intestinal_Oscillator_Model.md) Tier 3)
- ✅ Egg-laying two-state pattern: inactive ~20 min, active ~2 min, 3-5 eggs/bout ([DD018](DD018_Egg_Laying_System_Architecture.md) Tier 3)
- ✅ Differentiable backend matches NEURON/jNML reference within ±5% ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) validation)
- ✅ SPH surrogate achieves <5% trajectory error, ≥100× speedup ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) validation)
- ✅ Auto-fitted parameters equal or improve [DD010](DD010_Validation_Framework.md) scores vs. hand-tuned baseline
- ✅ Body locomotion still within ±15% (no regression from adding organs)

**Datasets Needed:** See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) for the complete inventory. Key Phase 3 datasets:

- **Raizen 1994 EPG recordings** — DD007 pharyngeal validation
- **Thomas 1990 defecation data** — DD009 Tier 3 validation (50s period)
- **Collins 2016 egg-laying calcium imaging** — DD018 validation
- **SPH simulation training set** (500+ runs, ~2,500 GPU-hours) — DD017 surrogate training

**Blocking Dependencies:**

- Phase 1 complete (differentiated neurons)
- Organ-specific validation data curated (pharynx EPG, defecation period, egg-laying patterns)
- GPU cluster access for SPH surrogate training (500+ long runs)

---

## Phase 4: Mechanical Cell Identity + High-Fidelity Visualization (Months 13-18)

**Status:** ⚠️ **Proposed** (ready after Phase 3)

**Scope:**

| DD | Title | Dependencies | What Adds |
|----|-------|-------------|-----------|
| **[DD004](DD004_Mechanical_Cell_Identity.md)** | Mechanical Cell Identity | [DD003](DD003_Body_Physics_Architecture.md), [DD008](DD008_Data_Integration_Pipeline.md), [DD007](DD007_Pharyngeal_System_Architecture.md)/DD009 (cell positions) | Per-particle cell IDs (959 somatic cells), cell-type-specific elasticity/adhesion |
| **[DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md)** | Anatomical Mesh Deformation Pipeline | [DD003](DD003_Body_Physics_Architecture.md), [DD014](DD014_Dynamic_Visualization_Architecture.md) | GPU skinning + cage-based MVC + PBD collision for ~1.6M Virtual Worm vertices |
| **[DD014](DD014_Dynamic_Visualization_Architecture.md) (Phase 3)** | Public Experience Viewer | [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 2, [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) | Three.js + WebGPU, molecular scale, static site deployment, "Digital Organism In Your Browser" |

**Key Deliverables:**

1. **Tagged particle file** (extended SPH_Particle_v2 struct: 44 bytes with `cell_id`, `elasticity_mult`, `adhesion`)
2. **Cell-to-particle mapping** (`data/cell_to_particle_map.json`) — 959 somatic cells → particle indices
3. **Cell boundary meshes** (`data/cell_boundaries/*.obj`) — Per-cell 3D volumes from [Witvliet 2021](https://doi.org/10.1038/s41586-021-03778-8) EM
4. **Deformed Virtual Worm meshes** ([DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md)) — 688 anatomical meshes follow SPH body shape in real-time
5. **Three.js viewer** ([DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 3) — Client-side, no server, molecular scale with gene expression pipeline visible
6. **Static site deployment** — wormsim.openworm.org (GitHub Pages or CDN)

**Milestone:** 🎉 **"WormSim 2.0 — 959-Cell Digital Organism In Your Browser"**

- **What you run:** Open `wormsim.openworm.org` in any browser. No Docker, no installation, no server.
- **What you see — 3 scales of exploration:**
    - **Organism scale (default):** Smooth, translucent *C. elegans* crawling across the screen. Anatomical meshes (688 Virtual Worm pieces) deform with the SPH body in real-time. Pharynx pumps at the head, defecation contractions visible every ~50s.
    - **Tissue/Cell scale (zoom in):** Click any of 959 individually labeled cells. Neurons glow by voltage. Muscles flash by contraction. Intestinal cells show calcium waves. Inspector panel shows cell identity (WBbt ID), real-time traces, and links to WormBase.
    - **Molecular scale (zoom further):** See ion channels opening/closing on a neuron's membrane. Calcium flowing through IP3 receptors in intestinal cells. Gene transcription → mRNA export → ribosomal translation → vesicle trafficking → channel insertion (per [DD014.1](DD014.1_Visual_Rendering_Specification.md) Mockups 13-14).
- **Validated against:** All previous tiers still passing — kinematics ([Yemini 2013](https://doi.org/10.1038/nmeth.2560) ±15%), functional connectivity ([Randi 2023](https://doi.org/10.1038/s41586-023-06683-4)), organ rhythms (pharynx, intestine, egg-laying). Cell-type-specific elasticity produces realistic body mechanics: intestine soft (0.8x), cuticle stiff (5-10x), muscles intermediate (1.5x).
- **Performance:** 60fps on a 2020-era laptop. All 688 meshes deform in <4ms per frame. Progressive OME-Zarr loading — start viewing immediately while more data streams in background.

**Success Criteria:**

- ✅ All 959 somatic cells mapped to ≥1 SPH particle each
- ✅ Cell-type-specific elasticity: intestine (0.8x baseline), cuticle (5-10x), muscles (1.5x), hypodermis (0.5x)
- ✅ Tier 3 validation: kinematic metrics within ±15% with `cell_identity: true` enabled
- ✅ Mesh deformation: All 688 Virtual Worm meshes deform with SPH body, no interpenetration, <4ms per frame (60fps budget)
- ✅ Three.js viewer: 60fps on 2020-era laptop, all 3 scales working, static deployment (no server required)
- ✅ Molecular scale: Gene transcription → mRNA export → ribosomal translation → vesicle trafficking → channel insertion visible ([DD014.1](DD014.1_Visual_Rendering_Specification.md) Mockups 13-14)
- ✅ WormBrowser feature parity: layer peeling, search by cell name, click-to-identify, static hosting — all WormBrowser features matched ([DD014](DD014_Dynamic_Visualization_Architecture.md) checklist)
- ✅ browser.openworm.org redirects to wormsim.openworm.org

**Datasets Needed:** See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) for the complete inventory. Key Phase 4 datasets:

- **Witvliet 2021 cell boundary meshes** — DD004 particle tagging (needs EM conversion)
- **Virtual Worm Blender meshes** (688 meshes, ~1.6M vertices) — DD014.2 deformation
- **Cell-type mechanical properties** — DD004 elasticity/adhesion parameters

**Blocking Dependencies:**

- Phase 3 complete (organ systems implemented)
- Witvliet EM data converted to cell boundary meshes
- Virtual Worm meshes exported from Blender to individual OBJ files
- GPU access for mesh deformation compute shaders (WebGPU or local testing)

---

## Phase 5: Intracellular Signaling Cascades (Months 19-24+)

**Status:** 📝 **Not Yet Specified** — Placeholder for future work

**Anticipated Scope:**

- Detailed GPCR cascades (Gq/Gs/Gi → PLC/adenylyl cyclase → IP3/cAMP → PKA/PKC)
- Second messenger dynamics (IP3, DAG, cAMP, cGMP)
- Channel phosphorylation and trafficking
- Non-neuronal peptide signaling (intestine, hypodermis, gonad)
- Cross-tissue signaling (endocrine, paracrine)

**Why Deferred:**
Current phenomenological models ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md) conductance modulation, [DD009](DD009_Intestinal_Oscillator_Model.md) simplified IP3R) capture functional effects without full biochemical detail. Phase 5 adds mechanistic depth when validation requires it.

**Milestone (Projected):** **"Molecular-Level Intracellular Dynamics"**

**Foundation Model Opportunities ([bio.rodeo](https://bio.rodeo/models))**

Phase 5's biggest blocker is the lack of *C. elegans*-specific biochemical rate constants — most GPCR cascade kinetics come from mammalian systems. Protein foundation models can bridge this gap by predicting binding affinities, conformational dynamics, and pathway structure from sequence rather than requiring per-species experimental measurement:

| Model | Developer | Phase 5 Application |
|-------|-----------|---------------------|
| [Boltz-2](https://github.com/jwohlwend/boltz) | MIT/Recursion | Predict GPCR-G protein complex structures AND second messenger (IP3, cAMP, DAG) binding affinities to target proteins (PKA, PKC, IP3R). Single-GPU, approaching FEP+ accuracy |
| [AlphaFold 3](https://github.com/google-deepmind/alphafold3) | DeepMind | Model full signaling complex assemblies: GPCR→Gα→effector (PLC, adenylyl cyclase) with bound ligands, ions, and lipids |
| [BioEmu-1](https://github.com/microsoft/BioEmu) | Microsoft | Simulate GPCR activation (inactive→active conformational transition), channel phosphorylation-induced gating changes, and kinase catalytic dynamics at 100,000x MD speed — extract rate constants from conformational landscapes |
| [NatureLM](https://github.com/microsoft/NatureLM) | Microsoft | Unified protein + small molecule model (46.7B params). Predict cross-domain interactions: neuropeptide → GPCR → second messenger → kinase. Estimate binding affinities and ADMET properties for signaling molecules |
| [SubCell](https://github.com/CZI-BioHub/SubCell) | CZI/Human Protein Atlas | Subcellular protein localization from microscopy. Map where signaling proteins localize within cells (ER vs. plasma membrane vs. cytoplasm), constraining spatial compartmentalization of cascades. Trained on human cells — would need adaptation for *C. elegans* |
| [OntoProtein](https://github.com/zjunlp/OntoProtein) | Zhejiang University | GO-informed protein-protein interaction prediction. Infer kinase-substrate relationships (which PKA/PKC isoforms phosphorylate which ion channels) from Gene Ontology structure, filling gaps where direct experimental data is unavailable |
| [scPRINT](https://github.com/jkobject/scprint) | Institut Pasteur | Gene network inference from 50M cells. Identify co-regulation patterns between GPCR pathway components in CeNGEN data (e.g., which receptor, G protein, and effector genes are co-expressed in each neuron class), suggesting functional pathway wiring |

**Key insight:** BioEmu-1 + Boltz-2 together could predict most of the "Biochemical rate constants" listed below from protein structure alone — GPCR activation rates from conformational dynamics, second messenger binding K_d from complex prediction, and phosphorylation effects on channel gating from before/after conformational ensembles. This reduces Phase 5's dependency on scarce *C. elegans*-specific experimental kinetics.

**Precedent: Whole-Cell Computational Modeling ([Karr et al. 2012](https://doi.org/10.1016/j.cell.2012.05.044))**

Phase 5's goal — mechanistic intracellular signaling from GPCR activation to channel phosphorylation — is conceptually related to the first whole-cell computational model, built for *Mycoplasma genitalium* by [Karr, Sanghvi, Macklin et al. (2012)](https://doi.org/10.1016/j.cell.2012.05.044) in Markus Covert's lab at Stanford. That model demonstrated that a complete intracellular simulation is achievable:

- **28 submodels** covering DNA replication, transcription, translation, metabolism, protein complexation, and cell division — each using the formalism best suited to its biology (FBA for metabolism, stochastic/Gillespie for transcription, ODE for metabolite dynamics, Boolean logic for gene regulation, Markov chains for RNA degradation)
- **16 shared cell state variables** (chromosome, transcripts, RNA, polypeptides, protein monomers/complexes, metabolites, ribosomes, RNA polymerase, geometry, mass, time, etc.) integrated at 1-second timesteps with sequential random-order execution
- **1,900+ parameters** curated manually from 900+ publications, with cross-species transfer from mammalian/bacterial data filling gaps
- **Validation:** 79% accuracy on gene essentiality predictions; correctly predicted phenotypes for 72% of tested single-gene knockouts

Karr's [2014 Stanford dissertation](https://searchworks.stanford.edu/view/10590731) identified three key limitations that constrained the approach:

1. **Parameter curation bottleneck:** ~6 person-years to manually extract 1,900 rate constants from 900 papers — and *M. genitalium* has only 525 genes (the smallest free-living genome). *C. elegans* has ~20,000 genes.
2. **Cross-species parameter transfer:** ~30% of parameters were borrowed from other organisms (E. coli, yeast, mammalian) due to missing *M. genitalium* measurements. Accuracy of these transfers was unknown.
3. **Scaling challenge:** The hybrid multi-formalism approach worked for a 525-gene minimal cell but was not demonstrated for organisms with thousands of genes and complex multicellular signaling.

**How Foundation Models Transform the Whole-Cell Approach for *C. elegans***

The Karr/Covert limitations that seemed intractable in 2012 are now addressable with the foundation models listed above:

| Karr 2012 Limitation | Foundation Model Solution | Improvement |
|----------------------|--------------------------|-------------|
| **Parameter curation** (6 person-years, 900 papers) | BioEmu-1 predicts conformational dynamics → rate constants from structure alone; Boltz-2 predicts binding affinities from complex structures | Months → days for ~50 key GPCR cascade parameters |
| **Cross-species transfer** (borrowing mammalian rates) | ESM Cambrian / OntoProtein predict *C. elegans*-specific kinetics from worm protein sequences, no need to borrow from mammals | Species-specific predictions from sequence |
| **Pathway inference** (manually reading papers) | scPRINT infers gene regulatory networks from CeNGEN 50M-cell atlas; NatureLM predicts protein-small molecule interactions across domains | Automated pathway wiring from expression data |
| **Scaling to 20,000 genes** | Only ~200-300 signaling genes are relevant to Phase 5 GPCR cascades (not whole-genome); [DD005](DD005_Cell_Type_Differentiation_Strategy.md) CeNGEN data identifies which genes are expressed per cell type | Scoped to signaling genes, not whole genome |
| **Subcellular compartmentalization** (not modeled in Karr) | SubCell predicts protein localization (ER vs. membrane vs. cytoplasm), constraining spatial cascade models | Compartment assignment from microscopy |

The key architectural lesson from Karr et al. is the **hybrid multi-formalism** approach: use ODEs where kinetics are smooth, stochastic simulation where copy numbers are low, and FBA where metabolic flux balance is the right abstraction. Phase 5 should adopt this principle — GPCR cascades are well-suited to ODEs, but stochastic events (neuropeptide vesicle release, channel insertion) may require Gillespie-style simulation.

**Why Phase 5 is tractable even though whole-cell eukaryotic modeling isn't solved yet.** As of 2026, no one has built a Karr-level "every gene product accounted for" whole-cell model of a eukaryotic cell. The Covert lab scaled from *M. genitalium* (525 genes) to [*E. coli* (4,288 genes)](https://github.com/CovertLab/vEcoli) — still prokaryotic but 8x the gene count — and in [2023 extended it to whole-colony simulations](https://doi.org/10.1371/journal.pcbi.1011232) with single-cell heterogeneity. For eukaryotes, the yeast [WM_S288C model](https://doi.org/10.1016/j.bpj.2020.01.040) integrates 15 cellular states and 26 processes across ~6,447 genes, but is described as ["an important first step"](https://doi.org/10.1016/j.tibtech.2021.06.010) rather than complete — the [data integration challenge alone is still being solved](https://doi.org/10.1093/femsyr/foae011) (YCMDB database, 2024). The eukaryotic gap comes from compartmentalization (nucleus, ER, Golgi, mitochondria), complex gene regulation (chromatin, splicing), and intracellular signaling — exactly the biology Phase 5 targets. But Phase 5 does **not** need to be a whole-cell model. It only needs the GPCR→second messenger→channel phosphorylation cascades for the ~200-300 signaling genes expressed in *C. elegans* neurons ([DD005](DD005_Cell_Type_Differentiation_Strategy.md) CeNGEN data scopes this precisely). That is a far more tractable problem than modeling all 20,000 genes, and the foundation models above make it feasible without the 6-person-year parameter curation that even the 525-gene *M. genitalium* model required.

**Datasets Needed:** See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) "Projected Datasets (Phases 5-7)" for inventory. Key needs: biochemical rate constants, proteomics, subcellular calcium imaging, GPCR-G protein coupling specificity — many may be predictable via BioEmu-1 + Boltz-2 foundation models.

---

## Phase 6: Developmental Modeling (Year 2+)

**Status:** 📝 **Not Yet Specified** — Placeholder for multi-stage simulation

**Existing Work: [DevoWorm](../../Projects/DevoWorm/)**

The [DevoWorm project](../../Projects/DevoWorm/) ([devoworm.weebly.com](https://devoworm.weebly.com/), [github.com/devoworm](https://github.com/devoworm)) has been building toward developmental modeling since 2014 as an OpenWorm sub-project. DevoWorm's three research areas map directly onto Phase 6 needs:

- **Developmental Dynamics:** Quantitative embryogenesis datasets, differentiation trees, and embryogenetic connectome analysis — directly applicable to modeling neuron birth order, cell lineage, and stage-specific neural topology
- **Cybernetics and Digital Morphogenesis:** Cellular automata (Morphozoic) and Cellular Potts (CompuCell3D) models of embryogenesis — candidate frameworks for body morphogenesis simulation (L1 ~240 µm → adult ~1000 µm)
- **Reproduction and Developmental Plasticity:** Larval development and life-history data — validation targets for stage-specific behavioral differences

Phase 6 should build on DevoWorm's datasets and models rather than starting from scratch. Key integration points:

- DevoWorm's [embryogenetic connectome](https://github.com/devoworm/embryogenetic-connectome) analysis provides the developmental graph connecting cell lineage to neural circuit formation
- DevoWorm's [differentiation trees](https://www.biorxiv.org/content/early/2016/07/07/062539) complement [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s CeNGEN-based cell-type approach by adding temporal dynamics (when each neuron class differentiates)
- DevoWorm's CompuCell3D models could inform the body size scaling mechanics in [DD003](DD003_Body_Physics_Architecture.md)/[DD004](DD004_Mechanical_Cell_Identity.md)

**Anticipated Scope:**

- Witvliet developmental connectome series (L1 → L2 → L3 → L4 → adult, 8 stages)
- Neuron birth and death (programmed cell death, 131 cells die during development)
- Body size scaling (L1 ~240 µm → adult ~1000 µm)
- Stage-specific validation (L1 locomotion differs from adult)
- CeNGEN L1 expression integration
- Integration of DevoWorm embryogenetic connectome and differentiation tree data

**Milestone (Projected):** **"Worm That Grows"**

- Announcement: "Simulate C. elegans development from L1 larva to adult, watching neurons born and the body grow."

**Datasets Needed:** See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) "Projected Datasets (Phases 5-7)" for inventory. Key resources: Witvliet developmental connectome series (in `cect`), CeNGEN L1 expression, Packer 2019 embryonic scRNA-seq, DevoWorm embryogenetic connectome and differentiation trees.

---

## Phase 7: Male-Specific Modeling (Year 3+)

**Status:** 📝 **Not Yet Specified** — Placeholder for male hermaphrodite simulation

**Anticipated Scope:**

- 385-neuron male connectome ([Cook2019](https://doi.org/10.1038/s41586-019-1352-7)MaleReader)
- 83 male-specific neurons (ray neurons, HOB, spicule motor neurons)
- Male tail anatomy (fan, rays, spicules) in [DD003](DD003_Body_Physics_Architecture.md)/DD004
- Mating circuit and copulation behavior

**Milestone (Projected):** **"Both Sexes Simulated"**

**Datasets Needed:** See [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) "Projected Datasets (Phases 5-7)" for inventory. Key resources: Cook 2019 male connectome (in `cect`), male behavioral/mating data, male-specific tail anatomy.

---

## Complete Dataset Inventory

For the canonical inventory of all datasets across all phases, see **[DD024: Validation Data Acquisition Pipeline](DD024_Validation_Data_Acquisition_Pipeline.md)**. DD024 catalogs:

- **Tier 1-4 validation datasets** — Electrophysiology, functional connectivity, behavioral kinematics, causal/interventional data
- **Connectome & molecular datasets** — Connectome data available via `cect` ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)), expression data, cell ontologies
- **Implementation & reference datasets** — Model inputs (BAAIWorm, Virtual Worm, ion channel sequences), reference implementations (CE_locomotion), training data (SPH simulation runs)
- **Projected datasets (Phases 5-7)** — Biochemical kinetics, developmental data, male-specific anatomy

Each dataset is tagged with its phase, consumer DD, acquisition method, and status. For connectome-specific datasets in detail, see also [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md).

---

## Dependency Summary (What Blocks What)

**Critical Path (must be done in order):**
```
Phase A ([DD013](DD013_Simulation_Stack_Architecture.md), [DD008](DD008_Data_Integration_Pipeline.md), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md), [DD025](DD025_Protein_Foundation_Model_Pipeline.md)) → Phase 1 ([DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD014](DD014_Dynamic_Visualization_Architecture.md)/[DD014.1](DD014.1_Visual_Rendering_Specification.md)) → Phase 2 ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD019](DD019_Closed_Loop_Touch_Response.md), [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md), [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md)) → Phase 3 ([DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md))
```

**Parallelizable:**

- Phase 1 [DD014](DD014_Dynamic_Visualization_Architecture.md)/[DD014.1](DD014.1_Visual_Rendering_Specification.md) (viewer + rendering spec) can proceed alongside [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (cell differentiation)
- Phase 2 [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) (environment) and [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (proprioception) can proceed in parallel with [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) and [DD019](DD019_Closed_Loop_Touch_Response.md)
- Phase 3 organ DDs ([DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md)) can be implemented in any order or in parallel
- Phase 4 [DD004](DD004_Mechanical_Cell_Identity.md) (cell identity) and [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (mesh deformation) can proceed in either order
- Phase A [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (foundation model kinetics) can proceed in parallel with all other Phase A work (no infrastructure dependencies)

**What Blocks Everything:**

- **Integration Maintainer recruitment** — Without this, [DD013](DD013_Simulation_Stack_Architecture.md) doesn't get implemented
- **Data Maintainer recruitment** — Without this, [DD008](DD008_Data_Integration_Pipeline.md) OWMeta doesn't get revived and Phase 1+ datasets lack unified access
- **Validation Maintainer recruitment** — Without this, [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) doesn't get revived
- **Phase A completion** — Without config system, data layer, and automated validation, contributor workflow doesn't work

---

## Timeline Summary

| Phase | Duration | Calendar (if start March 2026) | Cumulative Cells | Cumulative DD Implementation |
|-------|----------|-------------------------------|------------------|------------------------------|
| Phase 0 | Complete | Already done | 397 (302 neurons + 95 muscles) | 4 DDs ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD003](DD003_Body_Physics_Architecture.md), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md)) |
| Phase A | 4 weeks | Mar 2026 | (no change) | +7 DDs ([DD013](DD013_Simulation_Stack_Architecture.md), [DD008](DD008_Data_Integration_Pipeline.md), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md), [DD011](DD011_Contributor_Progression_Model.md), [DD012](DD012_Design_Document_RFC_Process.md), [DD015](DD015_AI_Contributor_Model.md), [DD025](DD025_Protein_Foundation_Model_Pipeline.md)) |
| Phase 1 | 3 months | Apr-Jun 2026 | 397 (differentiated, not added) | +3 DDs ([DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD010](DD010_Validation_Framework.md) Tier 2, [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 1, [DD014.1](DD014.1_Visual_Rendering_Specification.md)) |
| Phase 2 | 3 months | Jul-Sep 2026 | 403 (add 6 touch neurons explicitly modeled) | +4 DDs ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD019](DD019_Closed_Loop_Touch_Response.md), [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md), [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md), [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 2) |
| Phase 3 | 6 months | Oct 2026-Mar 2027 | 514 (add 63 pharynx + 20 intestine + 28 egg-laying) | +4 DDs ([DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)) |
| Phase 4 | 6 months | Apr-Sep 2027 | **959** (all somatic cells) | +2 DDs ([DD004](DD004_Mechanical_Cell_Identity.md), [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md), [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 3) |
| **TOTAL** | **~18 months** | **Mar 2026 - Sep 2027** | **959 cells** | **23 DDs implemented** |

**Phases 5-7:** Year 3+ (intracellular, developmental, male-specific)

---

## Major Milestones (What You Run, What You See)

### Milestone 1: "Containerized Stack" (End of Phase A)
- **When:** Week 4 (late March 2026)
- **Run:** `docker compose run quick-test` — full build + simulation + validation in <5 minutes
- **See:** Terminal pass/fail report. Video output of worm locomotion. JSON validation scores.
- **Validated against:** [Yemini 2013](https://doi.org/10.1038/nmeth.2560) kinematics (Tier 3), [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity (Tier 2)

### Milestone 2: "Biologically Distinct Neurons" (End of Phase 1)
- **When:** Month 3 (June 2026)
- **Run:** `docker compose up viewer` — open `localhost:8501`
- **See:** 3D worm with 302 neurons colored by 128 classes. Click any neuron — inspector shows class-specific dynamics. Compare differentiated vs. generic model side-by-side.
- **Validated against:** [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) — functional connectivity correlation improves ≥20% over generic baseline

### Milestone 3: "The Worm Can Feel" (End of Phase 2)
- **When:** Month 6 (September 2026)
- **Run:** `docker compose run simulation --config closedloop_touch` — tap the worm at t=5s
- **See:** Worm reverses direction within <1s, travels backward ≥1 body length, resumes forward. Anterior tap → backward, posterior tap → forward. Neuropeptide clouds visible as slow modulatory mist.
- **Validated against:** [Chalfie 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985) tap withdrawal; [Wicks 1996](https://doi.org/10.1523/JNEUROSCI.16-12-04017.1996) direction discrimination; ≥3 peptide knockout phenotypes ([Li 1999](https://doi.org/10.1111/j.1749-6632.1999.tb07895.x), [Rogers 2003](https://doi.org/10.1038/nn1140))

### Milestone 4: "Multi-Organ Organism" (End of Phase 3)
- **When:** Month 12 (March 2027)
- **Run:** `docker compose run simulation --config full_organism` (~20 simulated minutes)
- **See:** Worm crawls while pharynx pumps at 3-4 Hz, intestine fires calcium waves every ~50s triggering defecation, and egg-laying bouts occur every ~20 min. All visible simultaneously in the viewer.
- **Validated against:** [Raizen 1994](https://doi.org/10.1016/0896-6273(94)90207-0) pharyngeal EPG; [Thomas 1990](https://doi.org/10.1093/genetics/124.4.855) defecation period; [Collins 2016](https://doi.org/10.7554/eLife.21126) egg-laying calcium imaging

### Milestone 5: "WormSim 2.0" (End of Phase 4)
- **When:** Month 18 (September 2027)
- **Run:** Open `wormsim.openworm.org` — no installation required
- **See:** Smooth worm with 688 deforming anatomical meshes. Zoom from organism → tissue (click any of 959 cells) → molecular (ion channels, gene transcription). 60fps on a laptop.
- **Validated against:** All previous tiers passing. Cell-type-specific mechanics produce realistic body deformation.

---

## Success Metrics Across All Phases

| Metric | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|---------|---------|---------|---------|---------|
| **Total Cells** | 397 | 397 (diff.) | 403 | 514 | **959** |
| **Neuron Classes** | 1 (generic) | **128** | 128 | 128 | 128 |
| **Coupling Loops** | 1 (neural→body) | 1 | **2** (add body→sensory) | 2 | 2 |
| **Organ Systems** | 0 | 0 | 0 | **3** (pharynx, intestine, egg-laying) | 3 |
| **Modulation Layers** | 0 | 0 | **1** (31,479 peptide-receptor) | 1 | 1 |
| **Tier 2 Validation** | -- | ✅ r > 0.5 | ✅ | ✅ | ✅ |
| **Tier 3 Validation** | ✅ ±15% | ✅ | ✅ | ✅ | ✅ |
| **Viewer Scales** | 0 (raw particles) | 2 (organism, tissue) | 2 | 2 | **3** (add molecular) |
| **Public Access** | No | No | No | No | ✅ Static site |

---

## Phase Placement Rationale

Why is each DD in its current phase — and not earlier or later? This section documents the reasoning so future contributors and reviewers can evaluate whether phase assignments still hold as circumstances change.

### Phase 0: Existing Foundation

These DDs describe **already-implemented** subsystems. They are Phase 0 because the code exists and works.

| DD | Why Phase 0 |
|----|-------------|
| [DD001](DD001_Neural_Circuit_Architecture.md) | c302 Levels A-D exist, generate NeuroML networks. The 302-neuron HH circuit runs and produces movement. |
| [DD002](DD002_Muscle_Model_Architecture.md) | GenericMuscleCell exists with Ca²⁺→force coupling. Validated against Boyle & Cohen 2008. |
| [DD003](DD003_Body_Physics_Architecture.md) | Sibernetic v1.0+ works (OpenCL backend stable). ~100K SPH particles, fluid-structure interaction. |
| [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | `cect` v0.2.7 exists with 30+ connectome datasets accessible via Python API. |

### Phase A: Infrastructure Bootstrap

Phase A DDs either (a) provide infrastructure that all later phases depend on, or (b) have zero infrastructure dependencies and can run in parallel.

| DD | Why Phase A (not later) | Why not earlier (it's already first) |
|----|------------------------|--------------------------------------|
| [DD013](DD013_Simulation_Stack_Architecture.md) | **CRITICAL PATH.** Without Docker, `openworm.yml`, and CI, contributors can't build, test, or validate changes. Every subsequent DD needs this. | It *is* the earliest. Can't implement science DDs without the tools to validate them. |
| [DD008](DD008_Data_Integration_Pipeline.md) | Phase 1+ datasets (CeNGEN, Randi 2023, connectomes) need unified access via OWMeta. WBbt ID normalization must happen before CeNGEN ingestion. | N/A — already first phase. |
| [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | Tier 3 kinematic validation is broken (toolbox doesn't install on Python 3.12). Can't validate DD005's output without it. | N/A. |
| [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) | Validation data must exist before validation can run. Digitizing Thomas 1990, Raizen 1994, Chalfie 1985 data takes time and should start immediately. | N/A. |
| [DD012](DD012_Design_Document_RFC_Process.md) | Governance: need the DD process defined before more DDs are proposed. Low effort (~8 hours). | N/A. |
| [DD011](DD011_Contributor_Progression_Model.md) | Governance: need contributor framework before recruiting. Low effort (~8 hours). | N/A. |
| [DD015](DD015_AI_Contributor_Model.md) | AI agents need registration, review gates, and workflow before they contribute code. Depends on [DD012](DD012_Design_Document_RFC_Process.md). | N/A. |
| [DD025](DD025_Protein_Foundation_Model_Pipeline.md) | **Zero infrastructure dependencies.** Inputs (WormBase sequences, literature kinetics) are available today. Derisks [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s uncertain expression→conductance mapping. BioEmu-1 (100,000x MD speed) made this feasible. | Originally in Phase 3 as DD017 Component 3. Promoted because it has no blockers and provides a safety net for Phase 1. |

### Phase 1: Cell-Type Differentiation

Phase 1 is the first *modeling* phase. Its DDs differentiate the 302 identical neurons into 128 biologically distinct classes and establish visual + validation infrastructure.

| DD | Why Phase 1 (not earlier) | Why not later |
|----|--------------------------|---------------|
| [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Needs CeNGEN data ingested via [DD008](DD008_Data_Integration_Pipeline.md) (Phase A), config system from [DD013](DD013_Simulation_Stack_Architecture.md) (Phase A), and analysis toolbox from [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Phase A) to validate output. | Everything downstream assumes differentiated neurons. If the expression→conductance approach fails, better to discover that in Phase 1 than Phase 3. Also: DD005's scientific risk is highest — validate early. |
| [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 1 | Needs DD001-DD003 output formats defined (Phase 0). Produces OME-Zarr export pipeline needed by all later visualization phases. | Viewer is how people *see* the simulation. Delaying it means months of work with no visual feedback, which kills contributor engagement. |
| [DD014.1](DD014.1_Visual_Rendering_Specification.md) | Defines canonical color palette and materials. Needs the viewer architecture ([DD014](DD014_Dynamic_Visualization_Architecture.md)) to be specified first. | Phase 2 adds neuropeptide volumetric clouds and strain heatmaps — needs the color/material system already established. |
| [DD010](DD010_Validation_Framework.md) Tier 2 | Needs [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (differentiated neurons to validate) and Randi 2023 data (from [DD008](DD008_Data_Integration_Pipeline.md)/[DD024](DD024_Validation_Data_Acquisition_Pipeline.md)). | The functional connectivity gate (r > 0.5) must be active before Phase 2 builds on top of differentiated neurons. Without it, Phase 2 could build on a broken foundation. |
| [DD025](DD025_Protein_Foundation_Model_Pipeline.md) integration | Phase A cross-validation must complete first. Needs [DD005](DD005_Cell_Type_Differentiation_Strategy.md) pipeline to exist so predictions can feed in as calibration priors. | Predictions are most valuable when [DD005](DD005_Cell_Type_Differentiation_Strategy.md) is actively calibrating — waiting until Phase 3 wastes the derisking opportunity. |

### Phase 2: Slow Modulation + Closed-Loop Sensory

Phase 2 closes the sensory loop (body→neuron feedback) and adds the neuropeptide modulation layer. These DDs require differentiated neurons from Phase 1.

| DD | Why Phase 2 (not earlier) | Why not later |
|----|--------------------------|---------------|
| [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Neuropeptide modulation on generic neurons would be meaningless — the 31,479 peptide-receptor interactions are cell-type-specific. Needs [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (Phase 1) differentiation. | [DD018](DD018_Egg_Laying_System_Architecture.md) (Phase 3) requires serotonergic modulation (HSN neurons). The neuropeptide layer must exist before egg-laying can work. |
| [DD019](DD019_Closed_Loop_Touch_Response.md) | Needs differentiated sensory neurons ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)) with cell-type-specific MEC-4 channels. Building bidirectional body↔neuron coupling requires stable [DD001](DD001_Neural_Circuit_Architecture.md)+[DD003](DD003_Body_Physics_Architecture.md) integration (Phase 0/A). | Closed-loop sensory input is prerequisite for any emergent behavior (chemotaxis, thermotaxis). Without it, the worm is "deaf" — can't respond to its environment. |
| [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) | Needs [DD003](DD003_Body_Physics_Architecture.md) for substrate physics and [DD019](DD019_Closed_Loop_Touch_Response.md) for the sensory coupling framework. Can't do chemotaxis without both gradient fields and sensory neurons that respond to them. | Chemotaxis (CI > 0.5) and thermotaxis are key behavioral validation targets. Demonstrating them in Phase 2 is a major milestone ("The Worm Can Feel"). |
| [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) | Needs [DD019](DD019_Closed_Loop_Touch_Response.md)'s bidirectional coupling framework (body→neuron path). Stretch receptors on B-class motor neurons require the same SPH→strain→channel pipeline that touch uses. | Proprioception stabilizes the locomotion wavelength (±10% vs. ±15%). Without it, forward locomotion degrades when other subsystems add load. Phase 3 organ systems need stable locomotion. |
| [DD001](DD001_Neural_Circuit_Architecture.md) Level D Stage 1 | Proof-of-concept multicompartmental neurons. Needs [DD005](DD005_Cell_Type_Differentiation_Strategy.md) to know which channels each neuron class expresses before you can model their compartmental distribution. | Level D is needed eventually for spatially realistic signal propagation. Starting with 5 representative neurons in Phase 2 validates the approach before committing to all 302. |

### Phase 3: Organ Systems + Hybrid ML

Phase 3 adds three organ subsystems and the ML acceleration framework. These DDs require differentiated neurons (Phase 1) and ideally the modulation layer (Phase 2).

| DD | Why Phase 3 (not earlier) | Why not later |
|----|--------------------------|---------------|
| [DD007](DD007_Pharyngeal_System_Architecture.md) | The pharynx has 20 neurons + 20 muscles that need differentiated parameters ([DD005](DD005_Cell_Type_Differentiation_Strategy.md)). Pharyngeal neurons use unique channels (e.g., EAT-2) that benefit from the neuropeptide modulation layer ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md)). | Must be implemented before Phase 4's 959-cell integration. The pharynx is a semi-autonomous organ — a visible, validatable milestone. |
| [DD009](DD009_Intestinal_Oscillator_Model.md) | The 20-cell IP3/Ca²⁺ oscillator is relatively independent but couples to the neural circuit via DVB and AVL neurons. Needs [DD001](DD001_Neural_Circuit_Architecture.md) neural coupling. Validation data (Thomas 1990 defecation timing) needs digitization (started in [DD024](DD024_Validation_Data_Acquisition_Pipeline.md), Phase A). | Defecation motor program (50s period) is one of the best-characterized *C. elegans* behaviors. A quantitative validation target that must be met before Phase 4's full-organism claim. |
| [DD018](DD018_Egg_Laying_System_Architecture.md) | **Most complex organ circuit.** HSN serotonergic command neurons require [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (Phase 2) neuropeptide/serotonin modulation. Vulval muscles use EGL-19/UNC-103 channels that need [DD005](DD005_Cell_Type_Differentiation_Strategy.md). Tyramine/octopamine signaling adds another modulation layer. | Two-state egg-laying pattern (active bouts interspersed with long inactive periods) is a behavioral phenotype used in hundreds of published mutant screens. Must work before claiming "digital organism." |
| [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) | **Component 1 (differentiable backend):** Needs stable DD001+DD002+DD009 equations to port to PyTorch. If equations change during Phase 1-2, the port must be redone. Best to wait until the ODE system stabilizes. Also benefits from having multiple coupled subsystems (neural + muscle + intestine) to auto-fit against simultaneously. **Component 2 (SPH surrogate):** Needs 500+ full SPH simulation runs as training data (~2,500 GPU-hours). Training data goes stale if DD004 (Phase 4) changes particle mechanics or DD019 (Phase 2) adds bidirectional coupling that alters body dynamics. Maximum infrastructure dependencies — the opposite of DD025. **Component 4 (learned sensory):** Phase 2 attempts the mechanistic route first (DD019 touch, DD022 chemotaxis, DD023 proprioception). The learned model fills gaps that remain *after* the mechanistic approach is tested. Using ML before trying mechanism contradicts OpenWorm's core commitment to interpretability. | Auto-fitted parameters (Component 1) are needed before Phase 4's 959-cell integration — manual tuning won't scale. The SPH surrogate (Component 2) enables fast iteration for Phase 4's multi-organ coupled simulations. |

### Phase 4: Mechanical Cell Identity + Visualization

Phase 4 completes the organism: all 959 somatic cells with cell-type mechanics and a public web viewer.

| DD | Why Phase 4 (not earlier) | Why not later |
|----|--------------------------|---------------|
| [DD004](DD004_Mechanical_Cell_Identity.md) | Per-cell mechanical properties (elasticity, adhesion) should be informed by organ system behavior (Phase 3). Setting intestine elasticity before implementing the intestine means guessing. Also needs [Witvliet 2021](https://doi.org/10.1038/s41586-021-03778-8) EM cell boundaries, which require significant data conversion work. | This is the final modeling step — assigns all 959 somatic cells to SPH particles with cell-type-specific physics. Completing this means the "virtual organism" claim is real. |
| [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) | Needs [DD004](DD004_Mechanical_Cell_Identity.md) cell boundaries and [DD003](DD003_Body_Physics_Architecture.md) SPH body shape. The GPU skinning pipeline can't be tested without both. The 688 Virtual Worm meshes need to deform with simulated body motion, which requires a stable coupled simulation. | Photorealistic deformation is what makes "WormSim 2.0" visually compelling. Without it, the viewer shows raw particles instead of anatomical meshes. |
| [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 3 | Needs all previous visualization phases complete. Three.js + WebGPU public deployment requires stable content (all organ systems implemented and validated). Static site deployment to wormsim.openworm.org. | This is the capstone: "Digital Organism In Your Browser." Delays here delay the most visible milestone and the Nature/Science paper. |

---

## Frequently Asked Questions

**Q: Why is Phase A first if it's infrastructure, not science?**
A: Without the config system ([DD013](DD013_Simulation_Stack_Architecture.md)) and automated validation ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)), contributors can't test their work efficiently. Better to invest 4 weeks in infrastructure that enables the next 18 months of science, than to implement science DDs without the tools to validate them.

**Q: Can Phase 3 organ DDs ([DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md)) be implemented in parallel?**
A: Yes — they're semi-independent subsystems. Different contributors can work on pharynx, intestine, and egg-laying simultaneously. [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (hybrid ML) can also proceed in parallel.

**Q: Why is [DD004](DD004_Mechanical_Cell_Identity.md) (Cell Identity) in Phase 4, not earlier?**
A: [DD004](DD004_Mechanical_Cell_Identity.md) requires per-cell mechanical properties (elasticity, adhesion) that are informed by organ system behavior. Better to implement organs first (Phase 3), observe their mechanics, then add cell-specific properties in Phase 4. [DD004](DD004_Mechanical_Cell_Identity.md) is also needed for [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) mesh deformation.

**Q: What if Phase 1 [DD005](DD005_Cell_Type_Differentiation_Strategy.md) fails validation (Tier 2 doesn't improve)?**
A: The calibration approach (expression→conductance scaling) is uncertain. If it fails, fall back to [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (foundation model→params) or manual curation. [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s scientific risk is why it's Phase 1 — validate the approach early before building more on top of it.

**Q: When do we write papers?**
A: After each major milestone:

- Phase 1: "CeNGEN-Parameterized Neural Circuit" (target: *eNeuro* or *Frontiers in Neuroinformatics*)
- Phase 2: "Closed-Loop Sensorimotor Behavior in Whole-Organism Simulation" (target: *PLoS Computational Biology*)
- Phase 3: "Multi-Organ, Multi-Timescale C. elegans Simulation" (target: *Nature Communications* or *Cell Systems*)
- Phase 4: "Complete 959-Cell Digital Organism" (target: **Nature** or **Science**)

**Q: Why is DD025 (foundation model kinetics) in Phase A, not Phase 3 with the rest of DD017?**
A: Component 3 derisks [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s uncertain transcript→conductance mapping. BioEmu-1 (100,000x MD speed) invalidated the original "computationally expensive" rejection. The inputs (WormBase sequences, literature kinetics) are available now with no infrastructure dependencies. Cross-validation in Phase A provides a safety net: if [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s naive mapping fails in Phase 1, structure-based predictions are ready immediately.

---

- **Approved by:** Pending (awaiting founder review)
- **Maintained by:** Integration L4 Maintainer (when appointed)
- **Next Review:** After Phase A completion (reassess timeline based on actual progress)
