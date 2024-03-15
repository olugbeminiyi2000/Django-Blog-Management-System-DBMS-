from django.urls import path
from . import views


app_name = "blogs"
urlpatterns = [
    path("signup", views.SignUp.as_view(), name="signup"),
    path("home", views.homepage, name="home"),
    path("blog/<int:special_number>/Blog", views.AllComment.as_view(), name="comment"),
    path("blog/<int:dj_user_pk>/create", views.BlogCreate.as_view(), name="create"),
    path("blog/<int:dj_user_pk>/read/<int:start>/<int:end>/<int:counter>", views.BlogRead.as_view(), name="read"),
    path("blog/<int:dj_user_pk>/readupdate/<int:start>/<int:end>/<int:counter>", views.BlogReadUpdate.as_view(), name="readupdate"),
    path("blog/<int:dj_user_pk>/update/<int:blog_post_id>/<path:back_path>", views.BlogUpdate.as_view(), name="update"),
    path("blog/<int:dj_user_pk>/readdelete/<int:start>/<int:end>/<int:counter>", views.BlogReadDelete.as_view(), name="readdelete"),
    path("blog/<int:dj_user_pk>/delete/<int:blog_post_id>/<path:back_path>", views.BlogDelete.as_view(), name="delete"),
    path("blog/<int:blog_post_id>/confirm/<path:back_path>", views.ConfirmDelete.as_view(), name="confirm"),
]
