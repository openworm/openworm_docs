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

- 📋 [DD012: RFC Process](DD012_Design_Document_RFC_Process.md) — How DDs work
- 🌟 [DD005: Cell Differentiation](DD005_Cell_Type_Differentiation_Strategy.md) — Reference implementation
- 🗺️ [Integration Map](INTEGRATION_MAP.md) — How all DDs couple together
- 📅 [Phase Roadmap](DD_PHASE_ROADMAP.md) — 18-month timeline to 959 cells

**Analysis & Resources:**

- 📊 [Comprehensive Analysis](DD_COMPREHENSIVE_ANALYSIS_2026-02-19.md) — Inconsistencies, gaps, recommendations
- 💎 [Code Reuse Opportunities](DD_CODE_REUSE_OPPORTUNITIES.md) — Existing repos, 200-300 hour savings
- 📦 [GitHub Repo Inventory](https://github.com/openworm/openworm-admin/blob/main/GITHUB_REPO_INVENTORY.md) — All 109 OpenWorm repositories

---

## Implementation Roadmap (By Phase)

### Phase 0: Existing Foundation ✅

**Milestone:** "First Whole-Nervous-System Simulation" (already achieved)

| DD | Title | Status | What It Does |
|----|-------|--------|--------------|
| [DD001](DD001_Neural_Circuit_Architecture.md) | Neural Circuit Architecture | ✅ Accepted | 302 neurons, HH Level C1, graded synapses |
| [DD002](DD002_Muscle_Model_Architecture.md) | Muscle Model Architecture | ✅ Accepted | 95 muscles, Ca²⁺→force coupling |
| [DD003](DD003_Body_Physics_Architecture.md) | Body Physics Architecture | ✅ Accepted | Sibernetic SPH, ~100K particles |
| [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) | Connectome Data Access | ✅ Accepted | cect API, [Cook2019](https://doi.org/10.1038/s41586-019-1352-7) default |

### Infrastructure Bootstrap ⚠️

**Milestone:** "Containerized Stack with Automated Validation"
**Duration:** 4 weeks
**Status:** Proposed — must complete before modeling phases

| DD | Title | What It Delivers |
|----|-------|------------------|
| [DD013](DD013_Simulation_Stack_Architecture.md) | Simulation Stack | Docker, CI/CD, openworm.yml config |
| [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | Movement Toolbox Revival | Tier 3 validation (8 tasks, 33 hours) |
| [DD012](DD012_Design_Document_RFC_Process.md) | RFC Process | DD template, governance |
| [DD011](DD011_Contributor_Progression_Model.md) | Contributor Progression | Observer to Senior Contributor (L0-L5) |

### Phase 1: Cell-Type Differentiation ⚠️

**Milestone:** "Biologically Distinct Neurons"
**Duration:** 3 months
**Key:** 128 neuron classes from CeNGEN, functional connectivity improves ≥20%

| DD | Title | What Changes |
|----|-------|--------------|
| [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Cell-Type Differentiation | 128 distinct neuron classes (not 302 identical) |
| [DD014 Phase 1](DD014_Dynamic_Visualization_Architecture.md) | Trame Viewer | OME-Zarr export, organism + tissue scales |
| [DD010 Tier 2](DD010_Validation_Framework.md) | Functional Connectivity | Validate vs. [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) (r > 0.5) |

### Phase 2: Slow Modulation + Closed-Loop ⚠️

**Milestone:** "The Worm Can Feel and Modulate"
**Duration:** 3 months
**Key:** 31,479 neuropeptide connections + bidirectional touch response

| DD | Title | What Adds |
|----|-------|-----------|
| [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Neuropeptides | GPCR modulation, seconds timescale |
| [DD019](DD019_Closed_Loop_Touch_Response.md) | Touch Response | MEC-4 channel, tap withdrawal |
| [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) | Environment | Gradients, substrates, stimuli |
| [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) | Proprioception | Stretch receptors, motor coordination |

### Phase 3: Organ Systems ⚠️

**Milestone:** "Multi-Organ Digital Organism"
**Duration:** 6 months
**Key:** Pharynx, intestine, egg-laying, ML acceleration

| DD | Title | What Adds |
|----|-------|-----------|
| [DD007](DD007_Pharyngeal_System_Architecture.md) | Pharyngeal System | 63 cells, 3-4 Hz pumping |
| [DD009](DD009_Intestinal_Oscillator_Model.md) | Intestinal Oscillator | 20 cells, 50s defecation |
| [DD018](DD018_Egg_Laying_System_Architecture.md) | Egg-Laying System | 28-cell circuit, two-state |
| [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) | Hybrid ML | Differentiable sim, 1000× speedup |

### Phase 4: Complete Organism ⚠️

**Milestone:** "959-Cell Photorealistic Whole Organism"
**Duration:** 6 months
**Key:** All somatic cells, mesh deformation, public web viewer

| DD | Title | What Adds |
|----|-------|-----------|
| [DD004](DD004_Mechanical_Cell_Identity.md) | Mechanical Cell Identity | 959 cells with cell-type mechanics |
| [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) | Mesh Deformation | GPU skinning, photorealistic |
| [DD014 Phase 3](DD014_Dynamic_Visualization_Architecture.md) | Public Viewer | Molecular scale, viewer.openworm.org |

---

## All Design Documents (Complete List)

!!! tip "Browse on GitHub"
    All Design Documents are maintained in the [openworm-admin repository](https://github.com/openworm/openworm-admin/tree/main/design_documents).
    **Total:** 25 DDs ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) + [DD014.1](DD014.1_Visual_Rendering_Specification.md)/DD014.2 + DD016 archived)

### By Topic

**Neural Systems:**
[DD001](DD001_Neural_Circuit_Architecture.md) (architecture), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (differentiation), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (neuropeptides), [DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx neurons), [DD018](DD018_Egg_Laying_System_Architecture.md) (egg-laying HSN/VC), [DD019](DD019_Closed_Loop_Touch_Response.md) (touch neurons)

**Muscle Systems:**
[DD002](DD002_Muscle_Model_Architecture.md) (body wall), [DD007](DD007_Pharyngeal_System_Architecture.md) (pharyngeal), [DD018](DD018_Egg_Laying_System_Architecture.md) (reproductive)

**Body Mechanics:**
[DD003](DD003_Body_Physics_Architecture.md) (SPH), [DD004](DD004_Mechanical_Cell_Identity.md) (cell identity), [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (mesh deformation), [DD019](DD019_Closed_Loop_Touch_Response.md) (strain readout)

**Organ Systems:**
[DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx), [DD009](DD009_Intestinal_Oscillator_Model.md) (intestine), [DD018](DD018_Egg_Laying_System_Architecture.md) (egg-laying)

**Sensory Systems:**
[DD019](DD019_Closed_Loop_Touch_Response.md) (touch/MEC-4), [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) (environment), [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (proprioception)

**Data & Validation:**
[DD008](DD008_Data_Integration_Pipeline.md) (OWMeta), [DD010](DD010_Validation_Framework.md) (3-tier validation), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (connectome/cect), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (movement toolbox)

**Infrastructure:**
[DD013](DD013_Simulation_Stack_Architecture.md) (simulation stack), [DD014](DD014_Dynamic_Visualization_Architecture.md) (visualization), [DD014.1](DD014.1_Visual_Rendering_Specification.md) (visual rendering), [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (mesh deformation)

**Governance:**
[DD011](DD011_Contributor_Progression_Model.md) (contributor progression), [DD012](DD012_Design_Document_RFC_Process.md) (RFC process), [DD015](DD015_AI_Contributor_Model.md) (AI contributors)

**Hybrid/Advanced:**
[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (mechanistic-ML hybrid)

---

## How to Use Design Documents

### For Contributors

1. **Find a DD** matching your interest (neural modeling → [DD001](DD001_Neural_Circuit_Architecture.md), visualization → [DD014](DD014_Dynamic_Visualization_Architecture.md), etc.)
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

Follow [DD012 (RFC Process)](DD012_Design_Document_RFC_Process.md) template.
Use [DD005 (Cell Differentiation)](DD005_Cell_Type_Differentiation_Strategy.md) as your reference implementation.

---

## Status Badges

- ✅ **Accepted** — Binding specification, implementations must comply
- ⚠️ **Proposed** — Under review or approved but not yet implemented
- 🔴 **Blocked** — Cannot proceed (missing prerequisite)
- 📦 **Archived** — Deferred or superseded

---

## External Links

- **[GitHub Repository](https://github.com/openworm/openworm-admin/tree/main/design_documents)** — All DD markdown files
- **[Phase Roadmap](DD_PHASE_ROADMAP.md)** — Timeline and milestones
- **[Integration Map](INTEGRATION_MAP.md)** — Dependency graph
- **[Code Reuse Guide](DD_CODE_REUSE_OPPORTUNITIES.md)** — Accelerate implementation
