Muscle-Neuron-Channel Integration
=================================

High-level Overview
-------------------

The fidelity of OpenWorm to its biological counterpart, C. elegans, depends on the realism of its constituent parts, such as computationally-modelled cells. The internal dynamics of these cells are largely controlled by ion channels, so a biophysically-informed ion channel model will, in-turn, support a realistic model of the entire organism.

Broadly speaking, the team for this project will develop a workflow and tools to simulate *C. elegans* cell dynamics using simulated ion channel (*intracellular*) dynamics.

[![image](http://docs.google.com/drawings/d/1WzHYpgHZBDvbAxIb-KDDw0OatI8KWXQ8h_BeMVaQ2wM/pub?w=1238&amp;h=869)](https://docs.google.com/drawings/d/1WzHYpgHZBDvbAxIb-KDDw0OatI8KWXQ8h_BeMVaQ2wM/edit)

The literature will be mined for scientific papers with ion channel data, which will be fed to the ChannelWorm pipeline. Inside the pipeline, data are extracted from the papers by various means, including digitization of figures. These data are then used to construct ion channel models.

Each ion channel model is simulated and, depending on its performance in a set of validation tests, takes one of two paths. If the model passes validation, it is stored in the project's database (PyOpenWorm) for later use. Otherwise the model fails validation, and is used as input for the optimization package. After tuning a model's parameters to the literature values, the model is updated, simulated, and passed to the validation phase again. This loop of modeling, validation and optimization may take several runs before a model passes.

Once the ion channel models are successfully validated and stored in the PyOpenWorm database, they can be incorporated into cellular models in both the Muscle Model and c302 (Neuron) subprojects. In each of these sections - PyOpenWorm database, Muscle Model and c302 - there are corresponding validation tests that ensure the integrity of their respective components. The validation tests will employ a similar approach in each subproject, and will be written using the same framework.

### Tracking progress

Issues for this set of projects are organized on our [project board](https://github.com/orgs/openworm/projects/5), and may give a clearer picture of what is going on in each of them.

Below is a similarly organized board keeping track of our higher-level *milestones* in each repository (in the Muscle / Neuron / Channel list), which will be updated as this meta-project develops.

[![](trello.png)](https://trello.com/b/mPaT7Ol0/openworm-release-10-milestone-roadmap-not-individual-tasks-issues)

### Modeling / Validation / Optimization Loop

[![image](https://docs.google.com/drawings/d/13JvpUktlTXN2GKH9fXzacXQWudm5MQUMXXY94cr6S50/pub?w=778&h=370)](https://docs.google.com/drawings/d/13JvpUktlTXN2GKH9fXzacXQWudm5MQUMXXY94cr6S50/edit)

This figure describes, in a general way, how ion channel models are simulated and incrementally fit to their observed counterparts, as will be done in [the ChannelWorm subproject](https://github.com/VahidGh/ChannelWorm/).

Depending on the type of data being used (e.g. patch-clamp data or homology modelling), the implementation will differ, but our approach will still follow this pattern.

Let's take an example channel model being compared to patch-clamp data from the literature:

1.  We have a given channel model (ex: [ca\_boyle](https://github.com/openworm/muscle_model/blob/master/NeuroML2/ca_boyle.channel.nml/))
2.  Run it through simulating scripts (ex: [Rayner's scripts](https://github.com/openworm/BlueBrainProjectShowcase/blob/master/Channelpedia/iv_analyse.py/))
3.  These scripts give us a simulate I/V curve, which can be compared to a digitized I/V curve from the literature ([example digitized curve](https://plot.ly/~VahidGh/56/))
4.  Depending on the result of [a test](https://github.com/openworm/muscle_model/issues/30/) comparing these two I/V curves, the model is either *kept* or *optimized further* using NeuroTune.

Model Completion Dashboard
==========================

This is one possible interface that will display the results of the unifying modeling activity.

This interface allows a user to drill down into our model, and view the states of completion of modeled components at each level. At the highest level, matrices display, using a color indicator, the level of completion of each cell in the model.

By clicking one of these cells, the section below focuses on that cell. Ion channels that exist in that cell are displayed in a grid with completion coloring, and simulation/experimental data for the cell is compared in plots.

Individual ion channels can be clicked on and selected from the grid, with parameters and simulation/experimental comparison plots available.

Rolling over the data displayed at each level gives information about the references for that particular piece of data.

---

Clicking on the image below will let you view the raw drawing, and see more detailed annotations for each element.

[![](https://docs.google.com/drawings/d/1PcAMyBLZR3Z98gb4BDTUKp9PMDWZJHo2fnlYAVpISmo/pub?w=1672&h=2918)](https://docs.google.com/drawings/d/1PcAMyBLZR3Z98gb4BDTUKp9PMDWZJHo2fnlYAVpISmo/edit)

ChannelWorm
-----------

[The ChannelWorm subproject](https://github.com/VahidGh/ChannelWorm/) is, at a high level, a pipeline to convert ion channel *data* found in scientific papers into ion channel *models*. This pipeline involves:

1.  [Identification](https://github.com/VahidGh/ChannelWorm/issues/10/) of papers with ion channel data.
2.  Extraction of data from these papers, including figures, active parameters and tabular data.
3.  [Digitization](http://channelworm.readthedocs.org/en/latest/digitization/) of figures, and more generally, converting this information into machine-readable form.

The output of the pipeline will either be [fed into an optimization engine](http://channelworm.readthedocs.org/en/latest/optimization/) or [stored in a database](http://channelworm.readthedocs.org/en/latest/information-management/#data-management), depending on the results of [validation tests](http://channelworm.readthedocs.org/en/latest/validation/).

### Current roadmap

We are tracking milestones for this project over [here.](https://github.com/VahidGh/ChannelWorm/milestones/)

The tasks ahead include:

1.  Run [Rayner's scripts](https://github.com/openworm/BlueBrainProjectShowcase/blob/master/Channelpedia/iv_analyse.py/) on an example cell, and get output.
2.  Establish common format between outputs of Rayner's script (above) and [digitized plots](https://plot.ly/~VahidGh/56/) from scientific articles.
3.  Write test to compare digitized plots and plots generated from ion channel model.

### Issues list

Issues for this part of the project are tracked and raised in [the Github repo,](https://github.com/VahidGh/ChannelWorm/issues?q=is%3Aopen+is%3Aissue/) as well as the [ChannelWorm waffle board](https://waffle.io/VahidGh/ChannelWorm).

### Associated Repositories

- [ChannelWorm](https://github.com/VahidGh/ChannelWorm/)

Optimization
------------

The [Neurotune](https://github.com/vellamike/neurotune/) package provides neurotune a package for optimizing electrical models of excitable cells.

In other words, Neurotune provides a solution for optimizing the parameters of a model to match a specific output. In the case of ChannelWorm, the parameters are electrical ion channel parameters, and the desired output is patch-clamp data comparable to that observed in real life.

### Associated Repositories

- [Neurotune](https://github.com/vellamike/neurotune/)
- [NeuroTune docs](http://optimal-neuron.readthedocs.org/en/latest/architecture.html/)

## PyOpenWorm Unified Data Access Layer

We have consolidated a lot of data about the worm into a python library that creates a unified data access layer [called PyOpenWorm](https://github.com/openworm/pyopenworm). [Documentation for PyOpenWorm is available online](http://pyopenworm.readthedocs.org/en/latest/intro.html).

### Previous accomplishments

-   Building the original [OpenWorm database](https://groups.google.com/d/msg/openworm-discuss/2V5kF5na5fw/GnxZMgWYF7wJ)
-   [Initial release of PyOpenWorm](https://github.com/openworm/PyOpenWorm/releases/tag/0.0.1-alpha)

### Current roadmap

PyOpenWorm will be used in the information storage aspect of various other subprojects. For instance, ChannelWorm will use [its own fork of PyOpenWorm](https://github.com/openworm/PyOpenWorm/tree/channelworm/) to store Ion Channel data and models that it retrieves from scientific papers. Next steps involve:

1.  Adapting PyOpenWorm's existing infrastructure to serve ChannelWorm
2.  Filling the database with information, being sure to tag each fact with sources along the way.
3.  Finalize [remaining issues for PyOpenWorm version alpha0.5](https://github.com/openworm/PyOpenWorm/labels/alpha0.5)
4.  [Document Neuron Ion Channels: Types](https://github.com/openworm/OpenWorm/issues/31)
5.  [Document Ion channels: Research Claims](https://github.com/openworm/OpenWorm/issues/32)

### Issues list

Issues for PyOpenWorm are tracked [on Github](https://github.com/openworm/PyOpenWorm/issues/).

### Associated Repositories

- [PyOpenWorm](https://github.com/openworm/PyOpenWorm/)

Muscle Model
------------

The [muscle model subproject](https://github.com/openworm/muscle_model/) is concerned with modelling and simulation at the *cellular* level, specifically attempting to simulate the electrical dynamics of a *C. elegans* body wall muscle cell.

This depends on what happens in [ChannelWorm](#channelworm), since ion channel dynamics are integral to our simulation of membrane dynamics.

Because the muscle cell is driven both by an electrical model and a mechanical model, it is a focus of integration between different algorithms. Previously we have created a separate [repository for the muscle model](https://github.com/openworm/muscle_model) that is an adaptation of the work by [Boyle & Cohen, 2008](http://www.comp.leeds.ac.uk/netta/CV/papers/BC08b.pdf). We have an [approximately working version](http://www.opensourcebrain.org/projects/muscle_model/wiki) implemented in NEURON and are porting this to be fully NeuroML2 compliant.

The electrical side of the model is currently the focus of the OpenWorm Muscle / Neuron Team. You can connect with the team [on real time chat](https://gitter.im/openworm/muscle_model).

To catch up with recent developments of this team, please see the following resources:

-   Meeting \#1 ([YouTube Video](https://www.youtube.com/watch?v=6AhKE2Vg_Uw)) ([Agenda](https://docs.google.com/document/d/1BByFfABx91Ao-qKFYXAP0wQONlhdDy7MtSu8G0QxUes/edit))
-   Meeting \#2 ([YouTube Video](https://www.youtube.com/watch?v=HfGAJYwNt3c)) ([Agenda](https://docs.google.com/document/d/1gUBwNjK4OEYd22Pdjt5vcm0-L6cbIHEU6k51AnOcL24/edit?usp=drive_web))
-   Synapse journal club ([YouTube Video](https://www.youtube.com/watch?v=697Irn0J_54)) ([Slides](https://docs.google.com/presentation/d/1uMtXJNEXzzoPw45HG6sztqiiPDUn2jcUpHj7oiHxu38/edit?usp=sharing))
-   Meeting \#3 ([YouTube Video](https://www.youtube.com/watch?v=3KApBmFa6WY)) ([Agenda](https://docs.google.com/document/d/1JAH4Hs_J0tYbcEuxOMQ0fl2NPf6H6Z7kbe72lAi7SdA/edit))

Some additional background materials that will help explain neuroscience concepts relevant to to this in two minutes each are below:

-   [The neuron](https://www.youtube.com/watch?v=6qS83wD29PY)
-   [Membrane potential](https://www.youtube.com/watch?v=tIzF2tWy6KI)
-   [Synaptic transmission](https://www.youtube.com/watch?v=WhowH0kb7n0)
-   [Receptors and ligands](https://www.youtube.com/watch?v=NXOXZ-kaSVI)

### Previous accomplishments

-   Implementation of Boyle & Cohen muscle model [in python](https://github.com/openworm/muscle_model/tree/master/BoyleCohen2008/)
-   [Conversion of model into NEURON](https://github.com/openworm/muscle_model/tree/master/neuron_implementation/)
-   [Simulation](https://github.com/openworm/muscle_model#21-simulation-of-muscle-cell-ion-channels/) of NeuroML2 ion channels in LEMS

### Current roadmap

Some of the next steps for the muscle model subproject include:

1.   [Create unit test on the full muscle model that reproduces Figure 1A from Liu, Hollopeter, & Jorgensen 2009](https://github.com/openworm/muscle_model/issues/31)
2.   [Create unit test that verifies correct I/V curve for ca\_boyle NML2 channel](https://github.com/openworm/muscle_model/issues/30)
3.   [Update optimization.py to run with neurotune instead of optimalneuron](https://github.com/openworm/muscle_model/issues/18)

### Issues list

Issues for the muscle model are tracked [on Github.](https://github.com/openworm/muscle_model/issues/)

### Associated Repositories

- [Muscle\_model](https://github.com/openworm/muscle_model/)

c302
----

The [c302 subproject](https://github.com/openworm/CElegansNeuroML/tree/master/CElegans/pythonScripts/c302/) is an effort to simulate the connectome of *C. elegans*, which includes its 302 neurons. The neural dynamics will start out with biologically-unrealistic integrate and fire cells, and be replaced with incrementally more realistic dynamics, as tests pass. Like the musclemodel, dynamics of neurons depend on ion channel dynamics within the cells, and thus depend on the channelworm subproject.

### Previous accomplishments

-   Generate NeuroML2 using [libNeuroML](https://github.com/NeuralEnsemble/libNeuroML/) combined with connectivity data
-   Run simulations of the connectome in LEMS using [jNeuroML](https://github.com/NeuroML/jNeuroML/) or [pyNeuroML](https://github.com/NeuroML/pyNeuroML/)

### Current roadmap

1.  Create validation tests using [SciUnit](https://github.com/scidash/sciunit/) or a similar framework.
2.  Run validation tests.

### Issues list

Issues for c302 are tracked [in the CElegansNeuroML repo.](https://github.com/openworm/CElegansNeuroML/issues/)

### Associated Repositories

- [CElegansNeuroML](https://github.com/openworm/CElegansNeuroML/)
