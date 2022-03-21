import subprocess, sys
import numpy as np
import cv2
import time
from pprint import pprint

def set_game_window():
    p = subprocess.Popen(["powershell.exe",
    "-ExecutionPolicy",
    "Unrestricted",
    ".\\Set-Window.ps1"], 
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    out, err = p.communicate()
    try:
        print(f"[SETUP-STDOUT]: {out.decode('utf-8').strip()}")
    except Exception as e:
        print(f"[SETUP-STDERR]: {err.decode('utf-8').strip()}")
        print(e)

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

# [[940, -200], [1160, 50]]
# [[800, 1], [960, 100]]
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    # print(img.shape, mask.shape)
    # cv2.fillPoly(mask, vertices, 255)
    # y_min, y_max = vertices[0][1] + 58, vertices[1][1] + 58
    y_min, y_max = vertices[0][1], vertices[1][1]

    y_min = clamp(y_min, 0, img.shape[0]-1) 
    y_max = clamp(y_max, 0, img.shape[0]-1)
    
    # x_min, x_max = vertices[0][0] + 120, vertices[1, 0] + 120
    x_min, x_max = vertices[0][0], vertices[1, 0]

    x_min = clamp(x_min, 0, img.shape[1]-1)
    x_max = clamp(x_max, 0, img.shape[1]-1)
    # print(img.shape)
    # print(y_min, y_max, x_min, x_max)
    masked = img[y_min:y_max, x_min:x_max]
    return masked


def process_img(original_image, color):
    # processed_img = original_image
    processed_img = cv2.cvtColor(original_image, color)
    # th1=50, th2=100 OTTIMO
    # processed_img = cv2.Canny(processed_img, threshold1=50, threshold2=100)
    return processed_img

def detect_img(img, pattern, confidence, mode):
    dim = pattern.shape
    # print(pattern.shape, img.shape)

    stop = False
    found = []

    if pattern.shape[0] > img.shape[0] or  pattern.shape[1] > img.shape[1]:
        return found
    
    # while(not stop):
    res = cv2.matchTemplate(img, pattern, mode) 
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left, bottom_right, val = None, None, None
    max_methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED]
    min_methods = [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
    if(mode in max_methods and max_val > confidence):
        top_left = max_loc
        bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
        val = max_val
        found.append((top_left, bottom_right, val))
        img = cv2.rectangle(img, (top_left[0], top_left[1]), (top_left[0] + dim[1], top_left[1] + dim[0]), 0, 1)
    elif(mode in min_methods and min_val < confidence):
        top_left = min_loc
        bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
        val = min_val
        found.append((top_left, bottom_right, val))
        # img[top_left[0], top_left[1]] = 100
    else:
        stop = True
    return found

def debug_regions(i,screen):
    if screen.shape[0] != 0 and screen.shape[1] != 0 and screen.shape[2] != 0:
        cv2.namedWindow(f"window{i}")

        offset_x = 2653
        offset_y = 20
        cv2.moveWindow(f"window{i}", offset_x+i*150-700, offset_y)
        cv2.imshow(f"window{i}", screen)

def start_detection(screen, images):
    k=0
    detected_entities = []
    for k, im in enumerate(list(images.keys())):
        confidence = 0
        top_left = None
        i=0
        dict_imgs = images[im]['images']
        names = list(dict_imgs.keys())
        vals = list(dict_imgs.values())
        offset_x = images[im]['bounds'][0][0]
        offset_y = images[im]['bounds'][0][1]
        found = []
        while(i < len(names)):
            # processed_screen = region_of_interest(screen, yo)

            processed_screen = region_of_interest(screen, images[im]['bounds'])
            # debug_regions(k, processed_screen)

            # print(images[im]['name'])
            # print(yo)
            # print(images[im]['bounds'])
            
            # processed_screen = process_img(processed_screen, images[im]['img_color'])
            found = detect_img(
                img=processed_screen,
                pattern=vals[i],
                confidence=images[im]['threshold'],
                mode=images[im]['mode'])
            # if(len(found) == 0):
                # i+=1
            # else:
                # print(f"{names[i]}:{processed_screen.shape}")
            for f in found:
                top_left, bottom_right, confidence = f
                box_top_left = (top_left[0]+offset_x, top_left[1]+offset_y)
                box_bottom_right = (bottom_right[0]+offset_x, bottom_right[1]+offset_y)
                detected_entities.append({"box_top_left": box_top_left, "box_bottom_right": box_bottom_right, "img_name": im, "confidence": confidence})
            i+=1

    return detected_entities

def draw_entities(screen, entities, images):
    k = 0
    for e in entities:
        img = images[e['img_name']]
        # e['box_top_left'] =  (e['box_top_left'][0] + 120, e['box_top_left'][1] + 80)
        # e['box_bottom_right'] = (e['box_bottom_right'][0] + 120, e['box_bottom_right'][1] + 80)
        cv2.rectangle(screen,
            e['box_top_left'],
            e['box_bottom_right'],
            img['legend_color'], 
            1)
        cv2.putText(screen, 
            f"{img['name']} {e['confidence']:.5f}",
            (1080, 400+k),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.3,
            img['legend_color'], 
            1, 
            cv2.LINE_AA)
        k+=8

# def check_screenshot_noise():
#     screen1 = np.asarray(sct.grab(monitor))
#     screen1 = cv2.cvtColor(screen1, cv2.COLOR_BGRA2GRAY)
#     screen1 = setupgame.region_of_interest(screen1, [[417, 3], [533, 85]])
#     PressKey(S)
#     time.sleep(0.1)
#     ReleaseKey(S)
#     time.sleep(1)
#     screen2 = np.asarray(sct.grab(monitor))
#     screen2 = cv2.cvtColor(screen2, cv2.COLOR_BGRA2GRAY)
#     screen2 = setupgame.region_of_interest(screen2, [[417, 3], [533, 85]])
#     pprint(np.array_equal(screen1, screen2))
#     a = []
#     noise_threshold = 0
#     screen1 = screen1.reshape((472000, 4))cv
#     screen2 = screen2.reshape((472000, 4))
#     for px1, px2 in zip(screen1, screen2):
#         trovato = False
#         for ch1, ch2 in zip(px1, px2):
#             if(abs(int(ch1)-int(ch2)) > noise_threshold):
#                 trovato = True
#         if(trovato):
#             a.append((255, 255, 255, 255))
#         else:
#             a.append(px2)
#     screen3 = np.asarray(a, dtype=np.uint8).reshape((500, 944, 4))
#     screen3 = cv2.fastNlMeansDenoising(screen3, None, 10, 41, 21)
#     return screen1, screen2, screen3

def generate_minimap(entities):
    pprint(entities)
    return entities
