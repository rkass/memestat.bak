import Image
import math
import os
import sys
import numpy



 #cuts image into (width, hight*.4) at centerpoint
def centerCut(im):
  midpoint= int(im.size[1]/2); # hight
  points = (0, (midpoint - int(.15*im.size[1])), im.size[0], (midpoint + int(.15 *im.size[1]))) 
  cropped = im.crop(points);
  return cropped;


def compareWithTCH(im, xtiles, buckets):
  add=(im.size[0]/xtiles);
  xsplit=[];
  splitimage=[];
  
  for i in xrange (0,xtiles):
    xsplit.append(i*(im.size[0]/xtiles));
    box = (xsplit[i], 0, (xsplit[i]+add), im.size[1])
    splitimage.append(im.crop(box));
   
    
  
  return TCH(splitimage, buckets)

def TCH (split_image, buckets):
  TCH_array=[];
  sized=float(0.0);
    
  for i in xrange(0, len(split_image)):
    im = split_image[i].load()
    TCH_curr =[[0 for col in range(buckets)] for row in range(4)]
    for x in xrange(0, split_image[i].size[0]):
      for y in xrange(0, split_image[i].size[1]):
        sized+=1;
        pix = im[x, y]
        if isinstance(pix, int): 
          pix = (pix, pix, pix)
        red =   int(round(((pix[0])/255.0)*(buckets-1)));
        green = int(round(((pix[1])/255.0)*(buckets-1)));
        blue =  int(round(((pix[2])/255.0)*(buckets-1)));
        intense=int(round((red+green+blue)/3));

        TCH_curr[0][red]+=1
        TCH_curr[1][green]+=1
        TCH_curr[2][blue]+=1
        TCH_curr[3][intense]+=1
  
    TCH_array.append(TCH_curr);

  TCH_final = numpy.asarray(TCH_array, dtype=float);
  TCH_final *= (1.0/sized)
  return TCH_final;

   
"""
x = Image.open("/home/ryan/Dropbox/library/AnnoyingFacebookGirl.jpg");
z = centerCut(x);
z.show();
xtiles=7;
buckets = 11;
result = compareWithTCH(z, xtiles, buckets)
print result"""

      
      
     
      










