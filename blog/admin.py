from django.contrib import admin
from .models import Post, Category, Tag, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "category", "created_at", "published_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "content", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "created_at"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    search_fields = ("body", "author__username", "post__title")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Like)
admin.site.site_header = "Blog Platform Administration"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Content management"
