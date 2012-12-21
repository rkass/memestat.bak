import os   
import Image 
import numpy
import sys
import math
from cv2 import *
import scipy
import harris

dropBoxDir = str.strip(open('dropBoxDir', 'r').read()) + 'library/'

### HISTOGRAM FUNCTION #########################################################
def calcHistogram(src):
    # Convert to HSV
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)

    # Extract the H and S planes
    size = cv.GetSize(src)
    h_plane = cv.CreateMat(size[1], size[0], cv.CV_8UC1)
    s_plane = cv.CreateMat(size[1], size[0], cv.CV_8UC1)
    cv.Split(hsv, h_plane, s_plane, None, None)
    planes = [h_plane, s_plane]

    #Define numer of bins
    h_bins = 30
    s_bins = 32

    #Define histogram size
    hist_size = [h_bins, s_bins]

    # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
    h_ranges = [0, 180]

    # saturation varies from 0 (black-gray-white) to 255 (pure spectrum color)
    s_ranges = [0, 255]

    ranges = [h_ranges, s_ranges]

    #Create histogram
    hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)

    #Calc histogram
    cv.CalcHist([cv.GetImage(i) for i in planes], hist)

    cv.NormalizeHist(hist, 1.0)

    #Return histogram
    return hist

### EARTH MOVERS ############################################################
def calcEM(hist1,hist2,h_bins,s_bins):

  #Define number of rows
  numRows = h_bins*s_bins

  sig1 = cv.CreateMat(numRows, 3, cv.CV_32FC1)
  sig2 = cv.CreateMat(numRows, 3, cv.CV_32FC1)

  for h in range(h_bins):
      for s in range(s_bins):
          bin_val = cv.QueryHistValue_2D(hist1, h, s)
          cv.Set2D(sig1, h*s_bins+s, 0, cv.Scalar(bin_val))
          cv.Set2D(sig1, h*s_bins+s, 1, cv.Scalar(h))
          cv.Set2D(sig1, h*s_bins+s, 2, cv.Scalar(s))

          bin_val = cv.QueryHistValue_2D(hist2, h, s)
          cv.Set2D(sig2, h*s_bins+s, 0, cv.Scalar(bin_val))
          cv.Set2D(sig2, h*s_bins+s, 1, cv.Scalar(h))
          cv.Set2D(sig2, h*s_bins+s, 2, cv.Scalar(s))

  #This is the important line were the OpenCV EM algorithm is called
  return cv.CalcEMD2(sig1,sig2,cv.CV_DIST_L2)


def numMatchesHelp(img1, img2):
  print "called"
  matches = 0
  width, height = img1.size
  for x in range(width):
    for y in range(height):
      first = img1.getpixel((x, y))
      if isinstance(first, int):
        first = (first, first, first)
      width2, height2 = img2.size
      for x2 in range(width2):
        for y2 in range(height2):
          second = img2.getpixel((x2, y2))
          if isinstance(second, int):
            second = (second, second, second)
          if first == second:
            matches += 1
  return matches

def harrisHelp(img1, img2):
  initWidth, initHeight = img1.size
  img2 = img2.resize((initWidth, initHeight), Image.BILINEAR)
  im1 = scipy.array(img1.convert("L"))
  im2 = scipy.array(img2.convert("L"))
  h1 = harris.compute_harris_response(im1)
  h2 = harris.compute_harris_response(im2)
  f1 = harris.get_harris_points(h1, 6)
  f2 = harris.get_harris_points(h2, 6)
  distance = 0.
  print len(f1)
  print len(f2)
  for x in range(min(len(f2), len(f1))):
    distance += math.sqrt((f1[x][0] - f2[x][0])**2 + (f1[x][1] - f2[x][1])**2)
  return distance/len(f2)

