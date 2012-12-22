import urllib3

def fullSizePhoto(url):
  page = urllib3.PoolManager().request('GET', url)._body
  pageRev = page[:(page.find('.jpg') + 4)][::-1]
  return pageRev[:pageRev.find('=') - 1][::-1]

def imgurFullSize(url):

 
quickMemePic('http://www.quickmeme.com/meme/3saaww/')
  

