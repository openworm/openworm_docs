************************
Using OpenWorm Resources
************************


Explanations of the current code that has been produced, how to run it, how to use it

https://docs.google.com/a/openworm.org/presentation/d/1x0CPE74XNnISt9BVkyX3jYitvIq9j5QbamRWYrvp5fs/edit#slide=id.i35

https://drive.google.com/a/openworm.org/?tab=oo#folders/0B-GW0T4RUrQ6MTU0N2NmZmMtODAxOC00NDRlLWE3MmMtZDhjMGU4NjNhOTdl

CyberElegans
------------

When we first started, our team in Novosibirsk had produced an awesome
prototype of a neuromechanical c. elegans model which they called
'CyberElegans'. We recently published `an
article <http://iospress.metapress.com/content/p61284485326g608/?p=5e3b5e96ad274eb5af0001971360de3e&pi=4>`__
about it. If you watch `the movie that goes along with the
prototype <http://www.youtube.com/watch?v=3uV3yTmUlgo>`__, you can see
the basic components of the loop above in action:

|CyberElegans with muscle cells|

Here muscle cells cause the motion of the body of the worm along the
surface of its environment.

|Inside the CyberElegans model|

Inside the worm, motor neurons are responsible for activating the
muscles, which them makes the worms move. The blue portions of the loop
diagram above are those aspects that are covered by the initial
prototype. We are now in the process of both adding in the missing
portions of the loop, as well as making the existing portions more
biologically realistic, and making the software platform they are
operating on more scalable.

You can `download the binary for the CyberElegans <http://g.ua/MKja>`__
(Windows only)

Connectome Browser
------------------

The `Connectome browser <http://goo.gl/XGQPX>`__, created by the team at
the `Open Source Brain <http://opensourcebrain.org>`__, is a way to
explore the NeuroML connectome produced by the project. You can
investigate the current settings of the dynamics of each neuron, and by
clicking "selection mode" you can click on individual neurons to see
their synaptic partners in 3D. This is built from the [[Virtual Worm
Blender files]]

|Connectome browser|

WormBrowser
-----------

Explore the c. elegans in 3D! The
`WormBrowser <http://browser.openworm.org>`__ is an interactive virtual
experience of browsing the C. elegans worm anatomy. This is built from
the [[Virtual Worm Blender files]]

|WormBrowser|

Geppetto Simulation Engine
--------------------------

We have bundled up a version of the Geppetto simulation engine for you
to try on your own. Please follow `these installation
instructions <https://docs.google.com/document/d/1JhJwPUQyxNlZqlWNw_sBY9WPkov76elTkpWVnmwmVMQ/pub>`__
to get it running.

|Neuronal Simulator|

C. elegans NeuroML model in neuroConstruct
------------------------------------------

The NeuroML conversion of the [[Virtual Worm Blender files]] has been
imported into a `neuroConstruct <http://www.neuroConstruct.org>`__
project. [[This page\|Running the C. elegans model in neuroConstruct]]
provides instructions for obtaining the latest version of
neuroConstruct, getting the latest CElegans project and
generating/visualizing the cells and connections.

|CElegans\_nC|

.. |CyberElegans with muscle cells| image:: https://docs.google.com/drawings/d/142NbGecjnWuq6RxWgqREhKOXJ8oDo55wVvBuKQPyKCg/pub?w=430&h=297
.. |Inside the CyberElegans model| image:: https://docs.google.com/drawings/d/1fO_gQI_febpu4iHd1_UDrMNQ_eqvHgJynMqho7UC6gw/pub?w=460&h=327
.. |Connectome browser| image:: https:\/\/docs.google.com\/uc?authuser=0&id=0B_t3mQaA-HaMek5wb0trd00wVFU&export=download&revid=0B_t3mQaA-HaMWkIxc214bk12UU9lOWdDRHZKQzc2eWdOWm4wPQ
.. |WormBrowser| image:: https:\/\/docs.google.com\/uc?authuser=0&id=0B_t3mQaA-HaMdkMzaUI3VWVtOG8&export=download&revid=0B_t3mQaA-HaMTXhPY0R0VDlMejd3NVpVTkpRY2diZ01vcXNnPQ
.. |Neuronal Simulator| image:: https:\/\/docs.google.com\/uc?authuser=0&id=0B_t3mQaA-HaMazZld2tKZnRJSk0&export=download&revid=0B_t3mQaA-HaMMHk4Tkp5Q0J4VXZ3akFFRjhZMmxmcU1lVEQ0PQ
.. |CElegans\_nC| image:: https://github.com/openworm/CElegansNeuroML/raw/master/CElegans/images/CElegans_nC.png
