import cv2
import mediapipe as mp
import pyautogui
from tkinter import messagebox
import time
import tkinter as tk
from PIL import Image, ImageTk
from time import strftime 
import string
import playsound
#from tkinter import PhotoImage


class EyeTrackerApp:
    def __init__(self, root, video_source=0,):
        global eye_label, second_label
        self.root = root
        self.root.geometry("1068x730+200+98")
        self.root.title(" Fatigue Detection")
        self.root.config(bg="#242424")
        self.root.resizable(False,False)
        
        #icon image
        icon_image=tk.PhotoImage(file="images/icon.png")
        root.iconphoto(False,icon_image)
        
        #background image
        
        self.background_photo=Image.open("images/Layer 40 Frame.png")
        
        self.background_photo=ImageTk.PhotoImage(self.background_photo)
        tk.Label(root,image=self.background_photo,background="#242424").place(x=45,y=20)
        
        
        
        #logo
        self.logo=Image.open("images/logo.png")
        self.logo=ImageTk.PhotoImage(self.logo)
        
        myimage1=tk.Label(root,image=self.logo,background="#ecf0f1")
        myimage1.place(x=60,y=35)
        
        
        ###clock

        def clock():
                text=strftime(' %H:%M %p ')
                string2= strftime('%A')
                day.config(text=string2)
                lbl.config(text=text)
                lbl.after(1000,clock)
        lbl=tk.Label(root,font=('digital-7' ,20),width=8,bg="#ecf0f1",fg="#fff")
        lbl.place(x=150,y=35)
        day=tk.Label(root,font=('digital-7' ,10),width=8,bg="#ecf0f1",fg="#fff")
        day.place(x=150,y=70)
        clock()
        
        
        self.user=Image.open("images/user.png")
        self.user=ImageTk.PhotoImage(self.user)
        
        user_button=tk.Button(root,image=self.user,background="#ecf0f1",activebackground="#bcdeff",bd=0,cursor='hand2')
        user_button.place(x=940,y=50)
        
        
        self.notification=Image.open("images/notification.png")
        self.notification=ImageTk.PhotoImage(self.notification)
        
        notification_button=tk.Button(root,image=self.notification,background="#ecf0f1",activebackground="#bcdeff",bd=0,cursor='hand2')
        notification_button.place(x=905,y=58)
        
        
        tk.Label(root,text="Eye:",font="Arial 15",bg="#3d3d3d",fg="#171717").place(x=500,y=540)
        eye_label=tk.Label(root,font="Arial 20 bold",bg="#3d3d3d",fg="lightpink")
        eye_label.place(x=550,y=535)

        tk.Label(root,text="Duration:",font="Arial 15",bg="#3d3d3d",fg="#171717").place(x=750,y=540)
        second_label=tk.Label(root,font="Arial 30 bold",bg="#3d3d3d",fg="lightgreen")
        second_label.place(x=830,y=530)
        
        
        
        
        
        

        
        

        self.video_source = video_source
        self.cam = cv2.VideoCapture(self.video_source)

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

        self.screen_w, self.screen_h = pyautogui.size()

        self.canvas = tk.Canvas(root,bg="#1e1e1e")
        self.canvas.place(x=500,y=150)

        self.ts = [0, 0, False]
        self.photo = None  

        self.update()
    

    def update(self):
        _, img = self.cam.read()
        # img = cv2.resize(img, None, fx=7.0,fy=0.8)
        img = cv2.flip(img, 1)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        output = self.face_mesh.process(rgb_img)
        landmark_points = output.multi_face_landmarks
        img_h, img_w, _ = img.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * img_w)
                y = int(landmark.y * img_h)
                cv2.circle(img, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = self.screen_w * landmark.x
                    screen_y = self.screen_h * landmark.y

            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * img_w)
                y = int(landmark.y * img_h)
                cv2.circle(img, (x, y), 3, (0, 255, 255))
                
            eye_label.config(text=f'{(left[0].y - left[1].y):.7f}')

            if (left[0].y - left[1].y) < 0.009:
                print("blined")
                if not self.ts[2]:
                    self.ts[0] = time.perf_counter()
                    print("starter time is ", self.ts[0])
                    self.ts[2] = True
                else:
                    self.ts[1] = time.perf_counter()
                    print("final time is ", self.ts[1])
                    duration = self.ts[1] - self.ts[0]
                    second_label.config(text=f'{duration:.2f}')
                    print(duration)
                    if duration >= 3:
                        playsound.playsound('alert.mp3', True)
            else:
                self.ts[0] = 0
                self.ts[1] = 0
                self.ts[2] = False

        # Convert the OpenCV image to a PhotoImage object and display it on the canvas
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        resized_image= img.resize((450,300))
        self.photo = ImageTk.PhotoImage(resized_image)
        self.canvas.config(width=self.photo.width(), height=self.photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.root.after(1, self.update) 

if __name__ == "__main__":
    root = tk.Tk()
    
    app = EyeTrackerApp(root)
    

    root.mainloop()
