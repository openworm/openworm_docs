*****************
OpenWorm Projects
*****************

.. contents:: Table of Contents

NeuroMechanical Modeling - Sibernetic
=====================================

While our ultimate goal is to simulate every cell in the c. Elegans, we are starting out by building a model 
of its body, its nervous system, and its environment.  
`Sibernetic <http://sibernetic.org>`_ is the home of the C++ code base that implements the core of the model.  
We have implemented an algorithm called Smoothed Particle Hydrodynamics (SPH) to simulate the body of the 
worm and its environment using GPUs. This algorithm has been initially worked out in C++ (with OpenGL visualization).


To get a quick idea of what this looks like, check out the 
`latest movie <https://www.youtube.com/watch?v=SaovWiZJUWY>`_. In this movie you can 
see a simulated 3D c. elegans being activated in an environment.  Its muscles are located around the outside 
of its body, and as they turn red, they are exerting forces on the body that cause the bending to happen. 
In turn, the activity of the muscles are being driven by the activity of neurons within the body.

More detailed information is available on the :ref:`Sibenetic project page <sibernetic-project>`.


Geppetto Simulation Engine
==========================

In order to allow the world to play with the model easily, we are engineering `Geppetto <http://geppetto.org>`_, an open-source modular platform to enable multi-scale and multi-algorithm 
interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers 
out-of-the-box visualization of simulated models right in the browser. You can read about architectural 
concepts and learn more about the different plug-in bundles we are working on.

Geppetto, is written in Java and leverages technologies like 
`OSGi <http://www.osgi.org/>`_, 
`Spring Framework <http://www.springsource.org/spring-framework>`_, 
`OpenCL <http://www.khronos.org/opencl/>`_ and 
`Maven <http://maven.apache.org/>`_.

Geppetto's frontend is written using 
`THREE.js <http://mrdoob.github.com/three.js/>`_ and 
`WebGL <http://www.khronos.org/webgl/>`_.
Back-end / front-end communication happens via 
`JSON <http://www.json.org/>`_ messages through 
`WebSocket <http://www.websocket.org/>`_.

The engine runs on on Eclipse Virgo WebServer deployed on an Amazon 
`Elastic Compute Cloud <http://aws.amazon.com/ec2/>`_ Linux instance.

Sound familiar? Like to help? <a href="./contacts.html">Contact us</a>!

Previous accomplishments
------------------------

* Past releases of Geppetto

Current roadmap
--------------

`STORY: Worm wiggling in the browser <https://github.com/openworm/OpenWorm/issues?milestone=21&state=open>`_
As a user, I want to see the proof of concept sibernetic worm in my web browser so that anyone around the world can play with it.

Practically, this means porting the proof of concept scene into Geppetto.

`STORY: Interactive worm wiggling in browser <https://github.com/openworm/OpenWorm/issues?milestone=23&state=open>`_
As a user, I want to be able to see a visualization of the proof of concept worm wiggling in my web browser and be able to perturb it in a manner that causes the wiggling to change in a realistic manner.

This milestone suggests interactivity via Geppetto. The kind of perturbation is not defined yet-- ideally we should aim for the simplest kind we can think of that gives the user an interface to make modifications.

Associated Repositories
----------------------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| Repository                                                                                                          | Description                                | Language   |
+=====================================================================================================================+============================================+============+
| `org.gepetto <https://github.com/openworm/org.geppetto>`_                                                           | Geppetto Main Bundle and packaging         | Java       |
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.solver.sph <https://github.com/openworm/org.geppetto.solver.sph>`_                                    | PCI SPH Solver bundle for Geppetto         | Python     |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.simulator.jlems <https://github.com/openworm/org.geppetto.simulator.jlems>`_                          | jLEMS based simulator for Geppetto         | Java       |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.model.neuroml <https://github.com/openworm/org.geppetto.model.neuroml>`_                              | NeuroML Model Bundle for Geppetto          | Java       |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.core <https://github.com/openworm/org.geppetto.core>`_                                                | Geppetto core bundle                       | Javascript |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.frontend <https://github.com/openworm/org.geppetto.frontend>`_                                        | Geppetto frontend bundle - Web application | Java       |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.testbackend <https://github.com/openworm/org.geppetto.testbackend>`_                                  | Geppetto test backend for Geppetto         | Java       |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.simulator.sph <https://github.com/openworm/org.geppetto.simulator.sph>`_                              | SPH Simulator bundle for Geppetto          | Java       | 
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.simulation <https://github.com/openworm/org.geppetto.simulation>`_                                    | Generic simulation bundle for Geppetto     | Python     |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.model.sph <https://github.com/openworm/org.geppetto.model.sph>`_                                      | PCI SPH Model Bundle for Geppetto          | CSS        |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.samples <https://github.com/openworm/org.geppetto.samples>`_                                          | Sample simulations for Geppetto            | Python     |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.templatebundle <https://github.com/openworm/org.geppetto.templatebundle>`_                            | Template bundle                            | Javascript |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+



