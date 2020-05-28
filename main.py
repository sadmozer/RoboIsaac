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

def import_images(path):
    images = {}
    for f1 in listdir(path):
        folder_path = join(path, f1)
        if(isdir(folder_path)):
            images_in_dir =  {'images': {}}
            with open(join(folder_path, 'meta.json')) as b:
                meta = json.load(b)
                images_in_dir['bounds'] = np.array(meta['bounds'])
                images_in_dir['img_color'] = eval(f"cv2.COLOR_BGRA2{meta['img_color']}")
                images_in_dir['mode'] = eval(meta['mode'])
                images_in_dir['threshold'] = meta['threshold']
                images_in_dir['legend_color'] = meta['legend_color']
                images_in_dir['name'] = meta['name']
            for f2 in listdir(folder_path):
                file_path = join(folder_path, f2)
                file_name = f2.split(".")[0]
                file_format = f2.split(".")[-1].lower()
                if(isfile(file_path) and file_format == 'png'):
                    img = cv2.imread(file_path, flags=cv2.IMREAD_UNCHANGED)
                    images_in_dir['images'][images_in_dir['name']] = img
            images[f1] = images_in_dir
    return images

cv2.namedWindow('window')
# cv2.namedWindow('window2')

# cv2.resizeWindow('window', 400, 225)
# # cv2.moveWindow('window', 950, 20)
# cv2.imshow('window', np.zeros((504, 947, 3)))

images = import_images('.\images')
kkeys = [W, A, S, D]
timer = 0
rand = random.randint(0, 3)
monitor = {"top": 33, "left": 9, "width": 944, "height": 500}
map_check = False

def action(key, times=1, sleep=1):
    for i in range(times):
        PressKey(key)
        time.sleep(sleep)
        ReleaseKey(key)
        time.sleep(sleep)

if __name__ == "__main__":
    setupgame.set_game_window()
    screen = None
    while(True):
        with mss() as sct:
            screen = np.asarray(sct.grab(monitor))
            entities = setupgame.start_detection(screen, images)
            # minimap = setupgame.generate_minimap(entities)
            setupgame.draw_entities(screen, entities, images)
            # screen = setupgame.region_of_interest(screen, [[800, 1],[960, 100]])
            # time.sleep(5)
            # for i in range(5):
            # action(W, 2, 0.125)
            # action(D, 2, 0.195)
            # action(S, 2, 0.125)
            # action(A, 2, 0.195)
            # action(S, 2, 0.165)
            # action(D, 1, 0.125)
            cv2.imshow('window', screen)
            if(cv2.waitKey(25) & 0xFF == ord("q")):
                cv2.destroyAllWindows()
                break
    # while(True):
    #     cv2.imshow('window', screen)
    #     if(cv2.waitKey(25) & 0xFF == ord("q")):
    #         cv2.destroyAllWindows()
    #         break   
        # if(timer<rand):
        #     timer+=1
        # else:
        #     ReleaseKey(kkeys[rand])
        #     timer = 0
        #     rand = random.randint(0, 3)
        #     PressKey(kkeys[rand])
        # screen = np.array(ImageGrab.grab(bbox=(7, 30, 954, 534)))




