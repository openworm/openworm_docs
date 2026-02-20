Using OpenWorm Resources
========================

This page describes content that has been created by the project for use by the public. Currently we make simulation engines, visualization environments, and data sets available.
Our website [contains an additional list of resources](http://www.openworm.org/science.html) that are useful to biologists in particular.

Simulation engines
------------------

### Geppetto

!!! note "Superseded by DD014"
    Geppetto served OpenWorm well from 2014-2020 but has been superseded by [DD014: Dynamic Visualization Architecture](../design_documents/DD014_Dynamic_Visualization_Architecture.md), which specifies a Python-native Trame viewer. See [Archived Projects](../archived_projects.md#geppetto-web-platform-2014-2020) for context on this transition.

Geppetto is a generic multi-algorithm integration platform written in Java and HTML5 by Cantarelli, Idili, Martinez and Khayrulin whose goal is to enable the world to play with simulations via their web browser, dramatically reducing the barrier to entry.

![image](http://www.geppetto.org/images/cn2.png)

More information on running Geppetto is [available online](http://geppetto.org).

[The project page for Geppetto](../Projects/geppetto.md) has information about the history of its development with OpenWorm.

### Sibernetic

Sibernetic is the code base that currently implements the crawling model using Smoothed Particle Hydrodynamics (SPH). Sibernetic is a C++ / Python code base by Palyanov, Khayrulin and Vella, specified by [DD003: Body Physics Architecture](../design_documents/DD003_Body_Physics_Architecture.md).

![image](http://i.imgur.com/KSWjCaW.jpg)

More information on running Sibernetic is [available online](https://openworm.org/sibernetic/).

[The project page for Sibernetic](../Projects/sibernetic.md) has information about getting involved with its development.

### Connectome Engine and Lego Mindstorms robot

To start getting some practical experience playing with dynamics that come from the connectome, we have simplified it into a project called the 'connectome engine' and integrated its dynamics into a Lego Mindstorms EV3 robot. You can [see a movie of this in action](https://www.youtube.com/watch?v=D8ogHHwqrkI).

![image](http://i.imgur.com/OG7sOAD.jpg)

More information is available at [http://www.connectomeengine.com/]

### CyberElegans (Historical)

!!! note "Historical Prototype"
    CyberElegans was superseded by the current core chain: [DD001](../design_documents/DD001_Neural_Circuit_Architecture.md) (neurons) → [DD002](../design_documents/DD002_Muscle_Model_Architecture.md) (muscles) → [DD003](../design_documents/DD003_Body_Physics_Architecture.md) (body physics). See [Archived Projects](../archived_projects.md#cyberelegans-2010-2014) for context.

When we first started, our team in Novosibirsk had produced an awesome prototype of a neuromechanical c. elegans model which they called 'CyberElegans'. We published [an article](http://iospress.metapress.com/content/p61284485326g608/?p=5e3b5e96ad274eb5af0001971360de3e&pi=4) about it. If you watch [the movie that goes along with the prototype](http://www.youtube.com/watch?v=3uV3yTmUlgo), you can see the basic components of the loop above in action:

![CyberElegans with muscle cells](https://docs.google.com/drawings/d/142NbGecjnWuq6RxWgqREhKOXJ8oDo55wVvBuKQPyKCg/pub?w=430&h=297)

Here muscle cells cause the motion of the body of the worm along the surface of its environment.

![Inside the CyberElegans model](https://docs.google.com/drawings/d/1fO_gQI_febpu4iHd1_UDrMNQ_eqvHgJynMqho7UC6gw/pub?w=460&h=327)

Inside the worm, motor neurons are responsible for activating the muscles, which them makes the worms move. The blue portions of the loop diagram above are those aspects that are covered by the initial prototype. We are now in the process of both adding in the missing portions of the loop, as well as making the existing portions more biologically realistic, and making the software platform they are operating on more scalable.

You can [download the binary for the CyberElegans](https://github.com/openworm/CyberElegans) (Windows only)

This code base is not currently in active development.

Visualization Environments
--------------------------

### WormBrowser

Explore the c. elegans in 3D! The [WormBrowser](http://browser.openworm.org) is an interactive virtual experience of browsing the C. elegans worm anatomy. This is built from the [Virtual Worm Blender files](http://caltech.wormbase.org/virtualworm/)

Source code for [the web version](https://github.com/openworm/wormbrowser) and [an iOS version](https://github.com/openworm/openwormbrowser-ios) are available online. We don't currently have active development happening with either, but if you are interested in helping with the iOS code base, [here's a walkthrough](https://www.youtube.com/watch?v=b5X5fz7pZME) of how to get started with the codebase.

Data sets
---------

### OWMeta

A Python API for accessing information about *C. elegans* is available
at [OWMeta](http://github.com/openworm/OWMeta). This API consolidates
information from our [publicly accessible archive of data sets](https://drive.google.com/#folders/0B_t3mQaA-HaMejlrMmpnR2VjN0U)
that we have come across and adapted on Google Drive. OWMeta is part of the data integration pipeline specified by [DD008](../design_documents/DD008_Data_Integration_Pipeline.md).

### C. elegans NeuroML model in NeuroConstruct

The NeuroML conversion of the [Virtual Worm Blender files](http://caltech.wormbase.org/virtualworm/) has been imported into a [neuroConstruct](http://www.neuroConstruct.org) project. [This page](../running-nc/) provides instructions for obtaining the latest version of neuroConstruct, getting the latest CElegans project and generating/visualizing the cells and connections.

![CElegansnC](https://github.com/openworm/CElegansNeuroML/raw/master/CElegans/images/CElegans_nC.png)

More information about working with the data within it and other data entities can be found on the data representation [project page](../Projects/datarep.md)

---

## Continue Reading

- **[How It Works: Modeling](../modeling.md)** — How these resources fit into the multi-scale simulation architecture
- **[Design Documents](../design_documents/index.md)** — The complete technical roadmap
- **[Projects](../projects.md)** — Overview of all active projects and their governing DDs
- **[Community](../community.md)** — How to get involved
