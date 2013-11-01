************************
Introduction to OpenWorm
************************

* Project areas
* Overview of the roadmap
* \'You are here'\ in the roadmap
* GitHub Issues
* Description of all the repositories and how they map to the project areas
* Explanations of the current code that has been produced, how to run it, how to use it
* Breakdowns of current issues based on potential volunteers' incoming skills

Project Areas
=============
http://www.openworm.org/about.html
https://github.com/openworm/OpenWorm/wiki/Project-overview
https://github.com/openworm/OpenWorm/issues/milestones

**NeuroML Connectome**
We have converted all 302 neurons described in the WormBase Virtual Worm Blender files into multi-compartmental neuronal models described in NeuroML format. We are currently building descriptions of the synaptic junctions and the ion channels for each cell. You can explore the github repository.

**Geppetto Simulation Engine**
We are engineering Geppetto, a Java OSGi open-source modular platform to enable multi-scale and multi-algorithm interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers out-of-the-box visualization of simulated models right in the browser. You can read about architectural concepts and learn more about the different plug-in bundles we are working on.

**OpenWorm Browser**
The OpenWorm Browser enables ready access to a cell-by-cell 3D representation of the nematode C. elegans in a WebGL enabled browser. Checkout the source code and find out more on the github repository. We also ported this project to an iOS app to support the project.

**Fluid Mechanics Simulator**
We have implemented an algorithm called Smoothed Particle Hydrodynamics (SPH) to simulate the body of the worm and its environment using GPUs. This algorithm has been initiall worked out in C++ (with OpenGL visualization), then ported to Java as a bundle for Geppetto, our simulation engine.

**Optimization Engine**
The Optimization Engine uses optimization techniques like genetic algorithms to help fill gaps in our knowledge of the electrophysiology of C. elegans muscle cells and neurons. Check out the code on the github repository.


Overview of the Roadmap
=======================
https://github.com/openworm/OpenWorm/issues/milestones

.. _STORY: Muscle Cell model output closely matches that of real data: https://github.com/openworm/OpenWorm/issues?milestone=13&state=open
We will show that we have built a model of C. elegans muscle cell that matches data recorded from the nematode muscle cell. In part, we will use techniques of model optimization to fill in gaps in the model parameter space (deduce unmeasured parameters). The main technical challenge is tuning muscle cell passive properties and building a larger data set (more cell recordings).

.. _STORY: Build a test suite for the simulation from WormBehavior database: https://github.com/openworm/OpenWorm/issues?milestone=19&state=open
As a scientist or developer, I want to be able to run a test suite against the simulation that will show me how close the model is to real data.

In order for a model to demonstrate scientific value, it has to make falsifiable predictions. The target data to be able to predict will be drawn from the WormBehavior database. This milestone will involve working with these data, creating a code base that can compare movement output from the simulation with ground truth from the database and produce an accuracy score.

This story breaks down the epic to predict behavior from the WormBehavior database

.. _STORY: Proof of concept worm wiggling in Sibernetic: https://github.com/openworm/OpenWorm/issues?milestone=20&state=open
As a scientist or developer, I want to be able to run a program and see a wiggling worm in 3D in front of me.

This refers to having a running simulation with the following components:

Four rows of 'elastic matter muscles' fixed in a 'elastic matter shell'
'Elastic matter shell' is filled with liquid that puts outward pressure on shell
'Elastic matter muscles' put force on 'elastic matter shell'
Simple sinusoidal input (no neurons) can be applied to 'elastic matter muscles' to produce simple 'wiggling'.
To get rapidly to the end goal, this implementation will be done with some combination of Sibernetic + Configuration Generator + Python scripts. A Geppetto implementation will come later.

This story breaks down the epic to predict behavior from the WormBehavior database

.. _STORY: Worm wiggling in the browser: https://github.com/openworm/OpenWorm/issues?milestone=21&state=open
As a user, I want to see the proof of concept sibernetic worm in my web browser so that anyone around the world can play with it.

Practically, this means porting the proof of concept scene into Geppetto.

.. _STORY: Interactive worm wiggling in browser: https://github.com/openworm/OpenWorm/issues?milestone=23&state=open
As a user, I want to be able to see a visualization of the proof of concept worm wiggling in my web browser and be able to perturb it in a manner that causes the wiggling to change in a realistic manner.

This milestone suggests interactivity via Geppetto. The kind of perturbation is not defined yet-- ideally we should aim for the simplest kind we can think of that gives the user an interface to make modifications.

.. _Electrofluid Paper: https://github.com/openworm/OpenWorm/issues?milestone=17&state=open
We are writing a manuscript focusing on the work we have to implement SPH in the project and apply it to muscle cells and the worm body. @vellamike, @a-palyanov and @skhayrulin are taking the lead on this,

