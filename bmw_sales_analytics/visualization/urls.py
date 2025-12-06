from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('models/', views.models_page, name='models'),
    path('visualization/', views.redirect_home, name='visualization'),

    # payment gateway
    path('create_order/', views.create_order),
    path('payment_success/', views.payment_success),
]
