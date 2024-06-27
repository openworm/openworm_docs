Project Background
==================

History
-------

Established in January 2011, OpenWorm has since that time built a community of highly-motivated and highly-skilled individuals and coordinated their work. This community has produced scientific publications making use of scientific research published through open access, helping to show the validity of the open science approach we have taken.

Please [visit here](../fullhistory/) for a more extensive history of the project.

More information is available on the past history of [OpenWorm releases](../releases/).

Why do this?
------------

There has never been a scientific result in biology or neuroscience that is inconsistent with the idea that brains are 100% physical matter. We tend to forget, but our brains are tissues just like our lungs and heart are. If I could stick an electrode in your brain right now I could record activity from your neurons that corresponds with your thoughts. The problem is that scientists can't understand what all that activity means yet.

Scientists can make models of sending a rocket to land on the surface of Mars, but not a model of all the activity of your brain. Scientists lack well-agreed upon models of complex neuronal activity because such models are hard to produce.

Complex neuronal activity is the result of countless interactions between molecules happening inside, between, and around neurons. Because of all the interactions that make up complex neuronal activity, you need to gather up a lot of information to make models of it. Also because of all those interactions, you need sophisticated software platforms to manage all that information properly.

We are building a simulation platform to prove it is possible to make good models of complex neuronal activity, starting with a digital worm. We are making the simulation platform open source because we believe anyone should be able to use it to understand how neurons and cells work.

Why _C. elegans_?
-----------------

In the field of neuroscience, one of the simplest organisms that are studied is _Caenorhabditis elegans_, or _C. elegans_ for short. It only has 302 neurons, has a very consistent lifecycle, and is well studied. Its whole body has only 1000 cells total. With those 1000 cells it solves basic problems of feeding, mate-finding, predator and toxin avoidance using a nervous system driving muscles on a body in a complex world.

The cells in its body work together to produce its behavior. Instead of starting with the behavior and building a simple system to capture it, we are starting with making models of the individual cells and their interactions. If we do this correctly so that the cells act on each other as they do in the real organism, we will have a much more realistic model than we would get trying to go straight to the behavior.

This seems to us the only sensible starting point to creating a true biological simulation that captures enough details and has enough constraints to approximate real biology. Simulating a single cell that doesn't move (like a yeast cell) isn't going to provide us enough of a foundation to build up to more complex organisms by itself. If we can't accomplish a simulation at this humble scale, we'll never be able to do it at the massive scale of the human brain. The technology that would come out of this endeavor would be applicable to much more complex organisms down the road.

On models
---------

Models are the cornerstone of science. Tools like algebra, calculus, Newtonian mechanics and computer spreadsheets were advances because we could plug numbers into equations and get answers out that told us something about the world.

Unfortunately, neuroscience has few predictive models for how nervous systems work.

We are starting by building a full simulation of a small biological system with a reasonable number of parts. We are focused on capturing as much of the rich detail of that biological system as possible.

Concepts
--------

### Top-down simulation

Our first instincts when looking at a system we want to simulate is to come up with a list of its obvious features and then try to pick the simplest means of simulating it. In the case of obvious top-down ways to model a worm, one might capture the fact that it bends in a sinusoidal pattern as a good starting point, and begin implementing sine and cosine functions that can capture this.

There is an important place for this kind of simulation, but we have found that one rapidly runs into limitations of generalization. The model that worked great for crawling no longer works for turning around. The simplest thing possible is added to the model to make it work for turning around, but soon there is another aspect to capture, and then another. Soon, the model is a series of hacks that become increasingly brittle.

Instead of a pure top-down approach, we employ a balanced top-down, bottom-up approach, with a greater emphasis on the bottom up.

### Bottom-up simulation

Biology teaches us that when it comes to understanding how animals work, understanding the [behavior of cells is critical](http://en.wikipedia.org/wiki/Cell_biology). Our bodies are made up of between 40 and 100 trillion cells, and it is these cells working together that make up everything we are and do. Of particular interest are the cells in the brain and larger nervous system, that are responsible for our thoughts, creativity and feelings.

Today, science has barely scratched the surface of how to make best use of the enormous power of computers to create models of cellular activity. Scientists have not yet placed computer models of cells at the center of biology.

A "bottom-up" simulation, in this case, is an attempt to model the individual cells in the organism, giving them behaviors which, when combined together, produce the outward behavior of the entire organism. This is as opposed to building the organism without consideration for individual cells to start with, and adding cells in later.

In reality, we always have to do some bottom-up simulation along with top-down simulation, in order to make progress. But in general and where possible, we view what we are doing as focused on simulating cells first.

### Multi-algorithm integration

Just as mathematics has played a crucial role in the [description of physics](http://en.wikipedia.org/wiki/Mathematical_physics), [mathematicians have approached the field of biology](http://en.wikipedia.org/wiki/Mathematical_and_theoretical_biology) with the goal of describing biological activity more precisely. Generally speaking, this means that if it happens inside a biological organism, there should be a set of equations that can explain how it works. A great deal of creativity goes into coming up with such equations.

Once equations have been determined, computers are great at calculating them once they have been [turned into algorithms](http://en.wikipedia.org/wiki/Algorithm). Algorithms become the computer's way of handling a bunch of equations.

The challenge is that there are a lot of equations that are necessary to fully specify how cellular activity works. A [recent whole cell model](https://simtk.org/home/wholecell) of a relatively simple cell came up with 32 algorithms composed of many more equations and a ton of data.

The consequence of this from an engineering perspective is, in order to simulate complex living systems, we need software that is flexible enough to let us assemble the algorithms we need in just the right ways. We call this "multi-algorithm integration".

### Model optimization

There are a lot of aspects of _C. elegans_ that we will not be able to measure directly for a while based on experimental limitations. These are ["free parameters"](http://en.wikipedia.org/wiki/Free_parameter). The conventional wisdom on modeling is to minimize the number of free parameters as much as possible. Sometimes, the large number of free parameters are used as an argument to avoid making computational simulations.

In this case, we have to make do with what we have and make some good educated guesses about the free parameters. There is a [mathematical discipline that helps us do that known as optimization](http://en.wikipedia.org/wiki/Mathematical_optimization). For our purposes, you can think of this as generating many different versions of a model, each version with slightly different parameters, and then measuring if the model produces good results. If a model produces better results by changing the parameters in a particular way, you try to keep changing the parameters in that way and see if you get even better results. In this way, roughly speaking, optimization techniques enable scientists to turn a problem of lack of data into a problem that a computer can address using brute force calculations.

### NeuroML

[NeuroML is](http://en.wikipedia.org/wiki/NeuroML) an XML (Extensible Markup Language) based model description language that aims to provide a common data format for defining and exchanging models in computational neuroscience. The focus of NeuroML is on models which are based on the biophysical and anatomical properties of real neurons. NeuroML is known as an open standard, because its means of describing a model is publicly available for others to improve upon.
