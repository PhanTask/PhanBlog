from django.conf.urls import *
from blog.views import index
from blog.views import articleView
from blog.views import bloglistView
# from blog.views import searchView
from blog.views import submitComment
from blog.views import asynHandler
# url(r'([\s\S]*)',searchView),
urlpatterns = [url(r'^$',bloglistView),url(r'^(\d+)',articleView),url(r'^comment$',asynHandler,{'action':'submitComment'})]