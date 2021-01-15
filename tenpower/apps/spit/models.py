from django.db import models
from datetime import datetime
from django.db.models import CASCADE
from apps.users.models import User

# Create your models here.
class Spit(models.Model):
    """吐槽"""
    content = models.CharField(max_length=40)  # 吐槽内容
    publishtime = models.DateTimeField(default=datetime.utcnow)  # 发布时间
    user = models.ForeignKey(User, on_delete=CASCADE)
    visits = models.IntegerField()  # 浏览量
    thumbup = models.IntegerField()  # 点赞数
    comment = models.IntegerField()  # 回复数
    parent = models.ForeignKey('self', on_delete=CASCADE)  # 上级id
    collected = models.BooleanField(default=False)  # 是否收藏
    hasthumbup = models.BooleanField(default=False)  # 是否点赞

    class Meta:
        db_table = 'tb_spit'
        verbose_name = '吐槽'
        verbose_name_plural = verbose_name