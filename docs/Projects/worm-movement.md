Movement Validation
===================

In order to know that we are making meaningful scientific progress, we need to validate the model using information from real worms. The movement validation project is working with an existing database of worm movement to make the critical comparisons.

The main goal of the Movement Validation team is to finish a test pipeline so the OpenWorm project can run a behavioural phenotyping of its virtual worm, using the same statistical tests the Schafer lab used on their real worm data.

Previous accomplishments
------------------------

- All code necessary to reproduce Ev Yemini’s Nature Methods paper was obtained in October 2013. Jim has stored it in the [MRC\_wormtracker\_GUI repo](https://github.com/JimHokanson/mrc_wormtracker_gui).
    - This is in addition to the [SegWorm repo](https://github.com/openworm/SegWorm), although we will be merging them.
    - It has code to generate features from measurements.

- A [movement validation GitHub repository](https://github.com/MichaelCurrie/movement_validation) was started specifically with the goal of developing  the infrastructure to validate model worm movements against real worms.

Current roadmap
---------------

###[STORY: Build a test suite for the simulation from WormBehavior database](https://github.com/openworm/OpenWorm/issues?milestone=19&state=open)

As a scientist or developer, I want to be able to run a test suite against the simulation that will show me how close the model is to real data.

In order for a model to demonstrate scientific value, it has to make falsifiable predictions. The target data to be able to predict will be drawn from the WormBehavior database. This milestone will involve working with these data, creating a code base that can compare movement output from the simulation with ground truth from the database and produce an accuracy score.

This story breaks down the epic to predict behavior from the WormBehavior database.

###[EPIC: Correctly predict 80% of wild type (N2) behavior in WormBehavior database](https://github.com/openworm/OpenWorm/issues?milestone=22&state=open)

This epic is to have a simulation that can demonstrate it can predict (and therefore reproduce) 80% of the data collected about the N2 worm in the WormBehavior database. This means building a training set and a test set that are kept separate from each other, using the training set to tune up the model, then generating predictions, and comparing them against the test set, and doing some cross-validation).

This epic focuses on an output of simulation performance rather than the means of implementation, so any way to achieve this epic is welcome.

More information on next steps is available in a [recent progress report](https://docs.google.com/document/d/1sBgMAD-7RUjHwBgrC204LMqSC81byIaZNRm32lEGWMM/edit).

Issues list
-----------

All issues related to [movement validation](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=movement+validation&page=1&sort=comments&state=open) can be found on GitHub

Associated Repositories
-----------------------

<table>
<colgroup>
<col width="40%" />
<col width="54%" />
<col width="4%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Repository</th>
<th align="left">Description</th>
<th align="left">Language</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left"><a href="https://github.com/openworm/movement_validation">movement_validation</a></td>
<td align="left">A test pipeline that allows us to run a behavioural phenotyping of our virtual worm running the same test statistics the Shafer lab used on their worm data.</td>
<td align="left">Python</td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/SegWorm">SegWorm</a></td>
<td align="left">SegWorm is Matlab code from Dr. Eviatar Yemini built as part of the WormBehavior database (<a href="http://wormbehavior.mrc-lmb.cam.ac.uk/" class="uri">http://wormbehavior.mrc-lmb.cam.ac.uk/</a>)</td>
<td align="left">Matlab</td>
</tr>
</tbody>
</table>
