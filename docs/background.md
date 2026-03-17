Project Background
==================

History
-------

Established in January 2011, OpenWorm has since that time built a community of highly-motivated and highly-skilled individuals and coordinated their work. This community has produced scientific publications making use of scientific research published through open access, helping to show the validity of the open science approach we have taken.

Please [visit here](../fullhistory/) for a more extensive history of the project.

More information is available on the past history of [OpenWorm releases](../releases/).

Why do this?
------------

There has never been a scientific result in biology or neuroscience that is inconsistent with the idea that brains are 100% physical matter. We tend to forget, but our brains are tissues just like our lungs and heart are. If I could stick an electrode in your brain right now I could record activity from your neurons that corresponds with your thoughts. The problem is that scientists can't understand what all that activity means yet.

Scientists can make models of sending a rocket to land on the surface of Mars, but not a model of all the activity of your brain. Scientists lack well-agreed upon models of complex neuronal activity because such models are hard to produce.

Complex neuronal activity is the result of countless interactions between molecules happening inside, between, and around neurons. Because of all the interactions that make up complex neuronal activity, you need to gather up a lot of information to make models of it. Also because of all those interactions, you need sophisticated software platforms to manage all that information properly.

We are building a simulation platform to prove it is possible to make good models of complex neuronal activity, starting with a digital worm. We are making the simulation platform open source because we believe anyone should be able to use it to understand how neurons and cells work.

Why _C. elegans_?
-----------------

In the field of neuroscience, one of the simplest organisms that are studied is _Caenorhabditis elegans_, or _C. elegans_ for short. It only has 302 neurons, has a very consistent lifecycle, and is well studied. Its whole [connectome](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) (wiring diagram) has been mapped. Its whole body has only 1000 cells total. With those 1000 cells it solves basic problems of feeding, mate-finding, predator and toxin avoidance using a nervous system driving [muscles](design_documents/DD002_Muscle_Model_Architecture.md) on a body in a complex world.

The cells in its body work together to produce its behavior. Instead of starting with the behavior and building a simple system to capture it, we are starting with making models of the individual cells and their interactions. If we do this correctly so that the cells act on each other as they do in the real organism, we will have a much more realistic model than we would get trying to go straight to the behavior.

This seems to us the only sensible starting point to creating a true biological simulation that captures enough details and has enough constraints to approximate real biology. Simulating a single cell that doesn't move (like a yeast cell) isn't going to provide us enough of a foundation to build up to more complex organisms by itself. If we can't accomplish a simulation at this humble scale, we'll never be able to do it at the massive scale of the human brain. The technology that would come out of this endeavor would be applicable to much more complex organisms down the road.

On models
---------

Models are the cornerstone of science. Tools like algebra, calculus, Newtonian mechanics and computer spreadsheets were advances because we could plug numbers into equations and get answers out that told us something about the world.

Unfortunately, neuroscience has few predictive models for how nervous systems work.

We are starting by building a full simulation of a small biological system with a reasonable number of parts. We are focused on capturing as much of the rich detail of that biological system as possible.

Concepts
--------

### Top-down simulation

Our first instincts when looking at a system we want to simulate is to come up with a list of its obvious features and then try to pick the simplest means of simulating it. In the case of obvious top-down ways to model a worm, one might capture the fact that it bends in a sinusoidal pattern as a good starting point, and begin implementing sine and cosine functions that can capture this.

There is an important place for this kind of simulation, but we have found that one rapidly runs into limitations of generalization. The model that worked great for crawling no longer works for turning around. The simplest thing possible is added to the model to make it work for turning around, but soon there is another aspect to capture, and then another. Soon, the model is a series of hacks that become increasingly brittle.

Instead of a pure top-down approach, we employ a balanced top-down, bottom-up approach, with a greater emphasis on the bottom up.

### Bottom-up simulation

