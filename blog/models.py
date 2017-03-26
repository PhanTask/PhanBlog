# -*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
import hashlib


# 用户模型
class Master(models.Model):
    displayname = models.CharField(max_length=56)
    loginname = models.CharField(max_length=56)
    password = models.CharField(max_length=128)
    user_email = models.EmailField(blank=True)
    user_status = models.BooleanField()
    registered_date = models.DateField()

    def __str__(self):
        return self.displayname


# 分类模型
class Sort(models.Model):
    name = models.CharField(max_length=56, verbose_name='类型')
    blogcount = models.IntegerField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sort, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# 标签操作模型
class TagManager(models.Manager):
    @property
    def get_tag_list(self):  # 返回文章标签列表, 每个标签以及对应的文章数目
        tags = Tag.objects.all()  # 获取所有标签
        taglist = []
        for i in range(len(tags)):
            taglist.append([])
        for i in range(len(tags)):
            temp = Tag.objects.get(tagname=tags[i])  # 获取当前标签
            posts = temp.blogpost_set.all()  # 获取当前标签下的所有文章
            taglist[i].append(tags[i].tagname)
            taglist[i].append(len(posts))
        return taglist


# 标签模型
class Tag(models.Model):
    tagname = models.CharField(max_length=56, verbose_name='标签名称')
    blogcount = models.IntegerField()
    objects = models.Manager()
    tag_list = TagManager()  # 自定义的管理器

    def __str__(self):
        return self.tagname


# 博客模型
class BlogPost(models.Model):
    title = models.CharField(max_length=150, verbose_name='标题')
    body = RichTextUploadingField(verbose_name='正文')
    abstract = RichTextUploadingField(verbose_name='摘要')
    timestamp = models.DateTimeField(verbose_name='成稿日期')
    author = models.ForeignKey(Master, null=True)
    # tags = models.CharField(max_length=1024, verbose_name='标签', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    classic = models.ForeignKey(Sort, verbose_name='分类')
    ispublished = models.BooleanField(default=False, verbose_name='是否发布')
    commentcount = models.IntegerField(blank=True, default=0, verbose_name='评论')
    readcount = models.IntegerField(blank=True, default=0, verbose_name='阅读')

    def gettags(self):  # 返回一个文章对应的所有标签
        tag = self.tags.all()
        return tag

    def __str__(self):
        return self.title


# 评论模型
class Comment(models.Model):
    blog = models.ForeignKey(BlogPost)
    comment_content = models.TextField(max_length=1024)
    comment_reply = models.TextField(max_length=1024, default='')
    comment_date = models.DateTimeField()
    email = models.CharField(max_length=32)
    commentator = models.TextField(max_length=32)

    def __str__(self):
        return self.commentator


# 标签管理模型
class TagAdmin(admin.ModelAdmin):
    list_display = ('tagname', 'blogcount')


# 分类管理模型
class SortAdmin(admin.ModelAdmin):
    list_display = ('name', 'blogcount', 'slug')


# 博客管理模型
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ispublished', 'timestamp')


# 评论管理模型
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'comment_content', 'comment_date', 'email', 'commentator')


# 用户管理模型
class MasterAdmin(admin.ModelAdmin):
    list_display = ('displayname', 'loginname', 'password', 'user_email', 'user_status', 'registered_date')


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Sort, SortAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Tag, TagAdmin)
