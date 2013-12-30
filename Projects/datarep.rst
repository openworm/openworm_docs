.. _data-rep:

**********************************
Data Collection and Representation
**********************************

.. contents::


A lot of data about *c. elegans* is integrated into the model.  
In this project, we work on what forms we should put these data in to best leverage them
for building the model.  

Four sub-projects are contained within the data collection and representation project.

* OpenWorm Database
* NeuroML Connectome
* Muscle cell integration
* Data Visualization

OpenWorm Database
==================

We have consolidated a lot of data about the worm 
`into a database <https://github.com/openworm/OpenWorm/tree/master/OpenWorm%20database>`_.

* Database Name:	 mysql_31129_celegans
* Database Server:	my01.winhost.com
* Database User:	openworm
* Database Password:	openworm

`This thread <https://groups.google.com/d/topic/openworm-discuss/2V5kF5na5fw/discussion>`_ 
describes more about the database.

.. Cell and neuron list
.. [NEED DESCRIPTION]

.. Neuropeptide and ion channel database
.. [NEED DESCRIPTION]

.. Worm movies repository
.. [NEED DESCRIPTION]

.. Synapse position database
.. [NEED DESCRIPTION]


Previous accomplishments
------------------------

* Building the OpenWorm database

Current roadmap
--------------

* `Document Neuron Ion Channels: Types <https://github.com/openworm/OpenWorm/issues/31>`_
* `Document Ion channels: Research Claims <https://github.com/openworm/OpenWorm/issues/32>`_


Issues list
------------

All issues related to `working with data <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=data+parsing&page=1&sort=comments&state=open>`_, 
and `doing research <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=research&page=1&sort=comments&state=open>`_ can be found on GitHub.

Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                                                  | Language    |
+=====================================================================================================================+==============================================================================================================================================================+=============+
| `wormbrowser <https://github.com/openworm/wormbrowser>`_                                                            | The Worm Browser -- a 3D browser of the cellular anatomy of the c. elegans                                                                                   | Javascript  |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `openwormbrowser-ios <https://github.com/openworm/openwormbrowser-ios>`_                                            | OpenWorm Browser for iOS, based on the open-3d-viewer, which was based on Google Body Browser                                                                | Objective-C |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `data-viz <https://github.com/openworm/data-viz>`_                                                                  | Repository for scripts and other code items to create web-based visualizations of data in the project                                                        | Python      |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+

.. _data-rep-neuroml:

NeuroML Connectome
==================

Our computational strategy to accomplish this involves first reusing the 
*C. elegans* connectome and the 3D anatomical map of the *C. elegans* 
nervous system and body plan. We have used the NeuroML standard 
(Gleeson et al., 2010) to describe the 3D anatomical map of the c. elegans 
nervous system. This has been done by discretizing each neuron into multiple 
compartments, while preserving its three-dimensional position and structure. 
We have then defined the connections between the NeuroML neurons using the c. elegans 
connectome. Because NeuroML has a well-defined mapping into a system of Hodgkin-Huxley 
equations, it is currently possible to import the "spatial connectome" into the NEURON 
simulator (Hines & Carnevale 1997) to perform in silico experiments.

Previous accomplishments
------------------------

* Building the C Elegans NeuroML file

Current roadmap
---------------

`Updated NeuroML connectome model <https://github.com/openworm/OpenWorm/issues?milestone=15&state=open>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `NeuroML connectome model <https://github.com/openworm/CElegansNeuroML>`_ 
requires a number of updates before it can be used for multicompartmental simulations. 
Padraig Gleeson will take the lead on this.


* `Create sample NeuroML connectome output <https://github.com/openworm/OpenWorm/issues/114>`_
* `Remove Glutamate_GJ etc in neuroConstruct project <https://github.com/openworm/OpenWorm/issues/50>`_
* `Create or reuse a NeuroML description of c. elegans motor neuron synapses <https://github.com/openworm/OpenWorm/issues/124>`_

Issues list
------------

All issues related to `working with data <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=data+parsing&page=1&sort=comments&state=open>`_, 
and `doing research <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=research&page=1&sort=comments&state=open>`_ can be found on GitHub.


Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| Repository                                                                                                          | Description                                                                                                                      | Language   |
+=====================================================================================================================+==================================================================================================================================+============+
| `CElegansNeuroML <https://github.com/openworm/CElegansNeuroML>`_                                                    | NeuroML based C elegans model, contained in a neuroConstruct project                                                             | Java       |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `Blender2NeuroML <https://github.com/openworm/Blender2NeuroML>`_                                                    | Conversion script to bring neuron models drawn in Blender into NeuroML format                                                    | Python     |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `NEURONSimData <https://github.com/openworm/NEURONSimData>`_                                                        | Graphing voltage data from NEURON sims of C. elegans conectome                                                                   | Python     |   
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+

.. _data-rep-muscle:

Muscle Cell Integration
=======================

Because the muscle cell is driven both by an electrical model and a mechanical model, it
is a focus of integration between different algorithms.

Previous accomplishments
------------------------

* Creation of the muscle model repo


Current roadmap
---------------

* `Sync channel descriptions with Muscle model standalone <https://github.com/openworm/OpenWorm/issues/51>`_
* `Find neuroreceptors and synaptic information for MDL08 muscle cell <https://github.com/openworm/OpenWorm/issues/53>`_
* `Secondary mechanical/electrophysiological muscle cell integration <https://github.com/openworm/OpenWorm/issues/9>`_

Issues list
------------

All issues related to `working with data <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=data+parsing&page=1&sort=comments&state=open>`_, 
and `doing research <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=research&page=1&sort=comments&state=open>`_ can be found on GitHub.

Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                      | Language    |
+=====================================================================================================================+==================================================================================================================================+=============+
| `muscle_model <https://github.com/openworm/muscle_model>`_                                                          | model of c.elegans muscle in NEURON / Python                                                                                     | Python      |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+-------------+


Data Visualization
=======================

Visualizations can provide important insights into the complexity of biological models.

Previous accomplishments
------------------------

* OpenWorm browser
* OpenWorm browser iOS
* Hive Plots visualizations of connectome

Current roadmap
--------------

* `Create a D3 implementation of the C. elegans connectome HivePlot <https://github.com/openworm/OpenWorm/issues/89>`_

Issues list
------------

All issues related to `working with data <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=data+parsing&page=1&sort=comments&state=open>`_, 
and `doing research <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=research&page=1&sort=comments&state=open>`_ can be found on GitHub.

Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                      | Language    |
+=====================================================================================================================+==================================================================================================================================+=============+
| `wormbrowser <https://github.com/openworm/wormbrowser>`_                                                            | The Worm Browser -- a 3D browser of the cellular anatomy of the c. elegans                                                       | Javascript  |   
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+-------------+
| `openwormbrowser-ios <https://github.com/openworm/openwormbrowser-ios>`_                                            | OpenWorm Browser for iOS, based on the open-3d-viewer, which was based on Google Body Browser                                    | Objective-C |   
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+-------------+
| `data-viz <https://github.com/openworm/data-viz>`_                                                                  | Repository for scripts and other code items to create web-based visualizations of data in the project                            | Python      |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+-------------+


