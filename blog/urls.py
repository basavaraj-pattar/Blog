from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("posts/new/", views.post_create, name="post_create"),
    path("posts/<slug:slug>/", views.post_detail, name="post_detail"),
    path("posts/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("posts/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("posts/<slug:slug>/comment/", views.add_comment, name="add_comment"),
    path("posts/<slug:slug>/like/", views.toggle_like, name="toggle_like"),
    path("comments/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    path("tag/<slug:slug>/", views.tag_posts, name="tag_posts"),
]
