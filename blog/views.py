from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse
from blog.models import BlogPost
from blog.models import Sort
from blog.models import Comment
from blog.models import Tag
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from django.contrib.syndication.views import Feed  #RSS feed

import json
import requests
import traceback

class RSSFeed(Feed) :
    title = "PhanTask的博客"
    link = "feeds/blog/"
    description = "PhanTask的博客文章RSS feed"

    def items(self):
        return BlogPost.objects.order_by('-timestamp')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.timestamp

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return '/blog/%s/' % item.id

# Create your views here.
def index(request):
    # articles = BlogPost.objects.order_by('-timestamp')
    # classes = Sort.objects.all()
    # BlogPost.objects.order_by('-timestamp')
    tag = request.GET.get("tag")
    sort = request.GET.get("sort")
    c = None
    if sort:
        c = Sort.objects.get(name=sort)
        # print(c)
    if tag:
        c = Tag.objects.get(tagname=tag)
        # print(c)
    classes = Sort.objects.all()
    taglists = Tag.tag_list.get_tag_list
    tagCloud = json.dumps(taglists,ensure_ascii=False)
    articles=tag==None and sort==None and BlogPost.objects.order_by('-timestamp').filter(ispublished=1) \
             or tag!=None and BlogPost.objects.order_by('-timestamp').filter(ispublished=1).filter(tags=c) \
             or sort!=None and BlogPost.objects.order_by('-timestamp').filter(ispublished=1).filter(classic=c)
    paginator = Paginator(articles,5)
    page_num = request.GET.get('page')
    try:
        articles = paginator.page(page_num)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    comments= Comment.objects.order_by('-comment_date')
    t = loader.get_template("index.html")
    d = Context({'articles': articles, 'classes': classes,'comments':comments,'tagCloud':tagCloud,'hreftag':tag,'hrefsort':sort})
    return HttpResponse(t.render(d))

def bloglistView(request):
    # articles = BlogPost.objects.order_by('-timestamp')
    # classes = Sort.objects.all()
    # BlogPost.objects.order_by('-timestamp')
    bloglist = True
    classes = Sort.objects.all()
    taglists = Tag.tag_list.get_tag_list
    tagCloud = json.dumps(taglists,ensure_ascii=False)
    articles = BlogPost.objects.order_by('-timestamp')
    paginator = Paginator(articles,10)
    page_num = request.GET.get('page')
    try:
        articles = paginator.page(page_num)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    comments= Comment.objects.order_by('-comment_date')
    t = loader.get_template("index.html")
    d = Context({'articles': articles, 'classes': classes,'comments':comments,'tagCloud':tagCloud,'bloglist':bloglist})
    return HttpResponse(t.render(d))

def about(request):
    # articles = BlogPost.objects.order_by('-timestamp')
    # classes = Sort.objects.all()
    # BlogPost.objects.order_by('-timestamp')
    about = True
    classes = Sort.objects.all()
    taglists = Tag.tag_list.get_tag_list
    tagCloud = json.dumps(taglists,ensure_ascii=False)
    comments= Comment.objects.order_by('-comment_date')
    t = loader.get_template("index.html")
    d = Context({'classes': classes,'comments':comments,'tagCloud':tagCloud,'about':about})
    return HttpResponse(t.render(d))


def articleView(request, post_id):
    classics = Sort.objects.all()
    taglists = Tag.tag_list.get_tag_list
    tagCloud = json.dumps(taglists,ensure_ascii=False)
    if post_id and post_id != "":
        blog = BlogPost.objects.get(id=post_id)
        blog.readcount += 1
        blog.save()
    comments= Comment.objects.order_by('-comment_date')
    thesecomments = Comment.objects.filter(blog=blog)
    c = Context({"blog": blog, 'classes': classics, "comments": comments,"thesecomments": thesecomments,'tagCloud':tagCloud})
    t = loader.get_template("article.html")
    return HttpResponse(t.render(c))

@csrf_exempt
def asynHandler(request,action):
	return actions.get(action)(request)

@csrf_exempt
def submitComment(request):
    try:
        if request.POST:
            nickname = request.POST.get("nickname")
            email = request.POST.get("email")
            commentContent = request.POST.get("content")
            articleId = request.POST.get("articleId")
            blog = BlogPost.objects.get(id=int(articleId))
            commentdate = datetime.datetime.now()
            comment = Comment(blog=blog, comment_content=commentContent, comment_date=commentdate, email=email,
                              commentator=nickname)
            comment.save()

            blog.commentcount += 1
            blog.save()
    except:
        return HttpResponse("")
    return HttpResponse("ok")


# 定义异步操作类型
actions = {
    "submitComment": submitComment
}
