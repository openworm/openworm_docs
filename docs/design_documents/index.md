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
- 🌟 [DD001: Body Physics Engine](DD001_Body_Physics_Architecture.md) — Reference DD for this docs cycle; shows the spec/implementation cleavage and the 8-phase Validation Methodology pattern
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

OpenWorm's roadmap takes the project from today's 302 generic neurons to a complete 959-cell digital organism. The journey is organized into phases that manage scientific risk, build infrastructure first, and validate early. Phase 0 established the core architecture — coupled neural-muscle-body simulation runs and produces movement, though stabilization work remains (see Phase 1). Phases 1 and 2 lay the infrastructure and governance foundation. Phases 3-6 progressively add biological complexity — from cell-type specialization through organ systems to the complete organism.

The key insight behind this phasing: **validate the hardest science early**. Phase 3's expression→conductance mapping is the highest-risk step. If it fails, we discover it before the rest of the science is built on top of it. Each subsequent phase builds on validated foundations, not assumptions.

| Phase | Name | Status | What It Delivers | Key DDs | Cells |
|-------|------|--------|-----------------|---------|-------|
| 0 | Core Architecture | Functional | Neural circuit + muscle + body + connectome data — simulation runs, 83 stabilization issues tracked | 4 | 302 neurons + 95 muscles |
| 1 | Core Infrastructure | Proposed | `docker compose run quick-test`, unified data API, validation toolbox, baseline datasets, project dashboard | 5 | — |
| 2 | Governance & Derisking | Proposed (parallel with Phase 1) | L0-L5 contributor levels + badge taxonomy ([Contributor Progression](../contributing/contributor-progression.md)), DD proposal/review process ([Decision Process](../contributing/decision-process.md)), AI agent registration + task pipeline ([AI Contributors](../contributing/ai-contributors.md)), ion channel kinetics predictions derisking Phase 3 (DD021) | 4 | — |
| 3 | Cell-Type Specialization | Proposed | 128 neuron classes from generic → specialized | 4 | 302 specialized neurons |
| 4 | Modulation + Closed-Loop | Proposed | Neuropeptides, touch response, proprioception | 6 | +sensory loop |
| 5 | Organ Systems | Proposed | Pharynx, intestine, egg-laying, ML hybrid | 4 | +3 organs |
| 6 | Complete Organism | Proposed | 959 mechanically distinct cells, web viewer | 3 | 959 cells |

### Why This Order?

- **Phase 0:** The foundation is functional — coupled simulation runs and produces movement with 302 neurons, 95 muscles, and SPH body physics. 83 stabilization issues remain (containerization, validation scripts, dependency pinning), most addressed by Phase 1.
- **Phase 1:** Can't build/test/validate without containerization (DD011), data access (DD008), and validation toolbox (DD017). These block everything.
- **Phase 2:** Doesn't block modeling but enables governance at scale and derisks Phase 3 calibration via foundation model cross-validation (DD021). Runs in parallel with Phase 1.
- **Phase 3:** Highest scientific risk (expression→conductance mapping) — test early, fail fast. If it works, we have 128 distinct neuron classes. If it fails, DD021 predictions are the fallback.
- **Phase 4:** Closes the sensory loop — the worm can now respond to stimuli (touch, chemicals, temperature) and modulate behavior via neuropeptides.
- **Phase 5:** Adds organ systems (pharynx, intestine, egg-laying) that need the closed-loop substrate from Phase 4.
- **Phase 6:** Completes the organism — 959 mechanically distinct cells + public web viewer at wormsim.openworm.org.

For detailed milestones, success criteria, datasets, and blocking dependencies, see the **[Phase Roadmap](DD_PHASE_ROADMAP.md)**.

---

## All Design Documents (Complete List)

