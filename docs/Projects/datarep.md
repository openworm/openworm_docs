Data Collection and Representation
==================================

There is not a single data source for our simulation; in fact one of our unique challenges is coming up with new ways to work out how to integrate multiple data sets together. On this page you can read about how different dataset are used in the model.

Being an integrative model, OpenWorm utilizes different datasets, each with different file formats and interfaces to the model. There is no master representation of all the data incorporated into the model, instead our aim is to keep the model open to be able to cope with different data structures.

Consider the connectomics data. There are different useful ways to mine this data set. For example, a [NetworkX](https://networkx.github.io/) representation of the connectome as a complex graph enables questions to be asked about first and second nearest neighbors of a given neuron. In contrast, an [RDF](http://www.w3.org/RDF/) semantic graph representation is useful for reading and writing annotations about multiple aspects of a neuron, such as what papers have been written about it, multiple different properties it may have such as ion channels and neurotransmitter receptors and so on. A [NeuroML](http://www.neuroml.org/) representation is useful for answering questions about model morphology and simulation parameters. Lastly, a [Blender](http://www.blender.org/) representation is a full 3D shape definition that can be used for calculations in 3D space.

Using these different representations separately leads to ad hoc scripting for for each representation. This presents a challenge for data integration and consolidation of information. An ongoing development of the project is to create a unified data access layer (see PyOpenWorm below), which enables different representations to become encapsulated into an abstract view. This allows the user to work with objects related to the biological reality of the worm. This has the advantage that the user can forget about which representation is being used under the hood.

Here is a list of some of the data sets that we have used so far:

-   [The Virtual Worm (3D atlas of C. elegans anatomy)](http://caltech.wormbase.org/virtualworm/)
-   [The c. elegans connectome (wiring diagram of neurons)](http://www.wormatlas.org/neuronalwiring.html)
-   [Cell list of c. elegans](https://docs.google.com/spreadsheet/pub?key=0Avt3mQaA-HaMdGFnQldkWm9oUmQ3YjZ1LXJ4OHFnR0E&output=html)
-   [Ion channels used by c. elegans](https://docs.google.com/spreadsheet/pub?key=0Avt3mQaA-HaMdEd6S0dfVnE4blhaY2ZIWDBvZFNjT0E&output=html)
-   [Database of Worm behavioral phenotypes](http://www.ncbi.nlm.nih.gov/pubmed/23852451)

Currently our work on data collection and representation is divided among four subprojects:

-   NeuroML Connectome
-   Data Visualization
-   PyOpenWorm Unified Data Access Layer
-   Muscle cell integration

Below you can find information about each subproject, see the project’s current roadmap and access the associated data repositories

A lot of data about *c. elegans* is integrated into the model. In this project, we work on what forms we should put these data in to best leverage them for building the model.

NeuroML Connectome
------------------

Our computational strategy to accomplish this involves first reusing the *C. elegans* connectome and the 3D anatomical map of the *C. elegans* nervous system and body plan. We have used the NeuroML standard (Gleeson et al., 2010) to describe the 3D anatomical map of the c. elegans nervous system. This has been done by discretizing each neuron into multiple compartments, while preserving its three-dimensional position and structure. We have then defined the connections between the NeuroML neurons using the c. elegans connectome. Because NeuroML has a well-defined mapping into a system of Hodgkin-Huxley equations, it is currently possible to import the "spatial connectome" into the NEURON simulator (Hines & Carnevale 1997) to perform in silico experiments.

### Previous accomplishments

-   Building the C Elegans NeuroML file

### Current roadmap

###[Updated NeuroML connectome model](https://github.com/openworm/OpenWorm/issues?milestone=15&state=open)

The [NeuroML connectome model](https://github.com/openworm/CElegansNeuroML) provides a framework for [multi-compartmental modeling](https://en.wikipedia.org/wiki/Multi-compartment_model) of the c. elegans nervous system. We are continuing to refine this to include more and more information that is known about the anatomy and dynamics of the nervous system in order to reach ever-improving biological realism.

-   [Create sample NeuroML connectome output](https://github.com/openworm/OpenWorm/issues/114)
-   [Remove Glutamate\_GJ etc in neuroConstruct project](https://github.com/openworm/OpenWorm/issues/50)
-   [Create or reuse a NeuroML description of c. elegans motor neuron synapses](https://github.com/openworm/OpenWorm/issues/124)

### Issues list

All issues related to [working with data](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=data+parsing&page=1&sort=comments&state=open), and [doing research](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=research&page=1&sort=comments&state=open) can be found on GitHub.

### Associated Repositories


Repository | Description | Language
------------ | ------------- | ------------
<a href="https://github.com/openworm/CElegansNeuroML">CElegansNeuroML</a> | NeuroML based C elegans model, contained in a neuroConstruct project  | Java
<a href="https://github.com/openworm/Blender2NeuroML">Blender2NeuroML</a> | Conversion script to bring neuron models drawn in Blender into NeuroML format  | Python
<a href="https://github.com/openworm/NEURONSimData">NEURONSimData</a> | Graphing voltage data from NEURON sims of C. elegans conectome | Python
<a href="https://github.com/openworm/PyOpenWorm">PyOpenWorm</a> | Metadata extraction, translation, storage, and sharing | Python



Data Visualization
------------------

With the ever increasing capacity to collect data about biological system, the new challenge is to understand what these dataset tell us about the system. The computational neuroscience community is developing a range of methods to extract knowledge from these datasets. One approach the accomplish this task is to represent the data visually. Our team has already produced the [OpenWorm browser for web](http://browser.openworm.org) and [iOS](https://itunes.apple.com/us/app/openworm-browser/id595581306?mt=8), which makes it easy to visually study the anatomy of the the worm.

### Previous accomplishments

-   OpenWorm browser
-   OpenWorm browser iOS
-   Hive Plots visualizations of connectome

### Current roadmap

-   [Create a D3 implementation of the C. elegans connectome HivePlot](https://github.com/openworm/OpenWorm/issues/89)

### Issues list

All issues related to [working with data](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=data+parsing&page=1&sort=comments&state=open), and [doing research](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=research&page=1&sort=comments&state=open) can be found on GitHub.

### Associated Repositories

Repository | Description | Language
------------ | ------------- | ------------
<a href="https://github.com/openworm/wormbrowser">wormbrowser</a> | The Worm Browser -- a 3D browser of the cellular anatomy of the c. elegans | Javascript
<a href="https://github.com/openworm/openwormbrowser-ios">openwormbrowser-ios</a> | OpenWorm Browser for iOS, based on the open-3d-viewer, which was based on Google Body Browser | Objective-C
<a href="https://github.com/openworm/data-viz">data-viz</a> | Repository for scripts and other code items to create web-based visualizations of data in the project | Python
