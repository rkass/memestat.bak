import settings
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import Meme
import os

dropBoxDir = str.strip(open('../dropBoxDir', 'r').read())
filesInDir = os.listdir(dropBoxDir + 'library')
for f in filesInDir:
  newFile = dropBoxDir + 'library/' + f  
  objs = Meme.objects.filter(filename = newFile).count()
  if (objs == 0):
    Meme.objects.create(filename = newFile)
  elif (objs > 1):
    raise Exception("Duplicate file in memes collection: " + newFile)