Biology teaches us that when it comes to understanding how animals work, understanding the [behavior of cells is critical](https://en.wikipedia.org/wiki/Cell_biology). Our bodies are made up of between 40 and 100 trillion cells, and it is these cells working together that make up everything we are and do. Of particular interest are the cells in the brain and larger nervous system, that are responsible for our thoughts, creativity and feelings.

Today, science has barely scratched the surface of how to make best use of the enormous power of computers to create models of cellular activity. Scientists have not yet placed computer models of cells at the center of biology.

A "bottom-up" simulation, in this case, is an attempt to model the individual cells in the organism, giving them behaviors which, when combined together, produce the outward behavior of the entire organism. This is as opposed to building the organism without consideration for individual cells to start with, and adding cells in later.

In reality, we always have to do some bottom-up simulation along with top-down simulation, in order to make progress. But in general and where possible, we view what we are doing as focused on simulating cells first.

### Multi-algorithm integration

Just as mathematics has played a crucial role in the [description of physics](https://en.wikipedia.org/wiki/Mathematical_physics), [mathematicians have approached the field of biology](https://en.wikipedia.org/wiki/Mathematical_and_theoretical_biology) with the goal of describing biological activity more precisely. Generally speaking, this means that if it happens inside a biological organism, there should be a set of equations that can explain how it works. A great deal of creativity goes into coming up with such equations.

Once equations have been determined, computers are great at calculating them once they have been [turned into algorithms](https://en.wikipedia.org/wiki/Algorithm). Algorithms become the computer's way of handling a bunch of equations.

The challenge is that there are a lot of equations that are necessary to fully specify how cellular activity works. A [recent whole cell model](https://simtk.org/home/wholecell) of a relatively simple cell came up with 32 algorithms composed of many more equations and a ton of data.

The consequence of this from an engineering perspective is, in order to simulate complex living systems, we need software that is flexible enough to let us assemble the algorithms we need in just the right ways. We call this "multi-algorithm integration".

### Model optimization

There are a lot of aspects of _C. elegans_ that we will not be able to measure directly for a while based on experimental limitations. These are ["free parameters"](https://en.wikipedia.org/wiki/Free_parameter). The conventional wisdom on modeling is to minimize the number of free parameters as much as possible. Sometimes, the large number of free parameters are used as an argument to avoid making computational simulations.

In this case, we have to make do with what we have and make some good educated guesses about the free parameters. There is a [mathematical discipline that helps us do that known as optimization](https://en.wikipedia.org/wiki/Mathematical_optimization). For our purposes, you can think of this as generating many different versions of a model, each version with slightly different parameters, and then measuring if the model produces good results. If a model produces better results by changing the parameters in a particular way, you try to keep changing the parameters in that way and see if you get even better results. In this way, roughly speaking, optimization techniques enable scientists to turn a problem of lack of data into a problem that a computer can address using brute force calculations.

### NeuroML

[NeuroML](https://docs.neuroml.org) is an XML (Extensible Markup Language) based model description language that aims to provide a common data format for defining and exchanging models in computational neuroscience. The focus of NeuroML is on models which are based on the biophysical and anatomical properties of real neurons. NeuroML is known as an open standard, because its means of describing a model is publicly available for others to improve upon.

OpenWorm's [c302 framework](Projects/c302.md) generates NeuroML2 networks of the _C. elegans_ nervous system at multiple biophysical detail levels, as specified in [DD001: Neural Circuit Architecture](design_documents/DD001_Neural_Circuit_Architecture.md).

---

Mission & Design Principles
----------------------------

The concepts above — bottom-up cell-level modeling, multi-algorithm integration, optimization against experimental data — are all in service of a single mission:

> "OpenWorm is an open source project dedicated to creating the world's first virtual organism in a computer, a *C. elegans* nematode."

Or more simply: **"Building the first digital life form. Open source."**

This is an ambitious goal, and it requires discipline. We've crystallized our approach into four design principles that shape every architectural decision in the project:

1. **Biophysically realistic** — grounded in experimental data, not heuristic shortcuts
2. **Causally interpretable** — we can trace why behavior emerges from underlying mechanisms
3. **Validated** — tested against real worm physiology and behavior ([DD010: Validation Framework](design_documents/DD010_Validation_Framework.md))
4. **Composable** — subsystems integrate via clean interfaces so the whole is greater than the sum of its parts

And one core conviction about *how* to build it:

> "Worms are soft and squishy. So our model has to be too. We are building in the physics of muscles, soft tissues and fluids. Because it matters."

These principles are operationalized in the [Design Documents](design_documents/index.md), which serve as the technical roadmap from today's 302-neuron simulation to the complete 959-cell digital organism.

### Philosophical foundations

These design principles didn't emerge in a vacuum — they draw on several intellectual traditions that inform how we think about what it means to truly *understand* a biological system.

**Mechanistic explanation.** We follow [Machamer, Darden & Craver (2000)](https://doi.org/10.1086/392759), who argue that biological understanding requires identifying *mechanisms* — organized systems of entities and activities that produce phenomena. Each Design Document specifies a mechanism: ion channels produce membrane dynamics, muscles produce force, neurons produce behavior. Understanding means tracing the causal chain from molecular parts through cellular activities to organismal behavior.

**Causal models, not just predictive ones.** [Pearl (2000)](https://doi.org/10.1017/CBO9780511803161) draws a crucial distinction between systems that can *predict* outcomes (statistical models) and systems that can answer *"what if?"* questions (causal models). OpenWorm is designed as a causal model — we can ablate a virtual neuron and predict the behavioral consequence, not because we trained on ablation data, but because the model captures the mechanistic structure that makes the prediction follow from first principles. This is our core differentiator from data-driven foundation models.

**Emergence.** A simulated organism that exhibits behavior not explicitly programmed raises deep questions. Can higher-level properties (locomotion, foraging, arousal states) be fully explained by lower-level mechanisms (channel kinetics, calcium dynamics, synaptic transmission)? [Chalmers (2006)](https://doi.org/10.1093/acprof:oso/9780199544318.003.0011) distinguishes "weak" emergence (deducible in principle from lower-level laws) from "strong" emergence (not so deducible). Our multi-tier [validation framework](design_documents/DD010_Validation_Framework.md) directly tests whether behavior emerges from mechanism, by validating at every level independently.

**Completeness.** [Haspel et al. (2023)](https://arxiv.org/abs/2308.06578) argue that *C. elegans* offers a unique opportunity for observational and perturbational completeness — recording from and manipulating every neuron — which is a prerequisite for causal understanding ([Pearl & Mackenzie 2018](https://www.hachettebookgroup.com/titles/judea-pearl/the-book-of-why/9780465097616/)). OpenWorm complements this experimental agenda with *computational* completeness: modeling every cell, every connection, every signaling pathway. Together, experimental and computational completeness enable a depth of understanding that partial approaches cannot achieve.

??? note "References"
    - [Machamer P, Darden L, Craver CF (2000)](https://doi.org/10.1086/392759). "Thinking about Mechanisms." *Philos Sci* 67:1-25.
    - [Pearl J (2000)](https://doi.org/10.1017/CBO9780511803161). *Causality: Models, Reasoning, and Inference.* Cambridge University Press.
    - [Chalmers DJ (2006)](https://doi.org/10.1093/acprof:oso/9780199544318.003.0011). "Strong and Weak Emergence." In: *The Re-Emergence of Emergence.* Oxford University Press.
    - [Haspel G et al. (2023)](https://arxiv.org/abs/2308.06578). "To reverse engineer an entire nervous system." *arXiv* [q-bio.NC] 2308.06578.
    - Pearl J, Mackenzie D (2018). *The Book of Why: The New Science of Cause and Effect.* Basic Books.

---

## How These Concepts Connect to Design Documents

Each concept on this page has been formalized into an actionable Design Document (DD):

| Concept | Design Document | What It Specifies |
|---------|----------------|-------------------|
| Bottom-up simulation | [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD002](design_documents/DD002_Muscle_Model_Architecture.md), [DD003](design_documents/DD003_Body_Physics_Architecture.md) | The core chain: neurons → muscles → body physics |
| Multi-algorithm integration | [DD013](design_documents/DD013_Simulation_Stack_Architecture.md) | Docker-based simulation stack assembling all algorithms |
| Model optimization | [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) | Hybrid mechanistic-ML framework for parameter fitting |
| NeuroML | [DD001](design_documents/DD001_Neural_Circuit_Architecture.md), [DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md) | c302 generates NeuroML2 networks using cect connectome data |

---

## Continue Reading

- **[How It Works: Modeling](modeling.md)** — How these concepts come together in the current multi-scale architecture
- **[Validation Framework](validation.md)** — How we test that the model matches real worm biology
- **[Design Documents](design_documents/index.md)** — The complete technical roadmap from 302 neurons to 959 cells
- **[Full History](fullhistory.md)** — Detailed timeline from 1900 to present
