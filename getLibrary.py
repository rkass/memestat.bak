import urllib3

dropBoxDir = str.strip(open('dropBoxDir', 'r').read())
imgs = []
pageIndex = 0
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
    thumbnail = beginLink[:beginLink.find(">") - 2]
    thumbnailPage = urllib3.PoolManager().request('GET', thumbnail)
    f = open(dropBoxDir + 'thumbnail_library/' + name.replace(' ', '') + '.jpg', 'wb')
    f.write(thumbnailPage.data)
    f.close()

