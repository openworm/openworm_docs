Frequently Asked Questions
==========================

OpenWorm general
----------------

### Why _C. elegans_?

The tiny worm _C. elegans_ is by far the most understood and studied animal with a brain in all of biology. It was the first multi-cellular organism to have its genome mapped. It has only ~1000 cells and exactly 302 neurons, which have also been mapped as well as its “wiring diagram” making it also the first organism to have a complete connectome produced. This part gets particularly exciting for folks interested in artificial intelligence or computational neuroscience.

Three different Nobel prizes have been awarded for work on this worm, and it is increasingly being used as a model for better understanding disease and health relevant to all organisms, including humans. When making a complex computer model, it is important to start where the data are the most complete.

### What does the real worm do?

It has all sorts of behaviors! Some include:

-   It finds food and mates
-   It avoids toxins and predators
-   It lays eggs
-   It crawls and there are a bunch of different crawling motions

### Do you simulate all that?

We've started from a cellular approach so we are building behavior of individual cells and we are trying to get the cells to perform those behaviors. We are [starting with simple crawling](https://github.com/openworm/OpenWorm/wiki/Project-overview). The main point is that we want the worm's overall behavior to emerge from the behavior of each of its cells put together.

### So say the virtual organism lays eggs. Are the eggs intended to be new, viable OpenWorms, or is fertilization not a goal?

Right now we aren't addressing the egg laying or development capacity, however, the worm does have the [best known developmental history of any organism](https://docs.google.com/file/d/0B_t3mQaA-HaMbEtfZHhqUmRIX1E/edit?usp=sharing) so it would be really interesting to work on a computational development model.

### Does it need to know how to be a worm to act like a worm?

The "logic" part comes from the dynamics of the neurons interacting with each other. it is a little unintuitive but that's why makes up how it "thinks". So we are simulating those dynamics as well as we can rather than instructing it what to do when. Of course that will require a good mechanical model of how CE muscles respond to stimulation.

### Given all that we DON'T know about _C. elegans_ (all the various synaptic strengths, dynamics, gap junction rectification, long-range neuromodulation, etc.), how do you know the model you eventually make truly recapitulates reality?

All models are wrong, some models are useful :) We must have the model make a prediction and then test it. Based on how well the model fits the available data, we can quantify how well the model recapitulates reality.

