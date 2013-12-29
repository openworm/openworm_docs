*************************
OpenWorm Modeling Approach
**************************

Neuromechanical modeling
========================

While our ultimate goal is to simulate every cell in the c. Elegans, we
are starting out by building a model of its body, its nervous system,
and its environment.

To get a quick idea of what this looks like, check out the `CyberElegans
prototype <http://www.youtube.com/embed/3uV3yTmUlgo>`__. In this movie
you can see a simulated 3D c. elegans being activated in an environment.
Its muscles are located around the outside of its body, and as they turn
red, they are exerting forces on the body that cause the bending to
happen. In turn, the activity of the muscles are being driven by the
activity of neurons within the body.

These steps are outlined in blue text of the figure below:

|Greatly oversimplified causation loop|

Our end goal for the first version is to complete the entire loop. We
believe that this is the most meaningful place to begin because it
enables us to study the relationship between a nervous system, the body
it is controlling, and the environment that body has to navigate. We
also believe this is a novel development because there are no existing
computational models of any nervous systems that complete this loop.

When we first started, our team in Novosibirsk had produced an awesome
prototype. We recently published `an
article <http://iospress.metapress.com/content/p61284485326g608/?p=5e3b5e96ad274eb5af0001971360de3e&pi=4>`__
about it. If you watch `the movie that goes along with the
prototype <http://www.youtube.com/watch?v=3uV3yTmUlgo>`__, you can see
the basic components of the loop above in action:

|CyberElegans with muscle cells|

Here muscle cells cause the motion of the body of the worm along the
surface of its environment.

|Inside the CyberElegans model|

Inside the worm, motor neurons are responsible for activating the
muscles, which them makes the worms move. The blue portions of the loop
diagram above are those aspects that are covered by the initial
prototype. We are now in the process of both adding in the missing
portions of the loop, as well as making the existing portions more
biologically realistic, and making the software platform they are
operating on more scalable.

One of the aspects of making the model more biologically realistic has
been to incorporate a `3d model of the
anatomy <http://browser.openworm.org/>`__ of the worm into the
simulation. Instead of the blue motor neurons you can see in the
prototype, we have incorporated much more detailed models of neurons as
seen below:

|Neurons in WormBrowser|

This is a much more faithful representation of the neurons and their
positions within the worm's body. In addition, the muscle cells are
represented more realistically:

|Muscle cells in c. elegans|

Another component of making the model more biophysically realistic is to
use more sophisticated mathematics to drive the simulation that keep it
more closely tied to real biology. This is important because we want the
model to be able to inform real biological experiments and more
coarse-grained, simplified mathematics falls short in many cases.

Specifically for this loop, we have found that two sets of equations
will cover both aspects of the loop, broadly speaking:

|Simple loop overlaid with solvers|

As you can see, where the two sets of equations overlap is with the
activation of muscle cells. As a result, we have taken steps to use the
muscle cell as a pilot of our more biologically realistic modeling, as
well as our software integration of different set of equations assembled
into an algorithmic "solver". We have chosen a specific muscle cell to
target:

|Muscle cell highlighted|


Data collection and representation
----------------------------------

NeuroML Connectome
~~~~~~~~~~~~~~~~~~

Our computational strategy to accomplish this involves first reusing the
`c. elegans
connectome <http://dx.plos.org/10.1371/journal.pcbi.1001066>`__ and the
`3D anatomical map of the c. elegans nervous system and body
plan <http://g.ua/MhxC>`__. We have used the NeuroML standard (`Gleeson
et al., 2010 <http://dx.plos.org/10.1371/journal.pcbi.1000815>`__) to
describe the 3D anatomical map of the c. elegans nervous system. This
has been done by discretizing each neuron into multiple compartments,
while preserving its three-dimensional position and structure. We have
then defined the connections between the NeuroML neurons using the c.
elegans connectome. Because NeuroML has a well-defined mapping into a
system of Hodgkin-Huxley equations, it is currently possible to import
the “spatial connectome” into the NEURON simulator (`Hines & Carnevale
1997 <http://www.ncbi.nlm.nih.gov/pubmed/9248061>`__) to perform *in
silico* experiments.

Community outreach
------------------

Muscle cell integration
-----------------------

Optimization - Pyramidal
~~~~~~~~~~~~~~~~~~~~~~~~

These two algorithms, Hodgkin-Huxley and SPH, require parameters to be
set in order for them to function properly, and therefore create some
“known unknows” or “free parameters” we must define in order for the
algorithm to function at all. For Hodgkin-Huxley we must define the ion
channel species and set their conductance parameters. For SPH, we must
define mass and the forces that one set of particles exert on another,
which in turn means defining the mass of muscles and how much they pull.
The conventional wisdom on modeling is to minimize the number of free
parameters as much as possible, but we know there will be a vast
parameter space associated with the model.

To deal with the space of free parameters, two strategies are employed.
First, by using parameters that are based on actual physical processes,
many different means can be used to provide sensible estimates. For
example, we can estimate the volume and mass of a muscle cell based on
figures that have been created in the scientific literature that show
its basic dimensions, and some educated guesses about the weight of
muscle tissue. Secondly, to go beyond educated estimates into more
detailed measurements, we can employ model optimization techniques.
Briefly stated, these computational techniques enable a rational way to
generate multiple models with differing parameters and choose those sets
of parameters that best pass a series of tests. For example, the
conductances of motor neurons can be set by what keeps the activity
those neurons within the boundaries of an appropriate dynamic range,
given calcium trace recordings data of those neurons as constraints.

Electrophysiology / Mechanics integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. |Greatly oversimplified causation loop| image:: https://docs.google.com/drawings/d/1a_9zEANb4coI9xRv2fFu_-Ul9SOnhH_cVHHJgpCNo5I/pub?w=401&h=312
.. |CyberElegans with muscle cells| image:: https://docs.google.com/drawings/d/142NbGecjnWuq6RxWgqREhKOXJ8oDo55wVvBuKQPyKCg/pub?w=430&h=297
.. |Inside the CyberElegans model| image:: https://docs.google.com/drawings/d/1fO_gQI_febpu4iHd1_UDrMNQ_eqvHgJynMqho7UC6gw/pub?w=460&h=327
.. |Neurons in WormBrowser| image:: https://docs.google.com/drawings/d/1GIwzQRvmDtprPBLSGjJhuEHqYqEcKaHLyKK0s80a3lM/pub?w=391&h=224
.. |Muscle cells in c. elegans| image:: https://docs.google.com/drawings/d/1ayyyu6dv0S4-750j-WRYVBEaziZr3g3V1-UIadAfHck/pub?w=391&h=224
.. |Simple loop overlaid with solvers| image:: https://docs.google.com/drawings/d/1xL9NY-QcIeIfKXd-lN_x15fUGLM9vEL_sZzCLDvcT3Q/pub?w=401&h=312
.. |Muscle cell highlighted| image:: https://docs.google.com/drawings/d/1ZzCS0IXTb-n3GgaNLp98HS9X8ngHLtkcnildAYshuME/pub?w=535&h=289