Model Validation & Optimization engine
======================================

The Optimization Engine uses optimization techniques like genetic algorithms to help fill gaps in our 
knowledge of the electrophysiology of *C. elegans* muscle cells and neurons. Check out the code on the 
GitHub repository.

Previous accomplishments
------------------------

* Genetic algorithms applied to tuning muscle cell models

Associated Milestones
----------------------

`STORY: Muscle Cell model output closely matches that of real data <https://github.com/openworm/OpenWorm/issues?milestone=13&state=open>`_
We will show that we have built a model of C. elegans muscle cell that matches data recorded from the nematode muscle cell. In part, we will use techniques of model optimization to fill in gaps in the model parameter space (deduce unmeasured parameters). The main technical challenge is tuning muscle cell passive properties and building a larger data set (more cell recordings).

`STORY: Build a test suite for the simulation from WormBehavior database <https://github.com/openworm/OpenWorm/issues?milestone=19&state=open>`_
As a scientist or developer, I want to be able to run a test suite against the simulation that will show me how close the model is to real data.

In order for a model to demonstrate scientific value, it has to make falsifiable predictions. The target data to be able to predict will be drawn from the WormBehavior database. This milestone will involve working with these data, creating a code base that can compare movement output from the simulation with ground truth from the database and produce an accuracy score.

This story breaks down the epic to predict behavior from the WormBehavior database

`EPIC: Correctly predict 80% of wild type (N2) behavior in WormBehavior database <https://github.com/openworm/OpenWorm/issues?milestone=22&state=open>`_
This epic is to have a simulation that can demonstrate it can predict (and therefore reproduce) 80% of the data collected about the N2 worm in the WormBehavior database. This means building a training set and a test set that are kept separate from each other, using the training set to tune up the model, then generating predictions, and comparing them against the test set, and doing some cross-validation).

