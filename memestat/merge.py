def merge(im1, img2, x): 
  i1 = im1.load()
  img2 = img2.resize(im1.size)
  i2 = img2.load()
  for x in range(img2.size[0]):
    for y in range(img2.size[1]):
      i1[x, y] = ((i1[x, y][0]*x + i2[x, y][0]) / (x + 1), 
              (i1[x, y][1]*x + i2[x, y][1]) / (x + 1),(i1[x, y][2]*x + i2[x, y][2]) / (x + 1))

