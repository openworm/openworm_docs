*****************
OpenWorm Projects
*****************

Areas
=====

NeuroMechanical Modeling
------------------------

While our ultimate goal is to simulate every cell in the c. Elegans, we are starting out by building a model 
of its body, its nervous system, and its environment.

To get a quick idea of what this looks like, check out the CyberElegans prototype. In this movie you can 
see a simulated 3D c. elegans being activated in an environment. Its muscles are located around the outside 
of its body, and as they turn red, they are exerting forces on the body that cause the bending to happen. 
In turn, the activity of the muscles are being driven by the activity of neurons within the body.

Geppetto Simulation Engine
--------------------------

We are engineering Geppetto, a Java OSGi open-source modular platform to enable multi-scale and multi-algorithm 
interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers 
out-of-the-box visualization of simulated models right in the browser. You can read about architectural 
concepts and learn more about the different plug-in bundles we are working on.

Optimization Engine & Model Validation
--------------------------------------

The Optimization Engine uses optimization techniques like genetic algorithms to help fill gaps in our 
knowledge of the electrophysiology of *C. elegans* muscle cells and neurons. Check out the code on the 
GitHub repository.

.. **Data Collection and Representation**

.. **Community Outreach**


Detailed Roadmap
================
NeuroMechanical Modeling
------------------------

Fluid Mechanics Simulator
~~~~~~~~~~~~~~~~~~~~~~~~~

We have implemented an algorithm called Smoothed Particle Hydrodynamics (SPH) to simulate the body of the 
worm and its environment using GPUs. This algorithm has been initially worked out in C++ (with OpenGL visualization), 
then ported to Java as a bundle for Geppetto, our simulation engine.

*Associated Milestones*
`STORY: Proof of concept worm wiggling in Sibernetic <https://github.com/openworm/OpenWorm/issues?milestone=20&state=open>`_

As a scientist or developer, I want to be able to run a program and see a wiggling worm in 3D in front of me.

This refers to having a running simulation with the following components:

Four rows of 'elastic matter muscles' fixed in a 'elastic matter shell'
'Elastic matter shell' is filled with liquid that puts outward pressure on shell
'Elastic matter muscles' put force on 'elastic matter shell'
Simple sinusoidal input (no neurons) can be applied to 'elastic matter muscles' to produce simple 'wiggling'.
To get rapidly to the end goal, this implementation will be done with some combination of Sibernetic + Configuration Generator + Python scripts. A Geppetto implementation will come later.

This story breaks down the epic to predict behavior from the WormBehavior database

`Electrofluid Paper <https://github.com/openworm/OpenWorm/issues?milestone=17&state=open>`_
We are writing a manuscript focusing on the work we have to implement SPH in the project and apply it to muscle cells and the worm body. @vellamike, @a-palyanov and @skhayrulin are taking the lead on this,

The proposal is to do this after the Sibernetic proof of concept worm wiggling is complete.

*Associated Repositories*
`ConfigurationGenerator <https://github.com/openworm/ConfigurationGenerator>`_
Generation start scene configuration for PCI SPH solver
JavaScript

`CyberElegans <https://github.com/openworm/CyberElegans>`_
Neuromechanical model of C. Elegans

`Smoothed-Particle-Hydrodynamics <https://github.com/openworm/Smoothed-Particle-Hydrodynamics>`_
Known as Sibernetic, this is a C++ implementation of the Smoothed Particle Hydrodynamics algorithm for the OpenWorm project.
Java


Geppetto Simulation Engine
--------------------------
We are engineering Geppetto, a Java OSGi open-source modular platform to enable multi-scale and multi-algorithm interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers out-of-the-box visualization of simulated models right in the browser. You can read about architectural concepts and learn more about the different plug-in bundles we are working on.

*Associated Milestones*
`STORY: Worm wiggling in the browser <https://github.com/openworm/OpenWorm/issues?milestone=21&state=open>`_
As a user, I want to see the proof of concept sibernetic worm in my web browser so that anyone around the world can play with it.

Practically, this means porting the proof of concept scene into Geppetto.

`STORY: Interactive worm wiggling in browser <https://github.com/openworm/OpenWorm/issues?milestone=23&state=open>`_
As a user, I want to be able to see a visualization of the proof of concept worm wiggling in my web browser and be able to perturb it in a manner that causes the wiggling to change in a realistic manner.

