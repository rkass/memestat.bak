from django.db import models

class ImageMacro(models.Model):
  filename = models.FilePathField(max_length = 200)

class Meme(models.Model):
  classification = models.ForeignKey(ImageMacro, null = True, related_name = 'classification')
  thumbnailLink = models.URLField()
  fullSizeLink = models.URLField()
  score = models.IntegerField(null = True)
  submitter = models.CharField(max_length = 200, null = True)
  topCorr = models.DecimalField(max_digits = 11, decimal_places = 10, null = True)
  topDist = models.DecimalField(max_digits = 13, decimal_places = 10, null = True)
  source = models.CharField(max_length = 200)
  created = models.IntegerField()
  threadLink = models.URLField()
  strong_classification = models.BooleanField()
  img_corrupt = models.BooleanField()

class PotentialImageMacro(models.Model):
  thumbnailLink = models.URLField()
  fullSizeLink = models.URLField()
  score = models.IntegerField(null = True)
  submitter = models.CharField(max_length = 200, null = True)
  source = models.CharField(max_length = 200)
  created = models.IntegerField()
  threadLink = models.URLField()
  title = models.CharField(max_length = 200)
