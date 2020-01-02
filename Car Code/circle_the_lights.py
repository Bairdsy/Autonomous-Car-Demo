from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76

def image_average(img):
    average = img.mean(axis=0).mean(axis=0)
    return average

def image_max(img):
    average = img.max(axis=0).max(axis=0)
    return average


def image_crop(img, x, y, h, w):
    crop_img = img[y:y+h, x:x+w]
    return crop_img

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def convert_to_HSV(img):
    out_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return out_img

def reshape_with_xy(img):
    newimage = []
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            (blue, green, red) = img[i, j]
            #print(i,j,blue,green,red)
            newimage.append([red, green, blue, i, j ])
    return newimage

def reshape_from_xy(img):
    newimage = []
    for i in range(0,480):
        newrow = []
        for j in range(0,640):
            array = img[i*j]
            newrow.append([array[0], array[1], array[2]])
        newimage.append(newrow)
    return newimage
    
def fixbgr(out_image):
    #global out_image
    for i in range(0,out_image.shape[0]):
        for j in range(0,out_image.shape[1]):
            out_image[i,j] = [out_image[i,j,2],out_image[i,j,1],out_image[i,j,0]]
    return out_image

def get_colors(image, number_of_colors):
    
    modified_image = cv2.resize(image, (640, 480), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    #modified_image = reshape_with_xy(modified_image)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    cluster_labels = clf.labels_
    cluster_centers = clf.cluster_centers_

    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i]/255 for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]*255) for i in counts.keys()]
    rgb_colors = [ordered_colors[i]*255 for i in counts.keys()]
   
    if (debug_mode):

        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = ordered_colors)
        plt.savefig("piechart.png")
    
        out_image = cluster_centers[cluster_labels].reshape(480, 640, 3)
        out_image = fixbgr(out_image)
        cv2.imwrite("output.png", out_image)

    
    return rgb_colors

debug_mode = 0
    
for filename in glob.glob('Images/*.jpg'):
    print("working on "+filename)
    image = get_image(filename)
    #average = image_max(image)
    #sum = average[0] + average[1] + average[2]
    #print("BEFORE CROP:")
    #print(average)
    #print(sum)
    #hsv_average = image_max(convert_to_HSV(image))
    #hsv_sum = hsv_average[0] + hsv_average[1] + hsv_average[2]
    #print(hsv_average)
    #print(hsv_sum)
    image = fixbgr(image)
    #cv2.imshow("original", image)
    #cv2.waitKey(0)
    cropped = image_crop(image,0,100,180,640)
    orig = cropped.copy()

    #cropped = fixbgr(cropped)
    average = image_max(cropped)
    #sum = average[0] + average[1] + average[2]
    print("AFTER CROP:")
    print(average)
    #print(sum)
    hsv_average = image_max(convert_to_HSV(cropped))
    #hsv_sum = hsv_average[0] + hsv_average[1] + hsv_average[2]
    print(hsv_average)
    #print(hsv_sum)
    #cv2.imshow("cropped", cropped)
    #cv2.waitKey(0)

    image = orig.copy()
        
    if (hsv_average[2] >= 250):
        # apply a Gaussian blur to the image then find the brightest
        # region
#        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        if (average[0] >= 250):
            gray = cropped[:,:,0]
            gray = cv2.GaussianBlur(gray, (3, 5), 0)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
            cv2.circle(image, maxLoc, 20, (255, 0, 0), 2)

        if (average[1] >= 250):
            gray = cropped[:,:,1]
            gray = cv2.GaussianBlur(gray, (3, 5), 0)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
            cv2.circle(image, maxLoc, 20, (0, 255, 0), 2)

        if (average[2] >= 250):
            gray = cropped[:,:,2]
            gray = cv2.GaussianBlur(gray, (3, 5), 0)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
            cv2.circle(image, maxLoc, 20, (0, 0, 255), 2)

    # display the results of our newly improved method
    cv2.imshow("Result", image)
    cv2.waitKey(0)

    

#colors = get_colors(image,6)

#if (debug_mode):
#    print (colors)