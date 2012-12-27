import Image
import math
import os
import sys



 #cuts image into (width, hight*.4) at centerpoint
def centerCut(im):
  midpoint= int(im.size[1]/2); # hight
  points = (0, (midpoint - int(.15*im.size[1])), im.size[0], (midpoint + int(.15 *im.size[1]))) 
  cropped = im.crop(points);
  return cropped;


def compareWithTCH(im, xtiles):
  add=(im.size[0]/xtiles);
  xsplit=[];
  splitimage=[];
  
  for i in xrange (0,xtiles):
    xsplit.append(i*(im.size[0]/xtiles));
    box = (xsplit[i], 0, (xsplit[i]+add), im.size[1])
    splitimage.append(im.crop(box));
   
    
    #TCH_final[i] = TCH(split_image[i], 8)
  
  return splitimage

def TCH (split_image, buckets):
  color_bucket_split = 255/buckets;
  intensity_bucket_split = 765/buckets;
  for i in xrange(0, split_image.size):
    im = split_image[i].load()
    TCH_curr=[[0]*4]*10
    for x in xrange(0, im.size[0]):
      for y in xrange(0,im.size[1]):
        sized+=1;
      #if im[x,y][0] = 

