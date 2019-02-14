from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    url = models.URLField()
    icon = models.ImageField(upload_to='products/icons')
    image = models.ImageField(upload_to='products/images')
    publish_date = models.DateTimeField()
    total_votes = models.IntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def body(self):
        return self.description[:512] + '.....'

    def __str__(self):
        return self.title

    def date_pretty(self):
        return self.publish_date.strftime('%b %e %Y')

    # Then override models save method:
    def save(self, *args, **kwargs):
        if not self.id:
            # Only set the slug when the object is created.
            self.slug = slugify(self.title)  # Or whatever you want the slug to use
        super(Product, self).save(*args, **kwargs)
