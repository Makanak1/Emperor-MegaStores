from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegisterUserView.as_view()),
    path('login/',views.LoginUserView.as_view()),
    path('logout/',views.LogoutUserView.as_view()),
]