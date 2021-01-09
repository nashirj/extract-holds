https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/

References:
- [hold detection repo](https://github.com/scsukas8/NeuralClimb/tree/master/Hold%20Detection)
- [straighten img](https://stackoverflow.com/questions/11627362/how-to-straighten-a-rotated-rectangle-area-of-an-image-using-opencv-in-python)
- [detect rectangle 1](https://stackoverflow.com/questions/61166180/detect-rectangles-in-opencv-4-2-0-using-python-3-7)
- [detect rectangle 2](https://stackoverflow.com/questions/45767866/detect-rectangle-in-image-and-crop)
- [detect rectangle 3](https://stackoverflow.com/questions/57125879/improve-rectangle-contour-detection-in-image-using-opencv)



TRY THIS ONE OUT
https://stackoverflow.com/questions/57125879/improve-rectangle-contour-detection-in-image-using-opencv





## objective
- read image of wall
- detect corners of wall
    - ???
- straighten image given corners of wall
    - use cv.findHomograph and cv.warpPerspective
    - crop using np slicing
- detect holds on the wall
    - try using code from the NeuralClimb repo
- create 2d binary matrix with 1s where there are holds on the wall
    - dimensions of wall and each hold hole are known
    - center of each detected hold (x,y coord) are mapped to the nearest hold hole; set the corresponding index of bmatrix to 1
- for the sake of validation, draw bounding box around each hold


## later
- input binary matrix of holds, warped image as produced above
- draw bounding box around wall holds as specified by binary matrix


## considerations/complications
- lighting
- image dimensions
- background: plants and support beam


### alternate approach
- requires fixed camera location w.r.t the wall
- picture of board with nothing on it
- use pic as ground truth
- new images, just subtract difference, the difference is where we have a hold
- could threshold intensity so that differences in lighting doesn't give too much of a difference


### alternate approach
- try installing something on 4 corners that are unique beacon type things


throw away things that don't pass threshold area