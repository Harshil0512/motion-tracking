import cv2

cap = cv2.VideoCapture("./motion.mp4")
fourcc = cv2.VideoWriter().fourcc(*"mp4v")
_,frame1 = cap.read()
out = cv2.VideoWriter("motiontracking.mp4",fourcc,60,(frame1.shape[1],frame1.shape[0]))
_,frame2 = cap.read()
while cap.isOpened():
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(1,1),5)
    res,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilate = cv2.dilate(thresh,(20,20),iterations=25)
    contours,_ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for i in contours:
        (x,y,w,h) = cv2.boundingRect(i)
        if cv2.contourArea(i)>900:
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2,cv2.FONT_HERSHEY_SIMPLEX)
    cv2.imshow("Video",frame1)
    out.write(frame1)

    frame1 = frame2
    _,frame2 = cap.read()
    if cv2.waitKey(1 )== ord("q"):
        break

cv2.destroyAllWindows()