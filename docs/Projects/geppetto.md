Geppetto Simulation Engine
==========================

In order to allow the world to play with the model easily, we are engineering [Geppetto](http://geppetto.org), an open-source modular platform to enable multi-scale and multi-algorithm interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers out-of-the-box visualization of simulated models right in the browser. You can read about architectural concepts and learn more about the different plug-in bundles we are working on.

Geppetto, is written in Java and leverages technologies like [OSGi](http://www.osgi.org/), [Spring Framework](http://www.springsource.org/spring-framework), [OpenCL](http://www.khronos.org/opencl/) and [Maven](http://maven.apache.org/).

Geppetto's frontend is written using [THREE.js](http://mrdoob.github.com/three.js/) and [WebGL](http://www.khronos.org/webgl/). Back-end / front-end communication happens via [JSON](http://www.json.org/) messages through [WebSocket](http://www.websocket.org/).

The engine runs on on Eclipse Virgo WebServer deployed on an Amazon [Elastic Compute Cloud](http://aws.amazon.com/ec2/) Linux instance.

Previous accomplishments
------------------------

-   Past releases of Geppetto

Current roadmap --------------

[STORY: Worm wiggling in the browser](https://github.com/openworm/OpenWorm/issues?milestone=21&state=open) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a user, I want to see the proof of concept sibernetic worm in my web browser so that anyone around the world can play with it.

Practically, this means porting the proof of concept scene into Geppetto.

[STORY: Interactive worm wiggling in browser](https://github.com/openworm/OpenWorm/issues?milestone=23&state=open) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a user, I want to be able to see a visualization of the proof of concept worm wiggling in my web browser and be able to perturb it in a manner that causes the wiggling to change in a realistic manner.

This milestone suggests interactivity via Geppetto. The kind of perturbation is not defined yet-- ideally we should aim for the simplest kind we can think of that gives the user an interface to make modifications.

Issues list
-----------

The issues related to Geppetto are distributed across different repositories.

Issues related to general functionalities that need to be added to support the OpenWorm simulation are found [here](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=geppetto&page=1&sort=comments&state=open).

Issues related to the platform in general are found [here](https://github.com/openworm/org.geppetto/issues?state=open).

Ultimately every module of Geppetto has issues of its own, see the list of repositories below.

The issues are so splitted to allow capturing different granularities, having both issues that reflect what macro functionalities need to be added in the OpenWorm and Geppetto repository and having detailed close-to-the-code bugs in the individual repositories.

Associated Repositories ----------------------

<table>
<colgroup>
<col width="67%" />
<col width="25%" />
<col width="7%" />
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
<td align="left"><a href="https://github.com/openworm/org.geppetto">org.gepetto</a></td>
<td align="left">Geppetto Main Bundle and packaging</td>
<td align="left">Java</td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/org.geppetto.solver.sph">org.geppetto.solver.sph</a></td>
<td align="left">PCI SPH Solver bundle for Geppetto</td>
<td align="left">Java</td>
</tr>
<tr class="odd">
<td align="left"><a href="https://github.com/openworm/org.geppetto.simulator.jlems">org.geppetto.simulator.jlems</a></td>
<td align="left">jLEMS based simulator for Geppetto</td>
<td align="left">Java</td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/org.geppetto.model.neuroml">org.geppetto.model.neuroml</a></td>
<td align="left">NeuroML Model Bundle for Geppetto</td>
<td align="left">Java</td>
</tr>
<tr class="odd">
<td align="left"><a href="https://github.com/openworm/org.geppetto.core">org.geppetto.core</a></td>
<td align="left">Geppetto core bundle</td>
<td align="left">Java</td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/org.geppetto.frontend">org.geppetto.frontend</a></td>
<td align="left">Geppetto frontend bundle - Web application</td>
<td align="left">Java</td>
</tr>
<tr class="odd">
<td align="left"><a href="https://github.com/openworm/org.geppetto.testbackend">org.geppetto.testbackend</a></td>
<td align="left">Geppetto test backend for Geppetto</td>
<td align="left">Java</td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/org.geppetto.simulator.sph">org.geppetto.simulator.sph</a></td>
<td align="left">SPH Simulator bundle for Geppetto</td>
<td align="left">Java</td>
</tr>
<tr class="odd">
<td align="left"><a href="https://github.com/openworm/org.geppetto.simulation">org.geppetto.simulation</a></td>
<td align="left">Generic simulation bundle for Geppetto</td>
<td align="left">Java</td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/org.geppetto.model.sph">org.geppetto.model.sph</a></td>
<td align="left">PCI SPH Model Bundle for Geppetto</td>
<td align="left">Java</td>
</tr>
<tr class="odd">
<td align="left"><a href="https://github.com/openworm/org.geppetto.samples">org.geppetto.samples</a></td>
<td align="left">Sample simulations for Geppetto</td>
<td align="left">Descriptive</td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/org.geppetto.templatebundle">org.geppetto.templatebundle</a></td>
<td align="left">Template bundle</td>
<td align="left">Java</td>
</tr>
</tbody>
</table>
