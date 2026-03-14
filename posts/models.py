from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
# Create your models here.

class ActivePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS_CHOICES = (('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    tags = models.ManyToManyField(Tag,related_name="posts", blank=True  )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #  Custom manager
    objects = ActivePostManager()

    #  Access everything including deleted
    all_objects = models.Manager()


    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.is_deleted =True
        self.save()