This epic focuses on an output of simulation performance rather than the means of implementation, so any way to achieve this epic is welcome.


Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                                                  | Language    |
+=====================================================================================================================+==============================================================================================================================================================+=============+
| `movement_validation <https://github.com/openworm/movement_validation>`_                                            | A test pipeline that allows us to run a behavioural phenotyping of our virtual worm running the same test statistics the Shafer lab used on their worm data. | Java        |
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `SegWorm <https://github.com/openworm/SegWorm>`_                                                                    | SegWorm is Matlab code from Dr. Eviatar Yemini built as part of the WormBehavior database (http://wormbehavior.mrc-lmb.cam.ac.uk/)                           | Java        |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `HeuristicWorm <https://github.com/openworm/HeuristicWorm>`_                                                        |                                                                                                                                                              |             |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+


Data Collection and Representation
==================================

* Building the OpenWorm database
* Building the C Elegans NeuroML file

Previous accomplishments
------------------------

* OpenWorm browser
* OpenWorm browser iOS
* Hive Plots visualizations of connectome

Current roadmap
---------------

None

Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                                                  | Language    |
+=====================================================================================================================+==============================================================================================================================================================+=============+
| `wormbrowser <https://github.com/openworm/wormbrowser>`_                                                            | The Worm Browser -- a 3D browser of the cellular anatomy of the c. elegans                                                                                   | Objective-C |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `openwormbrowser-ios <https://github.com/openworm/openwormbrowser-ios>`_                                            | OpenWorm Browser for iOS, based on the open-3d-viewer, which was based on Google Body Browser                                                                | C++         |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+



**NeuroML Connectome**
Our computational strategy to accomplish this involves first reusing the *C. elegans* connectome and the 3D anatomical map of the *C. elegans* nervous system and body plan. We have used the NeuroML standard (Gleeson et al., 2010) to describe the 3D anatomical map of the c. elegans nervous system. This has been done by discretizing each neuron into multiple compartments, while preserving its three-dimensional position and structure. We have then defined the connections between the NeuroML neurons using the c. elegans connectome. Because NeuroML has a well-defined mapping into a system of Hodgkin-Huxley equations, it is currently possible to import the "spatial connectome" into the NEURON simulator (Hines & Carnevale 1997) to perform in silico experiments.

Current roadmap
---------------

`Updated NeuroML connectome model <https://github.com/openworm/OpenWorm/issues?milestone=15&state=open>`_
The `NeuroML connectome model <https://github.com/openworm/CElegansNeuroML>`_ requires a number of updates before it can be used for multicompartmental simulations. Padraig Gleeson will take the lead on this.

Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| Repository                                                                                                          | Description                                                                                                                      | Language   |
+=====================================================================================================================+==================================================================================================================================+============+
| `muscle_model <https://github.com/openworm/muscle_model>`_                                                          | model of c.elegans muscle in NEURON                                                                                              | XSLT       |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `CElegansNeuroML <https://github.com/openworm/CElegansNeuroML>`_                                                    | NeuroML based C elegans model, contained in a neuroConstruct project                                                             | Java       |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `Blender2NeuroML <https://github.com/openworm/Blender2NeuroML>`_                                                    | Conversion script to bring neuron models drawn in Blender into NeuroML format                                                    | Python     |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `NEURONSimData <https://github.com/openworm/NEURONSimData>`_                                                        | Graphing voltage data from NEURON sims of C. elegans conectome                                                                   |            |   
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+


Muscle Cell Integration
Optimization - Pyramidal

These two algorithms, Hodgkin-Huxley and SPH, require parameters to be set in order for them to function properly, and therefore create some "known unknows" or "free parameters" we must define in order for the algorithm to function at all. For Hodgkin-Huxley we must define the ion channel species and set their conductance parameters. For SPH, we must define mass and the forces that one set of particles exert on another, which in turn means defining the mass of muscles and how much they pull. The conventional wisdom on modeling is to minimize the number of free parameters as much as possible, but we know there will be a vast parameter space associated with the model.

To deal with the space of free parameters, two strategies are employed. First, by using parameters that are based on actual physical processes, many different means can be used to provide sensible estimates. For example, we can estimate the volume and mass of a muscle cell based on figures that have been created in the scientific literature that show its basic dimensions, and some educated guesses about the weight of muscle tissue. Secondly, to go beyond educated estimates into more detailed measurements, we can employ model optimization techniques. Briefly stated, these computational techniques enable a rational way to generate multiple models with differing parameters and choose those sets of parameters that best pass a series of tests. For example, the conductances of motor neurons can be set by what keeps the activity those neurons within the boundaries of an appropriate dynamic range, given calcium trace recordings data of those neurons as constraints.

Electrophysiology / Mechanics Integration

[NEEDS A DESCRIPTION]


**NEEDS A TOP LEVEL NAME TO DESCRIBE ELEMENTS BELOW**
Cell and neuron list
[NEED DESCRIPTION]

Neuropeptide and ion channel database
[NEED DESCRIPTION]

Worm movies repository
[NEED DESCRIPTION]

Synapse position database
[NEED DESCRIPTION]

Data visualization
[NEED DESCRIPTION]

Current roadmap
---------------

None



Community Outreach
==================

The effort to build the OpenWorm open science community is always ongoing.  

* Outreach via Social Media
* Documenting our progress
* Journal clubs

Previous accomplishments
------------------------

* Past Journal clubs
* Media attention
* Attracting contributors
* Attracting supporters

Current roadmap
---------------

None

Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| Repository                                                                                                          | Description                                                                                                                      | Language   |
+=====================================================================================================================+==================================================================================================================================+============+
| `org.openworm.website <https://github.com/openworm/org.openworm.website>`_                                          | OpenWorm Website                                                                                                                 | Python     |
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `OpenWorm <https://github.com/openworm/OpenWorm>`_                                                                  | Project Home repo for OpenWorm Wiki and Project-wide issues                                                                      | Matlab     |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `openworm_docs <https://github.com/openworm/openworm_docs>`_                                                        | Documentation for OpenWorm                                                                                                       |            |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+





