Current releases
================

The recent and planned releases for the Docker image which contains the assembled OpenWorm software stack can be found at the [OpenWorm Milestones](https://github.com/openworm/OpenWorm/milestones).



Past Releases
=============

Release 5,6,7 (2nd Half of 2013, 1st half of 2014, 2nd half of 2014)
--------------------------------------------------------------------
These releases have yet to be fully documented, as the project has transitioned
from a small group-only run project into a much larger volunteer-based
organization.

Some key milestones that were reached:

Release 7

-  **First OpenWorm Paper published**
-  **Donation of Brown Lab worm movement data**
-  **Successful shipments of physical rewards to Kickstarter backers**

Release 6

-  **First version of PyOpenWorm released**
-  **Successful Kickstarter campaign**

Release 5

-  **Movement validation team formed**
-  **Donation of code to reproduce movement validation**

Release 4 (1st Half of 2013) January - July 2013
------------------------------------------------

-   **OpenWorm website update** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=10&state=closed)
    -   completely renewed version of the website using bootstrap
-   **Tuning neurons based on real worm recordings** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=16&state=closed)
    -   plotted some calcium traces from Leifer's lab
-   **Ion Channel and Neuropeptide database** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=16&state=closed)
    -   Defined known neuropeptides for each neuron
-   **Data visualization experiments** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=8&state=closed)
    -   hive plots of connectome - poster at Neuroinformatics 2013
    -   D3JS experiments
-   **Submit a perspectives paper on OpenWorm** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=9&state=closed)
    -   drafted and submitted to frontiers - review process ongoing
-   **Synapse position crowdsourcing** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=11&state=closed)
-   **C++ Fluid mechanics engine improvements** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=2&state=closed)
    -   independent bundles of contracting elastic matter
    -   impermeable surfaces
    -   bug fixes on liquid and elastic matter
    -   renamed C++ implementation to Sibernetic
-   **Integration of membrane electrophysiology and muscle cell mechanics** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=1&state=closed)
    -   poster at CNS 2013
