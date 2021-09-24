
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),
    path("profile/<str:profile>", views.user_profile, name="user_profile"),
    path("add_follower/<str:profile>", views.add_follower, name="add_follower"),
    path("delete_follower/<str:profile>", views.delete_follower, name="delete_follower"),
    path("following/<str:profile>", views.following, name="following"),
    
    # API routes
    path("posts", views.posts, name="posts"),
    path("total_posts", views.total_posts, name="posts"),
    path("post/<int:post_id>", views.update_post, name="update_post"),
    path("is_liked/<str:post_id>", views.is_liked, name="is_liked"),
    path("like_post/<str:post_id>", views.like_post, name="like_post"),
    path("dislike_post/<str:post_id>", views.dislike_post, name="dislike_post")
]
