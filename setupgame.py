import subprocess, sys
import numpy as np
import cv2
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
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def process(original_image, color):
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
    elif(mode in min_methods and min_val < 1-confidence):
        top_left = min_loc
        bottom_right = (top_left[0] + dim[1], top_left[1] + dim[0])
        val = 1-min_val
    return top_left, bottom_right, val

def StartDetection(screen, images):
    for im in images:
        confidence = 0
        top_left = None
        i=0
        dict_imgs = images[im]['images']
        names = list(dict_imgs.keys())
        vals = list(dict_imgs.values())
        while(i < len(names) and not top_left):
            processed_screen = process(screen, images[im]['img_color'])
            processed_screen = region_of_interest(processed_screen, images[im]['bounds'])
            top_left, bottom_right, confidence = detect_img(
                img=processed_screen, 
                pattern=vals[i],
                confidence=images[im]['threshold'],
                mode=images[im]['mode'])
            if(not top_left):
                i+=1
        if(i < len(names)):
            cv2.rectangle(screen, top_left, bottom_right, images[im]['legend_color'], 1)
            cv2.putText(screen, f"{names[i][:1]}:{confidence:.5f}", (top_left[0]-5, top_left[1]-3), cv2.FONT_HERSHEY_SIMPLEX, 0.3, images[im]['legend_color'], 1, cv2.LINE_AA)