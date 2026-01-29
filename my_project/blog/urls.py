from django.urls import path 
from . import views 


urlpatterns = [
    path('',views.home,name="all-posts"),
    path('my-posts/',views.my_posts,name="my-posts"),
    path('detail/<int:pk>/',views.detail_post,name="detail-post"),
    path('create/',views.create_post,name="create-post"),
    path('update/<int:pk>/',views.update_post,name="update-post"),
    path('delete/<int:pk>/',views.delete_post,name="delete-post"),

    path('register/',views.register_view,name="register"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
]
