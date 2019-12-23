from threading import Thread
import cv2
import numpy as np
import os

class FaceRecognitionVideoStream:

    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        print("init")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath);

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        #iniciate id counter
        self.id = 0

        # names related to ids: example ==> Marcelo: id=1,  etc
        self.names = ['None', 'sharan', 'abhishek', 'jajuBhaiyya', 'vijay', 'W'] 

        # Initialize and start realtime video capture
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640) # set video widht
        self.cam.set(4, 480) # set video height
        _, self.frame = self.cam.read()
        # Define min window size to be recognized as a face
        self.minW = 0.1*self.cam.get(3)
        self.minH = 0.1*self.cam.get(4)

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False


    def start(self):
        print("start thread")
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        print("read")
        # keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                return
            # if the thread indicator variable is set, stop the thread
            ret, img =self.cam.read()
            # img = cv2.flip(img, -1) # Flip vertically
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = self.faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(self.minW), int(self.minH)),
            )
            print(faces)
            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    id = self.names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                
                cv2.putText(img, str(id), (x+5,y-5), self.font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), self.font, 1, (255,255,0), 1)  
            
            self.frame = img

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.cam.release()
        self.stopped = True