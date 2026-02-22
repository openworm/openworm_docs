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

**Phase Rationale:** These DDs describe **already-implemented** subsystems — the code exists and works. c302 generates NeuroML networks, GenericMuscleCell has Ca²⁺→force coupling, Sibernetic runs ~100K SPH particles, and `cect` provides 30+ connectome datasets. They form the working foundation everything else builds on.

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

**Cumulative Metrics:** 397 cells (302 neurons + 95 muscles) | 1 neuron class (generic) | 1 coupling loop (neural→body) | 0 organ systems | Tier 3 validated (±15%) | No viewer | 4 DDs implemented

---

## Phase A: Infrastructure Bootstrap (Weeks 1-4)

**Status:** ⚠️ **Proposed** — Must complete before modeling phases proceed

**Phase Rationale:** Phase A DDs either (a) provide infrastructure that **all** later phases depend on, or (b) have zero infrastructure dependencies and can run in parallel. Without Docker/CI ([DD013](DD013_Simulation_Stack_Architecture.md)), unified data access ([DD008](DD008_Data_Integration_Pipeline.md)), and working validation ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)), contributors can't build, test, or validate. [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) starts validation data digitization immediately. [DD025](DD025_Protein_Foundation_Model_Pipeline.md) has zero infrastructure dependencies and derisks Phase 1's uncertain expression→conductance mapping — BioEmu-1 (100,000x MD speed) made this feasible, and inputs (WormBase sequences, literature kinetics) are available today.

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

**Milestone:** 🎉 **"Containerized Stack with Automated Validation"** *(Target: Week 4, late March 2026)*

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

**Cumulative Metrics:** 397 cells (unchanged — infrastructure phase) | 1 neuron class (generic) | 1 coupling loop | 0 organ systems | Tier 2 + Tier 3 validation operational | No viewer | +7 DDs (11 total)

---

## Phase 1: Cell-Type Differentiation (Months 1-3)

**Status:** ⚠️ **Ready to Start** (after Phase A complete)

