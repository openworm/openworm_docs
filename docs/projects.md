## OpenWorm Projects

## Projects and Design Documents

OpenWorm's projects are now **formally specified in [Design Documents](design_documents/) (DDs)**. Each repository implements one or more DDs:

| Repository | Design Documents | Status | Role |
|------------|------------------|--------|------|
| [c302](Projects/c302/) | [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD002](design_documents/DD002_Muscle_Model_Architecture.md), [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md)-[DD009](design_documents/DD009_Intestinal_Oscillator_Model.md), [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md)-[DD019](design_documents/DD019_Closed_Loop_Touch_Response.md) | Active | Neural circuit, muscle models, organ systems |
| [Sibernetic](Projects/sibernetic/) | [DD003](design_documents/DD003_Body_Physics_Architecture.md), [DD004](design_documents/DD004_Mechanical_Cell_Identity.md) | Active | Body physics, SPH engine |
| [ConnectomeToolbox](https://github.com/openworm/ConnectomeToolbox) | [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) | Active | Connectome data access (cect API) |
| [Worm3DViewer](https://github.com/openworm/Worm3DViewer) | [DD014](design_documents/DD014_Dynamic_Visualization_Architecture.md) | Active | Visualization (Trame evolution) |
| [open-worm-analysis-toolbox](https://github.com/openworm/open-worm-analysis-toolbox) | [DD010](design_documents/DD010_Validation_Framework.md), [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) | Revival needed | Tier 3 behavioral validation |
| [OpenWorm (meta-repo)](Projects/docker/) | [DD013](design_documents/DD013_Simulation_Stack_Architecture.md) | Proposed | Integration, Docker stack |
| [Geppetto](Projects/geppetto/) | [DD014](design_documents/DD014_Dynamic_Visualization_Architecture.md) (historical) | Dormant | Web platform (superseded by Trame) |

**See [Integration Map](design_documents/INTEGRATION_MAP.md)** for the complete dependency graph.

---

### Currently active projects

-   [Neuromechanical modeling with Sibernetic](Projects/sibernetic/) — implements **[DD003](design_documents/DD003_Body_Physics_Architecture.md)** (Body Physics) + **[DD004](design_documents/DD004_Mechanical_Cell_Identity.md)** (Mechanical Cell Identity)
-   [c302 multiscale modelling framework](Projects/c302/) — implements **[DD001](design_documents/DD001_Neural_Circuit_Architecture.md)** (Neural Circuit) + **[DD002](design_documents/DD002_Muscle_Model_Architecture.md)** (Muscle Model) + **[DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md)-[DD009](design_documents/DD009_Intestinal_Oscillator_Model.md)**
-   [OpenWorm Browser](Projects/browser/)
-   [DevoWorm project](Projects/DevoWorm/)
-   [Docker simulation stack](Projects/docker/) — implements **[DD013](design_documents/DD013_Simulation_Stack_Architecture.md)** (Simulation Stack)
-   [Community outreach](Projects/community-proj/)

### Projects still maintained, less active

-   [Data collection and representation](Projects/datarep/) — relates to **[DD008](design_documents/DD008_Data_Integration_Pipeline.md)** (Data Integration) + **[DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md)** (Connectome Access)
-   [Movement analysis](Projects/worm-movement/) — implements **[DD010](design_documents/DD010_Validation_Framework.md)** (Validation) + **[DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** (Movement Toolbox)
-   [Geppetto Simulation Engine](Projects/geppetto/) — historical; superseded by **[DD014](design_documents/DD014_Dynamic_Visualization_Architecture.md)** (Dynamic Visualization)
-   [Optimization engine](Projects/optimization/) — relates to **[DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md)** (Hybrid Mechanistic-ML)
-   [Muscle-Neuron integration](Projects/muscle-neuron-integration/) — formalized in **[DD001](design_documents/DD001_Neural_Circuit_Architecture.md)** + **[DD002](design_documents/DD002_Muscle_Model_Architecture.md)**
-   [_C. elegans_ robots](Projects/c-elegans-robot/)

---

**NeuroMechanical Modeling - Sibernetic**

Sibernetic implements **[DD003 (Body Physics Architecture)](design_documents/DD003_Body_Physics_Architecture.md)** — the formal specification for SPH-based body mechanics including the PCISPH algorithm, ~100K particles, and fluid-structure interaction. See [DD003](design_documents/DD003_Body_Physics_Architecture.md) for the complete spec including particle types, validation criteria, and integration contract.

[Sibernetic](https://openworm.org/sibernetic/) is the home of the C++ code base that implements the core of the model. We have implemented an algorithm called Smoothed Particle Hydrodynamics (SPH) to simulate the body of the worm and its environment using GPUs.

To get a quick idea of what this looks like, check out the [latest movie](https://www.youtube.com/watch?v=SaovWiZJUWY). In this movie you can see a simulated 3D _C. elegans_ being activated in an environment. Its muscles are located around the outside of its body, and as they contract, they exert forces on the surrounding fluid, propelling the body forward via undulatory thrust.

More detailed information is available on the [Sibernetic project page](Projects/sibernetic/).

**c302 Neural Modeling Framework**

c302 implements **[DD001 (Neural Circuit Architecture)](design_documents/DD001_Neural_Circuit_Architecture.md)** — the multi-level Hodgkin-Huxley framework for all 302 neurons. It also serves as the foundation for [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md) (cell differentiation), [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) (neuropeptides), [DD007](design_documents/DD007_Pharyngeal_System_Architecture.md)-[DD009](design_documents/DD009_Intestinal_Oscillator_Model.md) (organ circuits), [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) (egg-laying), and [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md) (touch response).

c302 generates NeuroML2 networks at multiple levels of biophysical detail (Levels A-D), with **Level C1 (HH + graded synapses)** as the recommended default for coupling with Sibernetic.

More detailed information is available on the [c302 project page](Projects/c302/).

**Visualization**

The visualization platform is evolving per **[DD014 (Dynamic Visualization Architecture)](design_documents/DD014_Dynamic_Visualization_Architecture.md)**:

- **Phase 1:** Trame viewer (PyVista + live server)
- **Phase 2:** Interactive layers with validation overlays
- **Phase 3:** Three.js + WebGPU static site at wormsim.openworm.org (WormSim 2.0)

[Geppetto](Projects/geppetto/) served this role historically (2014-2020) and is preserved as [archival reference](archived_projects/).

**Movement Analysis and Validation**

The Movement Analysis project implements **[DD010 (Validation Framework)](design_documents/DD010_Validation_Framework.md)** — the 3-tier validation system that ensures our simulation matches real worm behavior. The analysis toolbox is being revived per **[DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)**.

More detailed information is available on the [Movement analysis project page](Projects/worm-movement/) and the [Validation page](validation/).

**Optimization and Parameter Fitting**

Now formalized in **[DD017 (Hybrid Mechanistic-ML Framework)](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md)** — differentiable simulation with gradient descent, neural surrogates for 1000x speedup, and foundation model predictions for channel kinetics.

More detailed information is available on the [Optimization project page](Projects/optimization/).

**Data Collection and Representation**

Formalized in **[DD008 (Data Integration Pipeline)](design_documents/DD008_Data_Integration_Pipeline.md)** and **[DD020 (Connectome Data Access)](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md)** — the ConnectomeToolbox (cect) is the canonical API for connectome data.

More detailed information is available on the [Data representation project page](Projects/datarep/).

**Community Outreach**

The effort to build the OpenWorm open science community is always ongoing. See the [contributor progression model ([DD011](design_documents/DD011_Contributor_Progression_Model.md))](design_documents/DD011_Contributor_Progression_Model.md) for the L0-L5 path.

More detailed information is available on the [Community project page](Projects/community-proj/).

**Muscle-Neuron Integration**

Now formalized in **[DD001](design_documents/DD001_Neural_Circuit_Architecture.md)** (neural) + **[DD002](design_documents/DD002_Muscle_Model_Architecture.md)** (muscle) + **[DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md)** (cell differentiation). The goal of creating biologically-realistic ion channel models from experimental data is specified with quantitative criteria and CeNGEN single-cell transcriptomics as the primary data source.

More detailed information is available on the [Muscle-Neuron integration project page](Projects/muscle-neuron-integration/).

**_C. elegans_ robot**

The goal of this project is twofold:

1. To build a robot that simulates sensory-motor functions of a _C. elegans_ nematode worm, including foraging for food.
2. To specify parts and instructions that will help anyone to build the robot.

More detailed information is available on the [_C. elegans_ robot project page](Projects/c-elegans-robot/).
