from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('home', views.index, name="home"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('new_order', views.order, name="new_order_page"),
    path('register', views.register_view, name='register'),
    path("calculate_price", views.calculate_price, name='calculate'),
    path("place_new_order", views.place_order, name='order'),
    path("profile_page", views.profile, name="profile"),
    path("order_details/<int:order_id>", views.order_details, name="order_details"),
    path("media/cargo_images/<str:picture>", views.display_picture, name="display_picture"),
    path("order_pictures/<int:order_id>", views.order_pictures, name="order_pictures"),
    path("react", views.react, name="react"),
    path("order_placed/<int:order_id>", views.order_placed, name="order_placed"),
    path("contact_us", views.contact , name='contact'),
    path("get_user", views.get_user, name='get_user'),
    path("calculate_path", views.calculate_path, name='calculate_path'),
]
