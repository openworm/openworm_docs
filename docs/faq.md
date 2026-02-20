Frequently Asked Questions
==========================

OpenWorm general
----------------

### Why _C. elegans_?

The tiny worm _C. elegans_ is by far the most understood and studied animal with a brain in all of biology. It was the first multi-cellular organism to have its genome mapped. It has only ~1000 cells and exactly 302 neurons, which have also been mapped as well as its "wiring diagram" making it also the first organism to have a complete connectome produced. This part gets particularly exciting for folks interested in artificial intelligence or computational neuroscience.

Three different Nobel prizes have been awarded for work on this worm, and it is increasingly being used as a model for better understanding disease and health relevant to all organisms, including humans. When making a complex computer model, it is important to start where the data are the most complete.

### What does the real worm do?

It has all sorts of behaviors! Some include:

-   It finds food and mates
-   It avoids toxins and predators
-   It lays eggs
-   It crawls and there are a bunch of different crawling motions

### Do you simulate all that?

Yes! Our roadmap progresses from today's 302-neuron crawling simulation to a complete 959-cell organism over 18 months:

- **Phase 0** (today): Crawling (302 neurons + 95 muscles + body physics, validated against Schafer lab kinematics)
- **Phase 1-2:** Cell differentiation (128 neuron classes from CeNGEN, [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md)) + closed-loop touch response ([DD019](design_documents/DD019_Closed_Loop_Touch_Response.md)) + neuropeptide modulation ([DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md))
- **Phase 3:** Pharynx pumping ([DD007](design_documents/DD007_Pharyngeal_System_Architecture.md)), intestinal defecation ([DD009](design_documents/DD009_Intestinal_Oscillator_Model.md)), egg-laying ([DD018](design_documents/DD018_Egg_Laying_System_Architecture.md))
- **Phase 4:** All 959 somatic cells ([DD004](design_documents/DD004_Mechanical_Cell_Identity.md)) with photorealistic visualization ([DD014.2](design_documents/DD014.2_Anatomical_Mesh_Deformation_Pipeline.md))

The main point is that we want the worm's overall behavior to **emerge from the behavior of each of its cells put together**. Each behavior is formally specified in a [Design Document](design_documents/) with quantitative validation targets.

### So say the virtual organism lays eggs. Are the eggs intended to be new, viable OpenWorms, or is fertilization not a goal?

Egg-laying is specified in **[DD018 (Egg-Laying System Architecture)](design_documents/DD018_Egg_Laying_System_Architecture.md)** — a 28-cell circuit (2 HSN serotonergic, 6 VC cholinergic, 16 sex muscles) that produces the characteristic two-state pattern (~20 min inactive, ~2 min active bursts). Implementation is Phase 3 work.

Developmental modeling (embryo to L1 to L4 to adult) is Phase 6 work in our roadmap, using the Witvliet developmental connectome series (8 stages). _C. elegans_ has the [best known developmental history of any organism](https://docs.google.com/file/d/0B_t3mQaA-HaMbEtfZHhqUmRIX1E/edit?usp=sharing), making it a fascinating future direction.

### Does it need to know how to be a worm to act like a worm?

The "logic" part comes from the dynamics of the neurons interacting with each other. It is a little unintuitive but that's what makes up how it "thinks". So we are simulating those dynamics as well as we can rather than instructing it what to do when. This is formalized in [DD001 (Neural Circuit Architecture)](design_documents/DD001_Neural_Circuit_Architecture.md), which uses Hodgkin-Huxley equations to model each neuron's electrical dynamics.

### Given all that we DON'T know about _C. elegans_ (all the various synaptic strengths, dynamics, gap junction rectification, long-range neuromodulation, etc.), how do you know the model you eventually make truly recapitulates reality?

All models are wrong, some models are useful :) We must have the model make a prediction and then test it. Based on how well the model fits the available data, we can quantify how well the model recapitulates reality.

We now have a formal **3-tier validation framework** ([DD010](design_documents/DD010_Validation_Framework.md)):

