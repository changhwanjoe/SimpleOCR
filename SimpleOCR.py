import os
import sys
import cv2
import numpy as np
import pytesseract
from  PIL import Image

X, Y = 50, 1550 # set roi vertex coordinates
W, H = 500, 400 # set roi bounding box 
PATH = './imgfiles' # set folder name

class SimpleOCR:
    def __init__(self):
        self.x, self.y = X, Y
        self.w, self.h = W, H
        self.path = PATH        
        if not os.path.isdir(self.path):        # if folder not exists
            os.mkdir(self.path)
        
        self.file_list = os.listdir(self.path)  # files in folder
        if len(self.file_list) == 0 :
            print("Folder is empty.")
            sys.exit()
        
        
    def run(self):
        for index, file_name in enumerate(self.file_list):
            x, y, w, h = self.x, self.y, self.w, self.h
            img = cv2.imread(self.path + '/' + file_name )                  
            roi = img[y:y+h, x:x+w]             # set roi   ---①
            print(f"roi.shape = {roi.shape}")   # roi shape (50,50,3)
            #cv2.imshow("roi", roi)

            #cv2.rectangle(roi, (0,0), (h-1, w-1), (0,255,0)) # roi 전체에 사각형 그리기 ---②
            
            roi_name = 'roi_'+str(index)+'.jpg'
            cv2.imwrite(roi_name, roi)

            result = pytesseract.image_to_string(Image.open(roi_name), lang='eng')
            
            li=result.split()
            print(f"li: {li}") 
            for ind,st in enumerate(result.split()):
                if st == "KSID":
                    print("ksid,",  li[ind+2])
                elif st =='Lat':
                    print("lat,",   li[ind+2])
                elif st =='Long':
                    print("long,",  li[ind+2])
    
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    so = SimpleOCR()
    so.run()