def harrisDistance(img1, img2):
  img2 = img2.resize(img1.size, Image.BILINEAR)
  im1 = scipy.array(img1.convert("L"))
  h1 = harris.compute_harris_response(im1)
  f1 = harris.get_harris_points(h1, 6)
  distance = 0.
  for x in range(len(f1)):
    x1 = int(f1[x][0])
    y1 = int(f1[x][1])
    first = img1.getpixel((x1, y1))
    second = img2.getpixel((x1, y1))
    if isinstance(first, int):
      first = (first, first, first)
    if isinstance(second, int):
      second = (second, second, second)
    distance += math.sqrt((first[0] - second[0])**2 +
          (first[1] - second[1])**2 + (first[2] - second[2])**2)
  return distance

def closest((x, y), pts):
  minDist = sys.maxint
  minIn = 0
  for x in range(len(pts)):
    x1 = int(pts[x][0])
    y1 = int(pts[x][1])
    dist = math.sqrt((x - x1)**2 + (y - y1)**2)
    if dist < minDist:
      minDist = dist
      minIn = x
  return minDist

def harrisComp(img1, img2):
  img2 = img2.resize(img1.size, Image.BILINEAR) 
  im1 = scipy.array(img1.convert("L"))
  im2 = scipy.array(img2.convert("L"))
  h1 = harris.compute_harris_response(im1)
  h2 = harris.compute_harris_response(im2)
  f1 = harris.get_harris_points(h1, 6)
  f2 = harris.get_harris_points(h2, 6)
  distance = 0.
  for x in range(len(f1)):
    distance += closest(f1[x], f2)
  return distance


def threeDPearsonHelp(img1, img2):
  initWidth, initHeight = img1.size
  img1 = img1.resize((initWidth * 16/initWidth, initHeight * 16/initWidth), Image.BILINEAR)
  width, height = img1.size
  img2 = img2.resize((width, height), Image.BILINEAR)
  r0, g0, b0, r1, g1, b1 = 0., 0., 0., 0., 0., 0.
  iters = 0
  for x in range(width):
    for y in range(height):
      first = img1.getpixel((x, y))
      second = img2.getpixel((x, y))
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)  
      if first != (255, 255, 255) and first != (0, 0, 0):
        r0 += first[0]
        g0 += first[1]
        b0 += first[2]
        r1 += second[0]
        g1 += second[1]
        b1 += second[2] 
        iters += 1
  r0 = r0 / iters
  g0 = g0 / iters
  b0 = b0 / iters
  r1 = r1 / iters
  g1 = g1 / iters
  b1 = b1 / iters
  num, denom0, denom1 = 0., 0., 0.
  for x in range(width):
    for y in range(height):
      first = img1.getpixel((x, y))
      second = img2.getpixel((x, y))
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)  
      xixm = math.sqrt((first[0] - r0)**2 + (first[1] - g0)**2 + (first[2] - b0)**2)
      yiym = math.sqrt((second[0] - r1)**2 + (second[1] - g1)**2 + (second[2] - b1)**2)
      num += xixm * yiym
      denom0 += xixm**2
      denom1 += yiym**2
  return num / (math.sqrt(denom0) * math.sqrt(denom1))
      



def oneDPearsonHelp(img1, img2):
  initWidth, initHeight = img1.size
  img1 = img1.resize((initWidth * 20/initWidth, initHeight * 20/initWidth), Image.BILINEAR)
  width, height = img1.size
  img2 = img2.resize((width, height), Image.BILINEAR)
  xtot, ytot = 0., 0.
  iters = 0
  for x in range(width):
    for y in range(height):
      first = img1.getpixel((x, y))
      second = img2.getpixel((x, y))
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
      first = img1.getpixel((x, y))
      second = img2.getpixel((x, y))
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
  distance = 0.0
  iters = 0.0
  for x in range(width):
    for y in range(height):
      first = img1.getpixel((x, y))
      second = img2.getpixel((x, y))
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)
      if True:#first != (255, 255, 255):
        distance += math.sqrt((first[0] - second[0])**2 +
          (first[1] - second[1])**2 + (first[2] - second[2])**2) 
        iters += 1
  return distance/iters

