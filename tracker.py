import cv2
import mediapipe as mp
import pyautogui
from tkinter import messagebox
import time
import playsound
import winsound

ts = [0,0,False]

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
while True:
    _, img = cam.read()
    img = cv2.flip(img, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_img)
    landmark_points = output.multi_face_landmarks
    img_h, img_w, _ = img.shape
    if landmark_points: 
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * img_w)
            y = int(landmark.y * img_h)
            cv2.circle(img, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * img_w)
            y = int(landmark.y * img_h)
            cv2.circle(img, (x, y), 3, (0, 255, 255))
        
        if (left[0].y - left[1].y) < 0.009:
            print("blined")
            
        
        
            if ts[2] == False:
                ts[0] = time.perf_counter()
                print("starter time is ",ts[0])
                ts[2] = True
                
            else:
                ts[1] = time.perf_counter()
                print("final time is ",ts[1])
                duration=ts[1]-ts[0]
                print(duration)
                
                if duration>=3:
                    winsound.playsound('alert.mp3', True)
            
        else:
            
            ts[0]=0
            ts[1]=0
            ts[2]=False
            
            
                
                    
            
            
            
            
            
            
    
            
##            
                # messagebox.showerror("error","Alert Alert")


                
    cv2.imshow('Eye tracker- Controlled Mouse', img)
    cv2.waitKey(1)

