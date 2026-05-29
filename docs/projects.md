## OpenWorm Projects

## Projects and Design Documents

OpenWorm's projects are now **formally specified in [Design Documents](design_documents/) (DDs)**. Each repository implements one or more DDs:

| Repository | Design Documents | Status | Role |
|------------|------------------|--------|------|
| [c302](Projects/c302/) | DD002, DD003, DD005-DD009, DD014-DD015 | Active | Neural circuit, muscle models, organ systems |
| [Sibernetic](Projects/sibernetic/) | [DD001](design_documents/DD001_Body_Physics_Architecture.md), DD004 | Active | Body physics, SPH engine |
| [ConnectomeToolbox](https://github.com/openworm/ConnectomeToolbox) | DD016 | Active | Connectome data access (cect API) |
| [Worm3DViewer](https://github.com/openworm/Worm3DViewer) | DD012 | Active | Visualization (Trame evolution) |
| [open-worm-analysis-toolbox](https://github.com/openworm/open-worm-analysis-toolbox) | DD010, DD017 | Revival needed | Tier 3 behavioral validation |
| [OpenWorm (meta-repo)](Projects/docker/) | DD011 | Proposed | Integration, Docker stack |
| [DevoWorm](Projects/DevoWorm/) | [Phase 8](design_documents/DD_PHASE_ROADMAP.md#phase-8-developmental-modeling), DD004, DD005 | Active | Developmental dynamics, morphogenesis |
| [Geppetto](Projects/geppetto/) | DD012 (historical) | Dormant | Web platform (superseded by Trame) |

**See [Integration Map](design_documents/INTEGRATION_MAP.md)** for the complete dependency graph.

---

### Currently active projects

-   [Neuromechanical modeling with Sibernetic](Projects/sibernetic/) — implements **[DD001](design_documents/DD001_Body_Physics_Architecture.md)** (Body Physics) + **DD004** (Mechanical Cell Identity)
-   [c302 multiscale modelling framework](Projects/c302/) — implements **DD002** (Neural Circuit) + **DD003** (Muscle Model) + **DD005-DD009**
-   [OpenWorm Browser](Projects/browser/)
-   [DevoWorm project](Projects/DevoWorm/) — developmental modeling for **[Phase 8](design_documents/DD_PHASE_ROADMAP.md#phase-8-developmental-modeling)**, connects to **DD004** + **DD005**
-   [Docker simulation stack](Projects/docker/) — implements **DD011** (Simulation Stack)
-   [Community outreach](Projects/community-proj/)

### Projects still maintained, less active

-   [Data collection and representation](Projects/datarep/) — relates to **DD008** (Data Integration) + **DD016** (Connectome Access)
-   [Movement analysis](Projects/worm-movement/) — implements **DD010** (Validation) + **DD017** (Movement Toolbox)
-   [Geppetto Simulation Engine](Projects/geppetto/) — historical; superseded by **DD012** (Dynamic Visualization)
-   [Optimization engine](Projects/optimization/) — relates to **DD013** (Hybrid Mechanistic-ML)
-   [Muscle-Neuron integration](Projects/muscle-neuron-integration/) — formalized in **DD002** + **DD003**
-   [_C. elegans_ robots](Projects/c-elegans-robot/)

---

**NeuroMechanical Modeling - Sibernetic**

Sibernetic implements **[DD001 (Body Physics Architecture)](design_documents/DD001_Body_Physics_Architecture.md)** — the formal specification for SPH-based body mechanics including the PCISPH algorithm, ~100K particles, and fluid-structure interaction. See [DD001](design_documents/DD001_Body_Physics_Architecture.md) for the complete spec including particle types, validation criteria, and integration contract.

[Sibernetic](https://openworm.org/sibernetic/) is the home of the C++ code base that implements the core of the model. We have implemented an algorithm called Smoothed Particle Hydrodynamics (SPH) to simulate the body of the worm and its environment using GPUs.

To get a quick idea of what this looks like, check out the [latest movie](https://www.youtube.com/watch?v=SaovWiZJUWY). In this movie you can see a simulated 3D _C. elegans_ being activated in an environment. Its muscles are located around the outside of its body, and as they contract, they exert forces on the surrounding fluid, propelling the body forward via undulatory thrust.

More detailed information is available on the [Sibernetic project page](Projects/sibernetic/).

**c302 Neural Modeling Framework**

c302 implements **DD002 (Neural Circuit Architecture)** — the multi-level Hodgkin-Huxley framework for all 302 neurons. It also serves as the foundation for DD005 (cell-type specialization), DD006 (neuropeptides), DD007-DD009 (organ circuits), DD014 (egg-laying), and DD015 (touch response).

c302 generates NeuroML2 networks at multiple levels of biophysical detail (Levels A-D), with **Level C1 (HH + graded synapses)** as the recommended default for coupling with Sibernetic.

More detailed information is available on the [c302 project page](Projects/c302/).

**Visualization**

The visualization platform is evolving per **DD012 (Dynamic Visualization Architecture)**:

- **Phase 3:** Trame viewer (PyVista + live server)
- **Phase 4:** Interactive layers with validation overlays
- **Phase 5:** Three.js + WebGPU static site at wormsim.openworm.org (WormSim 2.0)

[Geppetto](Projects/geppetto/) served this role historically (2014-2020) and is preserved as [archival reference](archived_projects/).

**Movement Analysis and Validation**

The Movement Analysis project implements **DD010 (Validation Framework)** — the 3-tier validation system that ensures our simulation matches real worm behavior. The analysis toolbox is being revived per **DD017**.

More detailed information is available on the [Movement analysis project page](Projects/worm-movement/) and the [Validation page](validation/).

**Optimization and Parameter Fitting**

Now formalized in **DD013 (Hybrid Mechanistic-ML Framework)** — differentiable simulation with gradient descent, neural surrogates for 1000x speedup, and foundation model predictions for channel kinetics.

More detailed information is available on the [Optimization project page](Projects/optimization/).

**Data Collection and Representation**

Formalized in **DD008 (Data Integration Pipeline)** and **DD016 (Connectome Data Access)** — the ConnectomeToolbox (cect) is the canonical API for connectome data.

More detailed information is available on the [Data representation project page](Projects/datarep/).

**DevoWorm — Developmental Modeling**

The [DevoWorm project](Projects/DevoWorm/) ([devoworm.weebly.com](https://devoworm.weebly.com/), [github.com/devoworm](https://github.com/devoworm)) focuses on developmental dynamics, digital morphogenesis, and developmental plasticity in *C. elegans*. DevoWorm's embryogenetic connectome analysis, differentiation trees, and CompuCell3D morphogenesis models form the foundation for **[Phase 8 (Developmental Modeling)](design_documents/DD_PHASE_ROADMAP.md#phase-8-developmental-modeling)** of the simulation roadmap — the "Worm That Grows" milestone. DevoWorm's work also connects to **DD004** (cell identity during body growth) and **DD005** (temporal dynamics of cell-type specification).

More detailed information is available on the [DevoWorm project page](Projects/DevoWorm/).

**Community Outreach**

The effort to build the OpenWorm open science community is always ongoing. See the [contributor progression model ([DD011](contributing/contributor-progression.md))](contributing/contributor-progression.md) for the L0-L5 path.

More detailed information is available on the [Community project page](Projects/community-proj/).

**Muscle-Neuron Integration**

Now formalized in **DD002** (neural) + **DD003** (muscle) + **DD005** (cell-type specialization). The goal of creating biologically-realistic ion channel models from experimental data is specified with quantitative criteria and CeNGEN single-cell transcriptomics as the primary data source.

More detailed information is available on the [Muscle-Neuron integration project page](Projects/muscle-neuron-integration/).

**_C. elegans_ robot**

The goal of this project is twofold:

1. To build a robot that simulates sensory-motor functions of a _C. elegans_ nematode worm, including foraging for food.
2. To specify parts and instructions that will help anyone to build the robot.

More detailed information is available on the [_C. elegans_ robot project page](Projects/c-elegans-robot/).
