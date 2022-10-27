import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    success, img = cap.read()
    # hands, img = detector.findHands(img, flipType=False)    # with draw
    hands = detector.findHands(img, draw=False)   # no draw
    # print(len(hands)) # if with no draw

    if hands:   # if there is a hand
        # hand 1
        hand1 = hands[0]    # the first hand appeared
        lmList1 = hand1['lmList']   # List of 21 landmarks points
        bbox1 = hand1['bbox']   # bounding box info of the hand : x, y, w, h
        centerPoint1 = hand1['center']  # center point x, y
        type1 = hand1['type']    # type of detected hand (left or right)

        fingers1 = detector.fingersUp(hand1)    # detect what finger is up return 0 or 1

        # length, info, img = detector.findDistance(lmList1[8], lmList1[12], img)     # WITH DRAW
        # length, info    = detector.findDistance(lmList1[8], lmList1[12], img)     # no DRAW

        if len(hands) == 2:
            # hand 2
            hand2 = hands[0]  # the first hand appeared
            lmList2 = hand2['lmList']  # List of 21 landmarks points
            bbox2 = hand2['bbox']  # bounding box info of the hand : x, y, w, h
            centerPoint2 = hand2['center']  # center point x, y
            type2 = hand2['type']  # type of detected hand (left or right)

            fingers2 = detector.fingersUp(hand2)  # detect what finger is up return 0 or 1

    cv2.imshow("Image", img)
    cv2.waitKey(1)