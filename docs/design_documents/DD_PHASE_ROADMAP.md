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

**Datasets Needed for Phase A** (see [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) for complete inventory)**:**

- Schafer lab N2 baseline kinematics (WCON format, for Tier 3) — **Status:** Partial (MAT format exists, needs WCON conversion)
- [Randi et al. 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity (302×302 correlation matrix) — **Status:** Needs ingestion into [DD008](DD008_Data_Integration_Pipeline.md)/DD020
- Yemini 2013 behavioral phenotype statistics (grounding for ±15% threshold) — **Status:** Needs supplement download
- Thomas 1990 defecation cycle data — **Status:** Needs digitization from paper
- Raizen 1994 pumping EPG data — **Status:** Needs digitization from paper
- O'Hagan 2005 MEC-4 channel kinetics — **Status:** Needs digitization from paper
- Chalfie 1985 touch response latency data — **Status:** Needs digitization from paper
- Ion channels with known kinetics (~50-100 channels, CSV: channel, structure, HH params) — **Status:** Needs curation from PDB + electrophysiology literature
- C. elegans ion channel sequences (FASTA from WormBase) — **Status:** ✅ Available

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

**Datasets Needed for Phase 1:**

| Dataset | Source | Format | Use Case | Status |
|---------|--------|--------|----------|--------|
| **CeNGEN L4 expression** | cengen.org | CSV (128 classes × 20,500 genes) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) conductance calibration | ✅ Available (download from cengen.org/downloads) |
| **Electrophysiology training set** | Goodman lab, Lockery lab, published papers | CSV (neuron_class, channel, measured_g, source_doi) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration regression | ⚠️ Needs curation (~20 neurons) |
| **[Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) functional connectivity** | Nature 623:406 supplement | NumPy .npy (302×302 correlation matrix) | [DD010](DD010_Validation_Framework.md) Tier 2 validation | ⚠️ Needs download + ingestion |
| **Ion channel gene list** | WormBase, CeNGEN | CSV (gene_symbol, channel_family, neuroml_model) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) gene→channel mapping | ⚠️ Needs curation (~100 ion channel genes) |

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
| **[DD001](DD001_Neural_Circuit_Architecture.md) Level E Stage 1** | Multicompartmental Neurons (Proof of Concept) | [DD001](DD001_Neural_Circuit_Architecture.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | 5 representative neurons with 14 ion channel classes, EM morphologies, fitted to electrophysiology |

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

**Datasets Needed for Phase 2:**

| Dataset | Source | Format | Use Case | Status |
|---------|--------|--------|----------|--------|
| **[Ripoll-Sanchez 2023](https://doi.org/10.1016/j.neuron.2023.09.043) neuropeptides** | Neuron 111:3570 Table S1 | CSV (31,479 interactions: source, target, peptide, receptor, distance) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) extrasynaptic connectome | ⚠️ Needs download from journal supplement |
| **3D neuron positions** | WormAtlas, [Long et al. 2009](https://doi.org/10.1038/nmeth.1366) | CSV (302 neurons × 3 coordinates) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) distance calculation | ⚠️ Needs extraction from WormAtlas or EM data |
| **Touch neuron electrophysiology** | [O'Hagan et al. 2005](https://doi.org/10.1038/nn1362), [Goodman et al. 2002](https://doi.org/10.1038/4151039a) | CSV (MEC-4 channel kinetics: V_half, tau, conductance) | [DD019](DD019_Closed_Loop_Touch_Response.md) MEC-4 model validation | ⚠️ Needs extraction from papers |
| **Tap withdrawal behavioral data** | [Chalfie et al. 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985), [Wicks et al. 1996](https://doi.org/10.1523/JNEUROSCI.16-12-04017.1996) | CSV (reversal latency, distance, direction) | [DD019](DD019_Closed_Loop_Touch_Response.md) Tier 3 validation | ⚠️ Needs extraction from papers |
| **Peptide knockout phenotypes** | [Li et al. 1999](https://doi.org/10.1111/j.1749-6632.1999.tb07895.x), [Rogers et al. 2003](https://doi.org/10.1038/nn1140) (FLP), others | CSV (peptide_gene, phenotype, metric, wild_type, knockout) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) validation | ⚠️ Needs curation from literature |
| **Chemotaxis behavioral data** | Iino & Yoshida 2009 | CSV (chemotaxis index, trajectory data) | [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) Tier 3 validation | ⚠️ Needs extraction from paper |
| **Thermotaxis behavioral data** | Hedgecock & Russell 1975, Mori & Ohshima 1995 | CSV (isothermal tracking, cultivation temp preference) | [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) Tier 3 validation | ⚠️ Needs extraction from papers |
| **B-class motor neuron stretch response** | Wen et al. 2012 | Calcium imaging (DB, VB response to body bending) | [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) Tier 1 validation | ⚠️ Needs extraction from paper |
| **CE_locomotion stretch receptor model** | [openworm/CE_locomotion](https://github.com/openworm/CE_locomotion) | C++ (StretchReceptor.cpp) | [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) reference implementation | ✅ Available (repo active 2026-02-18) |
| **BAAIWorm NMODL ion channel files and SWC morphology data** | [github.com/Jessie940611/BAAIWorm](https://github.com/Jessie940611/BAAIWorm), Apache 2.0, Zenodo: [10.5281/zenodo.13951773](https://doi.org/10.5281/zenodo.13951773) | NMODL (.mod) + SWC (.swc) | [DD001](DD001_Neural_Circuit_Architecture.md) Level E Stage 1 | ✅ Available (open-source) |

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

**Datasets Needed for Phase 3:**

| Dataset | Source | Format | Use Case | Status |
|---------|--------|--------|----------|--------|
| **[Raizen 1994](https://doi.org/10.1016/0896-6273(94)90207-0) EPG recordings** | Neuron 12:483 | CSV (pharyngeal muscle voltage traces) | [DD007](DD007_Pharyngeal_System_Architecture.md) validation | ⚠️ Needs digitization from paper figures |
| **[Thomas 1990](https://doi.org/10.1093/genetics/124.4.855) defecation data** | Genetics 124:855 | CSV (defecation cycle period distribution) | [DD009](DD009_Intestinal_Oscillator_Model.md) Tier 3 validation | ⚠️ Needs extraction |
| **[Collins 2016](https://doi.org/10.7554/eLife.21126) egg-laying calcium imaging** | eLife 5:e21126 | CSV (HSN/VC/vm2 calcium traces, bout intervals) | [DD018](DD018_Egg_Laying_System_Architecture.md) validation | ⚠️ Needs extraction from supplement |
| **SPH simulation training set** | Generate from Sibernetic | HDF5 (500+ runs: muscle_activation → trajectory pairs) | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) surrogate training | ⚠️ Generate during Phase 3 (~2,500 GPU-hours) |
| **Ion channel structures** | AlphaFold3, PDB | PDB files (C. elegans ion channel proteins) | [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (moved to Phase A) | ✅ Moved to Phase A datasets |
| **CeNGEN pharyngeal/intestinal/reproductive expression** | cengen.org | CSV (subset of L4 expression for non-neural cells) | [DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md) cell-type-specific params | ✅ Available (filter CeNGEN L4 by cell type) |

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

**Datasets Needed for Phase 4:**

| Dataset | Source | Format | Use Case | Status |
|---------|--------|--------|----------|--------|
| **[Witvliet 2021](https://doi.org/10.1038/s41586-021-03778-8) cell boundary meshes** | Nature 596:257 supplement | 3D EM reconstructions (OBJ or STL per cell) | [DD004](DD004_Mechanical_Cell_Identity.md) particle tagging | ⚠️ Needs extraction/conversion from EM data |
| **Virtual Worm Blender meshes** | Blender2NeuroML repo | .blend file (688 meshes, ~1.6M vertices) | [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) deformation | ✅ Available (Virtual_Worm_February_2012.blend) |
| **Cell-type mechanical properties** | Literature review (elasticity, adhesion per tissue type) | CSV (cell_type, elasticity_mult, adhesion_strength) | [DD004](DD004_Mechanical_Cell_Identity.md) physics params | ⚠️ Needs curation from biomechanics literature |
| **WBbt cell ontology** | WormBase | RDF or CSV (cell_name → WBbt_ID mapping) | [DD004](DD004_Mechanical_Cell_Identity.md) cell identity normalization | ✅ Available via WormBase API |

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

**Datasets Needed (Projected):**

- Biochemical rate constants (PLC activity, cAMP degradation, PKA/PKC kinetics)
- Protein abundance (proteomics for C. elegans neurons/muscles)
- Calcium imaging with subcellular resolution (ER, mitochondria, plasma membrane compartments)

---

## Phase 6: Developmental Modeling (Year 2+)

**Status:** 📝 **Not Yet Specified** — Placeholder for multi-stage simulation

**Anticipated Scope:**

- Witvliet developmental connectome series (L1 → L2 → L3 → L4 → adult, 8 stages)
- Neuron birth and death (programmed cell death, 131 cells die during development)
- Body size scaling (L1 ~240 µm → adult ~1000 µm)
- Stage-specific validation (L1 locomotion differs from adult)
- CeNGEN L1 expression integration

**Milestone (Projected):** **"Worm That Grows"**

- Announcement: "Simulate C. elegans development from L1 larva to adult, watching neurons born and the body grow."

**Datasets Needed (Projected):**

| Dataset | Source | Use Case | Status |
|---------|--------|----------|--------|
| **Witvliet series connectomes** (8 stages) | Nature 596:257 | Stage-specific neural topology | ✅ Available via `cect` WitvlietDataReader1-8 |
| **CeNGEN L1 expression** | cengen.org | L1 neuron differentiation | ✅ Available but less mature than L4 |
| **[Packer 2019](https://doi.org/10.1126/science.aax1971) embryonic scRNA-seq** | Science 365:eaax1971 | Embryonic gene expression | ⚠️ Needs ingestion |
| **Developmental behavioral data** | Literature (L1-L4 locomotion, feeding) | Stage-specific validation | ⚠️ Needs curation |

---

## Phase 7: Male-Specific Modeling (Year 3+)

**Status:** 📝 **Not Yet Specified** — Placeholder for male hermaphrodite simulation

**Anticipated Scope:**

- 385-neuron male connectome ([Cook2019](https://doi.org/10.1038/s41586-019-1352-7)MaleReader)
- 83 male-specific neurons (ray neurons, HOB, spicule motor neurons)
- Male tail anatomy (fan, rays, spicules) in [DD003](DD003_Body_Physics_Architecture.md)/DD004
- Mating circuit and copulation behavior

**Milestone (Projected):** **"Both Sexes Simulated"**

**Datasets Needed (Projected):**

- [Cook 2019](https://doi.org/10.1038/s41586-019-1352-7) male connectome (available via `cect`)
- Male behavioral data (mating assays, vulva location, spicule insertion)
- Male-specific anatomy (tail SPH model, spicule mechanics)

---

## Complete Dataset Inventory (All Phases)

### Connectome Datasets ([DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md))

| Dataset | Source | Year | `cect` Reader | Used In | Status |
|---------|--------|------|---------------|---------|--------|
| White et al. | Phil Trans R Soc B 314:1 | 1986 | `WhiteDataReader` | Historical reference | ✅ In `cect` |
| Varshney et al. | PLoS Comput Biol 7:e1001066 | 2011 | `VarshneyDataReader` | Legacy comparison | ✅ In `cect` |
| **[Cook 2019](https://doi.org/10.1038/s41586-019-1352-7) Hermaphrodite** | Nature 571:63 | 2019 | `Cook2019HermReader` | **PRIMARY** — [DD001](DD001_Neural_Circuit_Architecture.md) default | ✅ In `cect` |
| **[Cook 2019](https://doi.org/10.1038/s41586-019-1352-7) Male** | Nature 571:63 | 2019 | `Cook2019MaleReader` | Phase 7 (male modeling) | ✅ In `cect` |
| [Cook 2020](https://doi.org/10.1038/s41586-019-1352-7) | Update | 2020 | `Cook2020DataReader` | Updated analysis | ✅ In `cect` |
| **Witvliet Series (Stages 1-8)** | Nature 596:257 | 2021 | `WitvlietDataReader1-8` | Phase 6 (developmental), cross-validation | ✅ In `cect` |
| Brittin et al. | Contact area-based | 2021 | `BrittinDataReader` | Alternative weighting | ✅ In `cect` |
| **[Ripoll-Sanchez 2023](https://doi.org/10.1016/j.neuron.2023.09.043)** | Neuron 111:3570 | 2023 | `RipollSanchez*RangeReader` | **Phase 2** — [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) neuropeptides | ✅ In `cect` |
| **[Wang 2024](https://doi.org/10.7554/eLife.95402) Hermaphrodite** | eLife 13:RP95402 | 2024 | `Wang2024HermReader` | Neurotransmitter identity | ✅ In `cect` |
| [Wang 2024](https://doi.org/10.7554/eLife.95402) Male | eLife 13:RP95402 | 2024 | `Wang2024MaleReader` | Male neurotransmitters | ✅ In `cect` |
| [Yim 2024](https://doi.org/10.1038/s41467-024-45943-3) | Updated connectivity | 2024 | `Yim2024DataReader` | Recent analysis | ✅ In `cect` |
| OpenWormUnified | Experimental | 2024+ | `OpenWormUnifiedReader` | **WIP** — future default | ⚠️ Subject to change |

### Functional Datasets ([DD010](DD010_Validation_Framework.md), [DD005](DD005_Cell_Type_Differentiation_Strategy.md))

| Dataset | Source | Year | Format | Used In | Status |
|---------|--------|------|--------|---------|--------|
| **[Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) whole-brain calcium imaging** | Nature 623:406 | 2023 | 302×302 correlation matrix (.npy) | **Phase 1** — [DD010](DD010_Validation_Framework.md) Tier 2, [DD005](DD005_Cell_Type_Differentiation_Strategy.md) validation | ⚠️ Download from supplement |
| **[Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) neuron atlas** | Nature 623:406 | 2023 | Functional connectivity | [DD005](DD005_Cell_Type_Differentiation_Strategy.md), [DD010](DD010_Validation_Framework.md) | ✅ In `cect` (WormNeuroAtlasFuncReader) |
| Goodman lab electrophysiology | Various papers 1998-2005 | 1998+ | CSV (touch neurons: MEC-4, voltage-clamp traces) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration, [DD019](DD019_Closed_Loop_Touch_Response.md) validation | ⚠️ Needs curation |
| Lockery lab recordings | Various papers | 2000s | CSV (AVA, other interneurons) | [DD005](DD005_Cell_Type_Differentiation_Strategy.md) calibration | ⚠️ Needs curation |

### Expression Datasets ([DD005](DD005_Cell_Type_Differentiation_Strategy.md))

| Dataset | Source | Year | Format | Used In | Status |
|---------|--------|------|--------|---------|--------|
| **CeNGEN L4** | Cell 184:4329 | 2021 | CSV (128 neuron classes × 20,500 genes) | **Phase 1** — [DD005](DD005_Cell_Type_Differentiation_Strategy.md) neuron differentiation | ✅ Download from cengen.org |
| CeNGEN L1 | cengen.org | 2021+ | CSV (L1 neuron classes × genes) | Phase 6 (developmental) | ✅ Available but less mature |
| [Packer 2019](https://doi.org/10.1126/science.aax1971) embryonic scRNA-seq | Science 365:eaax1971 | 2019 | Embryonic gene expression | Phase 6 (embryonic modeling) | ⚠️ Needs ingestion |

### Anatomical / Morphological Datasets ([DD004](DD004_Mechanical_Cell_Identity.md), [DD008](DD008_Data_Integration_Pipeline.md), [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md))

| Dataset | Source | Year | Format | Used In | Status |
|---------|--------|------|--------|---------|--------|
| **Virtual Worm Blender model** | Caltech/WormBase (Grove & Sternberg) | 2012 | .blend (688 meshes, 37 materials) | [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) mesh deformation | ✅ In Blender2NeuroML repo |
| [Long et al. 2009](https://doi.org/10.1038/nmeth.1366) 3D atlas | Nature Methods 6:667 | 2009 | 3D nuclear positions (357 nuclei, L1) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (distance), [DD004](DD004_Mechanical_Cell_Identity.md) (cell positions) | ⚠️ Needs extraction |
| **WormAtlas anatomy** | wormatlas.org | Ongoing | EM images, cell descriptions, Slidable Worm | [DD004](DD004_Mechanical_Cell_Identity.md) (cell boundaries), [DD008](DD008_Data_Integration_Pipeline.md) (cell positions) | ✅ Available via web scraping or API |
| **[Witvliet 2021](https://doi.org/10.1038/s41586-021-03778-8) EM reconstructions** | Nature 596:257 | 2021 | 3D cell volumes (8 animals × 8 stages) | **Phase 4** — [DD004](DD004_Mechanical_Cell_Identity.md) cell boundaries | ⚠️ Needs conversion from EM data |

### Behavioral / Kinematic Datasets ([DD010](DD010_Validation_Framework.md) Tier 3)

| Dataset | Source | Year | Format | Used In | Status |
|---------|--------|------|--------|---------|--------|
| **Schafer lab N2 baseline** | [Yemini et al. 2013](https://doi.org/10.1038/nmeth.2560) database | 2013 | MAT files (skeleton time series) | [DD010](DD010_Validation_Framework.md) Tier 3 (primary) | ✅ In analysis toolbox examples/, needs WCON conversion |
| Schafer lab mutants | Yemini database | 2013+ | MAT files (unc-2, egl-19, others) | [DD010](DD010_Validation_Framework.md) mutant validation | ✅ In database |
| **Tierpsy Tracker dataset** | [Javer et al. 2018](https://doi.org/10.1038/s41592-018-0112-1) | 2018+ | WCON + HDF5 (multi-worm tracking) | [DD010](DD010_Validation_Framework.md) cross-validation | ⚠️ Explore for additional baselines |
| [Chalfie 1985](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985) tap withdrawal | Neuron 5:956 | 1985 | Behavioral metrics (reversal latency, distance) | [DD019](DD019_Closed_Loop_Touch_Response.md) Tier 3 validation | ⚠️ Digitize from paper |
| [Wicks 1996](https://doi.org/10.1523/JNEUROSCI.16-12-04017.1996) tap direction | J Neurobiol 31:1 | 1996 | Direction discrimination data | [DD019](DD019_Closed_Loop_Touch_Response.md) validation | ⚠️ Digitize from paper |

### Pharmacological / Genetic Perturbation Datasets ([DD006](DD006_Neuropeptidergic_Connectome_Integration.md), [DD018](DD018_Egg_Laying_System_Architecture.md))

| Dataset | Source | Year | Format | Used In | Status |
|---------|--------|------|--------|---------|--------|
| FLP peptide knockout phenotypes | [Li et al. 1999](https://doi.org/10.1111/j.1749-6632.1999.tb07895.x), Rogers 2003 | 1999+ | Behavioral assays (locomotion, reversal) | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) validation | ⚠️ Extract from papers |
| EGL mutant phenotypes | [Trent et al. 1983](https://doi.org/10.1093/genetics/104.4.619) (145 mutants) | 1983+ | Egg-laying defects (frequency, timing) | [DD018](DD018_Egg_Laying_System_Architecture.md) validation | ⚠️ Extract from papers |
| Serotonin pharmacology | [Waggoner et al. 1998](https://doi.org/10.1016/S0896-6273(00)80527-9) | 1998 | Exogenous 5-HT effects on egg-laying | [DD018](DD018_Egg_Laying_System_Architecture.md) validation | ⚠️ Extract from paper |

### Training Datasets for ML Components ([DD017](DD017_Hybrid_Mechanistic_ML_Framework.md))

| Dataset | Source | Format | Used In | Status |
|---------|--------|--------|---------|--------|
| **SPH simulation runs** (muscle activation → trajectory) | Generate from Sibernetic | HDF5 (500-1000 runs) | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 2 (SPH surrogate) | 📝 **Generate in Phase 3** (~2,500 GPU-hours) |
| Ion channels with known kinetics | PDB + electrophysiology papers | CSV (channel, structure, HH params) | [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (structure→kinetics) | ⚠️ Curate from literature (~50-100 channels) |
| Sensory neuron calcium imaging | Suzuki 2003/2008, Chalasani 2007, others | CSV (stimulus → Ca response) | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4 (learned sensory) | ⚠️ Extract from papers |

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

## Frequently Asked Questions

**Q: Why is Phase A first if it's infrastructure, not science?**
A: Without the config system ([DD013](DD013_Simulation_Stack_Architecture.md)) and automated validation ([DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)), contributors can't test their work efficiently. Better to invest 4 weeks in infrastructure that enables the next 18 months of science, than to implement science DDs without the tools to validate them.

**Q: Can Phase 3 organ DDs ([DD007](DD007_Pharyngeal_System_Architecture.md), [DD009](DD009_Intestinal_Oscillator_Model.md), [DD018](DD018_Egg_Laying_System_Architecture.md)) be implemented in parallel?**
A: Yes — they're semi-independent subsystems. Different contributors can work on pharynx, intestine, and egg-laying simultaneously. [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (hybrid ML) can also proceed in parallel.

**Q: Why is [DD004](DD004_Mechanical_Cell_Identity.md) (Cell Identity) in Phase 4, not earlier?**
A: [DD004](DD004_Mechanical_Cell_Identity.md) requires per-cell mechanical properties (elasticity, adhesion) that are informed by organ system behavior. Better to implement organs first (Phase 3), observe their mechanics, then add cell-specific properties in Phase 4. [DD004](DD004_Mechanical_Cell_Identity.md) is also needed for [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) mesh deformation.

**Q: What if Phase 1 [DD005](DD005_Cell_Type_Differentiation_Strategy.md) fails validation (Tier 2 doesn't improve)?**
A: The calibration approach (expression→conductance scaling) is uncertain. If it fails, fall back to [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 3 (foundation model→params) or manual curation. [DD005](DD005_Cell_Type_Differentiation_Strategy.md)'s scientific risk is why it's Phase 1 — validate the approach early before building more on top of it.

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
