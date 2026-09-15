from django.urls import path
from . import views

# app_name = "articles"

urlpatterns = [
    path('',view=views.home, name='home'),
    path("category/<int:category_id>/", views.post_by_category, name="post_by_category"),
    path("blogs/search/",view=views.search, name='search'),
    path('blogs/<slug:slug>/', view=views.blogs, name="blogs"),
    path('register/',view=views.register,name='register'),
    path('login/',view=views.login,name='login'),
    path('logout/',view=views.logout,name='logout'),
]