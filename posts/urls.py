from django.urls import path
from . import views

urlpatterns = [

    # ✅ Public
    path("", views.post_list, name="post_list"),

    # ✅ Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/posts/", views.my_posts, name="my_posts"),
    path("dashboard/create/", views.create_post, name="create_post"),

    path("dashboard/edit/<int:pk>/", views.edit_post, name="edit_post"),
    path("dashboard/delete/<int:pk>/", views.delete_post, name="delete_post"),

    path("dashboard/categories/", views.categories, name="categories"),

    # ✅ ALWAYS LAST
    path("<slug:slug>/", views.post_detail, name="post_detail"),
]