from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

from rest_framework import viewsets
from .serializers import PostSerializer

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import json

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    #post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = Post.objects.all().order_by('published_date')
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@csrf_exempt
def post_list_api(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        serializer_json = json.dumps(serializer.data, ensure_ascii=False, default=str, indent=None)
        #return JsonResponse(serializer_json, safe=False)
        return HttpResponse(serializer_json, content_type='application/json')

@csrf_exempt
def post_detail_api(request, pk):
    # try:
    #     post = Post.objects.get(pk=pk)
    # except Post.DoesNotExist:
    #     return HttpResponse(status=404)

    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        serializer_json = json.dumps(serializer.data, ensure_ascii=False)
        return HttpResponse(serializer_json, content_type='application/json')
