## OpenWorm Projects

The OpenWorm project is currently laid out into the major areas shown below:

###  Currently active projects

-   [Neuromechanical modeling with Sibernetic](../Projects/sibernetic/)
-   [c302 multiscale modelling framework](../Projects/c302/)
-   [OpenWorm Browser](../Projects/browser/)
-   [DevoWorm project](../Projects/DevoWorm/)
-   [Docker simulation stack](../Projects/docker/)
-   [Community outreach](../Projects/community-proj/)

###  Projects still maintained, less active

-   [Data collection and representation](../Projects/datarep/)
-   [Movement analysis](../Projects/worm-movement/)
-   [Geppetto Simulation Engine](../Projects/geppetto/)
-   [Optimization engine](../Projects/optimization/)
-   [Muscle-Neuron integration](../Projects/muscle-neuron-integration/)
-   [_C. elegans_ robots](../Projects/c-elegans-robot/)

<div style="width: 640px; height: 480px; margin: 10px; position: relative;"><iframe allowfullscreen frameborder="0" style="width:640px; height:480px" src="https://www.lucidchart.com/documents/embeddedchart/832c1c53-2840-421f-9546-01499bb9c753" id="pf3oYI3Y1wfX"></iframe></div>

**NeuroMechanical Modeling - Sibernetic**

While our ultimate goal is to simulate every cell in _C. elegans_, we are starting out by building a model of its body, its nervous system, and its environment. [Sibernetic](https://openworm.org/sibernetic/) is the home of the C++ code base that implements the core of the model. We have implemented an algorithm called Smoothed Particle Hydrodynamics (SPH) to simulate the body of the worm and its environment using GPUs. This algorithm has been initially worked out in C++ (with OpenGL visualization).

To get a quick idea of what this looks like, check out the [latest movie](https://www.youtube.com/watch?v=SaovWiZJUWY). In this movie you can see a simulated 3D _C. elegans_ being activated in an environment. Its muscles are located around the outside of its body, and as they contract, they exert forces on the surrounding fluid, propelling the body forward via undulutory thrust. In this model, the neural system is not considered and patterns of muscle contraction are explicitly defined.

More detailed information is available on the [Sibernetic project page](../Projects/sibernetic/).

**Geppetto Simulation Engine**

In order to allow the world to play with the model easily, we are engineering [Geppetto](http://geppetto.org), an open-source modular platform to enable multi-scale and multi-algorithm interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers out-of-the-box visualization of simulated models right in the browser. You can read about architectural concepts and learn more about the different plug-in bundles we are working on.

More detailed information is available on the [Geppetto project page](../Projects/geppetto/).

**Movement analysis**

In order to know that we are making meaningful scientific progress, we need to validate the model using information from real worms. The movement validation project is working with an existing database of worm movement to make the critical comparisons.

The Movement Analysis Team maintains the test pipeline so the OpenWorm project can run a behavioural phenotyping of its virtual worm.

More detailed information is available on the [Movement analysis project page](../Projects/worm-movement/).

**Optimization engine**

The Optimization engine uses optimization techniques like genetic algorithms to help fill gaps in our knowledge of the electrophysiology of _C. elegans_ muscle cells and neurons.

More detailed information is available on the [Optimization project page](../Projects/optimization/).

**Data Collection and Representation**

A lot of data about _C. elegans_ is integrated into the model. In this project, we work on what forms we should put these data in to best leverage them for building the model.

More detailed information is available on the [Data representation project page](../Projects/datarep/).

**Community Outreach**

The effort to build the OpenWorm open science community is always ongoing.

More detailed information is available on the [Community project page](../Projects/community-proj/).

**Muscle-Neuron Integration**

The goal of this project is to underpin our muscle and neuron models with biological data. This will be accomplished by creating biologically-realistic ion channel models from experimental data, which will then give rise to neural dynamics.

More detailed information is available on the [Muscle-Neuron integration project page](../Projects/muscle-neuron-integration/).

**_C. elegans_ robot**

The goal of this project is twofold:
1. To build a robot that simulates sensory-motor functions of a _C. elegans_ nematode worm, including foraging for food.
2. To specify parts and instructions that will help anyone to build the robot.

More detailed information is available on the [_C. elegans_ robot project page](../Projects/c-elegans-robot/).
