
# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render, get_object_or_404

from post.models import Post, Comment
from post.forms import PostForm, CommentForm

def add_post(request, add_post_success_url="home", template="post/add_post.html"):

	form = PostForm(request.POST or None)
	if form.is_valid():
		post = form.save(commit=False)
		post.author = request.user
		post.save()
		return redirect(add_post_success_url)

	return render(request, template, {'form': form})

def post_detail(request,slug):
	post = get_object_or_404(Post, slug=slug)
	comments=Comment.objects.filter(content_type=
		ContentType.objects.get_for_model(Post), object_id=post.id)
	#ipdb.set_trace()

	form = CommentForm(user=request.user)

	if request.POST:
		form = CommentForm(request.POST, user=request.user)

		if form.is_valid():
			comment = form.save(commit=False)
			comment.content_type = ContentType.objects.get_for_model(Post)
			comment.object_id = post.id
			comment.post = post
			comment.save()

		return redirect(post.get_absolute_url())

	return render(request,'post/post_detail.html',
							  {'post': post,'form': form, 'comments':comments})



def user_posts(request):
	posts = Post.objects.filter(author = request.user)
	return render(request,'post/user_posts.html',{'posts':posts})