We are currently evaluating the database behind [a recent paper on _C. elegans_ behavioral analysis](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3545781/pdf/pnas.201211447.pdf), which [resides here](http://wormbehavior.mrc-lmb.cam.ac.uk/index.php), as the standard we will use to test the model's external behavior. More on this [here](https://www.youtube.com/watch?v=YdBGbn_g_ls).

As an analogy to what we are aiming for, we are inspired by the work of the Covert lab in the creation of a [whole cell simulation](https://www.dropbox.com/s/jjzxw5f55z8nf5v/A%20Whole-Cell%20Computational%20Model%20Predicts%20Phenotype%20from%20Genotype%20-%20Karr%20et%20al.%20-%202012.pdf) that predicts phenotype from genotype at 80% accuracy. This is just a single cell model, but it has the same challenges of high complexity and fundamental understanding gaps that must be bridged via good assumptions.

### Is there only one solution to all those variables in the connectome that will make a virtual _C. elegans_ that resembles a real one, or are there multiple?

It is very likely to be multiple, [given what we know about the variability of neuronal networks in general](https://www.dropbox.com/s/rbab411kf5rb4zh/Similar%20network%20activity%20from%20disparate%20circuit%20parameters.%20-%20Prinz%2C%20Bucher%2C%20Marder%20-%202004.pdf). One technique to deal with this is to [generate multiple models that work](https://www.dropbox.com/s/05zx02h57vpvvqg/Multiple%20models%20to%20capture%20the%20variability%20in%20biological%20neurons%20and%20networks%20-%20Marder%2C%20Taylor%20-%202011.pdf) and analyze them under different conditions. What we are after is the [solution space that works](https://www.dropbox.com/s/hz2pv5cvomvsqez/Complex%20parameter%20landscape%20for%20a%20complex%20neuron%20model.%20-%20Achard%2C%20De%20Schutter%20-%202006.pdf) (see Fig 6 for an example), rather than a single solution. That said, it is extremely likely that the solution space is much smaller than the complete space of possibilities.

### Why not start with simulating something simpler? Are nematodes too complex for a first go at whole organism simulation?

Nematodes have been studied far more than simpler multi-cellular organisms, and therefore more data exist that we can use to build our model. We would need to get, for example, another connectome and another anatomical 3D map whereas in _C. elegans_ they already exist. The community of scientists using _C. elegans_ as their model organism is much larger than communities that studying simpler multi-cellular organisms, so the effect of the community size also weighed in on the decision.

### When do you think the simulation will be "complete", and which behaviors would that include?

Completion is a functional standard -- so it is complete when it fits all available data about worm behavior. Today, the gold standard for available data about worm behavior is encapsulated in the WormBehavior database, [described here](https://www.youtube.com/watch?v=YdBGbn_g_ls). More information from [the paper](https://www.dropbox.com/s/tqr3abcrr8dt3bi/A%20database%20of%20Caenorhabditis%20elegans%20behavioral%20phenotypes.%20-%20Yemini%20et%20al.%20-%202013.pdf).

At the moment we are focusing on integrating an electrophysiological simulation of the nervous system with a elastic matter and fluid dynamics simulation for how the body of the worm interacts with the environment. You can [read more about this here](https://github.com/openworm/OpenWorm/wiki/Project-overview)

Once the simulation of the nervous system is driving the physics-enabled body of the worm around a simulated petri dish, it will be comparable to the WormBehavior database. The degree of overlap between the simulated worm and the behavior of real worms will be very interesting to see --we are very curious to find this out!

### Currently, what are your biggest problems or needs?

To make this project move faster, we'd love more help from motivated folks. Both programmers and experimentalists. We have a lot we want to do and not enough hands to do it. People who are skeptical about mammal whole-brain simulations are prime candidates to be enthusiastic about whole-worm simulations. Read more about ways to help [on our website](http://www.openworm.org/get_involved.html).

### Where I could read about your "to do's?"

We have a set of [high level milestones](https://github.com/openworm/OpenWorm/issues/milestones) for the modeling direction we are taking up on GitHub. We also have [a master board of all issues](https://github.com/orgs/openworm/projects/9) across all our GitHub repositories that show a bunch of programming tasks we are working on.

### How do I know which issues are safe to work on? How do I know I won't be stepping on any toes of work already going on?

The [high-volume mailing list](https://groups.google.com/forum/?fromgroups#!forum/openworm-discuss) is the organizing mechanism of first resort when determining these questions. If you are interested in helping with an issue but don't know if others are working on it, search on the list, and if you don't see a recent update, post on the list and ask. The mechanism of second resort is to ask a question in the comment thread of the GitHub issue. All contributors are advised to report on their effort on the mailing list or on the GitHub issue as soon as they start working on a task in order to let everyone know. As much as possible we avoid doing work that don't get exposed through one or both of these mechanisms.

In general, you won't step on any toes though -- multiple people doing the same thing can still be helpful as different individuals bring different perspectives on tasks to the table.

### Do you all ever meet up somewhere physically?

Subsets of us meet frequently, and there have been two meetings of the core OpenWorm team, one in [Paris in July 2014](https://openworm.tumblr.com/post/57193347335/community-updates-from-openworm-in-paris), and a second in London in Fall of 2014.  We use Google+ hangout to meet face to face on a regular basis in general meetings and in standing meetings of the subprojects.

OpenWorm simulation and modeling
--------------------------------

### What is the level of granularity of these models (ie. cells, subcellular, etc.), and how does that play out in terms of computational requirements?

In order to make this work we have to make use of abstraction in the computer science sense, so something that is less complex today can be swapped in for something more complex tomorrow. This is inherent in the design of the simulation engine we are building

Right now our model of the electrical activity neurons is based on the Hodgkin Huxley equations. The muscles and the physical body of the worm are governed by an algorithm known as "smoothed particle hydrodynamics." So our initial complexity estimates are based on asking how much CPU horsepower do we need for these algorithms.

### What's the data source for your computer simulation of the living worm?

There is not a single data source for our simulation; in fact one of our unique challenges is coming up with new ways to work out how to integrate multiple data sets together. Here is a list of some of the data sets that we have used so far:

-   [The Virtual Worm (3D atlas of _C. elegans_ anatomy)](http://caltech.wormbase.org/virtualworm/)
-   [The _C. elegans_ connectome (wiring diagram of neurons)](http://www.wormatlas.org/neuronalwiring.html)
-   [Cell list of _C. elegans_](https://docs.google.com/spreadsheet/pub?key=0Avt3mQaA-HaMdGFnQldkWm9oUmQ3YjZ1LXJ4OHFnR0E&output=html)
-   [Ion channels used by _C. elegans_](https://docs.google.com/spreadsheet/pub?key=0Avt3mQaA-HaMdEd6S0dfVnE4blhaY2ZIWDBvZFNjT0E&output=html)
-   [Database of Worm behavioral phenotypes](http://www.ncbi.nlm.nih.gov/pubmed/23852451)

### Has there been previous modeling work on various subsystems illustrating what level of simulation is necessary to produce observed behaviors?

There have been [other modeling efforts in _C. elegans_ and their subsystems](http://www.artificialbrains.com/openworm#similar), as well as in academic journal articles. However, the question of "what level of simulation is necessary" to produce observe behaviors is still an open question.

### How are neurons simulated today?

There are a [number of neuronal simulators in use](http://software.incf.org/software/?getTopics=Computational%20neuroscience&b_start:int=0), and we have done considerable amount of work on top of one in particular, the [NEURON simulation environment](http://www.scholarpedia.org/article/Neuron_simulation_environment).

There are a wide variety of ways to simulate neurons, as shown in [figure two](http://i.imgur.com/aRGyCP3.png) of [Izhikevich 2004](http://www.ncbi.nlm.nih.gov/pubmed/15484883).

### What does a neuronal simulator do?

It calculates a system of equations to produce a read out of the changing membrane potential of a neuron over time. Some simulators enable ion channel dynamics to be included and enable neurons to be described in detail in space (multi-compartmental models), while others ignore ion channels and treat neurons as points connected directly to other neurons. In OpenWorm, we focus on multi-compartmental neuron models with ion channels.

### What is the connection between the basic proporties of _C. elegans_ neurons and human neurons?

_C.elegans_ neurons do not spike (i.e. have [action potentials](http://en.wikipedia.org/wiki/Action_potential)), which makes them different from human neurons. However, the same mathematics that describe the action potential (known as the [Hodgkin-Huxley model](http://en.wikipedia.org/wiki/Hodgkin%E2%80%93Huxley_model)) also describe the dynamics of neurons that do not exhibit action potentials. The biophysics of the neurons from either species are still similar in that they both have [chemical synapses](http://en.wikipedia.org/wiki/Chemical_synapse), both have [excitable cell membranes](http://en.wikipedia.org/wiki/Cell_membrane), and both use [voltage sensitive ion channels](http://en.wikipedia.org/wiki/Voltage-gated_ion_channel) to modify the [electrical potential across their cell membranes](http://en.wikipedia.org/wiki/Membrane_potential).

### What is the level of detail of the wiring diagram for the non-neuron elements?

There is a map between motor neurons and muscle cells in the published wiring diagram. There isn't much of a wiring diagram that touches other cell types beyond that. There is an anatomical atlas for where they are located. And you can work out the influence between cells based on molecular signals (known as peptides).

### How much new electrophysiological data will the project need to achieve its goals?

We are hoping that we get neuron by neuron fast calcium imaging of a lot of neurons.

### How will the parameters of the neurons be inferred from calcium imaging?

Basically we will use model optimization / genetic algorithms to search the parameter space for parameters that are unknown.

### What are you using genetic algorithms in OpenWorm for?

Because there are a lot of unknowns in the model, we use genetic algorithms (or more generally model optimization techniques) to help us generate many of possible models to match experimental data and then pick the ones most likely to be correct. [Here's a paper](https://www.dropbox.com/s/05zx02h57vpvvqg/Multiple%20models%20to%20capture%20the%20variability%20in%20biological%20neurons%20and%20networks%20-%20Marder%2C%20Taylor%20-%202011.pdf) that describes a process like this.

### What will the fitness function be?

Here are [some](https://twitter.com/OpenWorm/status/331818549834285058) [examples](https://twitter.com/OpenWorm/status/336831501222178817)

### How do you plan to extend its methods from single neurons to multiple neurons?

This project is all about biting off small workable pieces of the problem. The plan there is to chain this method. We are starting from a muscle cell whose example electrophysiology we have. Then we will approximate the six motor neurons synapsing onto it based on what we know about its ion channels and whatever more we can gather based on calcium imaging.Then we will be exploring how to tune the combined system of the single muscle cell with the 6 motor neurons connected to it as a network and radiate outwards from there.

### Do you need a connectome for these gap junctions as well or should an accurate enough cell model suffice?

The gap junctions are included in the _C. elegans_ connectome.

### What's the main differences between the single and multi-compartment models?

Single compartment models lack sufficient detail to capture the detailed shape of the neuron or muscle, which has been shown to influence the dynamics of the cell as a whole. Basically, only multi-compartment models get close enough to be comparable to real biology.

### What is NeuroML and what does it represent?

An introduction to NeuroML is available [on their website](https://neuroml.org/). In short, it is an XML based description of biological descriptions of neurons.

### How is excitation and inhibition in neurons handled in OpenWorm?

Inhibition and excitation will be handled via synapses. Different neurotransmitters and receptors are encoded in our model of the nervous system. Some of those include Glutamate "excitatory" and GABA "inhibitory." We have encoded information about the neurons in the [OpenWorm NeuroML spatial connectome](https://github.com/openworm/OpenWorm/wiki/C.-Elegans-NeuroML)

### How do I run the NeuroML connectome?

[Get the connectome NeuroML project](https://github.com/openworm/OpenWorm/wiki/Running-the-C.-elegans-model-in-neuroConstruct#getting-the-latest-celegans-neuroconstruct-project) that contains it and [load it up in NeuroConstruct](https://github.com/openworm/OpenWorm/wiki/Running-the-C.-elegans-model-in-neuroConstruct). [Install the NEURON simulation environment](http://www.neuron.yale.edu/neuron/download) and set the path to NEURON's bin directory containing nrniv within neuroConstruct's menu (Settings-\>General Preferences and Project Defaults). After generating cell positions (easiest to do this with the PharyngealNeurons\_inputs configuration), go to the export tab, the NEURON subtab, and press 'create hoc simulation'. Once this is completed the button will stop being greyed out and the 'Run simulation' button will be available. Clicking this should kick off the simulation run. Once this is completed, the output from the simulation should tell you that results are available in a directory named 'Sim\_XX' where XX will be a number. Go back to the Visualisation tab and click 'View Prev Sims in 3D..." Click on the box with the 'Sim\_XX' name that applies to the simulation run you did and press 'Load Simulation' at the bottom. Then at the bottom of the Visualisation screen click 'Replay' and the 'Replay simulation'. For PharyngealNeurons\_inputs, the color changes will be subtle, but they will be happening.

### I generated positions for the connectome in NeuroConstruct and tried to export to NEURON but it said NEURON was not found!

Double check that you have set the path to NEURON's **bin** directory containing nrniv within neuroConstruct's menu (Settings-\>General Preferences and Project Defaults). Just pointing to the root where the bin directory is located will **NOT** work.

### How does the NemaLoad project relate to OpenWorm?

We both want to see the _C. elegans_ reverse engineered as a means of understanding nervous systems. We've met a few times and David Darlymple contributes to the project and on the mailing list. We have a different approach right now, but they are complementary and could be unified down the road. Both projects have a lot of up front development work that we are doing now, us mainly in software and integrating data that already exists and David in building an ambitious experimental set up to collect a never-before-gathered data set.

### What is SPH?

[Smoothed Particle Hydrodynamics](http://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics#Uses_in_solid_mechanics). More information is [available online.](http://www.zora.uzh.ch/29724/1/Barbara.pdf)

### What are you doing with SPH?

We are building the body of the worm using particles that are being driven by SPH. This allows for physical interactions between the body of the worm and its environment.

OpenWorm code reuse
-------------------

### What are LEMS and jLEMS?

[LEMS (Low Entropy Model Specification)](http://lems.github.io/jLEMS/) is a compact model specification that allows definition of mathematical models in a transparent machine readable way. [NeuroML 2.0](https://docs.neuroml.org/Userdocs/NeuroMLv2.html) is built on top of LEMS and defines component types useful for describing neural systems (e.g. ion channels, synapses). [jLEMS](https://lems.github.io/LEMS/) is the Java library that reads, validates, and provides basic solving for LEMS. A utility, [jNeuroML](https://github.com/NeuroML/jNeuroML), has been created which bundles jLEMS, and allows any LEMS or NeuroML 2 model to be executed, can validate NeuroML 2 files, and convert LEMS/NeuroML 2 models to multiple simulator languages (e.g. NEURON, Brian) and to other formats.

### What is OSGi and how is it being used?

OSGi is a code framework that is at the heart of Geppetto. One of the basic underpinnings of [object-oriented programming](https://en.wikipedia.org/wiki/Object-oriented_programming) is that code modules should have low coupling-- meaning that code in one part of your program and code in another part of your program should minimize calling each other. Object oriented languages like Java help to enable programs to have low coupling at compile time, but it has been recognized that in order to have true modularity, the idea of low coupling needed to be extended through to run-time. OSGi is a code framework in Java that does this. With OSGi, code modules can be turned on and off at run-time without need for recompile. This provides for an extremely flexible code base that enables individual modules to be written with minimal concern about the rest of the code base.

This matters for OpenWorm as we anticipate many interacting modules that calculate different biological aspects of the worm. So here, each algorithm like Hodgkin Huxley or SPH can be put into an OSGi bundle in the same way that future algorithms will be incorporated. Down the road, this makes it far more likely for others to write their own plugin modules that run within Geppetto.

### What is Spring and how is it being used?

Spring is a code framework being used at the heart of Geppetto. It enables something called 'dependency injection', which allows code libraries that Geppetto references to be absent at compile time and called dynamically during run-time. It is a neat trick that allows modern code bases to require fewer code changes as the libraries it depends on evolves and changes. It is important for Geppetto because as it increasingly relies on more external code libraries, managing the dependencies on these needs to be as simple as possible.

### What is Tomcat and how is it being used?

Tomcat is a modern web server that enables Java applications to receive and respond to requests from web browsers via HTTP, and Geppetto runs on top of this. It has no OSGi functionality built into it by itself, that's what Virgo adds.

Geppetto implements OSGi via a Virgo server which itself runs on top of Tomcat. It is a little confusing, but the upshot is that Geppetto avoids having to build components like a web server and focus only on writing code for simulations.

### What is Virgo and how is it being used?

Virgo is a web server that wraps Tomcat and uses OSGi as its core framework, and Geppetto runs on top of this. On top of the code modularity framework that OSGi provides, Virgo adds the ability to receive and respond to requests from web browsers via HTTP. It is important for Geppetto because it is a web-based application.

### What is Maven and how is it being used?

Maven is a dependency management and automated build system for Java that is used by Geppetto to keep track of all the libraries it uses. If you are familiar with Make files, Maven provides a more modern equivalent in the form of a project object model file, or pom.xml. Whereas Spring is a library that appears in source code, Maven operates external to a code base, defining how code will get built and what libraries will be used. Maven enables external code libraries to be downloaded from the internet upon run time, which helps to avoid the bad programming practice of checking all your libraries into version control repositories.

It is important for OpenWorm because as Geppetto increasingly relies on other code libraries, we need easy ways to manage this.

OpenWorm links and resources
----------------------------

### Do you have a website?

<http://openworm.org>

### Where can I send my inquiries about the project?

<info@openworm.org>

### Where can I find the "worm browser"?

<http://browser.openworm.org>

### How do I join the public mailing list?

More info here: <http://www.openworm.org/contacts.html>

### Where are downloads located?

<http://www.openworm.org/downloads.html>
