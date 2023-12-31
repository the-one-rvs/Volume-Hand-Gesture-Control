import cv2 as cv
import time
import numpy as np 
import HandTrackingModule as htm 
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



wcam, hcam = 640, 480


cap = cv.VideoCapture(0) 
cap.set(3, wcam)
cap.set(4, wcam)

cTime=0
pTime=0

detector = htm.handDetector(detectionCon= 0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol= minVol
volBar= 400
volPer = 0

while True:
    isTrue, img = cap.read()

    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    if len(lmlist) != 0:
        
        x1, y1= lmlist[4][1], lmlist[4][2]
        x2, y2= lmlist[8][1], lmlist[8][2]

        cx,cy = (x1+x2)//2, (y1+y2)//2

        cv.circle(img, (x1,y1), 11, (100,50,170), cv.FILLED)
        cv.circle(img, (x2,y2), 11, (100,50,170), cv.FILLED)
        
        cv.circle(img, (cx,cy), 11, (100,50,170), cv.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        
        
        vol = np.interp(length, [30,200], [minVol , maxVol])
        volBar = np.interp(length, [30,200], [400,150])
        
        volPer = (1 + vol/ 65) * 100


        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length<50:
            cv.circle(img, (cx,cy), 11, (0,255,0), cv.FILLED)

        if vol>=(-2.0):
            cv.circle(img, (cx,cy), 11, (0,255,255), cv.FILLED)

        cv.rectangle(img, (50,150), (85,400), (150,250,100), 3)
        cv.rectangle(img, (50,int(volBar)), (85,400), (150,250,100), cv.FILLED)
        cv.putText(img, f'{int(volPer)} %', (40,450), cv.FONT_HERSHEY_COMPLEX, 1, (150,250,100), 3)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (40,50), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)

    cv.imshow('Camera',img)


    if cv.waitKey(20) & 0xFF==ord('d'):
        break

cap.release()
cv.destroyAllWindows()