def colorTotalsHelp(img1, img2):
  r0 = 0.
  g0 = 0.
  b0 = 0.
  r1 = 0.
  g1 = 0.
  b1 = 0.
  width0, height0 = img1.size
  width1, height1 = img2.size
  img1size = width0 * height0
  img2size = width1 * height1
  for x in range(width0): 
    for y in range(height0):
      pix = img1.getpixel((x, y))
      if isinstance(pix, int):
        pix = (pix, pix, pix)
      r0 += pix[0]
      g0 += pix[1]
      b0 += pix[2]
  for x in range(width1):
    for y in range(height1):
      pix = img2.getpixel((x, y))
      if isinstance(pix, int):
        pix = (pix, pix, pix)
      r1 += pix[0]
      g1 += pix[1]
      b1 += pix[2]
  r0 = r0 / img1size
  g0 = g0 / img1size
  b0 = b0 / img1size
  r1 = r1 / img2size
  g1 = g1 / img2size
  b1 = b1 / img2size
  return (r0 - r1)**2 + (g0 - g1)**2 + (b0 - b1)**2

def histogramHelp(img1, img2):
  hist1 = img1.histogram()
  img2 = img2.resize(img1.size, Image.BILINEAR)
  hist2 = img2.histogram()
  dist = 0  
  for x in range(len(hist2)):
    dist += (hist1[x] - hist2[x])**2.
  return dist

def numMatches():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/'+ t)
      filesInDir = os.listdir(dropBoxDir)
      best = 0
      bestFile = ""
      secondBest = 0
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisNum = numMatchesHelp(target, Image.open(dropBoxDir + fileInDir))
          if thisDist > best:
            secondBest = best
            secondBestFile = bestFile
            best = thisNum
            bestFile = fileInDir
          elif thisNum > secondBest:
            secondBest = thisNum
            secondBestFile = fileInDir
        print "done"
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)

def colorTotalsSplitHelp(img1, img2, hsplit, vsplit):
  distance = 0.
  width0, height0 = img1.size
  
  width1, height1 = img2.size
  img1size = width0 * height0
  img2size = width1 * height1
  for iters in range(hsplit * vsplit):
    r0 = 0.
    g0 = 0.
    b0 = 0.
    r1 = 0.
    g1 = 0.
    b1 = 0.
    for x in range(((iters + 1) % hsplit) * (width0 / hsplit)):
      for y in range(((iters + 1) % vsplit) * (height0 / vsplit)):
        pix = img1.getpixel((x, y))
        if isinstance(pix, int):
          pix = (pix, pix, pix)
        r0 += pix[0]
        g0 += pix[1]
        b0 += pix[2]
    for x in range(((iters + 1) % hsplit) * (width1 / hsplit)):
      for y in range(((iters + 1) % vsplit) * (height1 / vsplit)):
        pix = img2.getpixel((x, y))
        if isinstance(pix, int):
          pix = (pix, pix, pix)
        r1 += pix[0]
        g1 += pix[1]
        b1 += pix[2]
    r0 = r0 / img1size 
    g0 = g0 / img1size
    b0 = b0 / img1size
    r1 = r1 / img2size
    g1 = g1 / img2size
    b1 = b1 / img2size
    distance += (r0 - r1)**2 + (g0 - g1)**2 + (b0 - b1)**2
  return distance
     

def colorTotals():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails/')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/'+ t)
      filesInDir = os.listdir(thumbnails)
      best = sys.maxint
      bestFile = ""
      secondBest = sys.maxint
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisDist = colorTotalsHelp(target, Image.open(filesInDir + fileInDir))
          if thisDist < best:
            secondBest = best
            secondBestFile = bestFile
            best = thisDist
            bestFile = fileInDir
          elif thisDist < secondBest:
            secondBest = thisDist
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""


def threeDPearson():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/'+ t)
      filesInDir = os.listdir(dropBoxDir)
      best = -2
      bestFile = ""
      secondBest = -2
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisDist = threeDPearsonHelp(target, Image.open(dropBoxDir + fileInDir))
          if thisDist > best:
            secondBest = best
            secondBestFile = bestFile
            best = thisDist
            bestFile = fileInDir
          elif thisDist > secondBest:
            secondBest = thisDist
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""


