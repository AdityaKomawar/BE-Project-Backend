from django.db import models

# Create your models here.

class SingleImage(models.Model):
  name = models.CharField(max_length=200)
  image = models.ImageField(upload_to='images/', blank=True)

  def __str__(self):
    return self.name

  # def get_absolute_url(self):
  #   return reverse("singleimage_detail", kwargs={"pk": self.pk})
  
