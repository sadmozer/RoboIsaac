# Known issues

**ISSUE #1**: The detection window is significantly slow.

**FIX #1**: Changed screenshot library from PIL to MSS. Decreased the game screen area in which cv2.matchTemplate function searches for defined patterns: there's no need to check the whole image for static entities (like minimap rooms or doors)

---

**ISSUE #2**: Screenshots done to the game window while pressing any keyboard input are noisy. Some pixels can receive a small distortion (~5 points to each BGRA channel). See the file Noise.PNG

**FIX #2**: 
Create a file config.ini containing this:
```
[Options]
EnableColorCorrection=0
EnableCaustics=0
EnableShockwave=0
EnableLighting=0
EnableFilter=0
EnablePixelation=0
EnableBloom=0
```
Put it in the folder *C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\resources*. Then change **MaxRenderScale to 1**, **VSync to 0** in *C:\Users\Nick\Documents\My Games\Binding of Isaac Afterbirth\options.ini*

[Source](https://www.reddit.com/r/bindingofisaac/comments/2ld3t1/psa_how_to_speed_up_rebirth_considerably_even_on/)

---
**ISSUE #3**:
Screenshots done to the game window while the floor is Burning Basement are noisy.

**FIX #3**: TODO

