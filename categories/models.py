from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True) #link
    description = models.TextField(max_length=250, blank=True)
    cart_image = models.ImageField(upload_to='photos/categories/', blank =True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
            return reverse('product_by_category',args=[self.slug])


    def __str__(self):
        return self.category_name



class CategoryOffer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=True)
    off_percent = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def _str_(self):
        return self.name