import Image
import math
import os
import sys
import algo2


dropBoxDir = str.strip(open('../dropBoxDir', 'r').read()) + 'library/'

def oneDPearsonHelp(img1, img2):
  initWidth, initHeight = img1.size
  img1 = img1.resize((16, 16), Image.BILINEAR)
  width, height = img1.size
  img2 = img2.resize((width, height), Image.BILINEAR)
  i1 = img1.load()
  i2 = img2.load()
  xtot, ytot = 0., 0.
  iters = 0
  for x in range(width):
    for y in range(height):
      first = i1[x, y]
      second = i2[x, y]
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)
      if first != (255, 255, 255) and first != (0, 0, 0):
        xtot += first[0] + first[1] + first[2]
        ytot += second[0] + second[1] + second[2]
        iters += 1
  xm = xtot / iters
  ym = ytot / iters
  num, denom0, denom1 = 0., 0., 0.
  for x in range(width):
    for y in range(height):
      first = i1[x, y]
      second = i2[x, y]
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)
      xi = first[0] + first[1] + first[2]
      yi = second[0] + second[1] + second[2]
      num += (xi - xm) * (yi - ym)
      denom0 += (xi - xm)**2
      denom1 += (yi - ym)**2
  return num / (math.sqrt(denom0) * math.sqrt(denom1))

def rawDistanceHelp(img1, img2):
  initWidth, initHeight = img1.size
  img1 = img1.resize((8, 8), Image.BILINEAR)
  width, height = img1.size
  img2 = img2.resize((width, height), Image.BILINEAR)
  i1 = img1.load()
  i2 = img2.load()
  distance = 0.0
  iters = 0.0
  for x in range(width):
    for y in range(height):
      first = i1[x, y]
      second = i2[x, y]
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)
      if True:#first != (255, 255, 255):
        distance += math.sqrt((first[0] - second[0])**2 +
          (first[1] - second[1])**2 + (first[2] - second[2])**2)
        iters += 1
  return distance/iters

def correlationTopTwo(target, directory):
  best = -1
  bestFile = ""
  secondBest = -1
  secondBestFile = ""
  for libImage in os.listdir(directory):
    if libImage[0] != ".":
      thisCorrelation = oneDPearsonHelp(target, Image.open(directory + libImage))
      if thisCorrelation > best:
        secondBest = best
        secondBestFile = bestFile
        best = thisCorrelation
        bestFile = libImage
      elif thisCorrelation > secondBest:
        secondBest = thisCorrelation
        secondBestFile = libImage
  return (bestFile, secondBestFile)

def distanceTopTwo(target, directory):
  best = sys.maxint
  bestFile = ""
  secondBest = sys.maxint
  secondBestFile = ""
  for libImage in os.listdir(directory):
    if libImage[0] != ".":
      thisDist = rawDistanceHelp(target, Image.open(directory + libImage))
      if thisDist < best:
        secondBest = best
        secondBestFile = bestFile
        best = thisDist
        bestFile = libImage
      elif thisDist < secondBest:
        secondBest = thisDist
        secondBestFile = libImage
  return (bestFile, secondBestFile)

def distanceTop(target, directory):
  best = sys.maxint
  bestFile = ""
  for libImage in os.listdir(directory):
    if libImage[0] != ".":
      thisDist = rawDistanceHelp(target, algo2.centerCut(Image.open(directory + libImage)))
      if thisDist < best:
        best = thisDist
        bestFile = libImage
  return (bestFile, best)

def correlationTop(target, directory):
  best = -1
  bestFile = ""
  for libImage in os.listdir(directory):
    if libImage[0] != ".":
      thisCorrelation = oneDPearsonHelp(target, algo2.centerCut(Image.open(directory + libImage)))
      if thisCorrelation > best:
        best = thisCorrelation
        bestFile = libImage
  return (bestFile, best)

def classify(target, directory = dropBoxDir):
  target = Image.open(target)
  try:
    target_crop = algo2.centerCut(target)
  except:
    return (None, False, None, None)
  topFileByDist, topDistVal = distanceTop(target_crop, directory)
  if topDistVal < 20:
    #Strong Classification
    return ('library/' + topFileByDist, True, topDistVal, None)  
  elif topDistVal < 40: 
    #Weak Classification
    return ('library/' + topFileByDist, False, topDistVal, None)
  else:
    topFileByCorr, topCorrVal = correlationTop(target_crop, directory)
    parent = 'library/' + topFileByDist
    if parent != topFileByCorr: parent = None
    return (parent, False, topDistVal, topCorrVal)
