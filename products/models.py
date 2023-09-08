from datetime import timezone
from django.db import models
from django.forms import ValidationError
from django.urls import reverse

from  categories.models import Category
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug , self.slug])
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)


    def __str__(self) :
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)
    
variation_category_choice = {
    ('color' , 'color'),
    ('size' , 'size'),
}

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
    def clean(self):
        """
        Custom validation method to ensure variations with the same category and value are unique for a product.
        """
        existing_variations = Variation.objects.filter(
            product=self.product,
            variation_category=self.variation_category,
            variation_value=self.variation_value,
        )

        if self.pk:
            # If the instance has a primary key (it's being updated), exclude it from the query.
            existing_variations = existing_variations.exclude(pk=self.pk)

        if existing_variations.exists():
            raise ValidationError(
                "A variation with the same category and value already exists for this product."
            )
    
    class Meta:
        unique_together = (
            ("product", "variation_category", "variation_value"),
        )


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=True)
    off_percent = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def _str_(self):
        return self.name

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products', max_length=255)
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
