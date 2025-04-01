from django.urls import path
from AdminApp import views

urlpatterns=[
    path('index',views.index,name="index"),
    path('add_movies/',views.add_movies,name="add_movies"),
    path('save_movies',views.save_movies,name="save_movies"),
    path('view_moviews/',views.view_moviews,name="view_moviews"),
    path('del_movies/<int:mid>',views.del_movies,name="del_movies"),
    path('Edit_movies/<int:mid>',views.Edit_movies,name="Edit_movies"),


    path('add_genre/',views.add_genre,name="add_genre"),
    path('save_genre',views.save_genre,name="save_genre"),
    path('view_genre',views.view_genre,name="view_genre"),

    path('add_person/', views.add_person, name="add_person"),
    path('save_person', views.save_person, name="save_person"),
    path('list_persons', views.list_persons, name="list_persons"),
    path('delete_person/<int:person_id>',views.delete_person,name="delete_person"),

    path('loginpage/',views.loginpage,name="loginpage"),
    path('Admin_login/',views.Admin_login,name="Admin_login"),
    path('Admin_logout/',views.Admin_logout,name="Admin_logout"),



]