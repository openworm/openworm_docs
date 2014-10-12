## General Idea ##

The FTP server to use is: 

[ftp://anonymous@ftp.mrc-lmb.cam.ac.uk](ftp://anonymous@ftp.mrc-lmb.cam.ac.uk) 

anonymous login 

/pub/tjucikas/wormdatabase/results-12-06-08/Laura Grundy/

The following describes the way that data files are stored on the FTP server. 

NOTE: As of late August 2013 we are discussing possible mirroring of the data to improve access. In other words, this interface may to change.

## Specifics ##

When present, the first subdirectory is the gene name (e.g., "unc-8"); otherwise, for wild isolates and N2 the subdirectory is "gene_NA".

When present, the next subdirectory is the allele (e.g., "n491n1192"); otherwise, for wild isolates and N2 the subdirectory is "allele_NA".

The subdirectory thereafter is the strain name (e.g., "AQ2947" is the Schafer lab copy of the CGC's N2). The strain name is always present.

Beyond this point the subdirectories describe whether the worm is on food ("on_food" or "off_food" -- only a small subset of N2s and MECs were done off food). The sex ("XX" or "XO" -- the only males are N2). Whether a habituation period was observed ("30m_wait" or "no_wait" -- 25 N2 experiments were done with no habituation and recorded for 2 hours straight; otherwise, we always observed a 30 minute habituation period).

At the end the subdirectories become far less meaningful to you. They indicate the ventral side ("L" = anti-clockwise or "R" = clockwise -- this can be confusing due to the orientation of the video vs. the experimenter's annotation). The tracker we used (1 through 8). The date (YYYY-MM-DD___HH_MM_SS). And, finally, the experiment's filename. The actual feature files contain further annotations (e.g., the room we used, the frame rate, ...).

Here are 2 examples:

unc-8(n491n1192)
ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura%20Grundy/unc-8/n491n1192/MT2611/on_food/XX/30m_wait/L/tracker_2/2010-03-19___09_14_57/unc-8%20(rev)%20on%20food%20R_2010_03_19__09_14_57___2___2_features.mat

CB4856 - the famous Hawaiian wild isolate
ftp://anonymous@ftp.mrc-lmb.cam.ac.uk/pub/tjucikas/wormdatabase/results-12-06-08/Laura%20Grundy/gene_NA/allele_NA/CB4856/on_food/XX/30m_wait/L/tracker_1/2010-11-25___11_33_52/399%20CB4856%20on%20food%20R_2010_11_25__11_33_52___1___1_features.mat
