import urllib3
import json
import settings
import classify
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
dropBoxDir = str.strip(open('../dropBoxDir', 'r').read())
def fullSizePhoto(url):
  page = urllib3.PoolManager().request('GET', url)._body
  pageRev = page[:(page.find('.jpg') + 4)][::-1]
  return pageRev[:pageRev.find('=') - 1][::-1]

def processItem(arr):
  data = arr['data']
  q = Meme.objects.filter(threadLink = 'http://reddit.com' + data['permalink'])
  #Have we evaluated this submission yet?  Might be worth considering only checking 
  #memes within the last day.
  if q.count() == 1:
    #if we have, update the score and move on
    m = q[0]
    m.score = data['score']
    m.save()
  elif data['thumbnail'] != 'default':
    #have not evaluated this submission yet, run tests and store
    thumbnailPage = urllib3.PoolManager().request('GET', data['thumbnail'])
    filepath = dropBoxDir + 'target.jpg'
    f = open(filepath, 'wb')
    f.write(urllib3.PoolManager().request('GET', data['thumbnail']).data)
    f.close()
    classification = classify.classify(filepath)
    if ".jpg" in data['url']:
      fullSize = data['url']
    else:
      fullSize = fullSizePhoto(data['url'])
    if classification[0] == None:
      macro = None
    else:
      macro = ImageMacro.objects.get(filename = classification[0])
    m = Meme(classification = macro, thumbnailLink = data['thumbnail'],
          fullSizeLink = fullSize, score = data['score'], submitter = data['author'],
          corrDict = repr(classification[2]), distDict = repr(classification[1]),
          source = 'adviceanimals', created = data['created'], threadLink = 'http://reddit.com' + data['permalink'])
    m.save()
          

page = 'http://reddit.com/r/adviceanimals.json'
goDeeper = True #stop burrowing when we encounter a page with no posts over a score of 25
while(goDeeper):
  goDeeper = False
  pageJson = json.loads(urllib3.PoolManager().request('GET', page).data)
  for post in pageJson['data']['children']:
    if post['data']['score'] > 25:
      goDeeper = True
      processItem(post)
  lastId = pageJson['data']['after']
  page = 'http://reddit.com/r/adviceanimals.json?after=' + lastId
  print "On to the next"

