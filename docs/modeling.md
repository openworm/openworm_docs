OpenWorm Modeling Approach
==========================

Our main goal is to build the world's first virtual organism-- an *in silico* implementation of a living creature-- for the purpose of achieving an understanding of the events and mechanisms of living cells. Our secondary goal is to enable, via simulation, unprecedented in silico experiments of living cells to power the next generation of advanced systems biology analysis, synthetic biology, computational drug discovery and dynamic disease modeling.

In order to achieve these goals, we first began with an informal cartoon representation of a breakdown of cell types and various biological processes that the worm has. Here is a representation of a small subset of those processes, where arrows show the causal relationship between processes and cell types:

![Complex causation loop](https://docs.google.com/drawings/d/1VwzSDl_a_YCqOkO4tqrG8FzB0B5A50FWgO0qdkBpNB4/pub?w=401&h=312)

This picture is purposefully drawn with an underlying loop of causal relationships, and is partially inspired by the work of [Robert Rosen](http://www.amazon.com/Life-Itself-Comprehensive-Fabrication-Complexity/dp/0231075650). The decision to focus on any one loop is arbitrary. Many different loops of causal relationships could be plucked out of the processes that underly the worm. However, focusing on first dealing with the loop that deals with behavior in the environment and through the nervous system has several advantages as a starting point:

-   Crawling behavior of worms is relatively easy to measure
-   The 302 neurons responsible for the behavior are well mapped
-   Enables the study of the nervous system as a real time control system for a body
-   Provides the model with a minimum core to which other biological processes and cell types can be added.

Having chosen one loop to focus on first, we can now re-define the problem as how to construct an acceptable neuromechanical model. There have been other attempts to do this in the past and there are some groups currently working on the problem using different approaches (e.g. [Cohen](http://wormlab.eu/author/netta-cohen/), [Lockery](https://www.lockerylab.org/), [Si Elegans](http://www.si-elegans.eu/)).

Our approach involves building a 3D mechanical model of the worm body and nervous system, tuning the model using model optimization techniques, validating the model using real data, and ensuring the model is reproducible by other labs by exposing it through a web-based simulation engine.

Closing the loop with neuromechanical modeling
==============================================

While our ultimate goal is to simulate every cell in the _C. elegans_, we are starting out by building a model of its body and environment, its nervous system, and its muscle cells.

To get a quick idea of what this looks like, check out the [CyberElegans prototype](http://www.youtube.com/embed/3uV3yTmUlgo). In this movie you can see a simulated 3D _C. elegans_ being activated in an environment. Similar to the CyberElegans model, its muscles are located around the outside of its body, and as they turn red, they are exerting forces on the body that cause the bending to happen.

These steps are outlined in blue text of the figure below:

![Greatly oversimplified causation loop](https://docs.google.com/drawings/d/1a_9zEANb4coI9xRv2fFu_-Ul9SOnhH_cVHHJgpCNo5I/pub?w=401&h=312)

Our end goal for the first version is to complete the entire loop. We believe that this is the most meaningful place to begin because it enables us to study the relationship between a nervous system, the body it is controlling, and the environment that body has to navigate. We also believe this is a novel development because there are no existing computational models of any nervous systems that complete this loop. For an excellent review of the current state of research on this topic, check out [Cohen & Sanders, 2014](https://www.dropbox.com/s/6a76de0jpjm0ze0/Nematode%20locomotion%20dissecting%20the%20neuronal%E2%80%93environmental%20loop%20-%20Cohen%2C%20Sanders%20-%202014.pdf)

When we first started, our team in Novosibirsk had produced an awesome prototype. We recently published [an article](http://iospress.metapress.com/content/p61284485326g608/?p=5e3b5e96ad274eb5af0001971360de3e&pi=4) about it. If you watch [the movie that goes along with the prototype](http://www.youtube.com/watch?v=3uV3yTmUlgo), you can see the basic components of the loop above in action:

![CyberElegans with muscle cells](https://docs.google.com/drawings/d/142NbGecjnWuq6RxWgqREhKOXJ8oDo55wVvBuKQPyKCg/pub?w=430&h=297)

Here muscle cells cause the motion of the body of the worm along the surface of its environment.

![Inside the CyberElegans model](https://docs.google.com/drawings/d/1fO_gQI_febpu4iHd1_UDrMNQ_eqvHgJynMqho7UC6gw/pub?w=460&h=327)

Inside the worm, motor neurons are responsible for activating the muscles, which then makes the worms move. The blue portions of the loop diagram above are those aspects that are covered by the initial prototype. We are now in the process of both adding in the missing portions of the loop, as well as making the existing portions more biologically realistic, and making the software platform they are operating on more scalable.

Components
==========

In order to accomplish this vision, we have to describe the different pieces of the loop separately in order to understand how to model them effectively. This consists of modeling the body within an environment, the neurons, and the muscle cells.

Body and environment
--------------------

One of the aspects of making the model more biologically realistic has been to incorporate a [3d model of the anatomy](http://browser.openworm.org/) of the worm into the simulation.

To get a quick idea of what this looks like, check out the [latest movie](https://www.youtube.com/watch?v=SaovWiZJUWY). In this movie you can see a simulated 3D _C. elegans_ being activated in an environment. Its muscles are located around the outside of its body, and as they turn red, they are exerting forces on the body that cause the bending to happen.

In turn, the activity of the muscles are being driven by the activity of neurons within the body.

![image](http://i.imgur.com/KSWjCaW.jpg)

More detailed information is available on the [Sibernetic](https://openworm.org/sibernetic/) project page.

Having a virtual body now allows us to try out many different ways to control it using signals that could arise from neurons. Separately, we have been doing work to create a realistic model of the worm's neurons.

Neurons
-------

![Neurons in WormBrowser](https://docs.google.com/drawings/d/1GIwzQRvmDtprPBLSGjJhuEHqYqEcKaHLyKK0s80a3lM/pub?w=391&h=224)

This is a much more faithful representation of the neurons and their positions within the worm's body.

Our computational strategy to model the nervous system involves first reusing the [_C. elegans_ connectome](http://dx.plos.org/10.1371/journal.pcbi.1001066) and the 3D anatomical map of the _C. elegans_ nervous system and body plan. We have used the NeuroML standard ([Gleeson et al., 2010](http://dx.plos.org/10.1371/journal.pcbi.1000815)) to describe the 3D anatomical map of the _C. elegans_ nervous system. This has been done by discretizing each neuron into multiple compartments, while preserving its three-dimensional position and structure. We have then defined the connections between the NeuroML neurons using the _C. elegans_ connectome. Because NeuroML has a well-defined mapping into a system of Hodgkin-Huxley equations, it is currently possible to import the “spatial connectome” into the NEURON simulator ([Hines & Carnevale 1997](http://www.ncbi.nlm.nih.gov/pubmed/9248061)) to perform *in silico* experiments.

To start getting some practical experience playing with dynamics that come from the connectome, we have simplified it into a project called the 'connectome engine' and integrated its dynamics into a Lego Mindstorms EV3 robot. You can [see a movie of this in action](https://www.youtube.com/watch?v=D8ogHHwqrkI).

More information about working with the data within it and other data entities can be found on the [data representation project page](../Projects/datarep/#neuroml-connectome).

These neurons must eventually send signals to muscle cells.

Muscle cells
------------

![Muscle cells in _C. elegans_](https://docs.google.com/drawings/d/1ayyyu6dv0S4-750j-WRYVBEaziZr3g3V1-UIadAfHck/pub?w=391&h=224)

We have started our process of modeling muscle cells by choosing a specific muscle cell to target:

![Muscle cell highlighted](https://docs.google.com/drawings/d/1ZzCS0IXTb-n3GgaNLp98HS9X8ngHLtkcnildAYshuME/pub?w=535&h=289)

More information about working with the data within it and other data entities can be found on the [data representation project page](../Projects/muscle-neuron-integration/).

Once the body, neurons, and muscles are represented, we still have a lot of free parameters that we don't know. That's what leads us to the need to tune the model.

Tuning
======

The way we make the model biophysically realistic is to use sophisticated mathematics to drive the simulation that keep it more closely tied to real biology. This is important because we want the model to be able to inform real biological experiments and more coarse-grained, simplified mathematics falls short in many cases.

Specifically for this loop, we have found that two systems of equations will cover both aspects of the loop, broadly speaking:

![Simple loop overlaid with solvers](https://docs.google.com/drawings/d/1xL9NY-QcIeIfKXd-lN_x15fUGLM9vEL_sZzCLDvcT3Q/pub?w=401&h=312)

As you can see, where the two sets of equations overlap is with the activation of muscle cells. As a result, we have taken steps to use the muscle cell as a pilot of our more biologically realistic modeling, as well as our software integration of different set of equations assembled into an algorithmic "solver".

These two algorithms, Hodgkin-Huxley and SPH, require parameters to be set in order for them to function properly, and therefore create some “known unknows” or “free parameters” we must define in order for the algorithm to function at all. For Hodgkin-Huxley we must define the ion channel species and set their conductance parameters. For SPH, we must define mass and the forces that one set of particles exert on another, which in turn means defining the mass of muscles and how much they pull. The conventional wisdom on modeling is to minimize the number of free parameters as much as possible, but we know there will be a vast parameter space associated with the model.

To deal with the space of free parameters, two strategies are employed. First, by using parameters that are based on actual physical processes, many different means can be used to provide sensible estimates. For example, we can estimate the volume and mass of a muscle cell based on figures that have been created in the scientific literature that show its basic dimensions, and some educated guesses about the weight of muscle tissue. Secondly, to go beyond educated estimates into more detailed measurements, we can employ model optimization techniques. Briefly stated, these computational techniques enable a rational way to generate multiple models with differing parameters and choose those sets of parameters that best pass a series of tests. For example, the conductances of motor neurons can be set by what keeps the activity those neurons within the boundaries of an appropriate dynamic range, given calcium trace recordings data of those neurons as constraints.

If you'd be interested to help with tuning the model, please check out the [Optimization project page](../Projects/optimization/).

Validation
==========

In order to know that we are making meaningful scientific progress, we need to validate the model using information from real worms. The movement validation project is working with an existing database of worm movement to make the critical comparisons.

The main goal of the Movement Validation team is to finish a test pipeline so the OpenWorm project can run a behavioural phenotyping of its virtual worm, using the same statistical tests the Schafer lab used on their real worm data.

More detailed information is available on the [movement validation project page](../Projects/worm-movement/).

Reproducibility
===============

In order to allow the world to play with the model easily, we are engineering [Geppetto](http://geppetto.org), an open-source modular platform to enable multi-scale and multi-algorithm interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers out-of-the-box visualization of simulated models right in the browser. You can read about architectural concepts and learn more about the different plug-in bundles we are working on.

![image](http://www.geppetto.org/images/cn2.png)

The [project page for Geppetto](../Projects/geppetto/) has information about getting involved in its development with OpenWorm.
