.. _sibernetic-documentation:

*************************************
Sibernetic - PCI SPH algorithm
*************************************

.. contents::

This document contains information about PCI SPH algorithm represent in the works of Barbara Solenthaler [1]_, [2]_.

Sсheme
==========================
For simulating incompressible liquid PCI SPH method was realized represent in [1]_,[2]_. Main feature of PCI SPH algorithm includes in using Predicted-Corrector schema
"To avoid the time step restriction of WCSPH we propose to use a prediction-
correction scheme based on the SPH algorithm (PCISPH). In our method, the
velocities and positions are temporarily forwarded in time and the new particle
densities are estimated. Then, for each particle, the predicted variation from the
reference density is computed and used to update the pressure values, which in
turn enter the recomputation of the pressure forces. Similar to a Jacobi iteration
for linear systems, this process is iterated until it converges, i.e. until all particle density fluctuations are smaller than a user-defined threshold η (for example 1%). Note that this is a nonlinear problem since we include collision handling and updated kernel values in our iteration process. As a final step, the velocities and positions of the next physics update step are computed."[2]_. 
Also we include calculation of elastic forces for elastic particle - this force calculates by the next way for every elastic particle it takes a set of elastic connections after that 
The PCISPH method is illustrated in scheme below:

  .. code-block:: python
     :linenos:
        
     while animation
        for particle i from particles        # see [ref on neighbor search algorithm]
            find neighbor (i, t)             # fill up neighborMap see [ref on main data structures]
        for particle i from particles:
            compute forces F viscosity, gravity, surface tension (i,t)
            initialize pressure p(t)=0
            initialize pressure force F pressure = 0.0
        for particle i from particles:
            if i is elastic particle:
	        compute forces F elasticity
        while rho_error(t+1) >= 3% or iter <= minIteration
            for particle i from particles
                predict velocity v_i(t+1)    # predicted velocity from predicted
                                             #acceleration which was taken from 
                                             #predicted value of pressure force.                  
                                             #This value is storing in temp variables
                predict position x_i(t+1)    # predicted position storing from
                                             #predicted value of velocity in temp variables
            for particle i from particles
                predict density rho_i(t + 1) # predicted density storing in temp variables
                predict density variation rho_error(t + 1)
                update pressure p_i(t) += f(rho_error(t + 1))
            for particle i from particles
                compute pressure force F_i pressure(t)
        for particle i from particles
            calculate boundary interaction
            calculate membrane interaction
            compute new velocity_i(t + 1)  
            compute new position_i(t + 1)

minIteration usually it equal to 3.
Due to changing and predicting value of pressure value of acceleration and velocity could changing too also as well as position value which storing in special data buffer. From this it possible that it necessary to calculate new list of neighbors but for increasing an efficiency in algorithm current neighbors list is using. "This approximation leads to small errors in the density and pressure estimates. In the case of density overestimation the final real densities show lower fluctuations than the requested threshold 3%. In the opposite case – density underestimation – the correction loop might be aborted prematurely. Such situations are not yet handled in the current implementation but can be avoided by using sufficiently small time steps, or by recomputing the neighborhoods in these particular situations" [2]_. For handling of boundary interaction we use algorithm represented here [3]_. How elastic forces is calculating see `here<>`


Reference
==========================
.. [1] http://www.zora.uzh.ch/29724/1/Barbara.pdf

.. [2] http://graphics.ethz.ch/~sobarbar/papers/Sol09/Sol09.pdf

.. [3] http://cg.informatik.uni-freiburg.de/publications/2010_VRIPHYS_boundaryHandling.pdf
