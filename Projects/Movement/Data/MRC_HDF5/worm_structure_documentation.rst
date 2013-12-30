worm description
================

-  NOTE: Currently a description of the fields can be found at:
   https://github.com/openworm/SegWorm/blob/master/Worms/Features/wormFileSummary.m
-  Description of the processing steps can be found in:
-  Ev Yemini's PhD thesis
-  The supplemental material in this paper:
   http://www.nature.com/nmeth/journal/v10/n9/full/nmeth.2560.html#supplementary-information
-  Unless stated otherwise the dimensions are [1 x n\_frames]
-  lengths are in microns
-  areas in microns^2
-  NaN values present to indicate dropouts (why do these occur?)

Concepts
========

Bending :

Skeleton : Set of midpoints between each pairing of outside pixels.
::

    This allows for easier computations on the movement of the worm, 
    rather than looking at the contour.

Fields
======

-  These fields are all in the "worm" structure
-  Field depth is indicated by indentation level of the leading hyphen.
   For example:

``worm.morphology.length     worm.morphology.width.head     worm.morphology.width.midbody     worm.morphology.width.tail     worm.morphology.area``

-  a size indication [n x m] that is attached to a name which has child
   properties indicates that the entry is a structure array, For
   example:

\`\`\`\`

-  locomotion:

   -  motion:

      -  forward:

         -  frames: [1x69]
         -  start : 10422
         -  end : 10470
         -  time : 1.6317
         -  interTime : NaN
         -  interDistance: NaN
            Note from above this means:
            worm.locomotion.motion.forward.frames
            The values shown in this case are an example, such as from
            frames(1)

frames(1).start = 10422
frames(1).end = 10470
\`\`\`\`

-  The structure array entries typically refer to events (epochs) which
   do not occur for every frame, but rather occur occasionally
   throughout the recording (or not at all)

``- morphology: Units are um or um^2 or um/um, lengths are [1 x nFrames], NaN are observed     - length: [1 x nFrames] Head to tail length?     -  width:         - head   : [1 x nFrames]         - midbody: [1 x nFrames]         - tail   : [1 x nFrames]     -           area: [1 x nFrames] "area" within its contours     -  areaPerLength: [1 x nFrames] REDUNDANT INFO :/     - widthPerLength: [1 x nFrames] midbody/length -> REDUNDANT INFO :/ - posture:     - bends: (degrees, inside angle is + dorsal, - ventral)         - head:             - mean: [1 x nFrames]             - stdDev: [1 x nFrames]         - neck:             - mean:             - stdDev:         - midbody:             - mean:             - stdDev:          - hips:             - mean:              - stdDev:         - tail:             - mean:              - stdDev:     - amplitude: ???         - max:          - ratio:      - wavelength:         - primary: [1x26979] double         - secondary: [1x26979] double     - tracklength: [1x26979] double     - eccentricity: [1x26979] double     - kinks: Bend Counts     - coils:         - frames:             - start : 10422             - end   : 10470             - time  : 1.6317             - interTime    : NaN             - interDistance: NaN         - frequency: 0.00111309         - timeRatio: 0.00181623     - directions:         - tail2head: [1x26979]         - head     : [1x26979]         - tail     : [1x26979]     - skeleton: Note, worm is normalized to 49 points         - x: [49 x n_frames]         - y: [49 x n_frames]      - eigenProjection: [6x26979] The eigenprojection is computed from the worm's bend angles (low frequency???)     The eigenvectors for these projections come from a set of wild-type worms (source on this - nature methods supplemental????) - locomotion:     - motion:         - forward:             - frames: [1x69]                 - start: 0                 - end: 607                 - time: 20.2464                 - distance: 4193.92                 - interTime: 1.3653                 - interDistance: 15.6651             - frequency: 0.074577             - ratio:                 - time: 0.834167                 - distance: 0.898035         - backward:             - frames: [1x28]                 - start: 842                 - end: 876                 - time: 1.1655                 - distance: 239.056                 - interTime: 6.1938                 - interDistance: 872.12             - frequency: 0.0311665             - ratio:                 - time: 0.0724638                 - distance: 0.0901222         - paused:             - frames: [1x15]                 - start: 609                 - end: 647                 - time: 1.2987                 - distance: 12.5074                 - interTime: 16.983                 - interDistance: 2857.6             - frequency: 0.0166963             - ratio:                 - time: 0.0164943                 - distance: 0.00116571         - mode: [1x26979] double     - velocity:         - headTip:             - speed: [1x26979] double             - direction: [1x26979] double         - head:             - speed: [1x26979] double             - direction: [1x26979] double         - midbody:             - speed: [1x26979] double             - direction: [1x26979] double         - tail:             - speed: [1x26979] double             - direction: [1x26979] double         - tailTip:             - speed: [1x26979] double             - direction: [1x26979] double     - bends: (degrees, inside angle is + dorsal, - ventral)         - foraging: ?????             - amplitude:              - angleSpeed:         - head:             - amplitude: [1x26979] double             - frequency: [1x26979] double         - midbody:             - amplitude: [1x26979] double             - frequency: [1x26979] double         - tail:             - amplitude: [1x26979] double             - frequency: [1x26979] double     - turns:         - omegas:             - frames: []             - frequency: []             - timeRatio: []         - upsilons:             - frames: [41x1]                 - start: 1101                 - end: 1116                 - time: 0.5328                 - interTime: 35.7975                 - interDistance: 5385.61                 - isVentral: [1x1] logical             - frequency: 0.0456367             - timeRatio: 0.0947033 - path:     - range: [1x26979] double     - duration:         - arena:             - height: 297             - width: 245             - min:                 - x: 8401.06                 - y: 8631.52             - max:                 - x: 19886.6                 - y: 22565.2         - worm:             - indices: [9200x1] double             - times: [9200x1] double         - head:             - indices: [6856x1] double             - times: [6856x1] double         - midbody:             - indices: [7319x1] double             - times: [7319x1] double         - tail:             - indices: [4821x1] double             - times: [4821x1] double     - coordinates:         - x: [1x26979] double         - y: [1x26979] double     - curvature: [1x26979] double``
