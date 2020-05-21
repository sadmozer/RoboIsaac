import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui
from directkeys import PressKey, ReleaseKey, W, A, S, D
from pprint import pprint
import setupgame
from os import listdir
from os.path import isfile, join, isdir
import random
import json
from mss import mss
def process(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # th1=50, th2=100 OTTIMO
    # processed_img = cv2.Canny(processed_img, threshold1=50, threshold2=100)
    return processed_img

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

max_methods = [eval(m) for m in ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED']]
min_methods = [eval(m) for m in ['cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']]
def detect_img(img, pattern, confidence, mode):
    dim = pattern.shape
    res = cv2.matchTemplate(img, pattern, mode) 
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = None
    bottom_right = None
    val = None
    if(mode in max_methods and max_val > confidence):
        top_left = max_loc
        bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
        val = max_val
    elif(mode in min_methods and min_val < 1-confidence):
        top_left = min_loc
        bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
        val = 1-min_val
    return top_left, bottom_right, val

def import_images(path):
    images = {}
    for f1 in listdir(path):
        folder_path = join(path, f1)
        if(isdir(folder_path)):
            images_in_dir =  {'images': {}, 'bounds': {}}
            for f2 in listdir(folder_path):
                file_path = join(folder_path, f2)
                if(isfile(file_path)):
                    if(f2.split(".")[-1].lower() == 'png'):
                        img = cv2.imread(file_path)
                        images_in_dir['images'][f2.split(".")[0]] = process(img)
                    else:
                        with open(join(folder_path, 'bounds.json')) as b:
                            images_in_dir['bounds'] = np.array([json.load(b)['bounds']])
            images[f1] = images_in_dir
    return images

def enable_detection(screen, images):
    for im in images:
        confidence = 0
        top_left = None
        i=0
        curr_imgs = images[im]['images']
        names = list(curr_imgs.keys())
        vals = list(curr_imgs.values())
        while(i < len(names) and not top_left):
            top_left, bottom_right, confidence = detect_img(
                img=region_of_interest(screen, images[im]['bounds']), 
                pattern=vals[i],
                confidence=0.9,
                mode=cv2.TM_CCOEFF_NORMED)
            if(not top_left):
                i+=1
        if(i < len(names)):
            cv2.rectangle(screen, top_left, bottom_right, (255, 255, 0), 1)
            cv2.putText(screen, names[i], (top_left[0], top_left[1]-3), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1, cv2.LINE_AA)

cv2.namedWindow('window')
cv2.moveWindow('window', -1000, 20)
cv2.imshow('window', np.zeros((504, 947, 3)))

images = import_images('.\images')
setupgame.StartGame()

kkeys = [W, A, S, D]
timer = 0
rand = random.randint(0, 3)


with mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 33, "left": 9, "width": 944, "height": 500}

    while "Screen capturing":

        # Get raw pixels from the screen, save it to a Numpy array
        screen = np.array(sct.grab(monitor))

        gray_screen = process(screen)
        enable_detection(gray_screen, images)
        
        # Display the picture
        cv2.imshow('window', gray_screen)

        # Press "q" to quit
        if(cv2.waitKey(25) & 0xFF == ord("q")):
            cv2.destroyAllWindows()
            break

        if(timer<rand):
            timer+=1
        else:
            ReleaseKey(kkeys[rand])
            timer = 0
            rand = random.randint(0, 3)
            PressKey(kkeys[rand])
        # screen = np.array(ImageGrab.grab(bbox=(7, 30, 954, 534)))
        # new_screen = process(screen)
        # cv2.imshow('window', new_screen)



