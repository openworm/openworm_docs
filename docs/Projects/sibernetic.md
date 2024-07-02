NeuroMechanical Modeling - Sibernetic
=====================================

While our ultimate goal is to simulate every cell in the c. Elegans, we are starting out by building a model of its body, its nervous system, and its environment. [Sibernetic](https://openworm.org/sibernetic/) is the home of the C++ code base that implements the core of the model. We have implemented an algorithm called Smoothed Particle Hydrodynamics (SPH) to simulate the body of the worm and its environment using GPUs. This algorithm has been initially worked out in C++ (with OpenGL visualization).

To get a quick idea of what this looks like, check out the [latest movie](https://www.youtube.com/watch?v=SaovWiZJUWY). In this movie you can see a simulated 3D _C. elegans_ being activated in an environment. Its muscles are located around the outside of its body, and as they turn red, they are exerting forces on the body that cause the bending to happen.

Previous accomplishments
------------------------

-   Physics tests
-   Initial worm crawling

Current roadmap
---------------

### [Electrofluid Paper](https://github.com/openworm/OpenWorm/issues?milestone=17&state=closed)

We are writing a manuscript focusing on the work we have to implement SPH in the project and apply it to muscle cells and the worm body. [@vellamike](https://github.com/vellamike), [@a-palyanov](https://github.com/a-palyanov) and [@skhayrulin](https://github.com/skhayrulin) are taking the lead on this.

The proposal is to do this after the Sibernetic proof of concept worm wiggling, both of which have since been completed.

Issues list
-----------

All issues related to the [Sibernetic code base](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=sibernetic&page=1&sort=comments&state=open) can be found on GitHub.

Associated Repositories
-----------------------

<table>
<colgroup>
<col width="45%" />
<col width="50%" />
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
<td align="left"><a href="https://github.com/openworm/Smoothed-Particle-Hydrodynamics">Smoothed-Particle-Hydrodynamics</a></td>
<td align="left"><dl>
<dt>The Sibernetic code base containing the 2014 version of the worm body model,</dt>
<dd><p>a C++ implementation of the Smoothed Particle Hydrodynamics algorithm customised for the OpenWorm project.</p>
</dd>
</dl></td>
<td align="left">C++</td>
</tr>
<tr class="even">
<td align="left"><a href="https://github.com/openworm/ConfigurationGenerator">ConfigurationGenerator</a></td>
<td align="left">Generation start scene configuration for PCI SPH solver</td>
<td align="left">JavaScript</td>
</tr>
<tr class="odd">
<td align="left"><a href="https://github.com/openworm/CyberElegans">CyberElegans</a></td>
<td align="left">Circa 2010 Neuromechanical model of C. Elegans</td>
<td align="left">C++</td>
</tr>
</tbody>
</table>
