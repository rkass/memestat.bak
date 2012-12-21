import urllib3
import json


adviceAnimals = urllib3.PoolManager().request('GET',
  'http://reddit.com/r/adviceanimals.json')
aajson = json.loads(adviceAnimals.data)
thumbnail = aajson['data']['children'][0]['data']['thumbnail']
thumbnailPage = urllib3.PoolManager().request('GET', thumbnail)
f = open('/home/ryan/Dropbox/test.jpg', 'wb')
f.write(thumbnailPage.data)
f.close()
"""
wp = urllib3.PoolManager().request('GET', 
  'http://imgflip.com/memetemplates')
print wp"""
