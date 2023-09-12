from django.db import models
from django.urls import reverse
from django.utils import timezone
from extensions.utils import jalali_convertor
from django.utils.html import format_html
from account.models import User
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


# my manager
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status="p")
    
class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیردسته')
    title = models.CharField(max_length=200, verbose_name= "عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name= "آدرس دسته بندی")
    status = models.BooleanField(default=True, verbose_name= "آیا نمایش داده شود؟")
    position = models.IntegerField(verbose_name= "پوزیشن")

    class Meta:
        verbose_name = "دسته"
        verbose_name_plural = "دسته ها"
        ordering = ['position']
    
    def __str__(self):
        return self.title
    
    objects = CategoryManager()


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آی پی")

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="articles", verbose_name="نویسنده")
    title = models.CharField(max_length=200, verbose_name= "عنوان مقاله")
    slug = models.SlugField(max_length=100, unique=True, verbose_name= "آدرس مقاله")
    category = models.ManyToManyField(Category, verbose_name= "دسته بندی", related_name="articles")
    description = models.TextField(verbose_name="توضیح  مقاله")
    thumbnail = models.ImageField(upload_to="images", verbose_name="عکس")
    publish = models.DateTimeField(default= timezone.now, verbose_name="زمان انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
    is_special = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name="hits", verbose_name="بازدید ها")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"
        ordering = ['-publish']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("account:home")
    
    def jpublish(self):
        return jalali_convertor(self.publish)
    jpublish.short_description = "زمان انتشار"
    
    def thumbnail_tag(self):
        return format_html("<img width=100 height=90 style='border-radius: 20px' src='{}'>".format(self.thumbnail.url))
    thumbnail_tag.short_description = "عکس مقاله"

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "عنوان دسته بندی"
    
    objects = ArticleManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)