- **Tier 1:** Single-cell electrophysiology (patch clamp comparison)
- **Tier 2:** Circuit-level functional connectivity (must correlate r > 0.5 with [Randi 2023](https://doi.org/10.1038/s41586-023-06683-4) whole-brain imaging)
- **Tier 3:** Behavioral kinematics (speed, wavelength, frequency within +/-15% of Schafer lab database)

**Tiers 2 and 3 are blocking** — code cannot merge if validation regresses. See the [Validation page](validation/) for details.

### Is there only one solution to all those variables in the connectome that will make a virtual _C. elegans_ that resembles a real one, or are there multiple?

It is very likely to be multiple, [given what we know about the variability of neuronal networks in general](https://www.dropbox.com/s/rbab411kf5rb4zh/Similar%20network%20activity%20from%20disparate%20circuit%20parameters.%20-%20Prinz%2C%20Bucher%2C%20Marder%20-%202004.pdf). One technique to deal with this is to [generate multiple models that work](https://www.dropbox.com/s/05zx02h57vpvvqg/Multiple%20models%20to%20capture%20the%20variability%20in%20biological%20neurons%20and%20networks%20-%20Marder%2C%20Taylor%20-%202011.pdf) and analyze them under different conditions. What we are after is the [solution space that works](https://www.dropbox.com/s/hz2pv5cvomvsqez/Complex%20parameter%20landscape%20for%20a%20complex%20neuron%20model.%20-%20Achard%2C%20De%20Schutter%20-%202006.pdf) (see Fig 6 for an example), rather than a single solution.

[DD017 (Hybrid Mechanistic-ML Framework)](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) now specifies automated approaches: differentiable simulation with gradient descent for parameter fitting, plus foundation model predictions (ESM3/AlphaFold) for channel kinetics.

### Why not start with simulating something simpler? Are nematodes too complex for a first go at whole organism simulation?

Nematodes have been studied far more than simpler multi-cellular organisms, and therefore more data exist that we can use to build our model. We would need to get, for example, another connectome and another anatomical 3D map whereas in _C. elegans_ they already exist. The community of scientists using _C. elegans_ as their model organism is much larger than communities that studying simpler multi-cellular organisms, so the effect of the community size also weighed in on the decision.

### When do you think the simulation will be "complete", and which behaviors would that include?

**Phase 4 completion (~18 months from start):** 959 somatic cells, all major organ systems (pharynx, intestine, reproductive), validated against:

- [DD010](design_documents/DD010_Validation_Framework.md) Tier 3: Behavioral kinematics (Schafer lab)
- Organ-specific validation: Pumping 3-4 Hz, defecation 50+/-10s, egg-laying two-state pattern
- All cells have cell-type-specific mechanics ([DD004](design_documents/DD004_Mechanical_Cell_Identity.md))
- Public web viewer at viewer.openworm.org

**Beyond Phase 4:** Intracellular signaling (IP3/cAMP cascades), developmental modeling (growth, neuron birth/death), male-specific systems.

**"Complete" is relative** — biology is infinitely complex. We define completion as meeting all [DD010 validation criteria](design_documents/DD010_Validation_Framework.md) at the current phase. See the [Design Documents](design_documents/) for the full roadmap.

### Currently, what are your biggest problems or needs?

To make this project move faster, we'd love more help from motivated folks. Both programmers and experimentalists. We have a lot we want to do and not enough hands to do it.

**Current priorities:**

- **Infrastructure bootstrap:** Docker stack ([DD013](design_documents/DD013_Simulation_Stack_Architecture.md)), toolbox revival ([DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)), CI/CD pipeline
- **Phase 1 science:** CeNGEN cell differentiation ([DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md)), functional connectivity validation ([DD010](design_documents/DD010_Validation_Framework.md) Tier 2)
- **Integration + Validation maintainers:** Two critical L4 roles are currently vacant

Read more about ways to help [on our website](http://www.openworm.org/get_involved.html) or check the [contributor guide](community/).

### Where I could read about your "to do's?"

Our work is organized through [Design Documents](design_documents/), which define the complete roadmap from 302 neurons to 959 cells. Each DD contains deliverables, testing procedures, and integration contracts.

We also have [GitHub issues](https://github.com/orgs/openworm/projects) across all our repositories for specific programming tasks.

### How do I know which issues are safe to work on? How do I know I won't be stepping on any toes of work already going on?

We primarily use [Slack](http://openworm.org/contacts.html) for coordination. If you are interested in helping with an issue but don't know if others are working on it, ask in the relevant Slack channel. You can also comment on the GitHub issue directly. All contributors are advised to announce their intent on Slack or GitHub as soon as they start working on a task.

In general, you won't step on any toes though -- multiple people doing the same thing can still be helpful as different individuals bring different perspectives to the table.

For a structured approach, see the [DD contribution workflow](Community/github/#contributing-to-design-document-implementation) and the [contributor progression model](design_documents/DD011_Contributor_Progression_Model.md) (Observer to Senior Contributor, L0-L5).

### Do you all ever meet up somewhere physically?

Subsets of us meet frequently, and there have been two meetings of the core OpenWorm team, one in [Paris in July 2014](https://openworm.tumblr.com/post/57193347335/community-updates-from-openworm-in-paris), and a second in London in Fall of 2014. We use Slack and video calls to meet face to face on a regular basis.

OpenWorm simulation and modeling
--------------------------------

### What is the level of granularity of these models (ie. cells, subcellular, etc.), and how does that play out in terms of computational requirements?

We model at **five scales simultaneously** (detailed on the [modeling approach page](modeling/)):

| Scale | Design Documents | Computational Cost |
|-------|------------------|-------------------|
| Molecular | [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) | Low (parameter lookup) |
| Channel | [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD005](design_documents/DD005_Cell_Type_Differentiation_Strategy.md) | Moderate (HH equations per cell) |
| Cellular | [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD002](design_documents/DD002_Muscle_Model_Architecture.md), [DD007](design_documents/DD007_Pharyngeal_System_Architecture.md)-[DD009](design_documents/DD009_Intestinal_Oscillator_Model.md) | Moderate-High (302-959 cells) |
| Tissue | [DD003](design_documents/DD003_Body_Physics_Architecture.md), [DD004](design_documents/DD004_Mechanical_Cell_Identity.md) | High (~100K SPH particles) |
| Organism | [DD010](design_documents/DD010_Validation_Framework.md), [DD019](design_documents/DD019_Closed_Loop_Touch_Response.md) | Validation overhead |

In order to make this work we make use of abstraction, so something that is less complex today can be swapped in for something more complex tomorrow. [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) specifies neural surrogates that can provide 1000x speedup for body physics.

### What's the data source for your computer simulation of the living worm?

There is not a single data source for our simulation; in fact one of our unique challenges is coming up with new ways to work out how to integrate multiple data sets together. [DD008 (Data Integration Pipeline)](design_documents/DD008_Data_Integration_Pipeline.md) specifies the formal approach. Key datasets include:

-   [The Virtual Worm (3D atlas of _C. elegans_ anatomy)](http://caltech.wormbase.org/virtualworm/)
-   [The _C. elegans_ connectome](http://www.wormatlas.org/neuronalwiring.html) — accessed via [ConnectomeToolbox (cect)](https://github.com/openworm/ConnectomeToolbox) per [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md)
-   [CeNGEN single-cell transcriptomics](https://cengen.shinyapps.io/CengenApp/) — drives [cell-type differentiation](design_documents/DD005_Cell_Type_Differentiation_Strategy.md)
-   [Randi 2023 whole-brain calcium imaging](https://pubmed.ncbi.nlm.nih.gov/36859544/) — [Tier 2 validation](design_documents/DD010_Validation_Framework.md) target for functional connectivity
-   [Ripoll-Sanchez 2023 neuropeptide connectome](https://pubmed.ncbi.nlm.nih.gov/37080210/) — 31,479 interactions feeding the [neuropeptide model](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md)
-   [Schafer lab WCON behavioral database](http://wormbehavior.mrc-lmb.cam.ac.uk/) — [Tier 3 validation](design_documents/DD010_Validation_Framework.md) target for behavioral kinematics

### Has there been previous modeling work on various subsystems illustrating what level of simulation is necessary to produce observed behaviors?

There have been [other modeling efforts in _C. elegans_ and their subsystems](http://www.artificialbrains.com/openworm#similar), as well as in academic journal articles. However, the question of "what level of simulation is necessary" to produce observed behaviors is still an open question. Our [DD_CODE_REUSE_OPPORTUNITIES](design_documents/DD_CODE_REUSE_OPPORTUNITIES.md) document identifies 15 existing repos with reusable code, potentially saving 200-300 hours of implementation.

### How are neurons simulated today?

Our neural models are specified in [DD001 (Neural Circuit Architecture)](design_documents/DD001_Neural_Circuit_Architecture.md) and implemented in the [c302 framework](https://github.com/openworm/c302). c302 generates NeuroML2 networks at multiple levels of biophysical detail:

| Level | Cell Type | Synapses | Use Case |
|-------|-----------|----------|----------|
| A | Integrate-and-Fire | Event-driven | Topology testing |
| B | IAF + Activity | Event-driven | Community extensions |
| C | HH conductance-based | Event-driven | Working |
| **C1** | **HH + graded synapses** | **Graded** | **Recommended default** |
| D | Multicompartmental HH | Event-driven | Specialized studies |

**Level C1 is the default** because _C. elegans_ neurons communicate via graded potentials (not action potentials), and graded synapses are essential for coupling with the body physics (Sibernetic).

### What is the connection between the basic properties of _C. elegans_ neurons and human neurons?

_C. elegans_ neurons do not spike (i.e. have [action potentials](http://en.wikipedia.org/wiki/Action_potential)), which makes them different from human neurons. However, the same mathematics that describe the action potential (known as the [Hodgkin-Huxley model](http://en.wikipedia.org/wiki/Hodgkin%E2%80%93Huxley_model)) also describe the dynamics of neurons that do not exhibit action potentials. The biophysics of the neurons from either species are still similar in that they both have [chemical synapses](http://en.wikipedia.org/wiki/Chemical_synapse), both have [excitable cell membranes](http://en.wikipedia.org/wiki/Cell_membrane), and both use [voltage sensitive ion channels](http://en.wikipedia.org/wiki/Voltage-gated_ion_channel) to modify the [electrical potential across their cell membranes](http://en.wikipedia.org/wiki/Membrane_potential).

### What is the level of detail of the wiring diagram for the non-neuron elements?

There is a map between motor neurons and muscle cells in the published wiring diagram. Beyond that, [DD020 (Connectome Data Access)](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) specifies the ConnectomeToolbox (cect) as the canonical API for all connectivity data. The Witvliet developmental series (8 stages) and Ripoll-Sanchez neuropeptide connectome provide additional non-synaptic interaction data.

### What is SPH?

[Smoothed Particle Hydrodynamics](http://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics#Uses_in_solid_mechanics) — a mesh-free method for simulating fluid and solid mechanics using particles. More information is [available online.](http://www.zora.uzh.ch/29724/1/Barbara.pdf)

### What are you doing with SPH?

We are building the body of the worm using particles that are being driven by SPH. This is formally specified in [DD003 (Body Physics Architecture)](design_documents/DD003_Body_Physics_Architecture.md), which defines the PCISPH pressure solver, ~100K particles (liquid, elastic, boundary types), and validated body mechanics. This allows for physical interactions between the body of the worm and its environment.

OpenWorm code reuse
-------------------

### What are LEMS and jLEMS?

[LEMS (Low Entropy Model Specification)](http://lems.github.io/jLEMS/) is a compact model specification that allows definition of mathematical models in a transparent machine readable way. [NeuroML 2.0](https://docs.neuroml.org/Userdocs/NeuroMLv2.html) is built on top of LEMS and defines component types useful for describing neural systems (e.g. ion channels, synapses). [jLEMS](https://lems.github.io/LEMS/) is the Java library that reads, validates, and provides basic solving for LEMS. A utility, [jNeuroML](https://github.com/NeuroML/jNeuroML), has been created which bundles jLEMS, and allows any LEMS or NeuroML 2 model to be executed, can validate NeuroML 2 files, and convert LEMS/NeuroML 2 models to multiple simulator languages (e.g. NEURON, Brian) and to other formats.

### What about Geppetto, OSGi, Spring, Tomcat, Virgo, and Maven?

These were core technologies for the [Geppetto simulation platform](archived_projects.md#geppetto-web-platform-2014-2020), which served as our primary visualization and simulation environment from 2014-2020. Geppetto has been superseded by [DD014 (Dynamic Visualization)](design_documents/DD014_Dynamic_Visualization_Architecture.md), which specifies a lighter Python-native approach using Trame (Phase 1-2) and Three.js + WebGPU (Phase 3).

See [Archived Projects](archived_projects.md) for the full historical context.

OpenWorm links and resources
----------------------------

### Do you have a website?

<http://openworm.org>

### Where can I send my inquiries about the project?

<info@openworm.org>

### Where can I find the "worm browser"?

<http://browser.openworm.org>

### How do I join the community?

We primarily use [Slack](http://openworm.org/contacts.html) for day-to-day communication. Fill out our [volunteer application form](https://goo.gl/3ncZWn) to get an invite.

### Where are downloads located?

<http://www.openworm.org/downloads.html>