This milestone suggests interactivity via Geppetto. The kind of perturbation is not defined yet-- ideally we should aim for the simplest kind we can think of that gives the user an interface to make modifications.

*Associated Repositories* 
`org.geppetto <https://github.com/openworm/org.geppetto>`_
Geppetto Main Bundle / packaging
Java

`org.geppetto.solver.sph <https://github.com/openworm/org.geppetto.solver.sph>`_
PCI SPH Solver bundle for Geppetto
Python

`org.geppetto.simulator.jlems <https://github.com/openworm/org.geppetto.simulator.jlems>`_
jLEMS based simulator for Geppetto
Java

`org.geppetto.model.neuroml <https://github.com/openworm/org.geppetto.model.neuroml>`_
NeuroML Model Bundle for Geppettoo
Java

`org.geppetto.core <https://github.com/openworm/org.geppetto.core>`_
Geppetto core bundle
JavaScript

`org.geppetto.frontend <https://github.com/openworm/org.geppetto.frontend>`_
Geppetto frontend bundle (Web Application)
Java

`org.geppetto.testbackend <https://github.com/openworm/org.geppetto.testbackend>`_
Java 

`org.geppetto.simulator.sph <https://github.com/openworm/org.geppetto.simulator.sph>`_
SPH Simulator bundle for Geppetto
Java

`org.geppetto.simulation <https://github.com/openworm/org.geppetto.simulation>`_
Generic simulation bundle for Geppetto
Python

`org.geppetto.model.sph <https://github.com/openworm/org.geppetto.model.sph>`_
PCI SPH Model Bundle for Geppetto
CSS

`org.geppetto.samples <https://github.com/openworm/org.geppetto.samples>`_
Sample simulations for Geppetto
Python

`org.geppetto.templatebundle <https://github.com/openworm/org.geppetto.templatebundle>`_
JavaScript


Optimization Engine & Model Validation
--------------------------------------
.. [NEED DESCRIPTION]

*Associated Milestones*
`STORY: Muscle Cell model output closely matches that of real data <https://github.com/openworm/OpenWorm/issues?milestone=13&state=open>`_
We will show that we have built a model of C. elegans muscle cell that matches data recorded from the nematode muscle cell. In part, we will use techniques of model optimization to fill in gaps in the model parameter space (deduce unmeasured parameters). The main technical challenge is tuning muscle cell passive properties and building a larger data set (more cell recordings).

`STORY: Build a test suite for the simulation from WormBehavior database <https://github.com/openworm/OpenWorm/issues?milestone=19&state=open>`_
As a scientist or developer, I want to be able to run a test suite against the simulation that will show me how close the model is to real data.

In order for a model to demonstrate scientific value, it has to make falsifiable predictions. The target data to be able to predict will be drawn from the WormBehavior database. This milestone will involve working with these data, creating a code base that can compare movement output from the simulation with ground truth from the database and produce an accuracy score.

This story breaks down the epic to predict behavior from the WormBehavior database

`EPIC: Correctly predict 80% of wild type (N2) behavior in WormBehavior database <https://github.com/openworm/OpenWorm/issues?milestone=22&state=open>`_
This epic is to have a simulation that can demonstrate it can predict (and therefore reproduce) 80% of the data collected about the N2 worm in the WormBehavior database. This means building a training set and a test set that are kept separate from each other, using the training set to tune up the model, then generating predictions, and comparing them against the test set, and doing some cross-validation).

This epic focuses on an output of simulation performance rather than the means of implementation, so any way to achieve this epic is welcome.

*Associated Repositories*
`HeuristicWorm <https://github.com/openworm/HeuristicWorm>`_

`movement_validation <https://github.com/openworm/movement_validation>`_
A test pipeline that allows us to run a behavioural phenotyping of our virtual worm running the same test statistics the Shafer lab used on their worm data.

`SegWorm <https://github.com/openworm/SegWorm>`_
SegWorm is Matlab code from Dr. Eviatar Yemini built as part of the `WormBehavior database <http://wormbehavior.mrc-lmb.cam.ac.uk/>`_.
Java


Data Collection and Representation
----------------------------------
**OpenWorm Browser**
The OpenWorm Browser enables ready access to a cell-by-cell 3D representation of the nematode C. elegans in a WebGL enabled browser. Checkout the source code and find out more on the github repository. We also ported this project to an iOS app to support the project.

*Associated Milestones*
None

