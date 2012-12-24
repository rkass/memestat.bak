import Image

def sections(path, hsplit, vsplit):
  x = Image.open(path)
  width, height = x.size
  print width*height
  sectCount = [[]] * hsplit * vsplit
  for iters in range(hsplit * vsplit):
    w = (((iters) % hsplit) * (width / hsplit), ((iters + 1) % hsplit) * (width / hsplit), width)
    q = (((iters) % vsplit) * (height / vsplit), ((iters + 1) % vsplit) * (height / vsplit), height)
    n1 = normalize(w)
    n2 = normalize(q)
    print n1
    print n2
    for x in range(n1[0], n1[1]):
      for y in range(n2[0], n2[1]):
        sectCount[iters].append((x, y))
  for x in sectCount:
    print len(x)

def normalize((x, y, z)):
  if y == 0:
    return (x, z)
  else:
    return (x, y)
    
sections("/home/ryan/Dropbox/library/AnnoyingFacebookGirl.jpg", 2, 2)
