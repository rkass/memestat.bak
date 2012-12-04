from django.db import models

class Meme(models.Model):
  filename = models.FilePathField(max_length = 200)

class Thumbnail(models.Model):
  classification = models.ForeignKey(Meme)
  link = models.URLField()
  confidence = models.DecimalField(decimal_places = 10, max_digits = 50)
