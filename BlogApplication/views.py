from django.shortcuts import render
from post.models import Post

def index(request):
	posts = Post.objects.all().order_by("-created_on")
	return render(request,"index.html",{'user':request.user,'posts':posts})
