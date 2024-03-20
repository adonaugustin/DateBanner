# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 09:31:21 2023

@author: adon.augustin
"""

# libraries to install
#pip install pillow
#pip install opencv-python

import os
import PIL
import cv2
import datetime
from PIL import Image,ImageDraw, ImageFont, ImageColor
import platform
from PIL.ExifTags import TAGS


path="./Input/" #enter input folder path
output_path="./Output/"     #enter output folder(if we put path of input folder then the image will be replaced in the in put folder)
ImageDesc="Image Taken: "
font = ImageFont.truetype('Inconsolata.ttf', 70) #font used

threshold=1.0





def SizetoMb(size_of_file):
    sizeinmb=size_of_file/(1024*1024)
    return sizeinmb

def SizetoKb(size_of_file):
    sizeinkb=size_of_file/(1024)
    return sizeinkb

def CreateBanner(Row,Col,TextStart,value,image1):
    hex_color = "#189BD8" 
    banner = Image.new(mode="RGBA", size=(Row,80), color=(hex_color))
    draw = ImageDraw.Draw(banner)
    draw.text((((Row/2)-TextStart),0),ImageDesc+value,font=font)
    image1.paste(banner,(0,Col-80))
    return image1

def ResizeFiles():
    try:
        for filename in os.listdir(path):
            #if(len==1):
                #break

            print("converting",filename)

            if filename.endswith(".jpg") or filename.endswith(".png"):
               
                filepath=os.path.join(path, filename)
                sizeinmb=SizetoMb(os.path.getsize(filepath))
               
                image = Image.open(os.path.join(path, filename))
                image1=cv2.imread(os.path.join(path, filename))
                r,c,_=image1.shape
               
                exifdata = image.getexif()
                for tagid in exifdata:
                    tagname = TAGS.get(tagid, tagid)
                    value = exifdata.get(tagid)
   
                    # printing the final result
                    if isinstance(value, bytes):
                        value = value.decode()
                        
                        
                    if(tagname=="DateTime"):
                            
                        value = exifdata.get(tagid)
                        left, top, right, bottom = font.getbbox(ImageDesc+value)
                        width = font.getlength(ImageDesc+value)
                        #print(f'left: {left}, top: {top}, right: {right}, bottom: {bottom}, width: {width}')
                        #width of the text is calculated, so width/2 gives centre of the text.
                        #this text needed to be placed in banner such a way that it is in half of width of the text from 
                        #half of the banner
                       
                        asp_ratio=c/r
                        textstart=width/2
                       
                        if asp_ratio > threshold:
                            rot_img = image.rotate(0,expand=True)
                        else :
                            rot_img = image.rotate(270,expand=True)
                        
                        bannerCreate=CreateBanner(c,r,textstart,value,rot_img)
                        bannerCreate.save(output_path+'/'+filename, quality=70)
                        #bannerCreate.show()
                            
                   


                    continue
            else:
                continue

    except:
               print("Exception thrown. path does not exist.")
               input('press any key?\n')

def main():
    
   
    ResizeFiles()
   

if __name__=="__main__":
    main()
