.. _data-rep:

**********************************
Data Collection and Representation
**********************************

.. contents::

There is not a single data source for our simulation; in fact one of our unique challenges is coming up with new ways to 
work out how to integrate multiple data sets together. On this page you can read about how different dataset are used in 
the model. 

Being an integrative model, OpenWorm utilizes different datasets, each with different file formats and interfaces to the model. 
There is no master representation of all the data incorporated into the model, instead our aim is to keep the model open to 
be able to cope with different data structures.

Consider the connectomics data.  There are different useful ways to mine this data set. For example, a 
`NetworkX <https://networkx.github.io/>`_ representation 
of the connectome as a complex graph enables questions to be asked about first and second nearest neighbors of a given neuron. 
In contrast, an `RDF <http://www.w3.org/RDF/>`_ semantic graph representation is useful for reading and writing annotations about multiple aspects of a 
neuron, such as what papers have been written about it, multiple different properties it may have such as ion channels and 
neurotransmitter receptors and so on. A `NeuroML <http://www.neuroml.org/>`_ representation is useful for answering questions about model morphology and 
simulation parameters. Lastly, a `Blender <http://www.blender.org/>`_ representation is a full 3D shape definition that can be used for calculations in 
3D space. 

Using these different representations separately leads to ad hoc scripting for for each representation. This presents a 
challenge for data integration and consolidation of information. An ongoing development of the project is to create a 
unified data access layer (see PyOpenWorm below), which enables different representations to become encapsulated into an 
abstract view. This allows the user 
to work with objects related to the biological reality of the worm. This has the advantage that the user can forget about 
which representation is being used under the hood.

Here is a list of some of the data sets that we have used so far:

* `The Virtual Worm (3D atlas of C. elegans anatomy) <http://caltech.wormbase.org/virtualworm/>`_
* `The c. elegans connectome (wiring diagram of neurons) <http://www.wormatlas.org/neuronalwiring.html>`_
* `Cell list of c. elegans <https://docs.google.com/spreadsheet/pub?key=0Avt3mQaA-HaMdGFnQldkWm9oUmQ3YjZ1LXJ4OHFnR0E&output=html>`_
* `Ion channels used by c. elegans <https://docs.google.com/spreadsheet/pub?key=0Avt3mQaA-HaMdEd6S0dfVnE4blhaY2ZIWDBvZFNjT0E&output=html>`_
* `Database of Worm behavioral phenotypes <http://www.ncbi.nlm.nih.gov/pubmed/23852451>`_

Currently our work on data collection and representation is divided among four subprojects:

* NeuroML Connectome
* Data Visualization
* PyOpenWorm Unified Data Access Layer
* Muscle cell integration

Below you can find information about each subproject, see the project’s current roadmap and access the associated 
data repositories

A lot of data about *c. elegans* is integrated into the model.  
In this project, we work on what forms we should put these data in to best leverage them
for building the model.  

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
provides a framework for `multi-compartmental modeling <https://en.wikipedia.org/wiki/Multi-compartment_model>`_ of the 
c. elegans nervous system.  We are continuing to refine this to include more and more information that is known about the
anatomy and dynamics of the nervous system in order to reach ever-improving biological realism.


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


Data Visualization
=======================

With the ever increasing capacity to collect data about biological system, the new challenge is to understand what 
these dataset tell us about the system. The computational neuroscience community is developing a range of methods 
to extract knowledge from these datasets. One approach the accomplish this task is to represent the data visually. 
Our team has already produced the `OpenWorm browser for web <http://browser.openworm.org>`_ and `iOS <https://itunes.apple.com/us/app/openworm-browser/id595581306?mt=8>`_, 
which makes it easy to visually study the anatomy of the the worm. 

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



PyOpenWorm Unified Data Access Layer
====================================

We have consolidated a lot of data about the worm into a python library that creates a unified data access layer 
`called PyOpenWorm <https://github.com/openworm/pyopenworm>`_.  Documentation for PyOpenWorm 
`is available online <http://pyopenworm.readthedocs.org/en/latest/intro.html>_`.

Previous accomplishments
------------------------

* Building the original `OpenWorm database <https://groups.google.com/d/msg/openworm-discuss/2V5kF5na5fw/GnxZMgWYF7wJ>`_
* `Initial release of PyOpenWorm <https://github.com/openworm/PyOpenWorm/releases/tag/0.0.1-alpha>`_

Current roadmap
--------------

