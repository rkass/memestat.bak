from django.db import models

class ImageMacro(models.Model):
  filename = models.FilePathField(max_length = 200)

class Meme(models.Model):
  classification = models.ForeignKey(ImageMacro, null = True, related_name = 'classification')
  thumbnailLink = models.URLField()
  fullSizeLink = models.URLField()
  score = models.IntegerField(null = True)
  submitter = models.CharField(max_length = 200, null = True)
  bestCorr = models.ForeignKey(ImageMacro, related_name = 'best_corr')
  secondBestCorr = models.ForeignKey(ImageMacro, related_name = 'second_best_corr')
  bestCorrVal = models.DecimalField(decimal_places = 10, max_digits = 50)
  secondBestCorrVal = models.DecimalField(decimal_places = 10, max_digits = 50)
  bestDist = models.ForeignKey(ImageMacro, related_name = 'best_dist')
  secondBestDist = models.ForeignKey(ImageMacro, related_name = 'second_best_dist')
  bestDistVal = models.DecimalField(decimal_places = 10, max_digits = 50)
  secondBestDistVal = models.DecimalField(decimal_places = 10, max_digits = 50)
