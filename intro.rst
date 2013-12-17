************************
Introduction to OpenWorm
************************

Welcome
=======
OpenWorm is an open source project and open science community dedicated to creating the world's first whole organism 
in a computer, a *C. elegans* nematode, via bottom-up "systems biology" computational modeling. It is an association 
of highly motivated scientists and engineers who believe in Open Science and Open Access.

.. [pulled from Mission/Vision - let's adapt to be more welcoming]


Contributing to OpenWorm
========================
Anyone is free to sign up to help. To get to know a little about you, please fill out 
`this form <https://docs.google.com/a/openworm.org/spreadsheet/viewform?formkey=dC1CUDQtTV82MEJJcjY0NjdCcHpYdmc6MQ#gid=0>`_ 
and we'll get back to you within a few days.

While the heart of OpenWorm is computational modeling, we are always looking for people with talents beyond programming 
to contribute.  Are you a graphic designer, writer, PR specialist or simply someone with a love of science and expertise 
to share? Please reach out to us at info@openworm.org to discuss opportuntities with OpenWorm.


.. Navigating OpenWorm
.. ===================
.. To help you find your way around OpenWorm we suggest using this page 


Concepts
========


Top-down simulation
-------------------

Our first instincts when looking at a system we want to simulate is to come up with a list of its obvious features 
and then try to pick the simplest means of simulating it.  In the case of obvious top-down ways to model a worm, 
one might capture the fact that it bends in a sinusoidal pattern as a good starting point, and begin implementing 
sine and cosine functions that can capture this.

There is an important place for this kind of simulation, but we have found that one rapidly runs into limitations 
of generalization.  The model that worked great for crawling no longer works for turning around.  The simplest 
thing possible is added to the model to make it work for turning around, but soon there is another aspect to 
capture, and then another.  Soon, the model is a series of hacks that become increasingly brittle.

Instead of a pure top-down approach, we employ a balanced top-down, bottom-up approach, with a greater emphasis 
on the bottom up.

Bottom-up simulation
--------------------

Biology teaches us that when it comes to understanding how animals work, understanding the 
`behavior of cells is critical <http://en.wikipedia.org/wiki/Cell_biology>`_.  
Our bodies are made up of between 40 and 100 trillion cells, and it is these cells working 
together that make up everything we are and do.  Of particular interest are the cells in the 
brain and larger nervous system, that are responsible for our thoughts, creativity and feelings.  

Today, science has barely scratched the surface of how to make best use of the enormous power of computers 
to create models of cellular activity.  Scientists have not yet placed computer models of cells at the center 
of biology.

A "bottom-up" simulation, in this case, is an attempt to model the individual cells in the organism, giving 
them behaviors which, when combined together, produce the outward behavior of the entire organism.  This is as 
opposed to building the organism without consideration for individual cells to start with, and adding cells in later.

In reality, we always have to do some bottom-up simulation along with top-down simulation, in order to make progress.  
But in general and where possible, we view what we are doing as focused on simulating cells first.

Multi-algorithm integration
---------------------------

Just as mathematics has played a crucial role in the `description of physics <http://en.wikipedia.org/wiki/Mathematical_physics>`_, 
`mathematicians have approached the field of biology <http://en.wikipedia.org/wiki/Mathematical_and_theoretical_biology>`_
with the goal of describing biological activity more precisely.  Generally speaking, this means that if it happens 
inside a biological organism, there should be a set of equations that can explain how it works.  A great deal of 
creativity goes into coming up with such equations.

Once equations have been determined, computers are great at calculating them once they have been 
`turned into algorithms <http://en.wikipedia.org/wiki/Algorithm>`_.  Algorithms become the computer's way of 
handling a bunch of equations.

The challenge is that there are a lot of equations that are necessary to fully specify how cellular activity works.  
A `recent whole cell model <https://simtk.org/home/wholecell>`_ of a relatively simple cell came up with 32 algorithms 
composed of many more equations and a ton of data.

The consequence of this from an engineering perspective is, in order to simulate complex living systems, 
we  need software that is flexible enough to let us assemble the algorithms we need in just the right ways.  
We call this "multi-algorithm integration".

Model optimization
------------------

There are a lot of aspects of the _c. elegans_ that we will not be able to measure directly for a while based 
on experimental limitations.  These are `"free parameters" <http://en.wikipedia.org/wiki/Free_parameter>`_.  
The conventional wisdom on modeling is to minimize the number of free parameters as much as possible.  
Sometimes, the large number of free parameters are used as an argument to avoid making computational simulations.

In this case, we have to make do with what we have and make some good educated guesses about the free parameters.  
There is a `mathematical discipline that helps us do that known as optimization 
<http://en.wikipedia.org/wiki/Mathematical_optimization>`_.  For our purposes, you can think of this as generating 
many different versions of a model, each version with slightly different parameters, and then measuring if the 
model produces good results.  If a model produces better results by changing the parameters in a particular way, 
you try to keep changing the parameters in that way and see if you get even better results.  In this way, 
roughly speaking, optimization techniques enable scientists to turn a problem of lack of data into a problem 
that a computer can address using brute force calculations.

NeuroML
-------

`NeuroML is <http://en.wikipedia.org/wiki/NeuroML>`_ an XML (Extensible Markup Language) based model description 
language that aims to provide a common data format for defining and exchanging models in computational neuroscience. 
The focus of NeuroML is on models which are based on the biophysical and anatomical properties of real neurons. 
(`Wikipedia <http://en.wikipedia.org/wiki/NeuroML>`_).

NeuroML is known as an open standard, because its means of describing a model is publicly available for 
others to improve upon.  
