# OpenWorm GitHub Organization — Repository Inventory

- **Last Updated:** 2026-02-19
- **Total Repositories:** 109
- **Source:** [github.com/orgs/openworm](https://github.com/orgs/openworm/repositories)

---

## Purpose

This inventory identifies which of OpenWorm's 109 GitHub repositories are:

1. **Active and maintained** (useful for current DD work)
2. **Referenced in Design Documents** (DD001-DD021)
3. **Dormant but potentially reusable** (could be revived)
4. **Deprecated** (archived, do not use)

---

## Core Simulation Stack (5 repos)

**These repos implement [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md)–[DD003](../design_documents/DD003_Body_Physics_Architecture.md), [DD013](../design_documents/DD013_Simulation_Stack_Architecture.md)–[DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md), [DD020](../design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md)** — the foundation of the simulation.

| Repository | Last Push | Stars | Status | Design Documents |
|------------|-----------|-------|--------|------------------|
| [OpenWorm](https://github.com/openworm/OpenWorm) | 2026-02-09 | 2,943 | **Active** — Meta-repo | [DD013](../design_documents/DD013_Simulation_Stack_Architecture.md) |
| [c302](https://github.com/openworm/c302) | 2026-02-18 | 135 | **Active** | [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md), [DD002](../design_documents/DD002_Muscle_Model_Architecture.md), [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md)–[DD009](../design_documents/DD009_Intestinal_Oscillator_Model.md), [DD018](../design_documents/DD018_Egg_Laying_System_Architecture.md)–[DD019](../design_documents/DD019_Closed_Loop_Touch_Response.md) |
| [sibernetic](https://github.com/openworm/sibernetic) | 2026-02-13 | 384 | **Active** | [DD002](../design_documents/DD002_Muscle_Model_Architecture.md) (coupling), [DD003](../design_documents/DD003_Body_Physics_Architecture.md), [DD004](../design_documents/DD004_Mechanical_Cell_Identity.md), [DD007](../design_documents/DD007_Pharyngeal_System_Architecture.md), [DD019](../design_documents/DD019_Closed_Loop_Touch_Response.md) |
| [ConnectomeToolbox](https://github.com/openworm/ConnectomeToolbox) | 2026-02-19 | 4 | **Active** (Neural Circuit L4 Maintainer) | [DD020](../design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) |
| [Worm3DViewer](https://github.com/openworm/Worm3DViewer) | 2025-12-01 | 0 | **Active** (visualization prototype) | [DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md), [DD014.2](../design_documents/DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) |

**All 5 are essential.** Changes to these repos affect multiple DDs.

---

## Data Access Layer (5 repos)

| Repository | Last Push | Stars | Status | Design Documents |
|------------|-----------|-------|--------|------------------|
| [owmeta](https://github.com/openworm/owmeta) | 2024-07-29 | 153 | **Deferred** (Phase 3+) | [DD008](../design_documents/DD008_Data_Integration_Pipeline.md) — see [OWMeta Ecosystem](#owmeta-ecosystem-9-repos-deferred-to-phase-3) |
| [owmeta-core](https://github.com/openworm/owmeta-core) | 2025-03-18 | 3 | **Deferred** (Phase 3+) | [DD008](../design_documents/DD008_Data_Integration_Pipeline.md) — see [OWMeta Ecosystem](#owmeta-ecosystem-9-repos-deferred-to-phase-3) |
| [tracker-commons](https://github.com/openworm/tracker-commons) | 2025-04-23 | 14 | **Maintained** | [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (WCON 1.0 spec) |
| [open-worm-analysis-toolbox](https://github.com/openworm/open-worm-analysis-toolbox) | 2020-01-16 | 48 | **Archived** — **Revival needed** | [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 3), [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (revival plan) |
| [movement_validation](https://github.com/openworm/movement_validation) | 2017-06-21 | 16 | **ARCHIVED** — Do not use | [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (historical — superseded by analysis toolbox) |

**Status:**

- `cect` (ConnectomeToolbox) is the **working data layer** for Phase 1-2 ([DD020](../design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md))
- `owmeta` is **deferred to Phase 3+** ([DD008](../design_documents/DD008_Data_Integration_Pipeline.md) acknowledges this)
- Analysis toolbox **blocks Tier 3 validation** ([DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) 8-task revival plan, 33 hours)

---

## NeuroML / Modeling (4 repos)

| Repository | Last Push | Stars | Status | Design Documents |
|------------|-----------|-------|--------|------------------|
| [CElegansNeuroML](https://github.com/openworm/CElegansNeuroML) | 2023-03-30 | 140 | **Archived** (authoritative NeuroML files) | [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md) (NeuroML cell definitions) |
| [Blender2NeuroML](https://github.com/openworm/Blender2NeuroML) | 2026-02-17 | 17 | **Active** | [DD014.2](../design_documents/DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (Virtual Worm meshes source) |
| [muscle_model](https://github.com/openworm/muscle_model) | 2025-05-15 | 48 | **Maintained** | [DD002](../design_documents/DD002_Muscle_Model_Architecture.md) (Boyle & Cohen implementation) |
| [hodgkin_huxley_tutorial](https://github.com/openworm/hodgkin_huxley_tutorial) | 2025-10-30 | 49 | **Active** | [DD011](../design_documents/DD011_Contributor_Progression_Model.md) (orientation badge "HH Tutorial Graduate") |

!!! note
    `CElegansNeuroML` is dormant but its NeuroML files are still authoritative. [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md) references this repo for cell template locations.

---

## Visualization / Browsers (6 repos)

| Repository | Last Push | Stars | Status | Design Documents |
|------------|-----------|-------|--------|------------------|
| [Worm3DViewer](https://github.com/openworm/Worm3DViewer) | 2025-12-01 | 0 | **Active** (Neural Circuit L4 Maintainer) | [DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md) Phase 1 (Trame viewer evolution) |
| [wormbrowser](https://github.com/openworm/wormbrowser) | 2026-02-13 | 49 | **Active** | [DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md) (historical 3D browser, still maintained) |
| [openwormbrowser-ios](https://github.com/openworm/openwormbrowser-ios) | 2026-01-20 | 20 | **Active** | Mobile version of worm browser |
| [WCONViewer](https://github.com/openworm/WCONViewer) | 2025-12-17 | 0 | **Maintained** | [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (WCON visualization tool) |
| [Worm2D](https://github.com/openworm/Worm2D) | 2025-07-24 | 0 | **Maintained** | 2D worm simulation |
| [WormWorx](https://github.com/openworm/WormWorx) | 2025-09-05 | 7 | **Maintained** | Alternative *C. elegans* simulator |

---

## Geppetto Platform (5 repos) — Deferred

| Repository | Last Push | Stars | Status | Notes |
|------------|-----------|-------|--------|-------|
| [org.geppetto.frontend](https://github.com/openworm/org.geppetto.frontend) | 2025-04-03 | 29 | **Deferred** | [DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md) mentions Geppetto (not using for Phase 1-2) |
| [geppetto-client](https://github.com/openworm/geppetto-client) | 2025-04-18 | 6 | **Deferred** | |
| [org.geppetto.core](https://github.com/openworm/org.geppetto.core) | 2025-03-28 | 22 | **Deferred** | |
| [org.geppetto.datasources](https://github.com/openworm/org.geppetto.datasources) | 2025-03-28 | 2 | **Deferred** | |
| [org.geppetto.docs](https://github.com/openworm/org.geppetto.docs) | 2020-08-04 | 3 | **Archived** | |

**[DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md) Decision:** Not using Geppetto for Phase 1-2 (too heavy, Java-based). Using Trame (PyVista) instead. Geppetto could be revisited in Phase 3 if needed.

---

## AI / LLM Integration (1 repo)

| Repository | Last Push | Stars | Status | Purpose |
|------------|-----------|-------|--------|---------|
| [openworm.ai](https://github.com/openworm/openworm.ai) | 2026-02-19 | 3 | **VERY ACTIVE** | LLM/AI scripts — may inform [DD015](../design_documents/DD015_AI_Contributor_Model.md) (AI Contributors) |

!!! note
    This repo is brand new or recently revived. Should be reviewed for [DD015](../design_documents/DD015_AI_Contributor_Model.md) AI contributor infrastructure.

---

## Educational / Outreach (3 repos)

| Repository | Last Push | Stars | Status | Purpose |
|------------|-----------|-------|--------|---------|
| [hodgkin_huxley_tutorial](https://github.com/openworm/hodgkin_huxley_tutorial) | 2025-10-30 | 49 | **Active** | [DD011](../design_documents/DD011_Contributor_Progression_Model.md) badge "Neuron Modeling Foundations" |
| [openworm.github.io](https://github.com/openworm/openworm.github.io) | 2026-02-01 | 29 | **Active** | Website (static HTML) |
| [openworm_docs](https://github.com/openworm/openworm_docs) | 2024-07-02 | 44 | **Inactive** (being replaced by this site) | ReadTheDocs documentation |

---

## Research Models & Data (17 repos)

External research code and datasets forked into the OpenWorm org. Not under active OpenWorm development, but code is recent and directly reusable for DDs.

| Repository | Last Push | Stars | DD Reuse |
|------------|-----------|-------|----------|
| [CE_locomotion](https://github.com/openworm/CE_locomotion) | 2026-02-18 | 2 | **VERY ACTIVE** — [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md)–[DD003](../design_documents/DD003_Body_Physics_Architecture.md) (neuromechanical locomotion), [DD023](../design_documents/DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (proprioceptive model, 30-50 hr savings) |
| [NicolettiEtAl2024_MN_IN](https://github.com/openworm/NicolettiEtAl2024_MN_IN) | 2025-11-04 | 0 | [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md), [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (motor/interneuron HH models), [DD007](../design_documents/DD007_Pharyngeal_System_Architecture.md) (pharyngeal neuron init), [DD023](../design_documents/DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (B-class templates) |
| [wormneuroatlas](https://github.com/openworm/wormneuroatlas) | 2025-10-22 | 2 | [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (CeNGEN), [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 2 — Randi 2023 data), [DD020](../design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) (complementary connectome data) |
| [CelegansNeuromechanicalGaitModulation](https://github.com/openworm/CelegansNeuromechanicalGaitModulation) | 2025-08-01 | 1 | [DD003](../design_documents/DD003_Body_Physics_Architecture.md) (gait physics), [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (surrogate training data), [DD023](../design_documents/DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (proprioceptive/curvature logic) |
| [tierpsy-tracker](https://github.com/openworm/tierpsy-tracker) | 2025-06-29 | 2 | [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 3 validation tool), [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (may replace 33-hr toolbox revival) |
| [JohnsonMailler_MuscleModel](https://github.com/openworm/JohnsonMailler_MuscleModel) | 2025-05-15 | 2 | [DD002](../design_documents/DD002_Muscle_Model_Architecture.md) (alternative muscle model), [DD007](../design_documents/DD007_Pharyngeal_System_Architecture.md) (Ca²⁺ coupling for pharyngeal muscle) |
| [NeuroPAL](https://github.com/openworm/NeuroPAL) | 2025-04-29 | 5 | [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (cell ID validation), [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 1 neuron ID), [DD024](../design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) (validation data) |
| [NicolettiEtAl2019_NeuronModels](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) | 2025-04-28 | 1 | [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md)/[DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (AWCon, RMD HH fits), [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 1 calibration expansion) |
| [wormpose](https://github.com/openworm/wormpose) | 2025-02-21 | 0 | [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (Component 4 training data), [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (skeleton format bridge) |
| [PlateauNoiseModel](https://github.com/openworm/PlateauNoiseModel) | 2025-01-30 | 0 | [DD007](../design_documents/DD007_Pharyngeal_System_Architecture.md) (pharyngeal plateau potentials — already cited) |
| [sibernetic_v3](https://github.com/openworm/sibernetic_v3) | 2024-09-27 | 1 | [DD003](../design_documents/DD003_Body_Physics_Architecture.md) (next-gen SPH), [DD013](../design_documents/DD013_Simulation_Stack_Architecture.md) (simulation stack), [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (bulk training data gen) |
| [NemaNode](https://github.com/openworm/NemaNode) | 2024-05-30 | 1 | [DD020](../design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) (cross-validation connectome data), [DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md) (interactive visualization reference) |
| [worm-functional-connectivity](https://github.com/openworm/worm-functional-connectivity) | 2023-07-07 | 0 | [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 2 alt. functional connectivity), [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (loss function target) |
| [multi-dev-sibernetic](https://github.com/openworm/multi-dev-sibernetic) | 2023-01-20 | 1 | [DD003](../design_documents/DD003_Body_Physics_Architecture.md) (multi-device SPH), [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (bulk sim data gen), [DD023](../design_documents/DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (coupling patterns) |
| [wormvae](https://github.com/openworm/wormvae) | 2022-04-26 | 0 | [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (connectome-constrained VAE — Components 2/4) |
| [WormsenseLab_ASH](https://github.com/openworm/WormsenseLab_ASH) | 2021-09-28 | 3 | [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (ASH calibration — already cited), [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 1 electrophysiology) |
| [owmeta-sciunit](https://github.com/openworm/owmeta-sciunit) | 2021-04-23 | 2 | [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 1 SciUnit framework), [DD013](../design_documents/DD013_Simulation_Stack_Architecture.md) (CI integration) |

**High-priority evaluations:**

- **tierpsy-tracker:** If the OpenWorm fork reads WCON, it may replace the entire 33-hour analysis toolbox revival ([DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md))
- **CE_locomotion:** Already implements `StretchReceptor.cpp` — 30-50 hours of proprioception work saved ([DD023](../design_documents/DD023_Proprioceptive_Feedback_and_Motor_Coordination.md))
- **NicolettiEtAl models:** Published HH parameter fits expand the ~20-neuron calibration set for [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md)

---

## Repo-to-DD Cross-Reference

| DD | Primary Repos | Secondary Repos (research/reuse) |
|----|--------------|-----------------------------------|
| [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md) (Neural) | c302, CElegansNeuroML | hodgkin_huxley_tutorial (education), NicolettiEtAl2024_MN_IN, NicolettiEtAl2019_NeuronModels (HH fits) |
| [DD002](../design_documents/DD002_Muscle_Model_Architecture.md) (Muscle) | c302, sibernetic (coupling) | muscle_model, JohnsonMailler_MuscleModel (alternatives) |
| [DD003](../design_documents/DD003_Body_Physics_Architecture.md) (Body Physics) | sibernetic | sibernetic_v3 (next-gen), multi-dev-sibernetic (multi-device), CelegansNeuromechanicalGaitModulation (gait) |
| [DD004](../design_documents/DD004_Mechanical_Cell_Identity.md) (Cell Identity) | sibernetic | — |
| [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (Cell Differentiation) | c302, wormneuroatlas | NeuroPAL (cell ID), NicolettiEtAl models (calibration), WormsenseLab_ASH (electrophysiology) |
| [DD006](../design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) (Neuropeptides) | c302 | — |
| [DD007](../design_documents/DD007_Pharyngeal_System_Architecture.md) (Pharynx) | c302 | PlateauNoiseModel (plateau potentials), JohnsonMailler_MuscleModel (Ca²⁺ coupling), NicolettiEtAl models (pharyngeal neurons) |
| [DD008](../design_documents/DD008_Data_Integration_Pipeline.md) (Data Integration) | owmeta, owmeta-core | ConnectomeToolbox (Phase 1-2 bridge), owmeta ecosystem (9 repos — see below) |
| [DD009](../design_documents/DD009_Intestinal_Oscillator_Model.md) (Intestine) | c302 | — |
| [DD010](../design_documents/DD010_Validation_Framework.md) (Validation) | open-worm-analysis-toolbox, tracker-commons | wormneuroatlas (Tier 2), tierpsy-tracker (Tier 3), owmeta-sciunit (Tier 1), worm-functional-connectivity (Tier 2 alt.), NicolettiEtAl models (Tier 1 calibration) |
| [DD013](../design_documents/DD013_Simulation_Stack_Architecture.md) (Integration) | OpenWorm (meta-repo) | owmeta-sciunit (CI validation) |
| [DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md) (Visualization) | Worm3DViewer, OpenWorm (Docker) | wormbrowser, WCONViewer, Worm2D, NemaNode (interactive reference) |
| [DD014.2](../design_documents/DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (Mesh Deformation) | Blender2NeuroML (Virtual Worm meshes) | — |
| [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (Hybrid ML) | openworm-ml (TBD) | CE_locomotion, wormvae (VAE), wormpose (pose data), CelegansNeuromechanicalGaitModulation (training data), multi-dev-sibernetic (bulk sims) |
| [DD018](../design_documents/DD018_Egg_Laying_System_Architecture.md) (Egg-Laying) | c302 | — |
| [DD019](../design_documents/DD019_Closed_Loop_Touch_Response.md) (Touch) | c302, sibernetic (bidirectional coupling) | — |
| [DD020](../design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) (Connectome) | ConnectomeToolbox | wormneuroatlas (complementary), NemaNode (cross-validation), VarshneyEtAl2011 (historical) |
| [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (Movement Toolbox) | open-worm-analysis-toolbox, tracker-commons | tierpsy-tracker (may replace toolbox), wormpose (skeleton bridge) |
| [DD023](../design_documents/DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (Proprioception) | c302, sibernetic | CE_locomotion (StretchReceptor.cpp), CelegansNeuromechanicalGaitModulation (gait logic), NicolettiEtAl2024_MN_IN (B-class templates) |
| [DD024](../design_documents/DD024_Validation_Data_Acquisition_Pipeline.md) (Validation Data) | — | NeuroPAL, wormneuroatlas (validation datasets) |

---

## For DD Authors: How to Reference Repos

**In Integration Contract — Repository & Packaging section:**

```markdown
| Item | Value |
|------|-------|
| **Repository** | `openworm/c302` |
| **Docker stage** | `neural` in multi-stage Dockerfile (DD013) |
| **`versions.lock` key** | `c302` |
| **Build dependencies** | NEURON 8.2.6 (pip), ConnectomeToolbox/`cect` (pip), pyNeuroML (pip) |
```

**Always link to repos:**

- Use full URL in first mention: [`openworm/c302`](https://github.com/openworm/c302)
- Subsequent mentions: `c302` (no link needed)

---

## OWMeta Ecosystem (9 repos) — Deferred to Phase 3+

[DD008](../design_documents/DD008_Data_Integration_Pipeline.md) defers OWMeta integration to Phase 3+. These repos are working code but not needed until the semantic data layer is activated. `cect` (ConnectomeToolbox) serves as the Phase 1-2 data bridge.

| Repository | Last Push | Stars | Role |
|------------|-----------|-------|------|
| [owmeta](https://github.com/openworm/owmeta) | 2024-07-29 | 153 | Primary data integration — semantic RDF graph |
| [owmeta-core](https://github.com/openworm/owmeta-core) | 2025-03-18 | 3 | Core library for OWMeta |
| [owmeta-bundles](https://github.com/openworm/owmeta-bundles) | 2023-05-19 | 2 | Data bundles for owmeta |
| [owmeta-pytest-plugin](https://github.com/openworm/owmeta-pytest-plugin) | 2023-02-04 | 2 | Pytest plugin for testing with owmeta-core |
| [owmeta-core-data](https://github.com/openworm/owmeta-core-data) | 2023-01-20 | 1 | Schema data for owmeta-core |
| [owmeta-movement](https://github.com/openworm/owmeta-movement) | 2021-12-24 | 2 | Movement data utilities ([DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) related) |
| [owmeta-modeldb](https://github.com/openworm/owmeta-modeldb) | 2021-05-10 | 2 | ModelDB integration |
| [rdflib-zodb](https://github.com/openworm/rdflib-zodb) | 2022-05-30 | 2 | RDFLib Store backed by ZODB |
| [YAROM](https://github.com/openworm/YAROM) | 2020-01-25 | 3 | Yet Another RDF-Object Mapper (predecessor to owmeta-core) |

---

## Inactive Repos (14 repos)

Post-2020 activity but no current DD priority. Not broken, just not in the critical path.

| Repository | Last Push | Stars | Description |
|------------|-----------|-------|-------------|
| [MetaWorm](https://github.com/openworm/MetaWorm) | 2024-06-30 | 2 | Related project — see [Full History](../fullhistory.md#projects-similar-to-openworm) |
| [simulate](https://github.com/openworm/simulate) | 2025-03-07 | 0 | Links to online simulations of the worm |
| [VarshneyEtAl2011](https://github.com/openworm/VarshneyEtAl2011) | 2024-02-09 | 0 | Historical connectome data ([DD020](../design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) uses Cook2019 instead) |
| [bt-gsoc-2019](https://github.com/openworm/bt-gsoc-2019) | 2024-01-29 | 1 | BitTorrent Client, Access Control and Data Integrity (GSoC) |
| [OpenWormData](https://github.com/openworm/OpenWormData) | 2023-06-02 | 3 | Data bundle — superseded by cect/owmeta |
| [movement_cloud](https://github.com/openworm/movement_cloud) | 2022-11-15 | 6 | Cloud movement analysis — superseded by [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) revival plan |
| [Newsletter](https://github.com/openworm/Newsletter) | 2022-09-10 | 1 | Community newsletter |
| [sibernetic_view](https://github.com/openworm/sibernetic_view) | 2022-07-30 | 0 | Sibernetic model viewer |
| [hydramuscle](https://github.com/openworm/hydramuscle) | 2022-06-16 | 1 | Biophysical model of the muscle of *Hydra* (not *C. elegans*) |
| [robots](https://github.com/openworm/robots) | 2021-11-10 | 24 | *C. elegans* robots |
| [worm-math-book](https://github.com/openworm/worm-math-book) | 2021-06-12 | 2 | Online book: mathematical concepts and models |
| [openworm-scholar](https://github.com/openworm/openworm-scholar) | 2021-05-09 | 2 | Enhanced notifications of published research |
| [jenkins](https://github.com/openworm/jenkins) | 2021-01-05 | 1 | Old CI infrastructure |
| [simple-C-elegans](https://github.com/openworm/simple-C-elegans) | 2020-06-08 | 6 | Minimalist Python *C. elegans* model — [DD011](../design_documents/DD011_Contributor_Progression_Model.md) onboarding resource |

---

## Archived / Pre-2020 Repository List (21 repos)

Last pushed before Jan 2020. Historical or experimental. May contain useful code or data but likely requires modernization.

| Repository | Last Push | Stars | Description | Potential DD Reuse |
|------------|-----------|-------|-------------|-------------------|
| [OpenData](https://github.com/openworm/OpenData) | 2019-08-25 | 4 | GSoC 2019 Open Data project | — |
| [ChannelWorm2](https://github.com/openworm/ChannelWorm2) | 2018-09-16 | 11 | Ion channel models (v2) | [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (ion channel curation) |
| [ChannelWorm](https://github.com/openworm/ChannelWorm) | 2018-08-27 | 12 | Ion channel models (v1) | [DD005](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (ion channel database, HH fitter) |
| [model_completion_dashboard](https://github.com/openworm/model_completion_dashboard) | 2018-07-08 | 2 | Model Completion Dashboard | — |
| [tests](https://github.com/openworm/tests) | 2018-06-03 | 3 | Cross-repo tests | [DD013](../design_documents/DD013_Simulation_Stack_Architecture.md) (historical CI patterns) |
| [recurrent](https://github.com/openworm/recurrent) | 2018-02-12 | 2 | Natural language date parsing | — |
| [org.wormsim.frontend](https://github.com/openworm/org.wormsim.frontend) | 2017-08-12 | 3 | WormSim frontend | — |
| [movement_validation_cloud](https://github.com/openworm/movement_validation_cloud) | 2017-05-13 | 1 | Cloud movement validation | — |
| [owcs](https://github.com/openworm/owcs) | 2017-04-16 | 2 | — | — |
| [neuronal-analysis](https://github.com/openworm/neuronal-analysis) | 2017-03-05 | 4 | Neuronal dataset tools | [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 1 comparison scripts) |
| [behavioral_syntax](https://github.com/openworm/behavioral_syntax) | 2017-01-30 | 5 | Behavioral syntax (Andre Brown) | [DD010](../design_documents/DD010_Validation_Framework.md) (Tier 3 behavioral features) |
| [pharyngeal_muscle_model](https://github.com/openworm/pharyngeal_muscle_model) | 2017-01-19 | 3 | pm3 pharyngeal muscle NEURON model | [DD007](../design_documents/DD007_Pharyngeal_System_Architecture.md) (Ca²⁺ oscillations — already cited, 20-30 hr savings) |
| [CyberElegans](https://github.com/openworm/CyberElegans) | 2016-12-19 | 36 | Neuromechanical model | [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md)–[DD003](../design_documents/DD003_Body_Physics_Architecture.md), [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (benchmark) |
| [sibernetic_NEURON](https://github.com/openworm/sibernetic_NEURON) | 2016-12-19 | 5 | Sibernetic-NEURON interface | [DD013](../design_documents/DD013_Simulation_Stack_Architecture.md) (coupling patterns) |
| [skeletonExtraction](https://github.com/openworm/skeletonExtraction) | 2016-12-19 | 8 | Sibernetic → COLLADA animation | [DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md), [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (skeleton extraction logic) |
| [sibernetic_config_gen](https://github.com/openworm/sibernetic_config_gen) | 2016-12-19 | 4 | Sibernetic scene config generator | [DD013](../design_documents/DD013_Simulation_Stack_Architecture.md) (scene generation) |
| [BlueBrainProjectShowcase](https://github.com/openworm/BlueBrainProjectShowcase) | 2016-10-18 | 2 | BBP models in NeuroML | [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md) (NeuroML reference models) |
| [SegWorm](https://github.com/openworm/SegWorm) | 2016-05-27 | 5 | Schafer lab MATLAB code (Yemini) | [DD021](../design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (historical ground truth) |
| [HeuristicWorm](https://github.com/openworm/HeuristicWorm) | 2015-05-11 | 3 | Heuristic worm model | — |
| [org.wormsim.bower](https://github.com/openworm/org.wormsim.bower) | 2015-04-29 | 2 | WormSim bower UI components | — |
| [bionet](https://github.com/openworm/bionet) | 2015-04-26 | 32 | Artificial biological neural network | [DD017](../design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) (neural network architecture) |

---

## Maintenance Status Legend

| Status | Meaning |
|--------|---------|
| **Active** | Commits within last 3 months, actively developed |
| **Maintained** | Commits within last year, stable and working |
| **Research** | External research code forked into OpenWorm; recent but not under active OpenWorm development; directly reusable for DDs |
| **Deferred** | Working code, intentionally deferred to a later phase (e.g., OWMeta to Phase 3+) |
| **Inactive** | Post-2020 activity but no current DD priority; not broken, just not in the critical path |
| **Archived** | Pre-2020, historical or experimental; may need modernization |
| **ARCHIVED** | Explicitly superseded or deprecated, do not use |

---

- **Total OpenWorm GitHub Repositories:** 109
- **Active / Maintained:** ~20
- **Research Models & Data:** ~17
- **Geppetto Platform (dormant):** 5
- **OWMeta Ecosystem (deferred):** 9
- **Inactive:** ~14
- **Archived (pre-2020):** ~21
- **Other (educational, outreach, etc.):** ~23

- **Maintained by:** Integration L4 Maintainer (when appointed)
- **Next Update:** After Phase A (add any new repos created for organ DDs)
