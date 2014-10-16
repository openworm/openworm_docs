.. _sibernetic-documentation:

*************************************
Sibernetic - main data structures
*************************************

.. contents::

This document contains information about main data structures their format 
and information how they evolving through the simulation.
Each simulation based on SPH methods [1] is representing with a number of particles which interact with each other through equation of motion.
Each particle in simulation could be described with a bunch of physical qualities every quality is needed for obtaining displacement of particular particle at the step (t+1) from values for step (t).

For describing 3D vector 4 cells in array is usually using first 3 is for coordinates and 4th is a auxiliary cell also 4 component vector is needed for better vectorization of array. For taking e.g. position vector of particle with some *id*: 
    .. math::
    
         x_id = position[4 * id + 0]
    
         y_id = position[4 * id + 1]
    
         z_id = position[4 * id + 2]

         p_id = position[4 * id + 3]

**NOTATIONS**

**PARTICLE_COUNT** - number of particles in particular simulation

numOfElasticP - number of elastic particles

H - smoothing radius (support radius) "The support radius h is typically chosen so that the average number of neighbors of a particle is around 30-40." [ref on Solenailer dissertation]

**MAX_NEIGHBOR_COUNT** - maximal numbers of neighbors it's equal to 32. 

**MAX_MEMBRANES_INCLUDING_SAME_PARTICLE** - max number of membranes for one particle it's equal to 7

**XMIN**, **YMIN**, **ZMIN** - coordinates of lowest point of boundary box usually it equal to 0

**XMAX**, **YMAX**, **ZMAX** - coordinates of highest point of boundary box

Physical Properties
=========================
position
---------------------------
Containing information about current positions for all particles. Position buffer is represent as a 1d array with size = 4 * **PARTICLE_COUNT** * (1 + 1). In first 4 * **PARTICLE_COUNT** cells of array information about position is stored in next cells information stored information needed for membrane handling [ref to membrane handling algorithm].

velocity
---------------------------                                  
Containing information about current velocities for all particles. Velocity buffer is represent as a 1d array with size = 4 * **PARTICLE_COUNT** * 2 the same as in position buffer.

acceleration
---------------------------
Containing information about current accelerations for all particles. 
    .. math::
            a_i m_i = F^viscosity_i + F^surfaceTension_i + F^gravity_i + F^elasticInteraction_i + F^muscleForce_i + F^pressure_i
:math:`F^elasticInteraction_i, F^muscleForce_i` could be zero for sure it's calculating only for muscle fibers and elastic connections between elastic particles.
Acceleration buffer is represent as a 1d array with size = 4 * **PARTICLE_COUNT** * 3 firs block  from 0 to 4 * **PARTICLE_COUNT** - 1 stores information about impact of ViscosityForces, SurfaceTension, GravityForces, ElasticForces  and MuscleForce forces to acceleration of particle second block from 4 * **PARTICLE_COUNT** to 4 * PARTICLE_COUNT * 2 - 1 storing information about impact of PressureForces force during work of predictive-corrective cycle [ref to PCI SPH algorithm] and last one block storing information about acceleration taking on previous time step it needed for explicit integration methods like LeapFrog [ref]. 

rho
---------------------------
Containing information about density for all particles. Density buffer is represent as a 1d array with size = 2 * **PARTICLE_COUNT** in first block from 0 to **PARTICLE_COUNT** - 1 contains current value of density for all particles at the same time second block contains information about predicted value of density for more info see [ref to PCI SPH algorithm].

elasticConnectionsData
--------------------------
List of connection vector. Elastic connection buffer is represent as a 1d array with size =  numOfElasticP * **MAX_NEIGHBOR_COUNT** * 4. For every elastic particle **MAX_NEIGHBOR_COUNT** connection vector is allocated. Connection vector is a 4 component vector in first cell of which it contains id of particle which connected with this in second cell it contains information about distance between this two particles 3th cell contains info about muscle to which this connection or fiber is belonging.

muscle_activation_signal
------------------------
Array storing data (activation signals) for an array of muscles. 

Data structures needed for Neighbour search algorithm
======================
In next subsection data structures needed for neighbour search algorithm is described [ref on neighbor search alogorithm]

sortedPosition
----------------------
Array storing information about positions after sorting for more info see [ref on neighbor search alogorithm]. After finish of neighbor search we work with this buffers.

sortedVelocity
----------------------
Array storing information about velocities after sorting for more info see [ref on neighbor search alogorithm]. After finish of neighbor search we work with this buffers. For every particles 

neighborMap
----------------------
Contains information about neighbors for all particles size = **PARTICLE_COUNT** * **MAX_NEIGHBOR_COUNT** * 2. In this map information stored in 2D vectors first component of which is indicate an id of neighbour particle and second stored size of distance length. For every particle **MAX_NEIGHBOR_COUNT** of such vector is allocated. List of neighbour for particular particle with *id = i* is equal to sequence of cells in neighborMap with start = i * **MAX_NEIGHBOR_COUNT** * 2 and end = (i * **MAX_NEIGHBOR_COUNT** + **MAX_NEIGHBOR_COUNT** - 1) * 2

particleIndex
----------------------
List of pairs [CellIndex, particleIndex] needed for neighbor search. Size of particleIndex is equal to **PARTICLE_COUNT** * 2.

particleIndexBack
----------------------
List of particleIndex before sorting

gridCellIndex
----------------------
Buffer with position of in particleIndex from which  located in the cell right now gridCellIndex[i] = someNumber, if cell has no particles it's equal -1. . Size of  = gridCellsX * gridCellsY * gridCellsZ
where

    .. math::
           gridCellsX = \frac{\left \lfloor \textbf{XMAX} - \textbf{XMIN} \right \rfloor}{H} + 1
    
           gridCellsY = \frac{\left \lfloor \textbf{YMAX} - \textbf{YMIN} \right \rfloor}{H} + 1
    
           gridCellsZ = \frac{\left \lfloor \textbf{ZMAX} - \textbf{ZMIN} \right \rfloor}{H} + 1

gridCellIndexFixedUp
-------------------------
The same that gridCellIndex but without empty cells.

Membrane handling data buffers
===========================

membraneData
----------------
Elementary membrane is built on 3 adjacent particles (i,j,k) and should have a form of triangle highly recommended that i-j, j-k and k-i are already connected with springs to keep them close to each other during whole lifetime of the simulation.

particleMembranesList
-------------------------
Potentially any particle can be connected with others via membrane(s) this buffer contains **MAX_MEMBRANES_INCLUDING_SAME_PARTICLE** integer data cells per particle
each cell can contain -1 in case when no or no more membranes are associated with this particle, or the index of corresponding membrane in membraneData list otherwise.

Reference
==========================
[1] - http://en.wikipedia.org/wiki/Smoothed-particle_hydrodynamics
