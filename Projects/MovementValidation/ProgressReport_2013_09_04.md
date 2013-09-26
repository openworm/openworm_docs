# Worm Behavior Database #

- Date: 2013-09-04
- Author: Jim Hokanson

The following describes current progress regarding the worm behavior database.

## Brief Summary ##
Data has provided to us by Dr William Schafer's lab at the MRC Laboratory of Molecular Biology. It is currently unclear what if any update mechanisms will be in place when more experiments are added to the current collection.

A few gists have been provided which demonstrate how to work with the data.

## Data Source ##

I've tried to start documenting this data source at:
https://github.com/JimHokanson/openworm_docs/blob/master/Movement/Data/MRC_HDF5.md

If we ever get data from other groups the idea would be to document these in the same folder. The documentation location might change once a more official documentation strategy is in place.

## Data Contents ##

The data contents are described in links on the data source page:
https://github.com/JimHokanson/openworm_docs/blob/master/Movement/Data/MRC_HDF5.md#worm-file-structure

The documentation has been started but the descriptions are currently incomplete.

## Data Analysis ##
Significant data analysis has yet to begin. Look for more issues to be started on this topic.

## Current Coding Efforts ##

This code traverses the structure, plots each field, and saves the plot to disk.
https://gist.github.com/PeterMcCluskey/6418155

Plot of movement
https://gist.github.com/JimHokanson/6425605

A little bit of code on understanding a Matlab structure array as seen by h5py:
https://gist.github.com/JimHokanson/6420348

## Reference Code ##
Dr. Schafer's lab has also shared their analysis code (in Matlab) which takes a video and creates the information that is stored in the data files. Given the documentation available on the file format, it might not be needed. Nevertheless this is available at:
https://github.com/openworm/SegWorm

As is the code itself can not be run due to missing dependencies.

There is also a branch which is attempting to make the code a bit more readable and to convert most of the code into using objects:
https://github.com/JimHokanson/SegWorm/tree/classes

Currently this branch requires code which can be found at:
https://github.com/JimHokanson/matlab_standard_library

Both versions also require the Image Toolbox and possibly the Statistics Toolbox.