*Associated Repositories*
`wormbrowser <https://github.com/openworm/wormbrowser>`_
The Worm Browser -- a 3D browser of the cellular anatomy of the c. elegans 
Objective-C

`openwormbrowser-ios <https://github.com/openworm/openwormbrowser-ios>`_
OpenWorm Browser for iOS, based on the open-3d-viewer, which was based on Google Body Browser
C++


**NeuroML Connectome**
Our computational strategy to accomplish this involves first reusing the *C. elegans* connectome and the 3D anatomical map of the *C. elegans* nervous system and body plan. We have used the NeuroML standard (Gleeson et al., 2010) to describe the 3D anatomical map of the c. elegans nervous system. This has been done by discretizing each neuron into multiple compartments, while preserving its three-dimensional position and structure. We have then defined the connections between the NeuroML neurons using the c. elegans connectome. Because NeuroML has a well-defined mapping into a system of Hodgkin-Huxley equations, it is currently possible to import the "spatial connectome" into the NEURON simulator (Hines & Carnevale 1997) to perform in silico experiments.

*Associated Milestones*
`Updated NeuroML connectome model <https://github.com/openworm/OpenWorm/issues?milestone=15&state=open>`_
The `NeuroML connectome model <https://github.com/openworm/CElegansNeuroML>`_ requires a number of updates before it can be used for multicompartmental simulations. Padraig Gleeson will take the lead on this.

*Associated Repositories*
`CElegansNeuroML <https://github.com/openworm/CElegansNeuroML>`_
NeuroML based *C. elegans model*, contained in a neuroConstruct project
Java

`Blender2NeuroML <https://github.com/openworm/Blender2NeuroML>`_
Conversion script to bring neuron models drawn in Blender into NeuroML format
Python

`NEURONSimData <https://github.com/openworm/NEURONSimData>`_

Graphing voltage data from NEURON sims of C. elegans conectome

`muscle_model <https://github.com/openworm/muscle_model>`_
Model of c.elegans muscle in NEURON
XSLT

Muscle Cell Integration
Optimization - Pyramidal

These two algorithms, Hodgkin-Huxley and SPH, require parameters to be set in order for them to function properly, and therefore create some "known unknows" or "free parameters" we must define in order for the algorithm to function at all. For Hodgkin-Huxley we must define the ion channel species and set their conductance parameters. For SPH, we must define mass and the forces that one set of particles exert on another, which in turn means defining the mass of muscles and how much they pull. The conventional wisdom on modeling is to minimize the number of free parameters as much as possible, but we know there will be a vast parameter space associated with the model.

To deal with the space of free parameters, two strategies are employed. First, by using parameters that are based on actual physical processes, many different means can be used to provide sensible estimates. For example, we can estimate the volume and mass of a muscle cell based on figures that have been created in the scientific literature that show its basic dimensions, and some educated guesses about the weight of muscle tissue. Secondly, to go beyond educated estimates into more detailed measurements, we can employ model optimization techniques. Briefly stated, these computational techniques enable a rational way to generate multiple models with differing parameters and choose those sets of parameters that best pass a series of tests. For example, the conductances of motor neurons can be set by what keeps the activity those neurons within the boundaries of an appropriate dynamic range, given calcium trace recordings data of those neurons as constraints.

Electrophysiology / Mechanics Integration
.. [NEEDS A DESCRIPTION]



.. **NEEDS A TOP LEVEL NAME TO DESCRIBE ELEMENTS BELOW**
.. Cell and neuron list
.. [NEED DESCRIPTION]

.. Neuropeptide and ion channel database
.. [NEED DESCRIPTION]

.. Worm movies repository
.. [NEED DESCRIPTION]

.. Synapse position database
.. [NEED DESCRIPTION]

.. Data visualization
.. [NEED DESCRIPTION]

*Associated Milestones*
None

*Associated Repositories*
`data-viz <https://github.com/openworm/data-viz>`_
Repository for scripts and other code items to create web-based visualizations of data in the project
Python



Community Outreach
------------------
.. [NEED DESCRIPTION]

*Associated Milestones*
None

*Associated Repositories*
`org.openworm.website <https://github.com/openworm/org.openworm.website>`_
OpenWorm Website 
Python

`OpenWorm <https://github.com/openworm/OpenWorm>`_
Project Home repo for OpenWorm Wiki and Project-wide issues 
Matlab

`openworm_docs <https://github.com/openworm/openworm_docs>`_
Documentation for OpenWorm

