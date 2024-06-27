Optimization engine
===================

The Optimization engine uses optimization techniques like genetic algorithms to help fill gaps in our knowledge of the electrophysiology of _C. elegans_ muscle cells and neurons.

These two algorithms, Hodgkin-Huxley and SPH, require parameters to be set in order for them to function properly, and therefore create some "known unknowns" or "free parameters" we must define in order for the algorithm to function at all. For Hodgkin-Huxley we must define the ion channel species and set their conductance parameters. For SPH, we must define mass and the forces that one set of particles exert on another, which in turn means defining the mass of muscles and how much they pull. The conventional wisdom on modeling is to minimize the number of free parameters as much as possible, but we know there will be a vast parameter space associated with the model.

To deal with the space of free parameters, two strategies are employed. First, by using parameters that are based on actual physical processes, many different means can be used to provide sensible estimates. For example, we can estimate the volume and mass of a muscle cell based on figures that have been created in the scientific literature that show its basic dimensions, and some educated guesses about the weight of muscle tissue. Secondly, to go beyond educated estimates into more detailed measurements, we can employ model optimization techniques. Briefly stated, these computational techniques enable a rational way to generate multiple models with differing parameters and choose those sets of parameters that best pass a series of tests. For example, the conductances of motor neurons can be set by what keeps the activity those neurons within the boundaries of an appropriate dynamic range, given calcium trace recordings data of those neurons as constraints.

Previous accomplishments
------------------------

- Genetic algorithms applied to tuning muscle cell models

Current roadmap
---------------

### [STORY: Muscle Cell model output closely matches that of real data](https://github.com/openworm/OpenWorm/milestone/13?closed=1)

We will show that we have built a model of _C. elegans_ muscle cell that matches data recorded from the nematode muscle cell. In part, we will use techniques of model optimization to fill in gaps in the model parameter space (deduce unmeasured parameters). The main technical challenge is tuning muscle cell passive properties and building a larger data set (more cell recordings).

### Bionet: training _C. elegans_ with a specialized genetic algorithm

The _C. elegans_ connectome is a neural network wiring diagram that specifies synaptic neurotransmitters and junction types. It does not however quantify synaptic connection strengths. It is believed that measuring these must be done in live specimens, requiring emerging or yet to be developed techniques. Without the connection strengths, it is not fully known how the nematode's nervous system produces sensory-motor behaviors.

Bionet is an attempt to compute the connection strengths that produce desired sensory-motor behaviors. This is done by a hybrid genetic algorithm that trains a large space of 3000+ weights representing synapse connection strengths to perform given sensory-motor sequences. The algorithm uses both global and local optimization techniques that take advantage of the topology of the connectome. An artificial worm embodying the connectome and trained to perform sensory-motor behaviors taken from measurements of the actual _C. elegans_ would then behave realistically in an artificial environment. This is an important step toward creating a fully functional artificial worm. Indeed, knowing the artificial weights might cast light on the actual ones.

Using the NEURON simulation tool as a fitness evaluation function, the pharyngeal neuron assembly has been trained to produce given activation patterns, reducing activation differences from more than 50% to less than 5%. Looking ahead, training worm locomotion behaviors using Movement Validation measurements as models will allow the neural network to drive the Sibernetic body model realistically.

Issues list
-----------

none

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
<td align="left"><a href="https://github.com/openworm/HeuristicWorm">HeuristicWorm</a></td>
<td align="left">Executes a genetic algorithm to train a model of a neuron</td>
<td align="left"><blockquote>
<p>C++</p>
</blockquote></td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/bionet">bionet</a></td>
<td align="left">Artificial neural network for training <em>C. elegans<em> behaviors</td>
<td align="left"><blockquote>
<p>C++</p>
</blockquote></td>
</tr>
</tbody>
</table>
