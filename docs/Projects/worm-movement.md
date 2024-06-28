Movement Analysis
===================

In order to know that we are making meaningful scientific progress, we need to validate the model using information from real worms. The movement analysis team is working with an existing database of worm movement to make the critical comparisons.

The main goal of the Movement Analysis team is to finish a test pipeline so the OpenWorm project can run a behavioural phenotyping of its virtual worm, using the same statistical tests the Schafer lab used on their real worm data.


Tools Built
-----------

- [Open Worm Analysis Toolbox](https://github.com/openworm/open-worm-analysis-toolbox)
- [Tracker-Commons file format](https://github.com/openworm/tracker-commons/)

For more information, please visit the above pages.

Current roadmap
---------------

###[STORY: Build a test suite for the simulation from WormBehavior database](https://github.com/openworm/OpenWorm/issues?milestone=19&state=closed)

As a scientist or developer, I want to be able to run a test suite against the simulation that will show me how close the model is to real data.

In order for a model to demonstrate scientific value, it has to make falsifiable predictions. The target data to be able to predict will be drawn from the WormBehavior database. This milestone will involve working with these data, creating a code base that can compare movement output from the simulation with ground truth from the database and produce an accuracy score.

This story breaks down the epic to predict behavior from the WormBehavior database.

###[EPIC: Correctly predict 80% of wild type (N2) behavior in WormBehavior database](https://github.com/openworm/OpenWorm/milestone/22)

This epic is to have a simulation that can demonstrate it can predict (and therefore reproduce) 80% of the data collected about the N2 worm in the WormBehavior database. This means building a training set and a test set that are kept separate from each other, using the training set to tune up the model, then generating predictions, and comparing them against the test set, and doing some cross-validation).

This epic focuses on an output of simulation performance rather than the means of implementation, so any way to achieve this epic is welcome.

More information on next steps is available in a [recent progress report](https://docs.google.com/document/d/1sBgMAD-7RUjHwBgrC204LMqSC81byIaZNRm32lEGWMM/edit).

Issues list
-----------

Please visit the issues listed in the below repositories.

Associated Repositories
-----------------------

**OpenWorm Port of Schafer Lab's Worm Analysis Toolbox 1.3.4**

- [https://github.com/openworm/SegWorm](https://github.com/openworm/SegWorm)  (original MATLAB code, static)
- [https://github.com/JimHokanson/SegwormMatlabClasses](https://github.com/JimHokanson/SegwormMatlabClasses)  (Jim Hokanson's MATLAB fork, now static)
- [https://github.com/openworm/open-worm-analysis-toolbox](https://github.com/openworm/open-worm-analysis-toolbox)  (active Python port; formerly movement_validation)

**Cloud Computing**

- [https://github.com/openworm/movement_validation_cloud](https://github.com/openworm/movement_validation_cloud), forked from
- [https://github.com/joebowen/movement_validation_cloud](https://github.com/joebowen/movement_validation_cloud)

**Worm Tracker File Format Specification and Parser**

- [https://github.com/openworm/tracker-commons](https://github.com/openworm/tracker-commons)

**André Brown's "Eigenworms" Code**

- [https://github.com/aexbrown/Motif_Analysis](https://github.com/aexbrown/Motif_Analysis) (Deprecated in favour of Behavioural_Syntax below)
- [https://github.com/aexbrown/Behavioural_Syntax](https://github.com/aexbrown/Behavioural_Syntax) (in MATLAB)
- [https://github.com/AidanRocke/behavioral_syntax](https://github.com/AidanRocke/behavioral_syntax) (Aidan Rocke's Python port)

**Brown Lab Multiworm Tracking Code**

- [https://github.com/Behavioural-Genomics/tracking](https://github.com/Behavioural-Genomics/tracking) (Closed)
- [https://github.com/ver228/Multiworm_Tracking](https://github.com/ver228/Multiworm_Tracking) (Avelino Javer's work)
- [https://github.com/KezhiLi/Tracking_Hypo](https://github.com/KezhiLi/Tracking_Hypo)   (Kezhi Li's work; the computer vision code)
