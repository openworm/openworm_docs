************************
Introduction to OpenWorm
************************

* How to Participate
* Project Areas
* Detailed Roadmap
  - Neuromechanical Modeling
  - Geppetto Simulation Engine
  - Optimization Engine & Model Validation
  - Data Collection and Representation
  - Community Outreach


How to Participate
==================



Project Areas
=============
**NeuroMechanical Modeling**
While our ultimate goal is to simulate every cell in the c. Elegans, we are starting out by building a model of its body, its nervous system, and its environment.

To get a quick idea of what this looks like, check out the CyberElegans prototype. In this movie you can see a simulated 3D c. elegans being activated in an environment. Its muscles are located around the outside of its body, and as they turn red, they are exerting forces on the body that cause the bending to happen. In turn, the activity of the muscles are being driven by the activity of neurons within the body.

**Geppetto Simulation Engine**
We are engineering Geppetto, a Java OSGi open-source modular platform to enable multi-scale and multi-algorithm interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers out-of-the-box visualization of simulated models right in the browser. You can read about architectural concepts and learn more about the different plug-in bundles we are working on.

**Optimization Engine & Model Validation**
The Optimization Engine uses optimization techniques like genetic algorithms to help fill gaps in our knowledge of the electrophysiology of C. elegans muscle cells and neurons. Check out the code on the github repository.

**Data Collection and Representation**

**Community Outreach**





Detailed Roadmap
================
NeuroMechanical Modeling
------------------------

**Fluid Mechanics Simulator**
We have implemented an algorithm called Smoothed Particle Hydrodynamics (SPH) to simulate the body of the worm and its environment using GPUs. This algorithm has been initially worked out in C++ (with OpenGL visualization), then ported to Java as a bundle for Geppetto, our simulation engine.

*Associated Milestones*
.. _STORY: Proof of concept worm wiggling in Sibernetic: https://github.com/openworm/OpenWorm/issues?milestone=20&state=open
As a scientist or developer, I want to be able to run a program and see a wiggling worm in 3D in front of me.

This refers to having a running simulation with the following components:

Four rows of 'elastic matter muscles' fixed in a 'elastic matter shell'
'Elastic matter shell' is filled with liquid that puts outward pressure on shell
'Elastic matter muscles' put force on 'elastic matter shell'
Simple sinusoidal input (no neurons) can be applied to 'elastic matter muscles' to produce simple 'wiggling'.
To get rapidly to the end goal, this implementation will be done with some combination of Sibernetic + Configuration Generator + Python scripts. A Geppetto implementation will come later.

This story breaks down the epic to predict behavior from the WormBehavior database

.. _Electrofluid Paper: https://github.com/openworm/OpenWorm/issues?milestone=17&state=open
We are writing a manuscript focusing on the work we have to implement SPH in the project and apply it to muscle cells and the worm body. @vellamike, @a-palyanov and @skhayrulin are taking the lead on this,

The proposal is to do this after the Sibernetic proof of concept worm wiggling is complete.

*Associated Repositories*
.. _ConfigurationGenerator: https://github.com/openworm/ConfigurationGenerator
Generation start scene configuration for PCI SPH solver
JavaScript

.. _CyberElegans: https://github.com/openworm/CyberElegans
Neuromechanical model of C. Elegans

.. _Smoothed-Particle-Hydrodynamics: https://github.com/openworm/Smoothed-Particle-Hydrodynamics
Known as Sibernetic, this is a C++ implementation of the Smoothed Particle Hydrodynamics algorithm for the OpenWorm project.
Java


NeuroMechanical Modeling
------------------------

**Fluid Mechanics Simulator**





.. _STORY: Muscle Cell model output closely matches that of real data: https://github.com/openworm/OpenWorm/issues?milestone=13&state=open
We will show that we have built a model of C. elegans muscle cell that matches data recorded from the nematode muscle cell. In part, we will use techniques of model optimization to fill in gaps in the model parameter space (deduce unmeasured parameters). The main technical challenge is tuning muscle cell passive properties and building a larger data set (more cell recordings).

.. _STORY: Build a test suite for the simulation from WormBehavior database: https://github.com/openworm/OpenWorm/issues?milestone=19&state=open
As a scientist or developer, I want to be able to run a test suite against the simulation that will show me how close the model is to real data.

In order for a model to demonstrate scientific value, it has to make falsifiable predictions. The target data to be able to predict will be drawn from the WormBehavior database. This milestone will involve working with these data, creating a code base that can compare movement output from the simulation with ground truth from the database and produce an accuracy score.

This story breaks down the epic to predict behavior from the WormBehavior database



.. _STORY: Worm wiggling in the browser: https://github.com/openworm/OpenWorm/issues?milestone=21&state=open
As a user, I want to see the proof of concept sibernetic worm in my web browser so that anyone around the world can play with it.

Practically, this means porting the proof of concept scene into Geppetto.

.. _STORY: Interactive worm wiggling in browser: https://github.com/openworm/OpenWorm/issues?milestone=23&state=open
As a user, I want to be able to see a visualization of the proof of concept worm wiggling in my web browser and be able to perturb it in a manner that causes the wiggling to change in a realistic manner.

This milestone suggests interactivity via Geppetto. The kind of perturbation is not defined yet-- ideally we should aim for the simplest kind we can think of that gives the user an interface to make modifications.



.. _EPIC: Correctly predict 80% of wild type (N2) behavior in WormBehavior database: https://github.com/openworm/OpenWorm/issues?milestone=22&state=open
This epic is to have a simulation that can demonstrate it can predict (and therefore reproduce) 80% of the data collected about the N2 worm in the WormBehavior database. This means building a training set and a test set that are kept separate from each other, using the training set to tune up the model, then generating predictions, and comparing them against the test set, and doing some cross-validation).

This epic focuses on an output of simulation performance rather than the means of implementation, so any way to achieve this epic is welcome.


.. _Updated NeuroML connectome model ..https://github.com/openworm/OpenWorm/issues?milestone=15&state=open
The NeuroML connectome model at https://github.com/openworm/CElegansNeuroML requires a number of updates before it can be used for multicompartmental simulations. Padraig Gleeson will take the lead on this.

For the latest status on the milestones, visit: https://github.com/openworm/OpenWorm/issues/milestones





