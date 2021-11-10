C. elegans robot
=====================================

One of the goals of the OpenWorm project is to promote awareness of the biology of the C. elegans nematode worm. In the robotics project, 
this takes the form of creating physical implementations of the worm which approximate prevalent scientific models. The downside of this 
is that C. elegans is, of course, not a robot. However, simulating the worm in robotic form manifests a tangible aspect that pure software 
models do not possess. A worm robot also sidesteps working with the actual worm, a transparent 1mm organism, which requires special conditions 
and equipment, such as lighting and microscopes. Another aim of the robotics effort is to foster crossover education in biology, robotics, 
and coding. This can take the form of either specifying or producing kits of parts that can be assembled by students in school settings
or by generally interested parties.

The robot is controlled by a Raspberry Pi/ESP32 processor that contains a recorded simulation of the worm's
neuromuscular system (see references). The robot's body is a sequence of segments that mutually exert simulated muscle
contractions impemented by servos.

Repository
-----------

[OpenWorm robots](https://github.com/openworm/robots) repository on GitHub.

Folders:
1. WormHost: PC code to communicate with the onboard Raspberry Pi.
2. WormRPi: Raspberry Pi onboard code.
3. WormESP32: ESP32 onboard code.
4. WormSim: C. elegans neuromuscular simulator.
5. assembly: parts list, 3D printing .stl shape files, and assembly instructions.
6. docs: robot description.

References
-----------
Boyle, Berri and Cohen, "Gait modulation in C. elegans: an integrated neuromechanical model", Front. Comput. Neurosci., 2012.

Eduardo J. Izquierdo and Randall D. Beer, "An Integrated Neuromechanical Model of Steering in C. elegans", ECAL15

