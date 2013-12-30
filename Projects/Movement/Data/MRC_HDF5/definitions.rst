Definitions within Worm Movement Data
============

This is just a raw list. At some point it will need to be expanded and
perhaps linked to other places which discuss the specifics in better
detail.

1 muscle

   *  1/48 of contour
   *  1/24 of skeleton
   *  23-24 muscles per worm

Head & tail
   each occupies 1/6 of the total body

Length
   computed from the skeleton by converting chain-code pixel length
   (Freeman chain code, TODO: insert description) to microns

Width
   ?? computed from skeleton?? or contour?

Angles
   supplementary angles used relative to those formed by angle between
   muscle segments
   
   thus when the worm is straight, the angle is 0
   on contour:
   
     * inner sections are negative
     * outer sections are positive
   on skeleton:
   
     * +dorsal
     * -ventral

High frequency bends
   angle formed between two muscle segments at each point along contour
   and skeleton

Low frequency bends
   angle formed by points two muscle segments away from vertex muscle
   point
   
   half the spatial sampling rate of high-frequency bends

Chunks
   small segment of video wherein all worm shapes are aligned to share
   the same head-to-tail orientation