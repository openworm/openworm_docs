Running the NeuroML connectome in NeuroConstruct
================================================

The NeuroML conversion of the [Virtual Worm Blender files](http://caltech.wormbase.org/virtualworm/) has been imported into a [neuroConstruct](http://www.neuroConstruct.org) project.

This page provides instructions for obtaining the latest version of neuroConstruct, getting the latest CElegans project and generating/visualising the cells and connections.

Install neuroConstruct and the CElegans project
-----------------------------------------------

There is a [quick-start zip file](https://www.dropbox.com/s/xdu1bh5sq2x1nx6/CElegansNeuroConstructBundle-snapshot-20140107.zip) containing neuroConstruct and the C. elegans connectome project. Installation instructions are in the file [README.txt](https://github.com/rayner/CElegansNeuroConstructBundle/blob/master/README.txt) inside the zip file.

If you have any problems installing the quick-start package, please e-mail openworm-bundle -at- magic-cookie.co.uk with a description of what went wrong.

If you are a developer, or need the very latest changes, you may prefer to install from the GitHub repositories instead. See the [advanced installation instructions](https://github.com/openworm/OpenWorm/wiki/Running-the-C.-elegans-model-in-neuroConstruct#advanced-installation-instructions) at the end of this page for details.

Open the project
----------------

Run neuroConstruct as outlined in the installation instructions (using *ant run* or *nC.bat/nC.sh*). In the main menu select **File** -\> **Open** and browse to the location of **CElegans.ncx**. Select this file and press **Open**.

The project may take up to 20 seconds to load. When it does load, try clicking on one of the cells in the **Cell Types in project** box, e.g. ADAL. This will take you to the **Cell Types** tab and show a summary of the cell's electrical properties (note: these are not yet matched to the real electrophysiological properties of Celegans cells!) and the number of segments in the cell.

Click on **View/edit morphology** and this will visualise the cell in 3D, see below.

![ADAL](https://github.com/openworm/CElegansNeuroML/raw/master/CElegans/images/ADAL_nC.png)

Generate a network
------------------

Now generate a subset network. Go to tab **Generate**, select 'PharyngealNeurons\_inputs' from the dropdown and press **Generate cell positions and connections**. Now go to tab **Visualisation** and press **View** with **Latest Generated Positions** selected in the drop down box. On a Mac, you can hold down the option button, click and drag downwards to zoom in further than the slider allows.

Alternatively, you can generate a network of all 302 neurons. Go to tab **Generate** and select 'Default Simulation Configuration' from the dropdown and press **Generate cell positions and connections**.

The image below shows the generated full network.

![CElegansnC](https://github.com/openworm/CElegansNeuroML/raw/master/CElegans/images/CElegans_nC.png)

Executing the network in NEURON simulation environment.
-------------------------------------------------------

[Install the NEURON simulation environment](http://www.neuron.yale.edu/neuron/download) and set the path to NEURON's bin directory containing nrniv within neuroConstruct's menu (Settings-\>General Preferences and Project Defaults). After generating cell positions (easiest to do this with the PharyngealNeurons\_inputs configuration), go to the export tab, the NEURON subtab, and press 'create hoc simulation'. Once this is completed the button will stop being greyed out and the 'Run simulation' button will be available. Clicking this should kick off the simulation run. Once this is completed, the output from the simulation should tell you that results are available in a directory named 'Sim\_XX' where XX will be a number. Go back to the Visualisation tab and click 'View Prev Sims in 3D..." Click on the box with the 'Sim\_XX' name that applies to the simulation run you did and press 'Load Simulation' at the bottom. Then at the bottom of the Visualisation screen click 'Replay' and the 'Replay simulation'. For PharyngealNeurons\_inputs, the color changes will be subtle, but they will be happening.

Check the project
-----------------

In addition to being able to generate and view the project through the main GUI, a number of Python scripts are provided to test the configuration of the project. These scripts access functionality in the Java implementation of neuroConstruct by using [Jython](http://www.jython.org). More details on the Python interface to neuroConstruct can be found [here](http://www.neuroconstruct.org/docs/python.html).

A script to test various aspects of the project is *CheckProject.py*. Running this generates a number of the Simulation Configurations in succession and checks that the expected numbers of cells and connections are created:

    cd pythonScripts
    ~/neuroConstruct/nC.sh -python CheckProject.py

Generate NeuroML from the project
---------------------------------

A NeuroML file containing the structure of the cells & all connections can be generated in two ways:

### Through the GUI

After generating the network in the GUI as outlined above, go to tab **Export**, click on **Generate all NeuroML scripts**. To have a single file with all the NeuroML for cells, channels and network connections, select **Generate single NeuroML Level 3 file**.

### Using a Python script

Go to folder `pythonScript` and run:

    ~/neuroConstruct/nC.sh -python GenerateNeuroML.py


------------------------------------------------------------------------

Advanced installation instructions
----------------------------------

This section describes how to install directly from the GitHub repositories. If you are a developer, or need the very latest changes, this may be a better option than using the quick-start bundle.

### Install the latest neuroConstruct

First, [get the latest version of neuroConstruct from GitHub](https://github.com/NeuralEnsemble/neuroConstruct/blob/master/INSTALL). While there are binary installers available on the neuroConstruct download page, it's best to use the latest version of this application from the GitHub repository, as this will most likely be the version in which the C. elegans project was last saved.

For full details on installing neuroConstruct from GitHub, see here: <https://github.com/NeuralEnsemble/neuroConstruct/blob/master/INSTALL>

Contact p.gleeson -at- ucl.ac.uk if there you have any problems with this.

### Getting the latest CElegans neuroConstruct project

The latest CElegans project is being hosted on Github [here](https://github.com/openworm/CElegansNeuroML). You have a number of options for getting the project:

#### A) Zip file with latest project

Get a zipped file with the project [here](https://github.com/openworm/CElegansNeuroML/zipball/master). Unzip this and go to the *CElegans* folder.

#### B) Read only copy of latest project

Install [Git](https://help.github.com/articles/set-up-git) and get a read only clone of the Git repository:

    git clone git://github.com/openworm/CElegansNeuroML.git
    cd CElegansNeuroML/CElegans

You'll always be able to retrieve the latest version of the project with

    git pull

#### C) Fork the project

Fork yourself a personal copy of the project repository. Go to <https://github.com/openworm/CElegansNeuroML> for more details.