def oneDPearson():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/'+ t)
      filesInDir = os.listdir(dropBoxDir)
      best = -2
      bestFile = ""
      secondBest = -2
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisDist = oneDPearsonHelp(target, Image.open(dropBoxDir + fileInDir))
          if thisDist > best:
            secondBest = best
            secondBestFile = bestFile
            best = thisDist
            bestFile = fileInDir
          elif thisDist > secondBest:
            secondBest = thisDist
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""

def colorTotalsSplit(hsplit, vsplit):
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/' + t)
      filesInDir = os.listdir(dropBoxDir)
      best = sys.maxint
      bestFile = ""
      secondBest = sys.maxint
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisDist = colorTotalsSplitHelp(target, Image.open(dropBoxDir + fileInDir), hsplit, vsplit)
          if thisDist < best:
            secondBest = best
            secondBestFile = bestFile
            best = thisDist
            bestFile = fileInDir
          elif thisDist < secondBest:
            secondBest = thisDist
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""


def foundCode():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      targetIm = cv.LoadImage("/home/ryan/Dropbox/thumbnails/" + t)
      targetHistogram = calcHistogram(targetIm)
      filesInDir = os.listdir(dropBoxDir)
      best = sys.maxint
      bestFile = ""
      secondBest = sys.maxint
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          libIm = cv.LoadImage(dropBoxDir + fileInDir)
          libHistogram = calcHistogram(libIm)
          histComp = calcEM(libHistogram, targetHistogram, 30,32)
          if histComp < best:
            secondBest = best
            secondBestFile = bestFile
            best = histComp
            bestFile = fileInDir
          elif histComp < secondBest:
            secondBest = histComp
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""


def rawDistance():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/'+ t)
      filesInDir = os.listdir(dropBoxDir)
      best = sys.maxint
      bestFile = ""
      secondBest = sys.maxint
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisDist = rawDistanceHelp(target, Image.open(dropBoxDir + fileInDir))
          if thisDist < best:
            secondBest = best
            secondBestFile = bestFile
            best = thisDist
            bestFile = fileInDir
          elif thisDist < secondBest:
            secondBest = thisDist
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""

oneDPearson()


def harrisDist():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/'+ t)
      filesInDir = os.listdir(dropBoxDir)
      best = sys.maxint
      bestFile = ""
      secondBest = sys.maxint
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisDist = harrisComp(target, Image.open(dropBoxDir + fileInDir))
          if thisDist < best:
            secondBest = best
            secondBestFile = bestFile
            best = thisDist
            bestFile = fileInDir
          elif thisDist < secondBest:
            secondBest = thisDist
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""


def harrisCorners():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/'+ t)
      filesInDir = os.listdir(dropBoxDir)
      best = sys.maxint
      bestFile = ""
      secondBest = sys.maxint
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisDist = harrisDistance(target, Image.open(dropBoxDir + fileInDir))
          if thisDist < best:
            secondBest = best
            secondBestFile = bestFile
            best = thisDist
            bestFile = fileInDir
          elif thisDist < secondBest:
            secondBest = thisDist
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""

def histogram():
  thumbnails = os.listdir('/home/ryan/Dropbox/thumbnails')
  for t in thumbnails:
    if not t[0] == ".":
      target = Image.open('/home/ryan/Dropbox/thumbnails/'+ t)
      filesInDir = os.listdir(dropBoxDir)
      best = sys.maxint
      bestFile = ""
      secondBest = sys.maxint
      secondBestFile = ""
      for fileInDir in filesInDir:
        if not "." in fileInDir:
          thisDist = histogramHelp(target, Image.open(dropBoxDir + fileInDir))
          if thisDist < best:
            secondBest = best
            secondBestFile = bestFile
            best = thisDist
            bestFile = fileInDir
          elif thisDist < secondBest:
            secondBest = thisDist
            secondBestFile = fileInDir
      print "Best Match For " + t + ": " + bestFile + ", with score: " + str(best)
      print "Second Best Match For " + t + ": " + secondBestFile + ", with score: " + str(secondBest)
      print ""
