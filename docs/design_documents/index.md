# Design Documents

## Introduction

**Design Documents (DDs)** are OpenWorm's technical roadmap from today's 302-neuron simulation to the complete 959-cell digital organism. Each DD specifies one subsystem (neurons, muscles, body physics, pharynx, intestine), ensuring every piece is:

- **Biophysically realistic** — grounded in experimental data
- **Causally interpretable** — we can trace why behavior emerges
- **Validated** — tested against real worm physiology and behavior
- **Composable** — subsystems integrate via clean interfaces

## Mission Alignment

!!! quote "OpenWorm Mission"
    "OpenWorm is an open source project dedicated to creating the world's first virtual organism in a computer, a *C. elegans* nematode."

**Design Documents serve this mission** by providing the complete architectural blueprint — from ion channels to organism behavior — with quantitative success criteria and experimental validation at every level.

**Core Principle:** "Worms are soft and squishy. So our model has to be too. We are building in the physics of muscles, soft tissues and fluids. Because it matters."

## Quick Links

**New to Design Documents?**

- 📋 [DD012: RFC Process](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD012_Design_Document_RFC_Process.md) — How DDs work
- 🌟 [DD005: Cell Differentiation](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD005_Cell_Type_Differentiation_Strategy.md) — Reference implementation
- 🗺️ [Integration Map](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/INTEGRATION_MAP.md) — How all DDs couple together
- 📅 [Phase Roadmap](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD_PHASE_ROADMAP.md) — 18-month timeline to 959 cells

**Analysis & Resources:**

