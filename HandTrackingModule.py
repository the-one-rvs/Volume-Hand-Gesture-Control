import cv2 as cv
import mediapipe as mp 
import time

class handDetector():
    def __init__ (self, mode=False, complexity = 1, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame
    def findPosition(self, img, handNo=0, draw=True):

        lmlist=[]
        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id, cx,cy])
                if draw:
                    cv.circle(img, (cx,cy), 7 ,(0,140,255), cv.FILLED)
        return lmlist


def main():
    pTime = 0
    cTime = 0
    capture = cv.VideoCapture(0)
    detector = handDetector()
    while True:
        isTrue, img = capture.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv.imshow('Camera',img)

        if cv.waitKey(1) & 0xFF==ord('d'):
            break

    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
