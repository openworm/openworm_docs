.. _sibernetic-documentation:

*************************************
Sibernetic - PCI SPH algorithm
*************************************

.. contents::

This document contains information about PCI SPH algorithm represent in the works of Barbara Solenthaler [1, 2].

Sсhema
==========================


.. code-block:: python
    
     while animation
        for particle i from particles        # see [ref on neighbor search algorithm]
            find neighbor (i, t)             # fill up neighborMap see [ref on main data sstructures]
        for particle i from particles:
            compute forces F viscosity, gravity, surface tension (i,t)
            initialize pressure p(t)=0
            initialize pressure force F pressure = 0.0
        while rho_error(t+1) >= 3% or iter <= minIteration
            for particle i from particles
                predict velocity v_i(t+1)    # predicted velocity storing in temp variables
                predict position p_i(t+1)    # predicted position storing in temp variables
            for particle i from particles
                predict density rho_i(t + 1) # predicted density storing in temp variables
                predict density variation rho_error(t + 1)
                update pressure p_i(t) += f(rho_error(t + 1))
            for particle i from particles
                compute pressure force F_i pressure(t)
        for particle i from particles
            compute new velocity_i(t + 1)  
            compute new position_i(t + 1)

         

Reference
==========================
[1] - http://www.zora.uzh.ch/29724/1/Barbara.pdf

[2] - http://graphics.ethz.ch/~sobarbar/papers/Sol09/Sol09.pdf