- 📊 [Comprehensive Analysis](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD_COMPREHENSIVE_ANALYSIS_2026-02-19.md) — Inconsistencies, gaps, recommendations
- 💎 [Code Reuse Opportunities](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD_CODE_REUSE_OPPORTUNITIES.md) — Existing repos, 200-300 hour savings
- 📦 [GitHub Repo Inventory](https://github.com/SlarsonTech/openworm-admin/blob/main/GITHUB_REPO_INVENTORY.md) — All 109 OpenWorm repositories

---

## Implementation Roadmap (By Phase)

### Phase 0: Existing Foundation ✅

**Milestone:** "First Whole-Nervous-System Simulation" (already achieved)

| DD | Title | Status | What It Does |
|----|-------|--------|--------------|
| [DD001](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD001_Neural_Circuit_Architecture.md) | Neural Circuit Architecture | ✅ Accepted | 302 neurons, HH Level C1, graded synapses |
| [DD002](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD002_Muscle_Model_Architecture.md) | Muscle Model Architecture | ✅ Accepted | 95 muscles, Ca²⁺→force coupling |
| [DD003](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD003_Body_Physics_Architecture.md) | Body Physics Architecture | ✅ Accepted | Sibernetic SPH, ~100K particles |
| [DD020](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) | Connectome Data Access | ✅ Accepted | cect API, Cook2019 default |

### Phase A: Infrastructure Bootstrap ⚠️

**Milestone:** "Containerized Stack with Automated Validation"
**Duration:** 4 weeks
**Status:** Proposed — must complete before modeling phases

| DD | Title | What It Delivers |
|----|-------|------------------|
| [DD013](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD013_Simulation_Stack_Architecture.md) | Simulation Stack | Docker, CI/CD, openworm.yml config |
| [DD021](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | Movement Toolbox Revival | Tier 3 validation (8 tasks, 33 hours) |
| [DD012](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD012_Design_Document_RFC_Process.md) | RFC Process | DD template, governance |
| [DD011](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD011_Contributor_Progression_Model.md) | Contributor Progression | Observer to Senior Contributor (L0-L5) |

### Phase 1: Cell-Type Differentiation ⚠️

**Milestone:** "Biologically Distinct Neurons"
**Duration:** 3 months
**Key:** 128 neuron classes from CeNGEN, functional connectivity improves ≥20%

| DD | Title | What Changes |
|----|-------|--------------|
| [DD005](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD005_Cell_Type_Differentiation_Strategy.md) | Cell-Type Differentiation | 128 distinct neuron classes (not 302 identical) |
| [DD014 Phase 1](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD014_Dynamic_Visualization_Architecture.md) | Trame Viewer | OME-Zarr export, organism + tissue scales |
| [DD010 Tier 2](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD010_Validation_Framework.md) | Functional Connectivity | Validate vs. Randi 2023 (r > 0.5) |

### Phase 2: Slow Modulation + Closed-Loop ⚠️

**Milestone:** "The Worm Can Feel and Modulate"
**Duration:** 3 months
**Key:** 31,479 neuropeptide connections + bidirectional touch response

| DD | Title | What Adds |
|----|-------|-----------|
| [DD006](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) | Neuropeptides | GPCR modulation, seconds timescale |
| [DD019](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD019_Closed_Loop_Touch_Response.md) | Touch Response | MEC-4 channel, tap withdrawal |
| [DD022](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD022_Environmental_Modeling_and_Stimulus_Delivery.md) | Environment | Gradients, substrates, stimuli |
| [DD023](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) | Proprioception | Stretch receptors, motor coordination |

### Phase 3: Organ Systems ⚠️

**Milestone:** "Multi-Organ Digital Organism"
**Duration:** 6 months
**Key:** Pharynx, intestine, egg-laying, ML acceleration

| DD | Title | What Adds |
|----|-------|-----------|
| [DD007](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD007_Pharyngeal_System_Architecture.md) | Pharyngeal System | 63 cells, 3-4 Hz pumping |
| [DD009](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD009_Intestinal_Oscillator_Model.md) | Intestinal Oscillator | 20 cells, 50s defecation |
| [DD018](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD018_Egg_Laying_System_Architecture.md) | Egg-Laying System | 28-cell circuit, two-state |
| [DD017](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) | Hybrid ML | Differentiable sim, 1000× speedup |

### Phase 4: Complete Organism ⚠️

**Milestone:** "959-Cell Photorealistic Whole Organism"
**Duration:** 6 months
**Key:** All somatic cells, mesh deformation, public web viewer

| DD | Title | What Adds |
|----|-------|-----------|
| [DD004](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD004_Mechanical_Cell_Identity.md) | Mechanical Cell Identity | 959 cells with cell-type mechanics |
| [DD014.2](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) | Mesh Deformation | GPU skinning, photorealistic |
| [DD014 Phase 3](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD014_Dynamic_Visualization_Architecture.md) | Public Viewer | Molecular scale, viewer.openworm.org |

---

## All Design Documents (Complete List)

!!! tip "Browse on GitHub"
    All Design Documents are maintained in the [openworm-admin repository](https://github.com/SlarsonTech/openworm-admin/tree/main/design_documents).
    **Total:** 25 DDs (DD001-DD023 + DD014.1/DD014.2 + DD016 archived)

### By Topic

**Neural Systems:**
DD001 (architecture), DD005 (differentiation), DD006 (neuropeptides), DD007 (pharynx neurons), DD018 (egg-laying HSN/VC), DD019 (touch neurons)

**Muscle Systems:**
DD002 (body wall), DD007 (pharyngeal), DD018 (reproductive)

**Body Mechanics:**
DD003 (SPH), DD004 (cell identity), DD014.2 (mesh deformation), DD019 (strain readout)

**Organ Systems:**
DD007 (pharynx), DD009 (intestine), DD018 (egg-laying)

**Sensory Systems:**
DD019 (touch/MEC-4), DD022 (environment), DD023 (proprioception)

**Data & Validation:**
DD008 (OWMeta), DD010 (3-tier validation), DD020 (connectome/cect), DD021 (movement toolbox)

**Infrastructure:**
DD013 (simulation stack), DD014 (visualization), DD014.1 (visual rendering), DD014.2 (mesh deformation)

**Governance:**
DD011 (contributor progression), DD012 (RFC process), DD015 (AI contributors)

**Hybrid/Advanced:**
DD017 (mechanistic-ML hybrid)

---

## How to Use Design Documents

### For Contributors

1. **Find a DD** matching your interest (neural modeling → DD001, visualization → DD014, etc.)
2. **Read the "How to Build & Test" section** — copy-pasteable commands, green-light criteria
3. **Check Integration Contract** — what the DD consumes from other DDs, what it produces
4. **Implement according to spec** — DDs define quality criteria and validation procedures
5. **Reference DD in your PR** — Mind-of-a-Worm AI checks for DD compliance

### For Reviewers

1. **Mind-of-a-Worm flags relevant DDs** for each PR automatically
2. **Check Quality Criteria** — does the PR meet the DD's acceptance tests?
3. **Check Integration Contract** — if PR modifies coupling interfaces, coordinate with consuming DDs
4. **Check Alternatives Considered** — is the PR re-proposing a rejected approach?

### Writing a New DD

Follow [DD012 (RFC Process)](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD012_Design_Document_RFC_Process.md) template.
Use [DD005 (Cell Differentiation)](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD005_Cell_Type_Differentiation_Strategy.md) as your reference implementation.

---

## Status Badges

- ✅ **Accepted** — Binding specification, implementations must comply
- ⚠️ **Proposed** — Under review or approved but not yet implemented
- 🔴 **Blocked** — Cannot proceed (missing prerequisite)
- 📦 **Archived** — Deferred or superseded

---

## External Links

- **[GitHub Repository](https://github.com/SlarsonTech/openworm-admin/tree/main/design_documents)** — All DD markdown files
- **[Phase Roadmap](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD_PHASE_ROADMAP.md)** — Timeline and milestones
- **[Integration Map](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/INTEGRATION_MAP.md)** — Dependency graph
- **[Code Reuse Guide](https://github.com/SlarsonTech/openworm-admin/blob/main/design_documents/DD_CODE_REUSE_OPPORTUNITIES.md)** — Accelerate implementation
