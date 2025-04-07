from django.urls import path
from WebApp import views

urlpatterns=[
    path('',views.Home_Page,name="Home_Page"),

    path('User_Sign_Up/', views.User_Sign_Up, name="User_Sign_Up"),
    path('Save_Sign_Up/', views.Save_Sign_Up, name="Save_Sign_Up"),
    path('User_Sign_In', views.User_Sign_In, name="User_Sign_In"),
    path('User_Login/', views.User_Login, name="User_Login"),
    path('User_logout/', views.User_logout, name="User_logout"),

    path('Genre/',views.Genre,name="Genre"),
    path("genres/<int:genre_id>/", views.filtered_genre, name="filtered_genre"),

    path('Movie/',views.Movie,name="Movie"),
    path('trending_movies/',views.trending_movies,name="trending_movies"),
    path('CastList/',views.CastList,name="CastList"),
    path('movie/<int:movie_id>/', views.Movie_Details, name="Movie_Details"),
    path('wishlist/add/<int:movie_id>/', views.add_to_wishlist, name="add_to_wishlist"),
    path('wishlist/', views.view_wishlist, name="view_wishlist"),

]