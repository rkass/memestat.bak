import Image
import math
import os
import sys


dropBoxDir = str.strip(open('../dropBoxDir', 'r').read()) + 'library/'

def oneDPearsonHelp(img1, img2):
  initWidth, initHeight = img1.size
  img1 = img1.resize((initWidth * 20/initWidth, initHeight * 20/initWidth), Image.BILINEAR)
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
  img1 = img1.resize((initWidth * 16/initWidth, initHeight * 16/initWidth), Image.BILINEAR)
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


def classify(target):
  target = Image.open(target)
  topTwoCorr = correlationTopTwo(target, dropBoxDir)
  topTwoDist = distanceTopTwo(target, dropBoxDir)
  if topTwoDist[0] in topTwoCorr:
    return ('library/'+topTwoDist[0], topTwoDist, topTwoCorr)
  elif topTwoDist[1] in topTwoCorr:
    return ('library/'+topTwoDist[1], topTwoDist, topTwoCorr)
  else:
    return(None, topTwoDist, topTwoCorr)

