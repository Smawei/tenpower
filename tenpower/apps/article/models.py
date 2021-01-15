from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
# Create your models here.
from question.models import Label
from apps.users.models import User

class Article(models.Model):

    title = models.CharField(max_length=100, null=True, default=None, verbose_name="标题")
    content = RichTextUploadingField(default='', verbose_name='文章内容')