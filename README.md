--------------------------------------READ ME------------------------------------

Implemented a Image Classification System using python, which classfies the image in Headshot or landscape images.

Implemented KNN,3 FOld Cross validation, kMeans clustering, Single hierarchical clustering, but didnt plot the dendogram
Implemented a feature, if the lookup table is once filled then, it wont reload it, it will directly use the existing one saving the time of computing again if not exited.

These are the libraries imported,
If your system doesnt have one, please download it:

from PIL import Image
import csv
import os
import sys
import matplotlib.pyplot as plt
import random
import operator



To implement KNN:
PLease proovide the image with .jpeg extension only.
The image should be in some directory as the file.<e.g h2.jpeg> its already provided with the files in same directory.
If u wanna give some file which is another direcory specify the path.

To implement 3 fold cross validation:
The image files for this is already provided, please use that.They are by name 1 2 3. Each contains 20 headshot images and 20 landscape images. Named in a particular fashion. If you want to test it on your own data, please convert your data in this format only
The graph will plotted automatically, if you close the graph automatically the menu will be shown again

To implement Single linkage:
If the program crashes try reducing the data set, or use the existing dataset which is loaded in program as a b c
It displayes the cluster formation in order and at height at which the clusters are formed.


Notes: The logic for computation of histogram was given by Prof Natalia Khuri

