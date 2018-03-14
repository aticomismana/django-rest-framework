from django.urls import include, path, re_path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'postsDefaultRouter', views.PostViewSet)

urlpatterns = [
    re_path(r'^$', views.post_list, name='post_list'),
    re_path(r'^post/(?P<pk>\d+)$', views.post_detail, name='post_detail'),
    re_path(r'^post/new/$', views.post_new, name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),

    #url(r'^posts/$', views.PostViewSet, name='posts'),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^api/post/$', views.post_list_api),
    re_path(r'^api/post/(?P<pk>\d+)', views.post_detail_api),
]