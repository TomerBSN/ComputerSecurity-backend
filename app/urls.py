from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('forgot_pass/', views.ForgotPassView.as_view()),
    path('logout/', views.logout),
    path('menu/', views.menu),
    path('menu/change_pass/', views.ChangePassView.as_view()),
    path('menu/add_customer/', views.AddCustomerView.as_view()),
]
