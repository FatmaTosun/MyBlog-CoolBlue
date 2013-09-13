from django import forms
from models import Post, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ['author','slug']


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'text')

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(CommentForm, self).__init__(*args, **kwargs)
		if user.is_authenticated():
			del self.fields['name']
			del self.fields['email']