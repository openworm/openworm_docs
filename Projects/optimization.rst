.. _optimization:

Optimization engine
===================

.. contents::

The Optimization engine uses optimization techniques like genetic algorithms to help fill 
gaps in our knowledge of the electrophysiology of *C. elegans* muscle cells and neurons. 

These two algorithms, Hodgkin-Huxley and SPH, require parameters to be set in order for 
them to function properly, and therefore create some "known unknows" or "free parameters" 
we must define in order for the algorithm to function at all. For Hodgkin-Huxley we must 
define the ion channel species and set their conductance parameters. For SPH, we must 
define mass and the forces that one set of particles exert on another, which in turn 
means defining the mass of muscles and how much they pull. The conventional wisdom on 
modeling is to minimize the number of free parameters as much as possible, but we know 
there will be a vast parameter space associated with the model.

To deal with the space of free parameters, two strategies are employed. First, by using 
parameters that are based on actual physical processes, many different means can be 
used to provide sensible estimates. For example, we can estimate the volume and mass 
of a muscle cell based on figures that have been created in the scientific literature 
that show its basic dimensions, and some educated guesses about the weight of muscle 
tissue. Secondly, to go beyond educated estimates into more detailed measurements, we 
can employ model optimization techniques. Briefly stated, these computational techniques 
enable a rational way to generate multiple models with differing parameters and choose 
those sets of parameters that best pass a series of tests. For example, the conductances 
of motor neurons can be set by what keeps the activity those neurons within the boundaries 
of an appropriate dynamic range, given calcium trace recordings data of those neurons as 
constraints.

Previous accomplishments
------------------------

* Genetic algorithms applied to tuning muscle cell models

Current roadmap
----------------------

`STORY: Muscle Cell model output closely matches that of real data 
<https://github.com/openworm/OpenWorm/issues?milestone=13&state=open>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We will show that we have built a model of C. elegans muscle cell that matches data 
recorded from the nematode muscle cell. In part, we will use techniques of model 
optimization to fill in gaps in the model parameter space (deduce unmeasured parameters). 
The main technical challenge is tuning muscle cell passive properties and building a larger
data set (more cell recordings).


Issues list
-----------

none

Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                                                  | Language    |
+=====================================================================================================================+==============================================================================================================================================================+=============+
| `HeuristicWorm <https://github.com/openworm/HeuristicWorm>`_                                                        |                                                                                                                                                              |  C++        |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+

