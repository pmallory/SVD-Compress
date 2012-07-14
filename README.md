SVD-Compress
===========

A method to compress images using rank reduced singular value decompositions.

The general idea
----------------
A grayscale bitmap image is a big 2d array of numbers. Each number describes how intense a pixel is. 0 is black, 255 is white. A color image works the same way except there are three 2d arrays, one each for the red, blue and green components of each image. So to store a color image we need eight bits per color channel, for every single pixel in the image. That's a lot of data (and that's why people don't usually store images as bitmaps). Fortunately there are more efficient ways to store data.

Here's SVD-Compress' method:

- instead of calling each color channel an array call it a matrix. This is the most important step.
- find three matrices that when multiplied together equal the original matrix.
- These new matrices aren't any better then the original one, but they do have one handy property: The most "significant" parts of the original matrix are all pushed to the top left corners of the three new matrices.
- We can reduce the amount of data we're storing by chopping off the bottom right of each of the three smaller matrices. When you mulitply the trimmed matrices together you get a matrix the same size as the orignal matrix which closely resembles the original matrix, except you need less data to get it.
- If you chopped too much the compressed version of the matrix won't look very much like the original, but if you're careful there isn't any perceptible difference between the two.

