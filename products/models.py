from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.translation import get_language

from ckeditor.fields import RichTextField


class Category(models.Model):
    en_title = models.CharField(max_length=100)
    fa_title = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='category/category_image', null=True)

    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_modified = models.DateTimeField(auto_now=True)

    def get_name(self):
        curr_lang = get_language()
        if curr_lang == 'fa':
            return self.fa_title
        else:
            return self.en_title

    def __str__(self):
        return self.en_title

    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.id])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    title = models.CharField(max_length=100)
    description = RichTextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product/product_img/', blank=True)
    dimension = models.CharField(blank=True, max_length=60)
    weight = models.PositiveIntegerField(null=True)
    characteristic = RichTextField(null=True)

    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

    def __str__(self):
        return self.title


class ActiveCommentsManager(models.Manager):

    def get_queryset(self):
        return super(ActiveCommentsManager, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect'))
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name=_('your review'))
    stars = models.CharField(verbose_name=_('your score to this product'), max_length=10, choices=PRODUCT_STARS)

    active = models.BooleanField(default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-datetime_created',)

    #manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManager()

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])
