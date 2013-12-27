*************************************
Using OpenWorm Repositories on GitHub
*************************************

Accessing GitHub
================
To access the OpenWorm organization on GitHub and fully participate on issues, you will first need to create an account if you do not already have one. Note, you can comment on issues without a GitHub account, however, we recommend joining to maximize your ability to contribute to OpenWorm. Accounts are free and can be `created on the Github website <https://github.com/>`_.

Once you have joined GitHub, submit your username to info@openworm.org to be added to the OpenWorm organization.  
Once you have been accepted, log back into GitHub and select OpenWorm from the organization drop down menu to get 
started. You will now have access to be assigned issues, add issues and edit them.  

You can also directly access the `OpenWorm Organization on Github <https://github.com/organizations/openworm/>`_.


GitHub Issues
=============
Opening a New Issue
-------------------
After logging into GitHub, select the OpenWorm organization and then click on the repository in which the issue is 
located/relevant to. Click on the Issues tab on the menu to the right.

.. image:: http://i.imgur.com/Rh1uvmn.png

Next, click on the New Image button in the upper right corner of the screen.

.. image:: http://i.imgur.com/fvEQOJQ.png 

This will open the interface to create a new issue. You will need to add the following information:

* Name or short description of the issue

* Full description of the issue, including images if available.  (See below for more details on formatting the description.)

* Assign team members to the issue if appropriate

* Add a milestone if appropriate

* Add labels to categorize the issue such as what language is being used, issue status (not started, working, etc.) and what function the issue is related to.

.. image:: http://i.imgur.com/ozkZFsh.png 

Finally, click on Submit New Issue.

**Best Practices for OpenWorm**
When writing up the description for a given issue, provide as much context and detail as possible.  For clarity, we suggest the following format:

*Issue: Summarize the issue at hand and provide links when possible to relevant code, databases and information.

*Motivation: Provide a reasoning for the request and what resolving the issue will fix or what purpose it will serve.

*Steps: Create a list of specific steps that need to be completed to resolve the issue.

Links to relevant code, databases, documentation and related issues are strongly recommended.  

Check out `this example <https://github.com/openworm/OpenWorm/issues/140>`_ of a clearly written issue that follows best practices.


Interacting with Issues
-----------------------

`Generic information from GitHub <https://github.com/blog/831-issues-2-0-the-next-generation>`_


.. Best Practices for OpenWorm
.. [Need to fill this in]


Closing an Issue
----------------

* `Via pull requests <https://github.com/blog/1506-closing-issues-via-pull-requests>`_
* `Via commit messages <https://github.com/blog/1386-closing-issues-via-commit-messages>`_

.. [Add content]
.. Best Practices for OpenWorm
.. [Need to fill this in]


Contributing and Resolving Issues
=================================

`View the complete list of issues on GitHub<https://github.com/organizations/openworm/dashboard/issues>`_

To find issues that are relevant to your skillset and interest, first browse the list above and look for tags related to areas of functionality and coding language.  Alternatively, you can view a specific repository and the filter by tags related to the type of issue and coding language. Click on the issue name to open the details.  Feel free to explore and dig around.  

.. SHOULD ADD MORE INFORMATION ON MAKING COMMENTS, ACTUALLY MAKING CODE UPDATES, WHEN TO CLOSE OUT ISSUES (PROCESS)
.. (link to Data.rst sections on opening, replying to and closing issues)

.. Do we have a current list of contributors mapped to current issues?
.. Breakdowns of current issues based on potential volunteers' incoming skills
.. Using tags for categorizing tasks and issues


.. Using the Code
.. ==============
.. Explanations of the current code that has been produced, how to run it, how to use it
.. https://docs.google.com/a/openworm.org/presentation/d/1x0CPE74XNnISt9BVkyX3jYitvIq9j5QbamRWYrvp5fs/edit#slide=id.i35
.. https://drive.google.com/a/openworm.org/?tab=oo#folders/0B-GW0T4RUrQ6MTU0N2NmZmMtODAxOC00NDRlLWE3MmMtZDhjMGU4NjNhOTdl


Forking GitHub Repositories
===========================
On GitHub, click the Fork button on a project to create a "copy" that you can then modify independently. 

To fork an OpenWorm repository, go to https://github.com/openworm and hit the "Fork" button. GitHub will copy the repository to your account. This will copy the repo to your personal repository.  You can then make changes to the repository. Once you are done with the changes, hit the 'Pull Request' button on the repo page under your account. This will create a pull request asking the OpenWorm team to review, comment and merge the changes into the original repository.

For directions on doing this, check out the `help page from Github<https://help.github.com/articles/fork-a-repo>`_.


Posting Gists (gist.github.com)
===============================
Gist is a simple way to share snippets and pastes with others. All gists are Git repositories, so they are automatically versioned, forkable and usable from Git.  You can create a new gist here: https://gist.github.com/

How to:

* `Create Gists <https://help.github.com/articles/creating-gists>`_

* `Embed, Download and Copy Gists <https://help.github.com/articles/embedding-downloading-and-copying-gists>`_

Read the `latest news and updates <https://github.com/blog/search?page=1&q=gis>`_on Gists at GitHub.


Repositories
============

View the `full current list <https://github.com/openworm>`_ of repositories on GitHub.


