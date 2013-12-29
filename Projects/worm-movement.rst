.. _worm-movement:

Movement Validation
===================

.. contents::

In order to know that we are making meaningful scientific progress, we need to validate the model using information 
from real worms.  The movement validation project is working with an existing database of worm movement to make
the critical comparisons. 

The main goal of the Movement Validation team is to finish a test pipeline so the OpenWorm 
project can run a behavioural phenotyping of its virtual worm, using the same statistical 
tests the Schafer lab used on their real worm data.  

Previous accomplishments
------------------------

* All code necessary to reproduce Ev Yemini’s Nature Methods paper was obtained in October 2013.  Jim has stored it in the `MRC_wormtracker_GUI repo <https://github.com/JimHokanson/mrc_wormtracker_gui>`_.

  * This is in addition to the `SegWorm repo <https://github.com/openworm/SegWorm>`_, although we will be merging them.
  * It has code to generate features from measurements.

* A `movement validation GitHub repository <https://github.com/MichaelCurrie/movement_validation>`_ was started specifically with the goal of developing
 the infrastructure to validate model worm movements against real worms. 

   
Current roadmap
----------------------

`STORY: Build a test suite for the simulation from WormBehavior database 
<https://github.com/openworm/OpenWorm/issues?milestone=19&state=open>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a scientist or developer, I want to be able to run a test suite against the simulation that will show me how 
close the model is to real data.

In order for a model to demonstrate scientific value, it has to make falsifiable predictions. The target data to 
be able to predict will be drawn from the WormBehavior database. This milestone will involve working with these data, 
creating a code base that can compare movement output from the simulation with ground truth from the database and produce 
an accuracy score.

This story breaks down the epic to predict behavior from the WormBehavior database

`EPIC: Correctly predict 80% of wild type (N2) behavior in WormBehavior database 
<https://github.com/openworm/OpenWorm/issues?milestone=22&state=open>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This epic is to have a simulation that can demonstrate it can predict (and therefore reproduce) 80% of the data 
collected about the N2 worm in the WormBehavior database. This means building a training set and a test set that 
are kept separate from each other, using the training set to tune up the model, then generating predictions, and 
comparing them against the test set, and doing some cross-validation).

This epic focuses on an output of simulation performance rather than the means of implementation, so any way to 
achieve this epic is welcome.

More information on next steps is available in a 
`recent progress report <https://docs.google.com/document/d/1sBgMAD-7RUjHwBgrC204LMqSC81byIaZNRm32lEGWMM/edit>`_.

Issues list
-----------

All issues related to 
`movement validation <https://github.com/openworm/OpenWorm/issues?direction=desc&labels=movement+validation&page=1&sort=comments&state=open>`_ 
can be found on GitHub


Associated Repositories
-----------------------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                                                  | Language    |
+=====================================================================================================================+==============================================================================================================================================================+=============+
| `movement_validation <https://github.com/openworm/movement_validation>`_                                            | A test pipeline that allows us to run a behavioural phenotyping of our virtual worm running the same test statistics the Shafer lab used on their worm data. | Python      |
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `SegWorm <https://github.com/openworm/SegWorm>`_                                                                    | SegWorm is Matlab code from Dr. Eviatar Yemini built as part of the WormBehavior database (http://wormbehavior.mrc-lmb.cam.ac.uk/)                           | Matlab      |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+


