from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('dashboard',views.dashboard,name="dashboard"),
    
    path('ytvd',views.ytvd,name="ytvd"),
]
