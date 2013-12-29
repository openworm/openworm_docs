.. _geppetto-project:

Geppetto Simulation Engine
==========================

.. contents::

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


Previous accomplishments
------------------------

* Past releases of Geppetto

Current roadmap
--------------

`STORY: Worm wiggling in the browser 
<https://github.com/openworm/OpenWorm/issues?milestone=21&state=open>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a user, I want to see the proof of concept sibernetic worm in my web browser so 
that anyone around the world can play with it.

Practically, this means porting the proof of concept scene into Geppetto.

`STORY: Interactive worm wiggling in browser 
<https://github.com/openworm/OpenWorm/issues?milestone=23&state=open>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a user, I want to be able to see a visualization of the proof of concept 
worm wiggling in my web browser and be able to perturb it in a manner that 
causes the wiggling to change in a realistic manner.

This milestone suggests interactivity via Geppetto. The kind of perturbation is 
not defined yet-- ideally we should aim for the simplest kind we can think of that 
gives the user an interface to make modifications.

Issues list
-----------

All issues related to the 
`Geppetto codebase <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=geppetto&page=1&sort=comments&state=open>`_, can be found on GitHub

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