Geppetto
--------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| Repository                                                                                                          | Description                                | Language   |
+=====================================================================================================================+============================================+============+
| `org.gepetto <https://github.com/openworm/org.geppetto>`_                                                           | Geppetto Main Bundle and packaging         | Java       |
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.solver.sph <https://github.com/openworm/org.geppetto.solver.sph>`_                                    | PCI SPH Solver bundle for Geppetto         | Python     |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.simulator.jlems <https://github.com/openworm/org.geppetto.simulator.jlems>`_                          | jLEMS based simulator for Geppetto         | Java       |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.model.neuroml <https://github.com/openworm/org.geppetto.model.neuroml>`_                              | NeuroML Model Bundle for Geppetto          | Java       |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.core <https://github.com/openworm/org.geppetto.core>`_                                                | Geppetto core bundle                       | Javascript |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.frontend <https://github.com/openworm/org.geppetto.frontend>`_                                        | Geppetto frontend bundle - Web application | Java       |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.testbackend <https://github.com/openworm/org.geppetto.testbackend>`_                                  | Geppetto test backend for Geppetto         | Java       |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.simulator.sph <https://github.com/openworm/org.geppetto.simulator.sph>`_                              | SPH Simulator bundle for Geppetto          | Java       | 
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.simulation <https://github.com/openworm/org.geppetto.simulation>`_                                    | Generic simulation bundle for Geppetto     | Python     |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.model.sph <https://github.com/openworm/org.geppetto.model.sph>`_                                      | PCI SPH Model Bundle for Geppetto          | CSS        |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.samples <https://github.com/openworm/org.geppetto.samples>`_                                          | Sample simulations for Geppetto            | Python     |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+
| `org.geppetto.templatebundle <https://github.com/openworm/org.geppetto.templatebundle>`_                            | Template bundle                            | Javascript |    
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------+------------+


Models
------

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| Repository                                                                                                          | Description                                                                                                                      | Language   |
+=====================================================================================================================+==================================================================================================================================+============+
| `Smoothed-Particle-Hydrodynamics <https://github.com/openworm/Smoothed-Particle-Hydrodynamics>`_                    | Known as Sibernetic, this is a C++ implementation of the Smoothed Particle Hydrodynamics algorithm for the OpenWorm project.     | Java       |
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `muscle_model <https://github.com/openworm/muscle_model>`_                                                          | model of c.elegans muscle in NEURON                                                                                              | XSLT       |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `CElegansNeuroML <https://github.com/openworm/CElegansNeuroML>`_                                                    | NeuroML based C elegans model, contained in a neuroConstruct project                                                             | Java       |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `Blender2NeuroML <https://github.com/openworm/Blender2NeuroML>`_                                                    | Conversion script to bring neuron models drawn in Blender into NeuroML format                                                    | Python     |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `NEURONSimData <https://github.com/openworm/NEURONSimData>`_                                                        | Graphing voltage data from NEURON sims of C. elegans conectome                                                                   |            |   
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+


OpenWorm
--------

+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| Repository                                                                                                          | Description                                                                                                                      | Language   |
+=====================================================================================================================+==================================================================================================================================+============+
| `org.openworm.website <https://github.com/openworm/org.openworm.website>`_                                          | OpenWorm Website                                                                                                                 | Python     |
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `OpenWorm <https://github.com/openworm/OpenWorm>`_                                                                  | Project Home repo for OpenWorm Wiki and Project-wide issues                                                                      | Matlab     |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+
| `openworm_docs <https://github.com/openworm/openworm_docs>`_                                                        | Documentation for OpenWorm                                                                                                       |            |  
+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+------------+


Uncategorized
-------------

+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| Repository                                                                                                          | Description                                                                                                                                                  | Language    |
+=====================================================================================================================+==============================================================================================================================================================+=============+
| `movement_validation <https://github.com/openworm/movement_validation>`_                                            | A test pipeline that allows us to run a behavioural phenotyping of our virtual worm running the same test statistics the Shafer lab used on their worm data. | Java        |
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `ConfigurationGenerator <https://github.com/openworm/ConfigurationGenerator>`_                                      | Generation start scene configuration for PCI SPH solver                                                                                                      | JavaScript  |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `data-viz <https://github.com/openworm/data-viz>`_                                                                  | Repository for scripts and other code items to create web-based visualizations of data in the project                                                        | Python      |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `SegWorm* <https://github.com/openworm/SegWorm>`_                                                                   | SegWorm is Matlab code from Dr. Eviatar Yemini built as part of the WormBehavior database (http://wormbehavior.mrc-lmb.cam.ac.uk/)                           | Java        |  
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `wormbrowser <https://github.com/openworm/wormbrowser>`_                                                            | The Worm Browser -- a 3D browser of the cellular anatomy of the c. elegans                                                                                   | Objective-C |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `openwormbrowser-ios <https://github.com/openworm/openwormbrowser-ios>`_                                            | OpenWorm Browser for iOS, based on the open-3d-viewer, which was based on Google Body Browser                                                                | C++         |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `HeuristicWorm <https://github.com/openworm/HeuristicWorm>`_                                                        |                                                                                                                                                              |             |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+
| `CyberElegans <https://github.com/openworm/CyberElegans>`_                                                         | Neuromechanical model of C. Elegans                                                                                                                          |             |   
+---------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+


