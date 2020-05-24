import subprocess, sys
import numpy as np
import cv2
import time
def StartGame():
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

def region_of_interest(img, vertices):
    # mask = np.zeros_like(img)
    # print(img.shape, mask.shape)
    # cv2.fillPoly(mask, vertices, 255)
    masked = img[vertices[0][1]:vertices[1][1], vertices[0][0]:vertices[1][0]]

    return masked

def process(original_image, color):
    # processed_img = original_image
    processed_img = cv2.cvtColor(original_image, color)
    # th1=50, th2=100 OTTIMO
    # processed_img = cv2.Canny(processed_img, threshold1=50, threshold2=100)
    return processed_img

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
    elif(mode in min_methods and min_val < confidence):
        top_left = min_loc
        bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
        val = min_val
    return top_left, bottom_right, val

def start_detection(screen, images):
    k=0
    detected_entities = []
    for im in images:
        confidence = 0
        top_left = None
        i=0
        dict_imgs = images[im]['images']
        names = list(dict_imgs.keys())
        vals = list(dict_imgs.values())
        while(i < len(names) and not top_left):
            processed_screen = region_of_interest(screen, images[im]['bounds'])
            processed_screen = process(processed_screen, images[im]['img_color'])
            top_left, bottom_right, confidence = detect_img(
                img=region_of_interest(screen, images[im]['bounds']),
                pattern=vals[i],
                confidence=images[im]['threshold'],
                mode=images[im]['mode'])
            if(not top_left):
                i+=1
            else:
                # print(f"{names[i]}:{processed_screen.shape}")
                offset_x = images[im]['bounds'][0][0]
                offset_y = images[im]['bounds'][0][1]
                box_top_left = (top_left[0]+offset_x, top_left[1]+offset_y)
                box_bottom_right = (bottom_right[0]+offset_x, bottom_right[1]+offset_y)
                detected_entities.append({"box_top_left": box_top_left, "box_bottom_right": box_bottom_right, "img_name": im, "confidence": confidence})
    return detected_entities

def draw_entities(screen, entities, images):
    k = 0
    for e in entities:
        img = images[e['img_name']]
        cv2.rectangle(screen,
            e['box_top_left'],
            e['box_bottom_right'],
            img['legend_color'], 
            1)
        cv2.putText(screen, 
            f"{e['img_name']} {e['confidence']:.5f}",
            (800, 400+k),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.3,
            img['legend_color'], 
            1, 
            cv2.LINE_AA)
        k+=8

# https://www.reddit.com/r/bindingofisaac/comments/2ld3t1/psa_how_to_speed_up_rebirth_considerably_even_on/
def check_screenshot_noise():

    screen1 = np.asarray(sct.grab(monitor))
    # screen1 = cv2.cvtColor(screen1, cv2.COLOR_BGRA2GRAY)
    # screen1 = setupgame.region_of_interest(screen1, [[417, 3], [533, 85]])
    PressKey(S)
    time.sleep(0.1)
    ReleaseKey(S)
    time.sleep(1)
    screen2 = np.asarray(sct.grab(monitor))
    # screen2 = cv2.cvtColor(screen2, cv2.COLOR_BGRA2GRAY)
    # screen2 = setupgame.region_of_interest(screen2, [[417, 3], [533, 85]])
    pprint(np.array_equal(screen1, screen2))
    a = []
    noise_threshold = 0
    screen1 = screen1.reshape((472000, 4))
    screen2 = screen2.reshape((472000, 4))
    for px1, px2 in zip(screen1, screen2):
        trovato = False
        for ch1, ch2 in zip(px1, px2):
            if(abs(int(ch1)-int(ch2)) > noise_threshold):
                trovato = True
        if(trovato):
            a.append((255, 255, 255, 255))
        else:
            a.append(px2)
    screen3 = np.asarray(a, dtype=np.uint8).reshape((500, 944, 4))
    # screen3 = cv2.fastNlMeansDenoising(screen3, None, 10, 41, 21)
    return screen1, screen2, screen3