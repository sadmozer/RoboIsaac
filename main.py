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
def process(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # th1=50, th2=100 OTTIMO
    # processed_img = cv2.Canny(processed_img, threshold1=50, threshold2=100)
    # vertices = np.array([[85, 0], [85, 540], [860, 540], [860, 0]])
    # processed_img = region_of_interest(processed_img, [vertices])
    return processed_img

# def region_of_interest(img, vertices):
#     mask = np.zeros_like(img)
#     cv2.fillPoly(mask, vertices, 255)
#     masked = cv2.bitwise_and(img, mask)
#     return masked

max_methods = [eval(m) for m in ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED']]
min_methods = [eval(m) for m in ['cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']]
def detect_img(img, pattern, confidence, mode):
    print(pattern)
    dim = pattern.shape
    # res = cv2.matchTemplate(img, pattern, mode) 
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = None
    bottom_right = None
    # if(mode in max_methods and max_val > confidence):
    #     top_left = max_loc
    #     bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
    # elif(mode in min_methods and min_val < 1-confidence):
    #     top_left = min_loc
    #     bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
    return top_left, bottom_right

def import_images(path):
    images = {}
    for f1 in listdir(path):
        folder_path = join(path, f1)
        if(isdir(folder_path)):
            images_in_dir =  {'images': {}, 'bounds': {}}
            for f2 in listdir(folder_path):
                file_path = join(folder_path, f2)
                if(isfile(file_path):
                    if(f2.split(".")[-1] == 'png'):
                        img = cv2.imread(file_path)
                        images_in_dir['images'][f2.split(".")[0]] = process(img)
                    else:
                        with open(join(folder_path, 'bounds.json')) as b:
                            images_in_dir['bounds'] = json.load(b)
            images[f1] = images_in_dir
    return images

cv2.namedWindow('window')
cv2.moveWindow('window', -1000, 20)
cv2.imshow('window', np.zeros((504, 947, 3)))

images = import_images('.\images')
# setupgame.StartGame()

font = cv2.FONT_HERSHEY_SIMPLEX
iss = ['IsaacIdle', 'IsaacLeft', 'IsaacRight', 'IsaacUp']
kkeys = [W, A, S, D]
timer = 0
rand = random.randint(0, 3)

while(True):
    if(cv2.waitKey(25) & 0xFF == ord('q')):
        cv2.destroyAllWindows()
        break
    screen = np.array(ImageGrab.grab(bbox=(7, 30, 954, 534)))
    new_screen = process(screen)

    i=0
    for area in images:
        if(area == 'up_door'):
            top_left = True
            curr_imgs = area['images']
            while(i<len(list(curr_imgs)) and top_left):
                if(in_area)
                top_left, bottom_right = detect_img(
                    img=new_screen, 
                    pattern=in_area[i], 
                    confidence=0.90, 
                    mode=cv2.TM_CCOEFF_NORMED)
                i+=1
    # detected_entities = {}
    # for i in images:
    #     detected_entities[i] = detect_img(
    #         img=new_screen, 
    #         pattern=images[i], 
    #         confidence=0.90, 
    #         mode=cv2.TM_CCOEFF_NORMED)

    # for e in detected_entities:
    #     top_left, bottom_right = detected_entities[e]
    #     if(top_left):
    cv2.rectangle(new_screen, top_left, bottom_right, (255, 255, 0), 1)
    cv2.putText(new_screen, list(images[area].keys())[i], (top_left[0], top_left[1]-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        
    # if(timer<rand+5):
    #     timer+=1
    # else:
    #     ReleaseKey(kkeys[rand])
    #     timer = 0
    #     rand = random.randint(0, 3)
    #     PressKey(kkeys[rand])
    cv2.imshow('window', new_screen)




