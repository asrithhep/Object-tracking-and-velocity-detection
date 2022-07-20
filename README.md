# Object-tracking-and-velocity-detection

This respirotory containes code to detect moving objects and finding the velocity of the object in camera axis.\
\
I have mainly used OPENCV python modeule for this work.\


## The code contain two parts.

  * First part contain detecting object. I use contour method here. I use boxes to highlight the object of intrest.\
  * Second part contains the velocity detection. I use the size difference in object in each frame to detect the velocity  of object in camera axis.\
 ...
 
 Code required calliberation in order to find accurate velocity.
 
 ...
 
 ## For calliberation
     * 1)Use a image file to set the background.\
     * 2)choose apropreate treshold for countor selection. \
     * 3)use reference object with known size to caliberate the velocity.\
