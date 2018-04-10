# USAGE
# python image_diff.py -first images/original_01.png --second images/modified_01.png

# import the necessary packages
import argparse
import cv2               # OpenCV module
import numpy as np
import matplotlib.pyplot as plt

# Parse the Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True, help="first image")
ap.add_argument("-s", "--second", required=True, help="second image")
args = vars(ap.parse_args())


# load the two input images
image_1_2005 = cv2.imread(args["first"])    
image_2_2016 = cv2.imread(args["second"])
diff = cv2.imread(args["second"]) 


[row,col,dim] = diff.shape

# Initializing the variables
same = 0
different = 0
positive_green = 0
negative_red = 0

# Convert diff to white image
for i in range(row):
    for j in range(col):
        diff[i][j][0] = 255
        diff[i][j][1] = 255
        diff[i][j][2] = 255
        

for i in range(row):
    for j in range(col):
        difference = abs(int(image_2_2016[i][j][1]) - int(image_1_2005[i][j][1]))
        if np.array_equal((image_1_2005[i][j]),(image_2_2016[i][j])) or difference < 14.0:
            same = same + 1
            diff[i][j][0] = 255      # white
            diff[i][j][1] = 255
            diff[i][j][2] = 255
        else:
            different = different + 1
            if image_1_2005[i][j][1] > image_2_2016[i][j][1] or (int(image_2_2016[i][j][2]) - int(image_1_2005[i][j][2])) >25:
                negative_red = negative_red + 1;
                diff[i][j][0] = 0     # negative_red
                diff[i][j][1] = 0 
                diff[i][j][2] = 200 - (int(image_1_2005[i][j][1]) - int(image_2_2016[i][j][1]))* 2
            else:
                positive_green = positive_green + 1;
                diff[i][j][0] = 0     # positive_green
                diff[i][j][1] = 200 - (int(image_2_2016[i][j][1]) - int(image_1_2005[i][j][1]))* 2
                diff[i][j][2] = 0

total = positive_green + negative_red + same

positive_green_percent = (positive_green/total) * 100
negative_red_percent = (negative_red/total) * 100
nochange_percent = (same/total) * 100


positive_green_percent = 'The Growth percent is ' + str(positive_green_percent)
negative_red_percent = 'The Decrease percent is ' + str(negative_red_percent)
nochange_percent = 'The Percent of no change ' + str(nochange_percent)

# Show the Image difference
cv2.imshow("Difference", diff)


# Show the percentages
fig, ax = plt.subplots()
ax.axis('off')

ax.text(0.015, 0.6, positive_green_percent, color='green',fontsize=14,
        bbox=dict(facecolor='none', edgecolor='green',pad=10.0))

ax.text(0.015, 0.4, negative_red_percent, color='red',fontsize=14, 
        bbox=dict(facecolor='none', edgecolor='red', pad=10.0))

ax.text(0.01, 0.2, nochange_percent, color='blue',fontsize=14, 
        bbox=dict(facecolor='none', edgecolor='blue',pad=10.0))


fig.show()
cv2.imshow("Image 1",image_1_2005)
cv2.imshow("Image 2",image_2_2016)
cv2.waitKey(0)