!!! tip "Browse on GitHub"
    All Design Documents are maintained in this [openworm_docs repository](https://github.com/openworm/openworm_docs/tree/main/docs/design_documents).
    **Total:** 26 DDs (DD001-DD024 + DD012.1/DD012.2)

### By Topic

**Neural Systems:**
DD002 (architecture), DD005 (specialization), DD006 (neuropeptides), DD007 (pharynx neurons), DD014 (egg-laying HSN/VC), DD015 (touch neurons), DD023 (multicompartmental)

**Muscle Systems:**
DD003 (body wall), DD007 (pharyngeal), DD014 (reproductive)

**Body Mechanics:**
[DD001](DD001_Body_Physics_Architecture.md) (SPH), DD004 (cell identity), DD012.2 (mesh deformation), DD015 (strain readout)

**Organ Systems:**
DD007 (pharynx), DD009 (intestine), DD014 (egg-laying)

**Sensory Systems:**
DD015 (touch/MEC-4), DD018 (environment), DD019 (proprioception)

**Data & Validation:**
DD008 (OWMeta), DD010 (4-tier validation), DD016 (connectome/cect), DD017 (movement toolbox), DD020 (validation data acquisition), DD022 (reservoir computing validation)

**Infrastructure:**
DD011 (simulation stack), DD012 (visualization), DD012.1 (visual rendering), DD012.2 (mesh deformation), DD024 (project metrics dashboard)

**Governance:**
[Contributor Progression](../contributing/contributor-progression.md) (contributor progression), [Decision Process](../contributing/decision-process.md) (RFC process), [AI Contributors](../contributing/ai-contributors.md) (AI contributors)

**Hybrid/Advanced:**
DD013 (mechanistic-ML hybrid), DD021 (foundation model channel kinetics), DD022 (reservoir computing validation)

---

## Cross-Reference by Topic

### Neural Systems

- **Core:** DD002 (302-neuron HH architecture, graded synapses, Level C1)
- **Specialization:** DD005 (128 neuron classes from CeNGEN scRNA-seq)
- **Modulation:** DD006 (31,479 neuropeptide-receptor interactions, GPCR modulation, seconds timescale)
- **Pharynx:** DD007 (20 pharyngeal neurons, pumping circuit)
- **Egg-Laying:** DD014 (2 HSN serotonergic command neurons, 6 VC cholinergic motor neurons)
- **Touch:** DD015 (6 touch receptor neurons: ALM, AVM, PLM; tap withdrawal circuit, MEC-4 channel)
- **Multicompartmental:** DD023 (NeuroML2 multicompartmental cable-equation models; spatially resolved synapses)

### Muscle Systems

- **Body Wall:** DD003 (95 muscles, Ca²⁺→force coupling, [Boyle & Cohen 2008](https://doi.org/10.1016/j.biosystems.2008.05.025) parameters)
- **Pharynx:** DD007 (20 pharyngeal muscles, nonstriated, plateau potentials, gap-junction-synchronized)
- **Reproductive:** DD014 (16 sex muscles: 8 vulval, 8 uterine; EGL-19/UNC-103 channels)

### Body Mechanics

- **Physics Engine:** [DD001](DD001_Body_Physics_Architecture.md) (Sibernetic SPH, ~100K particles, PCISPH incompressibility, elastic bonds, muscle force injection)
- **Cell Identity:** DD004 (per-particle cell IDs from WBbt ontology, 959 somatic cells, cell-type-specific elasticity/adhesion)
- **Mesh Deformation:** DD012.2 (GPU skinning, cage-based MVC, PBD collision for Virtual Worm's 688 meshes)
- **Strain Readout:** DD015 (cuticle strain from SPH particles for mechanotransduction)

### Organ Systems

- **Pharynx:** DD007 (63 cells: 20 neurons + 20 muscles + 9 epithelial + 9 marginal + 4 gland + 1 valve; 3-4 Hz pumping)
- **Intestine:** DD009 (20 cells, IP3/Ca²⁺ oscillator, defecation motor program 50±10s period)
- **Reproductive:** DD014 (28-cell circuit: 2 HSN + 6 VC + 16 sex muscles + 4 uv1 feedback; two-state pattern)

### Sensory & Environment

- **Touch:** DD015 (MEC-4/MEC-10 DEG/ENaC mechanosensory channel, gentle + harsh touch)
- **Environment:** DD018 (substrates, chemical gradients, temperature, food particles)
- **Proprioception:** DD019 (stretch receptors, motor coordination)

### Data & Validation

- **Connectome:** DD016 (`cect` API v0.4.7, [Cook2019](https://doi.org/10.1038/s41586-019-1352-7) default, 30+ datasets)
- **Data Integration:** DD008 (OWMeta semantic RDF graph; Phase 5+ wraps `cect`)
- **Movement Validation:** DD017 (analysis toolbox revival, WCON 1.0, 5 kinematic metrics)
- **Validation Framework:** DD010 (4 tiers: electrophysiology, functional connectivity r > 0.5, behavioral ±15%, causal/interventional)
- **Validation Data:** DD020 (acquire, format, version-control all experimental datasets)
- **Reservoir Computing:** DD022 (tests whether the 302-neuron connectome functions as a reservoir computer — 5 RC properties × 4 neuron partitions, falsifiable predictions)

### Infrastructure & Visualization

- **Simulation Stack:** DD011 (Docker, openworm.yml, CI/CD, Integration Maintainer role)
- **Visualization:** DD012 (OME-Zarr, Trame→Three.js, 3-phase roadmap)
    - DD012.1: Visual Rendering Specification (colors, materials, lighting, 14 mockups)
    - DD012.2: Anatomical Mesh Deformation Pipeline (GPU skinning, ~1.6M vertices)

### Governance

- **Contributors:** [Contributor Progression](../contributing/contributor-progression.md) (L0-L5 progression, badge system)
- **RFC Process:** [Decision Process](../contributing/decision-process.md) (DD template, approval workflow, Mind-of-a-Worm enforcement)
- **AI Contributors:** [AI Contributors](../contributing/ai-contributors.md) (autonomous agents as L1-L3 contributors)

### Hybrid & Advanced

- **Mechanistic-ML:** DD013 (differentiable simulation, SPH surrogate, learned sensory transduction)
- **Foundation Model Kinetics:** DD021 (protein sequence → ion channel HH parameters, derisks DD005)
- **Reservoir Computing:** DD022 (tests RC framing of the connectome — 5 falsifiable predictions across 4 neuron partitions, either confirms or rejects the framework)

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
