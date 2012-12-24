from django.db import models

class ImageMacro(models.Model):
  filename = models.FilePathField(max_length = 200)

class Meme(models.Model):
  classification = models.ForeignKey(ImageMacro, null = True, related_name = 'classification')
  thumbnailLink = models.URLField()
  fullSizeLink = models.URLField()
  score = models.IntegerField(null = True)
  submitter = models.CharField(max_length = 200, null = True)
  corrDict = models.CharField(max_length = 10000)
  distDict = models.CharField(max_length = 10000)
  source = models.CharField(max_length = 200)
  created = models.IntegerField()
  threadLink = models.URLField()
