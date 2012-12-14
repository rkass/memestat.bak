import os   
import Image 
import numpy
import sys
import math

dropBoxDir = str.strip(open('dropBoxDir', 'r').read()) + 'library/'

#Looks at each pixel in img1 and tries to find point in img2 that's minimum distance
#then adds that distance to total
#terminates when img2 is empty
#images must be of equal size
#VVVEERRRRYYYY SLOOOWWWW
def distanceMatches(img1, img2):
  img1Width, img1Height = img1.size
  img1Pixels = img1.load()
  img2Pixels = img2.load()
  excluded = []
  totalDist = 0
  while(len(excluded) < img1.size):
    print "hey"
    minDist = 100
    minIndex = 0, 0
    for x in range(img1Width):
      for y in range(img1Height):
        if (not (x, y) in excluded):
          a = numpy.array(img1Pixels[x, y])
          b = numpy.array(img2Pixels[x, y])
          dist = numpy.linalg.norm(b-a)
          if (dist < minDist):
            minDist = dist
            minIndex = x, y
    excluded.append(minIndex)
    totalDist += minDist
  return totalDist

def rawDistance(img1, img2):
  width, height = img1.size
  if(img1.size != img2.size):
    img2 = img2.resize((width, height), Image.NEAREST)
  distance = 0
  img1Pixels = img1.load()
  img2Pixels = img2.load()
  for x in range(width):
    for y in range(height):
      print img2Pixels[x, y]
      distance += math.sqrt((img1Pixels[x, y][0] - img2Pixels[x, y][0])**2 +
        (img1Pixels[x, y][1] - img2Pixels[x, y][1])**2 + 
        (img1Pixels[x, y][2] - img2Pixels[x, y][2])**2) 
      #a = numpy.array(img1Pixels[x, y])
      #b = numpy.array(img2Pixels[x, y])
      #distance += numpy.linalg.norm(b - a)
  return distance

def rawDistance2(img1, img2):
  img1 = img1.resize((4, 4), Image.BILINEAR)
  width, height = img1.size
  img2 = img2.resize((width, height), Image.BILINEAR)
  distance = 0
  for x in range(width):
    for y in range(height):
      first = img1.getpixel((x, y))
      second = img2.getpixel((x, y))
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)
      distance += math.sqrt((first[0] - second[0])**2 +
        (first[1] - second[1])**2 + (first[2] - second[2])**2) 
  return distance

   
      
    
libImage =  Image.open(dropBoxDir+'../thumbnails/picard.jpg')

targImage =  Image.open(dropBoxDir+'../library/PicardWtf')
print rawDistance2(libImage, targImage)

"""
libImage =  Image.open(dropBoxDir+'../thumbnails2/onedoesnotsimply.jpg')
libPix = libImage.load()
target = Image.open(dropBoxDir+'../thumbnails2/writtenonedoesnotsimply.jpg')
if (libImage.size != target.size):
  print "not same size"
targetPixels = target.load()
targetWidth, targetHeight = target.size
numWhite = 0
notWhite = 0
for x in range(targetWidth):
  for y in range(targetHeight):
    if (targetPixels[x, y] == (255,255,255)):
      numWhite += 1
    else:
      notWhite += 1
    print targetPixels[x, y]


print notWhite
"""
filesInDir = os.listdir(dropBoxDir)
best = sys.maxint
secondBest = sys.maxint
for fileInDir in filesInDir:
  if not "." in fileInDir:
    thisDist = rawDistance2(libImage, Image.open(dropBoxDir + fileInDir))
    if thisDist < best:
      secondBest = best
      best = thisDist
    elif thisDist < secondBest:
      secondBest = thisDist
print "Best: "
print best
print "Second Best: "
print secondBest
