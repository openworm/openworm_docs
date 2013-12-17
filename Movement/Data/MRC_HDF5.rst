Data Source :

`ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura
Grundy`_

`First GitHub Issue`_

`ftp details`_

The data itself is a structure stored in Matlab's version of HDF5. For
the most part the structure is straightforward.

Two exceptions are: - object arrays
https://gist.github.com/JimHokanson/6420348 - strings: More info to
follow

Related Papers
--------------

Yemini E, Jucikas T, Grundy LJ, Brown AEX, Schafer WR (2013) A database
of Caenorhabditis elegans behavioral phenotypes. Nature methods.
http://www.nature.com/nmeth/journal/vaop/ncurrent/full/nmeth.2560.html

Worm File Structure
-------------------

The data file contains two structures:

1. `info`_
2. `worm`_

Documentation of these structures is well described in Ev Yemini's
thesis and in the supplemental section of the nature methods paper
(linked above)

.. _`ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura Grundy`: ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura%20Grundy
.. _First GitHub Issue: https://github.com/openworm/OpenWorm/issues/82
.. _ftp details: MRC_HDF5/ftp_structure.md
.. _info: MRC_HDF5/info_structure_documentation.md
.. _worm: MRC_HDF5/worm_structure_documentation.md