-   **Geppetto platform: 1st release** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=4&state=closed) / [release](https://github.com/openworm/org.geppetto/releases/tag/v0.0.2-alpha)
    -   basic simulation file XML specification
    -   simulation lifecycle and basic interaction
        -   load / start / stop / reset
    -   WebGL frontend visualization
        -   particle systems
        -   ball-stick morphologies
        -   camera controls: rotation / zoom / panning
    -   Multi-user support
        -   multiple-users can observe the same simulation
    -   Tooling and scripts to facilitate deployment / install etc.
-   **Geppetto plugin: single-compartment neuronal simulator** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=3&state=closed)
-   **Geppetto plugin: fluid mechanics solver** - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=14&state=closed)
    -   ported C++ version to Java for liquid and elastic matter support
    -   porting validation - [milestone](https://github.com/openworm/OpenWorm/issues?milestone=18&state=open)
        -   unit testing infrastructure to validate codebase

Journal clubs Posts Media Coverage

Release 3 (completed) May 2012 - November 2012
----------------------------------------------

This release, among many acheivements, we accomplished the following:

-   Published a paper
-   Made several presentations
-   Interacted with lots of folks doing community building
-   Got mentioned, pointed to, or referenced in several interesting articles
-   Built and advanced several code products

[Detailed release notes from this release can be found online](https://docs.google.com/a/metacell.us/document/d/1cg1YnKI92tN9HZeXachTfpRlKP10OuJhXlRBabeTnuI/pub)

Our second release pointed us in a good direction for the future, and provided some [exciting products](http://browser.openworm.org). In release 3, we worked to develop additional products that are more easily used by the outside world.

### EPIC-1: As a user, I want to be able to mark synapses and have them integrated into the model

The user will be able to contribute to a shared knowledge space of the positions and identities of _C. elegans_ synapses using an installation of CATMAID. This is important because the _C. elegans_ connectome does not currently incorporate synapse positions at all.

### EPIC-2: As a developer, I want to launch the simulation engine on Amazon AWS

This could be implemented with an auto-configuration system like [Fabric](http://docs.fabfile.org/en/1.8/) that automatically launches AWS instances and runs an installation script on it. This way we can control what OS / drivers are used on the target system.

### EPIC-3: As a user, I want to be able to see the body of the worm moving and changing color, driven by activity of the simulation engine (Simplified Worm)

It is important the outside users can see a visual representation of the simulation engine so that they can get a sense of what is going on with the project.

### EPIC-4: As a user, I want to be able to run a simulation that includes muscle cell physics as well as muscle cell membrane excitability

### EPIC-5: As a scientist, I want a detailed written summary of the physiology we intend to include in the model

This is a document written as prose that summarizes the physiological data that is known.. This should structure the information that currently exists and show where the gaps of knowledge are.

This is important because we want to build cells which are conductance based models. At the moment we don't know all the channels. This allows others to contribute what they know about this.

### EPIC-6: As a user, I want to see the optimized data matching the experimental results

This should enable the parameters of the muscle cell to be tuned with respect to real data.

EPIC-7: As a user, I want to see a WebGL visualization of [Smoothed Particle Hydrodynamics](http://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics) -----------------------------------------------------------------------------------------We want to be able to run the Smoothed Particle Hydrodynamics demos so we can see them through the browser.

### Presentation update

Release 2 (completed) October 2011 to April 2012
------------------------------------------------

Our major goal for this release was to integrate the work we have done in release one to do a detailed simulation of a body wall muscle cell, MDL08 (pictured below). While we did not complete all of the epics we set out for ourselves, we made significant progress in all of them, and learned a lot in the process. See the [Roadmap](https://github.com/openworm/OpenWorm/wiki/Roadmap) for more information on where we are now.

This muscle cell receives input from 8 motor neurons:

-   AS01
-   AS02
-   DA01
-   DA02
-   DB01
-   DD01
-   SMDDL
-   SMDDR

We want to combine the physical simulator, running PCI SPH, that should model the walls of the muscle cell and the force pulling on those walls when the muscle is active, with the cell membrane excitability simulator, (e.g., the Hodgkin Huxley simulator). In order to ensure that our simulation is returning results that match reality, we will tune the significant number of parameters in our simulation using a genetic algorithm.

### Component: Genetic Algorithm

**EPIC-1** As a user, I want to use a genetic algorithm to fit the parameters of the muscle cell and motor neurons to real data Component: Simulation Engine

**EPIC-2** As a user, I want to run a model developed in NeuroML on our simulation engine to be able to run NeuroML models on the Amazon cloud

**EPIC-3** As a user, I want to be able to run a simulation that includes muscle cell physics as well as muscle cell membrane excitability.

### Component: Worm Browser

**EPIC-4** As a user of the simulation engine, I want a browser-based visualization to show me the muscle cell output

### Component: Database

**EPIC-5** As a model builder, I want the best definition of the muscle cell model and motor neurons

**EPIC-6** As a model builder, I want to have a target output of the muscle cell.

### Component: Website

**EPIC-7** As a visitor to openworm.org, I want to be impressed with the professionalism of the project and want to contribute

### Component: Kickstarter

**EPIC-8** As an open worm team member, I want to launch a fundraising campaign to raise money for the project

Release 1 (completed) May 2011 - September 2011
-----------------------------------------------

We have set a completed a successful release 1 in September. It included the following features:

-   Multi-algorithm simulation engine
-   Create a generic architecture for combining algorithms operating at different time scales on different models
-   Create [conductance-based simulator](http://www.scholarpedia.org/article/Conductance-based_models) using [OpenCL](http://en.wikipedia.org/wiki/OpenCL)
-   Create a [smoothed particle hydrodynamics (SPH)](http://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics) simulator
-   Use the simulation engine architecture to combine these two algorithms to prove its generality and ability to cross algorithmic domains
-   Neuron database
-   Use the [Virtual Worm](http://caltech.wormbase.org/virtualworm/) Blender files to create a NeuroML compartmental description of the 302 neurons
-   Combine knowledge about the [synaptic structure of the neuronal network](http://www.wormatlas.org/neuronalwiring.html) with the compartmental description
-   Combine knowledge about the ion channel structure of the neuronal network with the compartmental description
-   Worm browser
-   Build a 3D interactive visualization of the Virtual Worm Blender files, akin to the [Google Body Browser](http://www.zygotebody.com/)

### Simulation Engine

-   As a developer, I would like a simulation engine prototype that provides a design proof of concept
-   As a developer, I want an alpha kernel for neuronal simulation for the prototype.
-   As a developer, I want a first draft of a simulation engine design
-   As a product manager, I want to see a working prototype of the SPH algorithm working with the existing [CyberElegans](http://www.youtube.com/watch?v=Ek49JSAiKjY) code
-   As a product manager, I want a initial test implementation example of the SPH algorithm implemented as a solver
-   As a developer, I want a simple test harness to function as client for the simulation engine prototype to ensure everything is working.
-   As a developer, I would like to have a prototype of a solver service, using the HH OpenCL alpha kernel.

### Neuron Database

-   As a developer, I want the Virtual Worm Blender files to include details about synapses so simulatable NeuroML can be produced
-   As a developer, I want to be able to convert the Virtual Worm meshes for neurons into complete simulation ready NeuroML descriptions of the neurons

### Worm Browser

-   As a user I want to visualize 3D models of the worm in the browser
-   As a user, I want to have GUI controls to zoom in and out of the worm
-   As a user, I want to drag the worm using "cylindrical mouse orbit" like google body browser
-   As a product manager, I want an example of a Unity3D web player that can visualize the Virtual Worm blender files to mitigate risk
-   As a developer, I want to have the 3D models of the worm prepared in a suitable format so they can be visualized in the Web Browser
-   As a user, I want to use a slider to smoothly make systems in the worm transparent
-   A more complete document describing our plans for release 2 is available.
