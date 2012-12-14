import urllib3

dropBoxDir = str.strip(open('dropBoxDir', 'r').read())
imgs = []
pageIndex = 9
while (pageIndex < 15):
  if (pageIndex == 0):
    wp = urllib3.PoolManager().request('GET', 'http://imgflip.com/memetemplates')
  else:
    wp = urllib3.PoolManager().request('GET', 'http://imgflip.com/memetemplates?page=' + str(pageIndex))
  pageIndex += 1
  page = wp._body
  while(True):
    find = page.find("mt-box")
    if (find == -1):
      break
    page = page[find + 1:] 
    beginLink = page[page.find("src") + 5:] 
    href = page[page.find("href"):]
    beginName = href[href.find(">") + 1:]  
    name = beginName[:beginName.find("<")]
    beginFull = page[page.find("mt-full") + 21:]
    full = "http://imgflip.com" + beginFull[:beginFull.find(">") - 1]
    fullSizeLink = urllib3.PoolManager().request('GET', full)
    fullSizePage = fullSizeLink._body
    imageLinkEndRev = fullSizePage[:fullSizePage.find(".jpg") + 4][::-1]
    imageLink = imageLinkEndRev[:imageLinkEndRev.find("\"")][::-1]
    fullSizeImage = urllib3.PoolManager().request('GET', imageLink)
    f = open(dropBoxDir + 'library/' + name.replace(' ', '') , 'wb')
    f.write(fullSizeImage.data)
    f.close()
    print name
    print imageLink

