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

For the philosophical commitments behind these principles — mechanistic explanation, causal interpretability (Pearl), emergence, and completeness — see [Background: Mission & Design Principles](../background.md#mission-design-principles). For how OpenWorm compares to similar projects, see [Full History](../fullhistory.md#projects-similar-to-openworm).

## Quick Links

**New to Design Documents?**

- 📋 [DD012: RFC Process](DD012_Design_Document_RFC_Process.md) — How DDs work, template structure
- 🌟 [DD005: Cell-Type Specialization](DD005_Cell_Type_Differentiation_Strategy.md) — Reference implementation with all sections filled
- 🗺️ [Integration Map](INTEGRATION_MAP.md) — PlantUML diagram showing how all DDs couple together
- 📅 [Phase Roadmap](DD_PHASE_ROADMAP.md) — 18-month implementation timeline with milestones

**Implementing or Contributing?**

- 🛠️ [Contributing Guide](contributing_guide.md) — How to use, write, and review DDs (lifecycle, templates, examples, anti-patterns, FAQ)
- 📈 [DD011: Contributor Progression](DD011_Contributor_Progression_Model.md) — L0→L5 path, badge system
- 🤖 [DD015: AI-Native Model](DD015_AI_Contributor_Model.md) — Autonomous agent registration

**Resources:**

- 📦 [GitHub Repo Inventory](../Resources/github-repo-inventory.md) — All 109 OpenWorm repositories (existing code resources are documented in each DD's "Existing Code Resources" section)

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

- **Milestone:** "Containerized Stack with Automated Validation"
- **Duration:** 4 weeks
- **Status:** Proposed — must complete before modeling phases

| DD | Title | What It Delivers |
|----|-------|------------------|
| [DD013](DD013_Simulation_Stack_Architecture.md) | Simulation Stack | Docker, CI/CD, openworm.yml config |
| [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | Movement Toolbox Revival | Tier 3 validation (8 tasks, 33 hours) |
| [DD012](DD012_Design_Document_RFC_Process.md) | RFC Process | DD template, governance |
| [DD011](DD011_Contributor_Progression_Model.md) | Contributor Progression | Observer to Senior Contributor (L0-L5) |
| [DD025](DD025_Protein_Foundation_Model_Pipeline.md) | Foundation Model Channel Kinetics | Predicted ion channel kinetics from sequence (parallel, derisks [DD005](DD005_Cell_Type_Differentiation_Strategy.md)) |
| [DD028](DD028_Project_Metrics_Dashboard.md) | Project Metrics Dashboard | Validation scores, contributor activity, CI health, phase progress |

### Phase 1: Cell-Type Specialization ⚠️

- **Milestone:** "Biologically Distinct Neurons"
- **Duration:** 3 months
- **Key:** 128 neuron classes from CeNGEN, functional connectivity improves ≥20%

| DD | Title | What Changes |
|----|-------|--------------|
| [DD005](DD005_Cell_Type_Differentiation_Strategy.md) | Cell-Type Specialization | 128 distinct neuron classes (not 302 identical) |
| [DD014 Phase 1](DD014_Dynamic_Visualization_Architecture.md) | Trame Viewer | OME-Zarr export, organism + tissue scales |
| [DD010 Tier 2](DD010_Validation_Framework.md) | Functional Connectivity | Validate vs. [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) (r > 0.5) |

### Phase 2: Slow Modulation + Closed-Loop ⚠️

- **Milestone:** "The Worm Can Feel and Modulate"
- **Duration:** 3 months
- **Key:** 31,479 neuropeptide connections + bidirectional touch response

| DD | Title | What Adds |
|----|-------|-----------|
| [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Neuropeptides | GPCR modulation, seconds timescale |
| [DD019](DD019_Closed_Loop_Touch_Response.md) | Touch Response | MEC-4 channel, tap withdrawal |
| [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) | Environment | Gradients, substrates, stimuli |
| [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) | Proprioception | Stretch receptors, motor coordination |
| [DD026](DD026_Reservoir_Computing_Validation.md) | Reservoir Computing Validation | Tests RC framing: 5 properties × 4 partitions, falsifiable predictions |
| [DD027](DD027_Multicompartmental_Neuron_Models.md) | Multicompartmental Neurons (PoC) | 5 representative neurons, 14 ion channel classes, EM morphologies |

### Phase 3: Organ Systems ⚠️

- **Milestone:** "Multi-Organ Digital Organism"
- **Duration:** 6 months
- **Key:** Pharynx, intestine, egg-laying, ML acceleration

| DD | Title | What Adds |
|----|-------|-----------|
| [DD007](DD007_Pharyngeal_System_Architecture.md) | Pharyngeal System | 63 cells, 3-4 Hz pumping |
| [DD009](DD009_Intestinal_Oscillator_Model.md) | Intestinal Oscillator | 20 cells, 50s defecation |
| [DD018](DD018_Egg_Laying_System_Architecture.md) | Egg-Laying System | 28-cell circuit, two-state |
| [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) | Hybrid ML | Differentiable sim, 1000× speedup (Component 3 extracted to [DD025](DD025_Protein_Foundation_Model_Pipeline.md)) |

### Phase 4: Complete Organism ⚠️

- **Milestone:** "959-Cell Photorealistic Whole Organism"
- **Duration:** 6 months
- **Key:** All somatic cells, mesh deformation, public web viewer

| DD | Title | What Adds |
|----|-------|-----------|
| [DD004](DD004_Mechanical_Cell_Identity.md) | Mechanical Cell Identity | 959 cells with cell-type mechanics |
| [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) | Mesh Deformation | GPU skinning, photorealistic |
| [DD014 Phase 3](DD014_Dynamic_Visualization_Architecture.md) | WormSim 2.0 | Molecular scale, wormsim.openworm.org |

---

## All Design Documents (Complete List)

!!! tip "Browse on GitHub"
    All Design Documents are maintained in this [openworm_docs repository](https://github.com/openworm/openworm_docs/tree/main/docs/design_documents).
    **Total:** 29 DDs ([DD001](DD001_Neural_Circuit_Architecture.md)-[DD028](DD028_Project_Metrics_Dashboard.md) + [DD014.1](DD014.1_Visual_Rendering_Specification.md)/[DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md); DD016 was merged into [DD005](DD005_Cell_Type_Differentiation_Strategy.md))

### By Topic

**Neural Systems:**
[DD001](DD001_Neural_Circuit_Architecture.md) (architecture), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (specialization), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (neuropeptides), [DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx neurons), [DD018](DD018_Egg_Laying_System_Architecture.md) (egg-laying HSN/VC), [DD019](DD019_Closed_Loop_Touch_Response.md) (touch neurons), [DD027](DD027_Multicompartmental_Neuron_Models.md) (multicompartmental)

**Muscle Systems:**
[DD002](DD002_Muscle_Model_Architecture.md) (body wall), [DD007](DD007_Pharyngeal_System_Architecture.md) (pharyngeal), [DD018](DD018_Egg_Laying_System_Architecture.md) (reproductive)

**Body Mechanics:**
[DD003](DD003_Body_Physics_Architecture.md) (SPH), [DD004](DD004_Mechanical_Cell_Identity.md) (cell identity), [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (mesh deformation), [DD019](DD019_Closed_Loop_Touch_Response.md) (strain readout)

**Organ Systems:**
[DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx), [DD009](DD009_Intestinal_Oscillator_Model.md) (intestine), [DD018](DD018_Egg_Laying_System_Architecture.md) (egg-laying)

**Sensory Systems:**
[DD019](DD019_Closed_Loop_Touch_Response.md) (touch/MEC-4), [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) (environment), [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (proprioception)

**Data & Validation:**
[DD008](DD008_Data_Integration_Pipeline.md) (OWMeta), [DD010](DD010_Validation_Framework.md) (4-tier validation), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (connectome/cect), [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (movement toolbox), [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (validation data acquisition), [DD026](DD026_Reservoir_Computing_Validation.md) (reservoir computing validation)

**Infrastructure:**
[DD013](DD013_Simulation_Stack_Architecture.md) (simulation stack), [DD014](DD014_Dynamic_Visualization_Architecture.md) (visualization), [DD014.1](DD014.1_Visual_Rendering_Specification.md) (visual rendering), [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (mesh deformation), [DD028](DD028_Project_Metrics_Dashboard.md) (project metrics dashboard)

**Governance:**
[DD011](DD011_Contributor_Progression_Model.md) (contributor progression), [DD012](DD012_Design_Document_RFC_Process.md) (RFC process), [DD015](DD015_AI_Contributor_Model.md) (AI contributors)

**Hybrid/Advanced:**
[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (mechanistic-ML hybrid), [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (foundation model channel kinetics), [DD026](DD026_Reservoir_Computing_Validation.md) (reservoir computing validation)

---

## Cross-Reference by Topic

### Neural Systems

- **Core:** [DD001](DD001_Neural_Circuit_Architecture.md) (302-neuron HH architecture, graded synapses, Level C1)
- **Specialization:** [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (128 neuron classes from CeNGEN scRNA-seq)
- **Modulation:** [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (31,479 neuropeptide-receptor interactions, GPCR modulation, seconds timescale)
- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (20 pharyngeal neurons, pumping circuit)
- **Egg-Laying:** [DD018](DD018_Egg_Laying_System_Architecture.md) (2 HSN serotonergic command neurons, 6 VC cholinergic motor neurons)
- **Touch:** [DD019](DD019_Closed_Loop_Touch_Response.md) (6 touch receptor neurons: ALM, AVM, PLM; tap withdrawal circuit, MEC-4 channel)
- **Multicompartmental:** [DD027](DD027_Multicompartmental_Neuron_Models.md) (NeuroML2 multicompartmental cable-equation models; spatially resolved synapses)

### Muscle Systems

- **Body Wall:** [DD002](DD002_Muscle_Model_Architecture.md) (95 muscles, Ca²⁺→force coupling, [Boyle & Cohen 2008](https://doi.org/10.1016/j.biosystems.2008.05.025) parameters)
- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (20 pharyngeal muscles, nonstriated, plateau potentials, gap-junction-synchronized)
- **Reproductive:** [DD018](DD018_Egg_Laying_System_Architecture.md) (16 sex muscles: 8 vulval, 8 uterine; EGL-19/UNC-103 channels)

### Body Mechanics

- **Physics Engine:** [DD003](DD003_Body_Physics_Architecture.md) (Sibernetic SPH, ~100K particles, PCISPH incompressibility, elastic bonds, muscle force injection)
- **Cell Identity:** [DD004](DD004_Mechanical_Cell_Identity.md) (per-particle cell IDs from WBbt ontology, 959 somatic cells, cell-type-specific elasticity/adhesion)
- **Mesh Deformation:** [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md) (GPU skinning, cage-based MVC, PBD collision for Virtual Worm's 688 meshes)
- **Strain Readout:** [DD019](DD019_Closed_Loop_Touch_Response.md) (cuticle strain from SPH particles for mechanotransduction)

### Organ Systems

- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (63 cells: 20 neurons + 20 muscles + 9 epithelial + 9 marginal + 4 gland + 1 valve; 3-4 Hz pumping)
- **Intestine:** [DD009](DD009_Intestinal_Oscillator_Model.md) (20 cells, IP3/Ca²⁺ oscillator, defecation motor program 50±10s period)
- **Reproductive:** [DD018](DD018_Egg_Laying_System_Architecture.md) (28-cell circuit: 2 HSN + 6 VC + 16 sex muscles + 4 uv1 feedback; two-state pattern)

### Sensory & Environment

- **Touch:** [DD019](DD019_Closed_Loop_Touch_Response.md) (MEC-4/MEC-10 DEG/ENaC mechanosensory channel, gentle + harsh touch)
- **Environment:** [DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) (substrates, chemical gradients, temperature, food particles)
- **Proprioception:** [DD023](DD023_Proprioceptive_Feedback_and_Motor_Coordination.md) (stretch receptors, motor coordination)

### Data & Validation

- **Connectome:** [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (`cect` API v0.2.7, [Cook2019](https://doi.org/10.1038/s41586-019-1352-7) default, 30+ datasets)
- **Data Integration:** [DD008](DD008_Data_Integration_Pipeline.md) (OWMeta semantic RDF graph; Phase 3+ wraps `cect`)
- **Movement Validation:** [DD021](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) (analysis toolbox revival, WCON 1.0, 5 kinematic metrics)
- **Validation Framework:** [DD010](DD010_Validation_Framework.md) (4 tiers: electrophysiology, functional connectivity r > 0.5, behavioral ±15%, causal/interventional)
- **Validation Data:** [DD024](DD024_Validation_Data_Acquisition_Pipeline.md) (acquire, format, version-control all experimental datasets)
- **Reservoir Computing:** [DD026](DD026_Reservoir_Computing_Validation.md) (tests whether the 302-neuron connectome functions as a reservoir computer — 5 RC properties × 4 neuron partitions, falsifiable predictions)

### Infrastructure & Visualization

- **Simulation Stack:** [DD013](DD013_Simulation_Stack_Architecture.md) (Docker, openworm.yml, CI/CD, Integration Maintainer role)
- **Visualization:** [DD014](DD014_Dynamic_Visualization_Architecture.md) (OME-Zarr, Trame→Three.js, 3-phase roadmap)
    - [DD014.1](DD014.1_Visual_Rendering_Specification.md): Visual Rendering Specification (colors, materials, lighting, 14 mockups)
    - [DD014.2](DD014.2_Anatomical_Mesh_Deformation_Pipeline.md): Anatomical Mesh Deformation Pipeline (GPU skinning, ~1.6M vertices)

### Governance

- **Contributors:** [DD011](DD011_Contributor_Progression_Model.md) (L0-L5 progression, badge system)
- **RFC Process:** [DD012](DD012_Design_Document_RFC_Process.md) (DD template, approval workflow, Mind-of-a-Worm enforcement)
- **AI Contributors:** [DD015](DD015_AI_Contributor_Model.md) (autonomous agents as L1-L3 contributors)

### Hybrid & Advanced

- **Mechanistic-ML:** [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (differentiable simulation, SPH surrogate, learned sensory transduction)
- **Foundation Model Kinetics:** [DD025](DD025_Protein_Foundation_Model_Pipeline.md) (protein sequence → ion channel HH parameters, derisks [DD005](DD005_Cell_Type_Differentiation_Strategy.md))
- **Reservoir Computing:** [DD026](DD026_Reservoir_Computing_Validation.md) (tests RC framing of the connectome — 5 falsifiable predictions across 4 neuron partitions, either confirms or rejects the framework)

---

## Contributing

See the **[Contributing Guide](contributing_guide.md)** for:

- How to use DDs as a contributor or reviewer
- Design Document lifecycle and status definitions
- Writing your first DD (7-step guide with template)
- Examples of excellent DDs
- Anti-patterns to avoid
- Frequently asked questions

---

## Additional Resources

- **[Phase Roadmap](DD_PHASE_ROADMAP.md)** — Complete timeline, milestones, dataset inventory
- **[Integration Map](INTEGRATION_MAP.md)** — Dependency graph, bottleneck analysis, coupling chains
- **[GitHub Repo Inventory](../Resources/github-repo-inventory.md)** — All 109 OpenWorm repos
