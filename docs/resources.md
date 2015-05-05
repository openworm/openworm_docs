Using OpenWorm Resources
========================

This page describes content that has been created by the project for use by the public. Currently we make simulation engines, visualization environments, and data sets available.

Simulation engines
------------------

### Sibernetic

Sibernetic is the code base that currently implements the crawling model. Sibernetic is a C++ / Python code base by Palyanov, Khayrulin and Vella that has been created expressly for the purpose of doing research and building the model quickly.

![image](http://i.imgur.com/KSWjCaW.jpg)

More information on running Sibernetic is [available online](http://sibernetic.org).

The project page for Sibernetic \<sibernetic-project\> has information about getting involved with its development.

### Geppetto

Geppetto is a generic multi-algorithm integration platform written in Java and HTML5 by Cantarelli, Idili, Martinez and Khayrulin whose goal is to enable the world to play with simulations via their web browser, dramatically reducing the barrier to entry. We are currently working to port the functionality in Sibernetic into Geppetto, which would transform the experience of seeing the model from looking at a YouTube video to being able to play and interact with the model in 3D.

![image](http://www.geppetto.org/images/cn2.png)

More information on running Geppetto is [available online](http://geppetto.org).

The project page for Geppetto \<geppetto-project\> has information about getting involved in its development with OpenWorm.

### Connectome Engine and Lego Mindstorms robot

To start getting some practical experience playing with dynamics that come from the connectome, we have simplified it into a project called the 'connectome engine' and integrated its dynamics into a Lego Mindstorms EV3 robot. You can [see a movie of this in action](https://www.youtube.com/watch?v=D8ogHHwqrkI).

![image](http://i.imgur.com/OG7sOAD.jpg)

This is currently in the process of being written up.

### CyberElegans

When we first started, our team in Novosibirsk had produced an awesome prototype of a neuromechanical c. elegans model which they called 'CyberElegans'. We recently published [an article](http://iospress.metapress.com/content/p61284485326g608/?p=5e3b5e96ad274eb5af0001971360de3e&pi=4) about it. If you watch [the movie that goes along with the prototype](http://www.youtube.com/watch?v=3uV3yTmUlgo), you can see the basic components of the loop above in action:

![CyberElegans with muscle cells](https://docs.google.com/drawings/d/142NbGecjnWuq6RxWgqREhKOXJ8oDo55wVvBuKQPyKCg/pub?w=430&h=297)

Here muscle cells cause the motion of the body of the worm along the surface of its environment.

![Inside the CyberElegans model](https://docs.google.com/drawings/d/1fO_gQI_febpu4iHd1_UDrMNQ_eqvHgJynMqho7UC6gw/pub?w=460&h=327)

Inside the worm, motor neurons are responsible for activating the muscles, which them makes the worms move. The blue portions of the loop diagram above are those aspects that are covered by the initial prototype. We are now in the process of both adding in the missing portions of the loop, as well as making the existing portions more biologically realistic, and making the software platform they are operating on more scalable.

You can [download the binary for the CyberElegans](http://g.ua/MKja) (Windows only)

This code base is not currently in active development.

Visualization Environments
--------------------------

### Connectome Browser

The [Connectome browser](http://goo.gl/XGQPX), created by the team at the [Open Source Brain](http://opensourcebrain.org), is a way to explore the NeuroML connectome produced by the project. You can investigate the current settings of the dynamics of each neuron, and by clicking "selection mode" you can click on individual neurons to see their synaptic partners in 3D. This is built from the [Virtual Worm Blender files](http://caltech.wormbase.org/virtualworm/)

![Connectome browser](https:\/\/docs.google.com\/uc?authuser=0&id=0B_t3mQaA-HaMek5wb0trd00wVFU&export=download&revid=0B_t3mQaA-HaMWkIxc214bk12UU9lOWdDRHZKQzc2eWdOWm4wPQ)

### WormBrowser (HTML5 and iOS)

Explore the c. elegans in 3D! The [WormBrowser](http://browser.openworm.org) is an interactive virtual experience of browsing the C. elegans worm anatomy. This is built from the [Virtual Worm Blender files](http://caltech.wormbase.org/virtualworm/)

![WormBrowser](https:\/\/docs.google.com\/uc?authuser=0&id=0B_t3mQaA-HaMdkMzaUI3VWVtOG8&export=download&revid=0B_t3mQaA-HaMTXhPY0R0VDlMejd3NVpVTkpRY2diZ01vcXNnPQ)

Source code for [the web version](https://github.com/openworm/wormbrowser) and [an iOS version](https://github.com/openworm/openwormbrowser-ios) are available online. We don't currently have active development happening with either, but if you are interested in helping with the iOS code base, [here's a walkthrough](https://www.youtube.com/watch?v=b5X5fz7pZME) of how to get started with the codebase.

Data sets
---------

OpenWorm Database ----------------

An web version of the OpenWorm database can [be browsed online](http://www.interintelligence.org/openworm/Entities.aspx).

More information about working with the data within it and other data entities can be found on the data representation project page \<data-rep\>.

### C. elegans NeuroML model in neuroConstruct

The NeuroML conversion of the [Virtual Worm Blender files](http://caltech.wormbase.org/virtualworm/) has been imported into a [neuroConstruct](http://www.neuroConstruct.org) project. This page \<running-nc\> provides instructions for obtaining the latest version of neuroConstruct, getting the latest CElegans project and generating/visualizing the cells and connections.

![CElegansnC](https://github.com/openworm/CElegansNeuroML/raw/master/CElegans/images/CElegans_nC.png)

More information about working with the data within it and other data entities can be found on the data representation project page \<data-rep\>.

### OpenWorm Spreadsheet data

We keep a [publicly accessible archive of data sets](https://drive.google.com/#folders/0B_t3mQaA-HaMejlrMmpnR2VjN0U) that we have come across and adapted on Google Drive. We are currently in the process of consolidating these data into the OpenWorm database. More information about working with the data within it and other data entities can be found on the data representation project page \<data-rep\>.