**Phase Rationale:** Phase 1 is the first *modeling* phase — it differentiates the 302 identical neurons into 128 biologically distinct classes. [DD005](DD005_Cell_Type_Differentiation_Strategy.md) is here because it needs CeNGEN data via [DD008](DD008_Data_Integration_Pipeline.md) and validation tools from [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (both Phase A), and because its scientific risk is highest — if expression→conductance mapping fails, better to discover it early. [DD014](DD014_Dynamic_Visualization_Architecture.md)/[DD014.1](DD014.1_Visual_Rendering_Specification.md) establish visual infrastructure because months of work with no visual feedback kills contributor engagement. [DD010](DD010_Validation_Framework.md) Tier 2 activates the functional connectivity gate (r > 0.5) so Phase 2 doesn't build on a broken foundation. [DD025](DD025_Protein_Foundation_Model_Pipeline.md) integration feeds foundation model predictions into [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration while it's actively running.

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

**Milestone:** 🎉 **"Biologically Distinct Neurons"** *(Target: Month 3, June 2026)*

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

**Cumulative Metrics:** 397 cells (differentiated, not added) | **128** neuron classes | 1 coupling loop | 0 organ systems | Tier 2 validated (r > 0.5) + Tier 3 (±15%) | 2 viewer scales (organism, tissue) | +3 DDs (14 total)

---

## Phase 2: Slow Modulation + Closed-Loop Sensory (Months 4-6)

**Status:** ⚠️ **Proposed** (ready after Phase 1)

**Phase Rationale:** Phase 2 closes the sensory loop (body→neuron feedback) and adds the neuropeptide modulation layer. [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) requires differentiated neurons from Phase 1 because the 31,479 peptide-receptor interactions are cell-type-specific — modulation on generic neurons would be meaningless. [DD019](DD019_Closed_Loop_Touch_Response.md) needs cell-type-specific MEC-4 channels from [DD005](DD005_Cell_Type_Differentiation_Strategy.md). Both must exist before Phase 3: [DD018](DD018_Egg_Laying_System_Architecture.md) requires serotonergic modulation, and emergent behaviors (chemotaxis, thermotaxis) require sensory input. [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) and [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) can proceed in parallel with [DD006](DD006_Neuropeptidergic_Connectome_Integration.md)/[DD019](DD019_Closed_Loop_Touch_Response.md). DD001 Level D Stage 1 starts with 5 representative multicompartmental neurons to validate the approach before committing to all 302.

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

**Milestone:** 🎉 **"The Worm Can Feel and Modulate"** *(Target: Month 6, September 2026)*

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

**Cumulative Metrics:** 403 cells (+6 touch neurons) | 128 neuron classes | **2** coupling loops (+body→sensory) | 0 organ systems | **1** modulation layer (31,479 peptide-receptor) | Tier 2 + Tier 3 validated | 2 viewer scales | +4 DDs (18 total)

---

## Phase 3: Organ Systems + Hybrid ML (Months 7-12)

**Status:** ⚠️ **Proposed** (ready after Phase 2)

**Phase Rationale:** Phase 3 adds three semi-autonomous organ subsystems and the ML acceleration framework. [DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx) and [DD018](DD018_Egg_Laying_System_Architecture.md) (egg-laying) need differentiated parameters from [DD005](DD005_Cell_Type_Differentiation_Strategy.md), and [DD018](DD018_Egg_Laying_System_Architecture.md) specifically requires [DD006](DD006_Neuropeptidergic_Connectome_Integration.md)'s serotonin modulation. [DD009](DD009_Intestinal_Oscillator_Model.md) (intestine) couples to neural circuits via DVB/AVL neurons. All three organ DDs can be implemented in parallel by different contributors. [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (hybrid ML) waits until Phase 3 because: (1) the differentiable backend needs stable ODE equations — porting during Phase 1-2 equation changes wastes effort, (2) the SPH surrogate needs 500+ training runs that go stale if body dynamics change, and (3) learned sensory models are only appropriate *after* the mechanistic approach (Phase 2) has been tried — using ML before mechanism contradicts OpenWorm's interpretability commitment.

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

**Milestone:** 🎉 **"From 302 Neurons to 433 Cells — Multi-Organ Simulation"** *(Target: Month 12, March 2027)*

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

**Cumulative Metrics:** 514 cells (+63 pharynx +20 intestine +28 egg-laying) | 128 neuron classes | 2 coupling loops | **3** organ systems (pharynx, intestine, egg-laying) | 1 modulation layer | Tier 2 + Tier 3 validated | 2 viewer scales | +4 DDs (22 total)

---

## Phase 4: Mechanical Cell Identity + High-Fidelity Visualization (Months 13-18)

**Status:** ⚠️ **Proposed** (ready after Phase 3)

**Phase Rationale:** Phase 4 completes the organism: all 959 somatic cells with cell-type mechanics and a public web viewer. [DD004](DD004_Mechanical_Cell_Identity.md) is here because per-cell mechanical properties (elasticity, adhesion) should be informed by organ system behavior — setting intestine elasticity before implementing the intestine means guessing. [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) needs both [DD004](DD004_Mechanical_Cell_Identity.md) cell boundaries and stable SPH body dynamics. [DD014](DD014_Dynamic_Visualization_Architecture.md) Phase 3 (Three.js + WebGPU public deployment) requires all content stable — static site deployment to wormsim.openworm.org is the capstone milestone. [DD004](DD004_Mechanical_Cell_Identity.md) and [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) can proceed in parallel.

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

**Milestone:** 🎉 **"WormSim 2.0 — 959-Cell Digital Organism In Your Browser"** *(Target: Month 18, September 2027)*

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

**Cumulative Metrics:** **959** cells (all somatic) | 128 neuron classes | 2 coupling loops | 3 organ systems | 1 modulation layer | Tier 2 + Tier 3 validated | **3** viewer scales (organism, tissue, molecular) | **Public access** (static site) | **23 DDs implemented**

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
