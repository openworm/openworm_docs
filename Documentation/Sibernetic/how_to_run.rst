.. _sibernetic-documentation:

*************************************
Sibernetic - documentation how to run instruction
*************************************

.. contents::

Clone Sibernetic repository from github on your machine:
::
 git clone https://github.com/openworm/Smoothed-Particle-Hydrodynamics.git
Or download `zip archive <https://github.com/openworm/Smoothed-Particle-Hydrodynamics/archive/master.zip>`_.
If you want to work with worm bory model you need switch to WormBodySimulation branch after cloning
::
 git checkout WormBodySimulation
Or download `zip archive <https://github.com/openworm/Smoothed-Particle-Hydrodynamics/archive/WormBodySimulation.zip>`_.

Linux
=========================

Install OpenCL on Ubuntu. OpenCL drivers depend on devices on which you're planning to run Sibernetic. 
 * `AMD OpenCL drivers <http://developer.amd.com/redirect/?newPage=http://developer.amd.com/tools-and-sdks/opencl-zone/opencl-tools-sdks/amd-accelerated-parallel-processing-app-sdk/>`_ 
 * `Intel OpenCL Drivers <https://software.intel.com/en-us/articles/opencl-drivers>`_
 * `Nvidia OpenCL Drivers <https://developer.nvidia.com/opencl>`_
Install instructions for Ubuntu can be found `here <http://develnoter.blogspot.co.uk/2012/05/installing-opencl-in-ubuntu-1204.html>`_. This step often causes problems, contact the openworm-discuss mailing list if you encounter issues.

Navigate to the project folder and run:
:: 
 make clean
 make all
Than run Sibernetic:
::
  ./Release/Sibernetic
Windows
=========================                                  
Install OpenCL on Windows. OpenCL drivers depend on devices on which you're planning to run Sibernetic. 
 * `AMD OpenCL drivers <http://developer.amd.com/redirect/?newPage=http://developer.amd.com/tools-and-sdks/opencl-zone/opencl-tools-sdks/amd-accelerated-parallel-processing-app-sdk/>`_ 
 * `Intel OpenCL Drivers <https://software.intel.com/en-us/articles/opencl-drivers>`_
 * `Nvidia OpenCL Drivers <https://developer.nvidia.com/opencl>`_
Root folder of project contains solution and project files for run in Microsoft Visual Studio you can build Sibernetic from src.

Mac OS
===========
OpenCL drivers should be on your Mac OS already.
Stay in the top-level folder and run:
::
 make clean -f makefile.OSX
 make all -f makefile.OSX
