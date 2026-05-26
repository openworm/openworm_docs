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

- 📋 [Decision Process](../contributing/decision-process.md) — How design decisions get made, DD template, RFC workflow (in the Contributing section)
- 🌟 [DD005: Cell-Type Specialization](DD005_Cell_Type_Differentiation_Strategy.md) — Reference implementation with all sections filled
- 🗺️ [Integration Map](INTEGRATION_MAP.md) — PlantUML diagram showing how all DDs couple together
- 📅 [Phase Roadmap](DD_PHASE_ROADMAP.md) — 18-month implementation timeline with milestones

**Implementing or Contributing?**

- 🛠️ [Contributing Guide](contributing_guide.md) — How to use, write, and review DDs (lifecycle, templates, examples, anti-patterns, FAQ)
- 📈 [Contributor Progression](../contributing/contributor-progression.md) — L0→L5 path, badge system (in the Contributing section)
- 🤖 [AI Contributors](../contributing/ai-contributors.md) — Autonomous agent registration (in the Contributing section)

**Resources:**

- 📦 [GitHub Repo Inventory](../Resources/github-repo-inventory.md) — All 109 OpenWorm repositories (existing code resources are documented in each DD's "Existing Code Resources" section)

---

## Phase Overview

OpenWorm's roadmap takes the project from today's 302 generic neurons to a complete 959-cell digital organism over ~18 months. The journey is organized into phases that manage scientific risk, build infrastructure first, and validate early. Phase 0 established the core architecture — coupled neural-muscle-body simulation runs and produces movement, though stabilization work remains (see Phase A1). Phases A1 and A2 lay the infrastructure and governance foundation. Phases 1-4 progressively add biological complexity — from cell-type specialization through organ systems to the complete organism.

The key insight behind this phasing: **validate the hardest science early**. Phase 1's expression→conductance mapping is the highest-risk step. If it fails, we discover it in month 3 (not month 12). Each subsequent phase builds on validated foundations, not assumptions.

| Phase | Name | Duration | What It Delivers | Key DDs | Cells |
|-------|------|----------|-----------------|---------|-------|
| 0 | Core Architecture | Functional | Neural circuit + muscle + body + connectome data — simulation runs, 83 stabilization issues tracked | 4 | 302 neurons + 95 muscles |
| A1 | Core Infrastructure | Wks 1-2 | `docker compose run quick-test`, unified data API, validation toolbox, baseline datasets, project dashboard | 5 | — |
| A2 | Governance & Derisking | Wks 3-4 | L0-L5 contributor levels + badge taxonomy ([Contributor Progression](../contributing/contributor-progression.md)), DD proposal/review process ([Decision Process](../contributing/decision-process.md)), AI agent registration + task pipeline ([AI Contributors](../contributing/ai-contributors.md)), ion channel kinetics predictions derisking Phase 1 ([DD021](DD021_Protein_Foundation_Model_Pipeline.md)) | 4 | — |
| 1 | Cell-Type Specialization | Mo 1-3 | 128 neuron classes from generic → specialized | 4 | 302 specialized neurons |
| 2 | Modulation + Closed-Loop | Mo 4-6 | Neuropeptides, touch response, proprioception | 6 | +sensory loop |
| 3 | Organ Systems | Mo 7-12 | Pharynx, intestine, egg-laying, ML hybrid | 4 | +3 organs |
| 4 | Complete Organism | Mo 13-18 | 959 mechanically distinct cells, web viewer | 3 | 959 cells |

### Why This Order?

- **Phase 0:** The foundation is functional — coupled simulation runs and produces movement with 302 neurons, 95 muscles, and SPH body physics. 83 stabilization issues remain (containerization, validation scripts, dependency pinning), most addressed by Phase A1.
- **Phase A1:** Can't build/test/validate without containerization ([DD011](DD011_Simulation_Stack_Architecture.md)), data access ([DD008](DD008_Data_Integration_Pipeline.md)), and validation toolbox ([DD017](DD017_Movement_Analysis_Toolbox_and_WCON_Policy.md)). These block everything.
- **Phase A2:** Doesn't block modeling but enables governance at scale and derisks Phase 1 calibration via foundation model cross-validation ([DD021](DD021_Protein_Foundation_Model_Pipeline.md)). Runs in parallel with A1.
- **Phase 1:** Highest scientific risk (expression→conductance mapping) — test early, fail fast. If it works, we have 128 distinct neuron classes. If it fails, DD021 predictions are the fallback.
- **Phase 2:** Closes the sensory loop — the worm can now respond to stimuli (touch, chemicals, temperature) and modulate behavior via neuropeptides.
- **Phase 3:** Adds organ systems (pharynx, intestine, egg-laying) that need the closed-loop substrate from Phase 2.
- **Phase 4:** Completes the organism — 959 mechanically distinct cells + public web viewer at wormsim.openworm.org.

For detailed milestones, success criteria, datasets, and blocking dependencies, see the **[Phase Roadmap](DD_PHASE_ROADMAP.md)**.

---

## All Design Documents (Complete List)

!!! tip "Browse on GitHub"
    All Design Documents are maintained in this [openworm_docs repository](https://github.com/openworm/openworm_docs/tree/main/docs/design_documents).
    **Total:** 29 DDs ([DD002](DD002_Neural_Circuit_Architecture.md)-[DD024](DD024_Project_Metrics_Dashboard.md) + [DD012.1](DD012.1_Visual_Rendering_Specification.md)/[DD012.2](DD012.2_Anatomical_Mesh_Deformation_Pipeline.md); DD016 was merged into [DD005](DD005_Cell_Type_Differentiation_Strategy.md))

### By Topic

**Neural Systems:**
[DD002](DD002_Neural_Circuit_Architecture.md) (architecture), [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (specialization), [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (neuropeptides), [DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx neurons), [DD014](DD014_Egg_Laying_System_Architecture.md) (egg-laying HSN/VC), [DD015](DD015_Closed_Loop_Touch_Response.md) (touch neurons), [DD023](DD023_Multicompartmental_Neuron_Models.md) (multicompartmental)

**Muscle Systems:**
[DD003](DD003_Muscle_Model_Architecture.md) (body wall), [DD007](DD007_Pharyngeal_System_Architecture.md) (pharyngeal), [DD014](DD014_Egg_Laying_System_Architecture.md) (reproductive)

**Body Mechanics:**
[DD001](DD001_Body_Physics_Architecture.md) (SPH), [DD004](DD004_Mechanical_Cell_Identity.md) (cell identity), [DD012.2](DD012.2_Anatomical_Mesh_Deformation_Pipeline.md) (mesh deformation), [DD015](DD015_Closed_Loop_Touch_Response.md) (strain readout)

**Organ Systems:**
[DD007](DD007_Pharyngeal_System_Architecture.md) (pharynx), [DD009](DD009_Intestinal_Oscillator_Model.md) (intestine), [DD014](DD014_Egg_Laying_System_Architecture.md) (egg-laying)

**Sensory Systems:**
[DD015](DD015_Closed_Loop_Touch_Response.md) (touch/MEC-4), [DD018](DD018_Environmental_Modeling_and_Stimulus_Delivery.md) (environment), [DD019](DD019_Proprioceptive_Feedback_and_Motor_Coordination.md) (proprioception)

**Data & Validation:**
[DD008](DD008_Data_Integration_Pipeline.md) (OWMeta), [DD010](DD010_Validation_Framework.md) (4-tier validation), [DD016](DD016_Connectome_Data_Access_and_Dataset_Policy.md) (connectome/cect), [DD017](DD017_Movement_Analysis_Toolbox_and_WCON_Policy.md) (movement toolbox), [DD020](DD020_Validation_Data_Acquisition_Pipeline.md) (validation data acquisition), [DD022](DD022_Reservoir_Computing_Validation.md) (reservoir computing validation)

**Infrastructure:**
[DD011](DD011_Simulation_Stack_Architecture.md) (simulation stack), [DD012](DD012_Dynamic_Visualization_Architecture.md) (visualization), [DD012.1](DD012.1_Visual_Rendering_Specification.md) (visual rendering), [DD012.2](DD012.2_Anatomical_Mesh_Deformation_Pipeline.md) (mesh deformation), [DD024](DD024_Project_Metrics_Dashboard.md) (project metrics dashboard)

**Governance:**
[Contributor Progression](../contributing/contributor-progression.md) (contributor progression), [Decision Process](../contributing/decision-process.md) (RFC process), [AI Contributors](../contributing/ai-contributors.md) (AI contributors)

**Hybrid/Advanced:**
[DD013](DD013_Hybrid_Mechanistic_ML_Framework.md) (mechanistic-ML hybrid), [DD021](DD021_Protein_Foundation_Model_Pipeline.md) (foundation model channel kinetics), [DD022](DD022_Reservoir_Computing_Validation.md) (reservoir computing validation)

---

## Cross-Reference by Topic

### Neural Systems

- **Core:** [DD002](DD002_Neural_Circuit_Architecture.md) (302-neuron HH architecture, graded synapses, Level C1)
- **Specialization:** [DD005](DD005_Cell_Type_Differentiation_Strategy.md) (128 neuron classes from CeNGEN scRNA-seq)
- **Modulation:** [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) (31,479 neuropeptide-receptor interactions, GPCR modulation, seconds timescale)
- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (20 pharyngeal neurons, pumping circuit)
- **Egg-Laying:** [DD014](DD014_Egg_Laying_System_Architecture.md) (2 HSN serotonergic command neurons, 6 VC cholinergic motor neurons)
- **Touch:** [DD015](DD015_Closed_Loop_Touch_Response.md) (6 touch receptor neurons: ALM, AVM, PLM; tap withdrawal circuit, MEC-4 channel)
- **Multicompartmental:** [DD023](DD023_Multicompartmental_Neuron_Models.md) (NeuroML2 multicompartmental cable-equation models; spatially resolved synapses)

### Muscle Systems

- **Body Wall:** [DD003](DD003_Muscle_Model_Architecture.md) (95 muscles, Ca²⁺→force coupling, [Boyle & Cohen 2008](https://doi.org/10.1016/j.biosystems.2008.05.025) parameters)
- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (20 pharyngeal muscles, nonstriated, plateau potentials, gap-junction-synchronized)
- **Reproductive:** [DD014](DD014_Egg_Laying_System_Architecture.md) (16 sex muscles: 8 vulval, 8 uterine; EGL-19/UNC-103 channels)

### Body Mechanics

- **Physics Engine:** [DD001](DD001_Body_Physics_Architecture.md) (Sibernetic SPH, ~100K particles, PCISPH incompressibility, elastic bonds, muscle force injection)
- **Cell Identity:** [DD004](DD004_Mechanical_Cell_Identity.md) (per-particle cell IDs from WBbt ontology, 959 somatic cells, cell-type-specific elasticity/adhesion)
- **Mesh Deformation:** [DD012.2](DD012.2_Anatomical_Mesh_Deformation_Pipeline.md) (GPU skinning, cage-based MVC, PBD collision for Virtual Worm's 688 meshes)
- **Strain Readout:** [DD015](DD015_Closed_Loop_Touch_Response.md) (cuticle strain from SPH particles for mechanotransduction)

### Organ Systems

- **Pharynx:** [DD007](DD007_Pharyngeal_System_Architecture.md) (63 cells: 20 neurons + 20 muscles + 9 epithelial + 9 marginal + 4 gland + 1 valve; 3-4 Hz pumping)
- **Intestine:** [DD009](DD009_Intestinal_Oscillator_Model.md) (20 cells, IP3/Ca²⁺ oscillator, defecation motor program 50±10s period)
- **Reproductive:** [DD014](DD014_Egg_Laying_System_Architecture.md) (28-cell circuit: 2 HSN + 6 VC + 16 sex muscles + 4 uv1 feedback; two-state pattern)

### Sensory & Environment

- **Touch:** [DD015](DD015_Closed_Loop_Touch_Response.md) (MEC-4/MEC-10 DEG/ENaC mechanosensory channel, gentle + harsh touch)
- **Environment:** [DD018](DD018_Environmental_Modeling_and_Stimulus_Delivery.md) (substrates, chemical gradients, temperature, food particles)
- **Proprioception:** [DD019](DD019_Proprioceptive_Feedback_and_Motor_Coordination.md) (stretch receptors, motor coordination)

### Data & Validation

- **Connectome:** [DD016](DD016_Connectome_Data_Access_and_Dataset_Policy.md) (`cect` API v0.2.7, [Cook2019](https://doi.org/10.1038/s41586-019-1352-7) default, 30+ datasets)
- **Data Integration:** [DD008](DD008_Data_Integration_Pipeline.md) (OWMeta semantic RDF graph; Phase 3+ wraps `cect`)
- **Movement Validation:** [DD017](DD017_Movement_Analysis_Toolbox_and_WCON_Policy.md) (analysis toolbox revival, WCON 1.0, 5 kinematic metrics)
- **Validation Framework:** [DD010](DD010_Validation_Framework.md) (4 tiers: electrophysiology, functional connectivity r > 0.5, behavioral ±15%, causal/interventional)
- **Validation Data:** [DD020](DD020_Validation_Data_Acquisition_Pipeline.md) (acquire, format, version-control all experimental datasets)
- **Reservoir Computing:** [DD022](DD022_Reservoir_Computing_Validation.md) (tests whether the 302-neuron connectome functions as a reservoir computer — 5 RC properties × 4 neuron partitions, falsifiable predictions)

### Infrastructure & Visualization

- **Simulation Stack:** [DD011](DD011_Simulation_Stack_Architecture.md) (Docker, openworm.yml, CI/CD, Integration Maintainer role)
- **Visualization:** [DD012](DD012_Dynamic_Visualization_Architecture.md) (OME-Zarr, Trame→Three.js, 3-phase roadmap)
    - [DD012.1](DD012.1_Visual_Rendering_Specification.md): Visual Rendering Specification (colors, materials, lighting, 14 mockups)
    - [DD012.2](DD012.2_Anatomical_Mesh_Deformation_Pipeline.md): Anatomical Mesh Deformation Pipeline (GPU skinning, ~1.6M vertices)

### Governance

- **Contributors:** [Contributor Progression](../contributing/contributor-progression.md) (L0-L5 progression, badge system)
- **RFC Process:** [Decision Process](../contributing/decision-process.md) (DD template, approval workflow, Mind-of-a-Worm enforcement)
- **AI Contributors:** [AI Contributors](../contributing/ai-contributors.md) (autonomous agents as L1-L3 contributors)

### Hybrid & Advanced

- **Mechanistic-ML:** [DD013](DD013_Hybrid_Mechanistic_ML_Framework.md) (differentiable simulation, SPH surrogate, learned sensory transduction)
- **Foundation Model Kinetics:** [DD021](DD021_Protein_Foundation_Model_Pipeline.md) (protein sequence → ion channel HH parameters, derisks [DD005](DD005_Cell_Type_Differentiation_Strategy.md))
- **Reservoir Computing:** [DD022](DD022_Reservoir_Computing_Validation.md) (tests RC framing of the connectome — 5 falsifiable predictions across 4 neuron partitions, either confirms or rejects the framework)

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