* Finalize `remaining issues for PyOpenWorm version alpha0.5 <https://github.com/openworm/PyOpenWorm/labels/alpha0.5>`_
* `Document Neuron Ion Channels: Types <https://github.com/openworm/OpenWorm/issues/31>`_
* `Document Ion channels: Research Claims <https://github.com/openworm/OpenWorm/issues/32>`_


Issues list
------------

All issues related to `working with data <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=data+parsing&page=1&sort=comments&state=open>`_, 
and `doing research <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=research&page=1&sort=comments&state=open>`_ can be found on GitHub.
Additionally, the PyOpenWorm project has `its own issues list <https://github.com/openworm/PyOpenWorm/issues?q=is%3Aopen+is%3Aissue>`_ and 
`a waffle board <https://waffle.io/openworm/PyOpenWorm>`_ for easier observation of what is going on.

Associated Repositories
-----------------------

+-------------------------------------------------------------+----------------------------------------------------------------------------------+-------------+
| Repository                                                  | Description                                                                      | Language    |
+=============================================================+==================================================================================+=============+
| `PyOpenWorm <https://github.com/openworm/pyopenworm>`_      | Unified, simple data access library for data & facts about c. elegans anatomy    | Python      |   
+-------------------------------------------------------------+----------------------------------------------------------------------------------+-------------+


.. _data-rep-muscle:

Muscle Cell Integration
=======================

Because the muscle cell is driven both by an electrical model and a mechanical model, it
is a focus of integration between different algorithms.  Previously we have created a 
separate `repository for the muscle model <https://github.com/openworm/muscle_model>`_ that is an adaptation
of the work by `Boyle & Cohen, 2008 <http://www.comp.leeds.ac.uk/netta/CV/papers/BC08b.pdf>`_.
We have an `approximately working version <http://www.opensourcebrain.org/projects/muscle_model/wiki>`_ implemented
in NEURON and are porting this to be fully NeuroML2 compliant.

The electrical side of the model is currently the focus of the OpenWorm Muscle / Neuron Team.  You can connect with the team `on real time chat <https://gitter.im/openworm/muscle_model>`_.

To catch up with recent developments of this team, please see the following resources:

* Meeting #1 (`YouTube Video <https://www.youtube.com/watch?v=6AhKE2Vg_Uw>`_) (`Agenda <https://docs.google.com/document/d/1BByFfABx91Ao-qKFYXAP0wQONlhdDy7MtSu8G0QxUes/edit>`_)
* Meeting #2 (`YouTube Video <https://www.youtube.com/watch?v=HfGAJYwNt3c>`_) (`Agenda <https://docs.google.com/document/d/1gUBwNjK4OEYd22Pdjt5vcm0-L6cbIHEU6k51AnOcL24/edit?usp=drive_web>`_)
* Synapse journal club (`YouTube Video <https://www.youtube.com/watch?v=697Irn0J_54>`_) (`Slides <https://docs.google.com/presentation/d/1uMtXJNEXzzoPw45HG6sztqiiPDUn2jcUpHj7oiHxu38/edit?usp=sharing>`_)
* Meeting #3 (`YouTube Video <https://www.youtube.com/watch?v=3KApBmFa6WY>`_) (`Agenda <https://docs.google.com/document/d/1JAH4Hs_J0tYbcEuxOMQ0fl2NPf6H6Z7kbe72lAi7SdA/edit>`_)

Some additional background materials that will help explain neuroscience concepts relevant to to this in two minutes each are below:

* `The neuron <https://www.youtube.com/watch?v=6qS83wD29PY>`_
* `Membrane potential <https://www.youtube.com/watch?v=tIzF2tWy6KI>`_
* `Synaptic transmission <https://www.youtube.com/watch?v=WhowH0kb7n0>`_
* `Receptors and ligands <https://www.youtube.com/watch?v=NXOXZ-kaSVI>`_

Current roadmap
---------------

* `Create unit test on the full muscle model that reproduces Figure 1A from Liu, Hollopeter, & Jorgensen 2009 <https://github.com/openworm/muscle_model/issues/31>`_
* `Create unit test that verifies correct I/V curve for ca_boyle NML2 channel <https://github.com/openworm/muscle_model/issues/30>`_
* `Update optimization.py to run with neurotune instead of optimalneuron <https://github.com/openworm/muscle_model/issues/18>`_

Issues list
------------

All issues related to `working with the muscle model <https://github.com/openworm/muscle_model/issues>`_, 
can be found on GitHub.

Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                      | Language    |
+=====================================================================================================================+==================================================================================================================================+=============+
| `muscle_model <https://github.com/openworm/muscle_model>`_                                                          | model of c.elegans muscle in NEURON / Python                                                                                     | Python      |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+-------------+


