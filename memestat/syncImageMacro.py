import settings
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import ImageMacro
import os

dropBoxDir = str.strip(open('../dropBoxDir').read())
filesInDir = os.listdir(dropBoxDir + 'library')
for f in filesInDir:
  newFile = 'library/' + f  
  ImageMacro.objects.get_or_create(filename = newFile)