The proposal is to do this after the Sibernetic proof of concept worm wiggling is complete.

.. _EPIC: Correctly predict 80% of wild type (N2) behavior in WormBehavior database: https://github.com/openworm/OpenWorm/issues?milestone=22&state=open
This epic is to have a simulation that can demonstrate it can predict (and therefore reproduce) 80% of the data collected about the N2 worm in the WormBehavior database. This means building a training set and a test set that are kept separate from each other, using the training set to tune up the model, then generating predictions, and comparing them against the test set, and doing some cross-validation).

This epic focuses on an output of simulation performance rather than the means of implementation, so any way to achieve this epic is welcome.


.. _Updated NeuroML connectome model ..https://github.com/openworm/OpenWorm/issues?milestone=15&state=open
The NeuroML connectome model at https://github.com/openworm/CElegansNeuroML requires a number of updates before it can be used for multicompartmental simulations. Padraig Gleeson will take the lead on this.


 \'You are here'\ in the roadmap
================================



GitHub Issues
=============
To access the repositories for OpenWorm on GitHub, you will first need to create an account if you do not already have one.  Accounts are free and can be set by visiting: https://github.com/
DO THEY HAVE TO BE MEMBERS OF THE OPENWORM GITHUB TO CONTRIBUTE???
They have to be added to the organization to be assigned to issues, add and edit them but not to comment on them.

Once completed, you can log back into GitHub and select OpenWorm from the organization drop down menu to get started. 
https://github.com/organizations/openworm

Opening a new issue on GitHub. 
After logging into GitHub, select the OpenWorm organization and then click on the repository in which the issue is located/relevant to. Click on the Issues tab on the menu to the right.
.. GitHubIssue1a:: http://i.imgur.com/Rh1uvmn.png

Next, click on the New Image button in the upper right corner of the screen.
.. GitHubIssue1b:: http://i.imgur.com/fvEQOJQ.png 

This will open the interface to create a new issue. You will need to add the following information:
* Name or short description of the issue
* Full description of the issue, including images if available
* Assign team members to the issue if appropriate
* Add a milestone if appropriate
* Add labels to categorize the issue

.. GitHubIssue1c:: http://i.imgur.com/ozkZFsh.png 

Finally, click on Submit New Issue.

Repositories
=============
Description of all the repositories and how they map to the project areas
View the full list with active links:
.. https://github.com/openworm 

Gepetto
-------------
org.geppetto.solver.sph
PCI SPH Solver bundle for Geppetto
Python

org.geppetto.simulator.jlems
jLEMS based simulator for Geppetto
Java

org.geppetto.model.neuroml
NeuroML Model Bundle for Geppettoo
Java

org.geppetto.core
Geppetto core bundle
JavaScript

org.geppetto.frontend
Geppetto frontend bundle (Web Application)
Java

org.geppetto.testbackend
Java 

org.geppetto.simulator.sph
SPH Simulator bundle for Geppetto
Java

org.geppetto.simulation
Generic simulation bundle for Geppetto
Python

org.geppetto
Geppetto Main Bundle / packaging
Java

org.geppetto.model.sph
PCI SPH Model Bundle for Geppetto
CSS

org.geppetto.samples
Python

org.geppetto.templatebundle
JavaScript

Models
------
Smoothed-Particle-Hydrodynamics
This is a C++ implementation of the Smoothed Particle Hydrodynamics algorithm for the OpenWorm project.
Java

muscle_model
model of c.elegans muscle in NEURON
XSLT

CElegansNeuroML
NeuroML based C elegans model, contained in a neuroConstruct project
Java

Blender2NeuroML
Conversion script to bring neuron models drawn in Blender into NeuroML format
Python



OpenWorm
--------
org.openworm.website
OpenWorm Website
Python

OpenWorm
Matlab

openworm_docs



Uncategorized
-------------
movement_validation

ConfigurationGenerator
JavaScript

data-viz
Python

SegWorm
Java

wormbrowser
Objective-C

openwormbrowser-ios
C++

HeuristicWorm

CyberElegans



Using the Code
==============
Explanations of the current code that has been produced, how to run it, how to use it
https://docs.google.com/a/openworm.org/presentation/d/1x0CPE74XNnISt9BVkyX3jYitvIq9j5QbamRWYrvp5fs/edit#slide=id.i35
https://drive.google.com/a/openworm.org/?tab=oo#folders/0B-GW0T4RUrQ6MTU0N2NmZmMtODAxOC00NDRlLWE3MmMtZDhjMGU4NjNhOTdl



Current Issues
==============
Do we have a current list of contributors mapped to current issues?
Breakdowns of current issues based on potential volunteers' incoming skills
Using tags for categorizing tasks and issues
