.. _model-validation:

Model Validation & Optimization engine
======================================

.. contents::

The Optimization Engine uses optimization techniques like genetic algorithms to help fill gaps in our 
knowledge of the electrophysiology of *C. elegans* muscle cells and neurons. Check out the code on the 
GitHub repository.

For more details on movement validation, check out the 
:ref:`movement validation project page <movement-validation>`.

Previous accomplishments
------------------------

* Genetic algorithms applied to tuning muscle cell models

Associated Milestones
----------------------

`STORY: Muscle Cell model output closely matches that of real data <https://github.com/openworm/OpenWorm/issues?milestone=13&state=open>`_
We will show that we have built a model of C. elegans muscle cell that matches data recorded from the nematode muscle cell. In part, we will use techniques of model optimization to fill in gaps in the model parameter space (deduce unmeasured parameters). The main technical challenge is tuning muscle cell passive properties and building a larger data set (more cell recordings).

`STORY: Build a test suite for the simulation from WormBehavior database <https://github.com/openworm/OpenWorm/issues?milestone=19&state=open>`_
As a scientist or developer, I want to be able to run a test suite against the simulation that will show me how close the model is to real data.

In order for a model to demonstrate scientific value, it has to make falsifiable predictions. The target data to be able to predict will be drawn from the WormBehavior database. This milestone will involve working with these data, creating a code base that can compare movement output from the simulation with ground truth from the database and produce an accuracy score.

This story breaks down the epic to predict behavior from the WormBehavior database

`EPIC: Correctly predict 80% of wild type (N2) behavior in WormBehavior database <https://github.com/openworm/OpenWorm/issues?milestone=22&state=open>`_
This epic is to have a simulation that can demonstrate it can predict (and therefore reproduce) 80% of the data collected about the N2 worm in the WormBehavior database. This means building a training set and a test set that are kept separate from each other, using the training set to tune up the model, then generating predictions, and comparing them against the test set, and doing some cross-validation).

This epic focuses on an output of simulation performance rather than the means of implementation, so any way to achieve this epic is welcome.


Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                                                  | Language    |
+=====================================================================================================================+==============================================================================================================================================================+=============+
| `movement_validation <https://github.com/openworm/movement_validation>`_                                            | A test pipeline that allows us to run a behavioural phenotyping of our virtual worm running the same test statistics the Shafer lab used on their worm data. | Python      |
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `SegWorm <https://github.com/openworm/SegWorm>`_                                                                    | SegWorm is Matlab code from Dr. Eviatar Yemini built as part of the WormBehavior database (http://wormbehavior.mrc-lmb.cam.ac.uk/)                           | Matlab      |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `HeuristicWorm <https://github.com/openworm/HeuristicWorm>`_                                                        |                                                                                                                                                              |  C++        |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+

