.. _sibernetic-project:

*************************************
NeuroMechanical Modeling - Sibernetic
*************************************

.. contents::

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

Previous accomplishments
=========================

* Physics tests
* Initial worm crawling

Current roadmap
=========================

+--------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| Associated Milestones                                                                                                          | Description                                                                                                           | 
+================================================================================================================================+=======================================================================================================================+
| `STORY: Proof of concept worm wiggling in Sibernetic <https://github.com/openworm/OpenWorm/issues?milestone=20&state=open>`_   | As a scientist or developer, I want to be able to run a program and see a wiggling worm in 3D in front of me.         |
|                                                                                                                                |                                                                                                                       |
|                                                                                                                                |This refers to having a running simulation with the following components:                                              |
|                                                                                                                                |                                                                                                                       |
|                                                                                                                                |Four rows of 'elastic matter muscles' fixed in a 'elastic matter shell'                                                |
|                                                                                                                                |'Elastic matter shell' is filled with liquid that puts outward pressure on shell                                       |
|                                                                                                                                |'Elastic matter muscles' put force on 'elastic matter shell'                                                           |
|                                                                                                                                | Simple sinusoidal input (no neurons) can be applied to 'elastic matter muscles' to produce simple 'wiggling'.         |
|                                                                                                                                | To get rapidly to the end goal, this implementation will be done with some combination of Sibernetic + Configuration  |
|                                                                                                                                |  Generator + Python scripts. A Geppetto implementation will come later.                                               |
|                                                                                                                                |                                                                                                                       |
|                                                                                                                                | This story breaks down the epic to predict behavior from the WormBehavior database                                    |
+--------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| `Electrofluid Paper <https://github.com/openworm/OpenWorm/issues?milestone=17&state=open>`_                                    | We are writing a manuscript focusing on the work we have to implement SPH in the project and apply it to muscle cells |
|                                                                                                                                | and the worm body. @vellamike, @a-palyanov and @skhayrulin are taking the lead on this,                               |
|                                                                                                                                |                                                                                                                       |
|                                                                                                                                | The proposal is to do this after the Sibernetic proof of concept worm wiggling is complete.                           |
|                                                                                                                                |                                                                                                                       |
+--------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+

Associated Repositories
=========================

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| Repository                                                                                                          | Description                                                                                                                      | Language   |
+=====================================================================================================================+==================================================================================================================================+============+
| `Smoothed-Particle-Hydrodynamics <https://github.com/openworm/Smoothed-Particle-Hydrodynamics>`_                    | Known as Sibernetic, this is a C++ implementation of the Smoothed Particle Hydrodynamics algorithm for the OpenWorm project.     | C++        |
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `ConfigurationGenerator <https://github.com/openworm/ConfigurationGenerator>`_                                      | Generation start scene configuration for PCI SPH solver                                                                          | JavaScript |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `CyberElegans <https://github.com/openworm/CyberElegans>`_                                                          | Neuromechanical model of C. Elegans                                                                                              | C++        |   
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+

