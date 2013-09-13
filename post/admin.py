from django.contrib import admin
from post.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "author", "created"]

admin.site.register(Comment, CommentAdmin)