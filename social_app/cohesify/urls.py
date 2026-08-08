from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("friends/", views.friends, name="friends"),
    path("profile/", views.profile, name="profile"),
    path("posts/", views.posts, name="posts"),
    path("comments/<int:post_id>", views.comments, name="comments"),
    path("search/", views.search, name="search"),
    path("undo_redo/", views.undo_redo, name="undo_redo"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]