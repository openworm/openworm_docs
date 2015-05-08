General Idea
============

The following describes the way that data files are stored on the FTP server.

NOTE: As of late August 2013 we are discussing possible mirroring of the data to improve access. In other words, this interface may to change.

Specifics
=========

When present, the first subdirectory is the gene name (e.g., "unc-8"); otherwise, for wild isolates and N2 the subdirectory is "gene\_NA".

When present, the next subdirectory is the allele (e.g., "n491n1192"); otherwise, for wild isolates and N2 the subdirectory is "allele\_NA".

The subdirectory thereafter is the strain name (e.g., "AQ2947" is the Schafer lab copy of the CGC's N2). The strain name is always present.

Beyond this point the subdirectories describe whether the worm is on food ("on\_food" or "off\_food" -- only a small subset of N2s and MECs were done off food). The sex ("XX" or "XO" -- the only males are N2). Whether a habituation period was observed ("30m\_wait" or "no\_wait" --25 N2 experiments were done with no habituation and recorded for 2 hours straight; otherwise, we always observed a 30 minute habituation period).

At the end the subdirectories become far less meaningful to you. They indicate the ventral side ("L" = anti-clockwise or "R" = clockwise --this can be confusing due to the orientation of the video vs. the experimenter's annotation). The tracker we used (1 through 8). The date (YYYY-MM-DD\_\_\_HH\_MM\_SS). And, finally, the experiment's filename. The actual feature files contain further annotations (e.g., the room we used, the frame rate, ...).

Here are 2 examples:

unc-8(n491n1192) [ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura%20Grundy/unc-8/n491n1192/MT2611/on\\\_food/XX/30m\\\_wait/L/tracker\\\_2/2010-03-19\\\_](ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura%20Grundy/unc-8/n491n1192/MT2611/on\_food/XX/30m\_wait/L/tracker\_2/2010-03-19\_)**09\_14\_57/unc-8%20(rev)%20on%20food%20R\_2010\_03\_19**09\_14\_57\_**2***2*features.mat

CB4856 - the famous Hawaiian wild isolate [ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura%20Grundy/gene\\\_NA/allele\\\_NA/CB4856/on\\\_food/XX/30m\\\_wait/L/tracker\\\_1/2010-11-25\\\_](ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura%20Grundy/gene\_NA/allele\_NA/CB4856/on\_food/XX/30m\_wait/L/tracker\_1/2010-11-25\_)**11\_33\_52/399%20CB4856%20on%20food%20R\_2010\_11\_25**11\_33\_52\_**1***1*features.mat
