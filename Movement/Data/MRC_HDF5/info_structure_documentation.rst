info
====

Contains experimental annotation.

Details
=======

* wt2: Short for Worm Tracker 2 

  * tracker: '2.0.4'
  * hardware: '2.0'
  * analysis: '2.0'
  * annotations: [ ] 
* video:     

  * length:         

    * frames: 26979         
    * time  : 898.401 
  * resolution: 

    * fps   : 30.03 
    * height: 480  
    * width : 640  
    * micronsPerPixels:    

      * x: -4.38109            
      * y: 4.38109         
    * fourcc: 'mjpg' - codec identifier    
  * annotations:         

    * frames: [1x26979] double, status codes for each frame. See reference for definition of these codes.
    * reference: [1x15] <- I think the 15 is an exhaustive list of all ids, a few examples of this are shown below  

      * reference(1) =>             
        * id: 1 - this # matches with the # above in frames 
        * function: 'segWorm:Success'   
        * message : 'The worm was successfully segmented.'   

      * reference(2) =>         
        * id: 2         
        * function: 'segWorm:DroppedFrame  
        * message: 'The video frame was dropped' 
* experiment:     

  * worm:         

    * genotype: 'acc-4(ok2371)III'  
    * gene: 'acc-4'         
    * allele: 'ok2371'         
    * strain: 'RB1832'  
    * chromosome: 'III'  
    * ventralSide: 'anticlockwise' OR 'clockwise'
    * agarSide: 'left' -> side of the body touching the agar
    * sex: 'hermaphrodite'  
    * age: 'young adult'         
    * habituation: '30 minutes' 
    * annotations: [] -> similar to annotations example above   

  * environment:  

    * timestamp: '2011-08-11 11:58:57.0'   
    * food: 'OP50'  
    * illumination: '627nm' -> peak wavelength  
    * temperature: '22C'         
    * chemicals: []         
    * arena: 'low-peptone NGM plate'   
    * tracker: '1' -> numerical id from 1 - 8, presumably this references a specific hardware rig which they have    
    * annotations: []
* files:    

  * video: [1x104] char -> .avi  
  * vignette: [1x128] char -> .info.xml.vignette.dat -> a correction for video vignetting 
  * info: [1x115] char -> .info.xml -> tracking information like microns/pixels  
  * stage: [1x114] char -> .log.csv -> logs stage movements  
  * directory: [1x51] char -> base path for these files  
  * computer: [1x17] char ex. -> PC207-13/10.3.1.69
* lab:  

  * name: 'William R Schafer' 
  * experimenter: 'Laura Grundy' 
  * address: 'Room S220 (left and mid bay), MRC Laboratory of Molecular Biology, Hills Road, Cambridge, CB2 0QH, UK' 
  * annotations: []``
