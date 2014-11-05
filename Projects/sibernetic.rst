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

Available Documentation
=========================

* :ref:`How to run <sibernetic-how-to-run>`
* :ref:`PCI-SPH algorithm <sibernetic-algorithm>`
* :ref:`Main data structures <sibernetic-data-structures>`

Current roadmap
=========================                                  

`Electrofluid Paper <https://github.com/openworm/OpenWorm/issues?milestone=17&state=open>`_ 
-------------------------------------------------------------------------------------------

We are writing a manuscript focusing on the work we have to implement SPH in the project and apply it to muscle cells 
and the worm body. @vellamike, @a-palyanov and @skhayrulin are taking the lead on this,

The proposal is to do this after the Sibernetic proof of concept worm wiggling is complete. 

Issues list
===========

All issues related to the 
`Sibernetic code base <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=sibernetic&page=1&sort=comments&state=open>`_ 
can be found on GitHub.

Associated Repositories
=========================

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| Repository                                                                                                          | Description                                                                                                                      | Language   |
+=====================================================================================================================+==================================================================================================================================+============+
| `Smoothed-Particle-Hydrodynamics <https://github.com/openworm/Smoothed-Particle-Hydrodynamics>`_                    | The Sibernetic code base containing the 2014 version of the worm body model,                                                     | C++        |
|                                                                                                                     |  a C++ implementation of the Smoothed Particle Hydrodynamics algorithm customised for the OpenWorm project.                      |            |
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `ConfigurationGenerator <https://github.com/openworm/ConfigurationGenerator>`_                                      | Generation start scene configuration for PCI SPH solver                                                                          | JavaScript |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `CyberElegans <https://github.com/openworm/CyberElegans>`_                                                          | Circa 2010 Neuromechanical model of C. Elegans                                                                                   | C++        |   
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+

