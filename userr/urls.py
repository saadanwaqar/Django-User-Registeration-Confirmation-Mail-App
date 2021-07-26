from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.index,name="index"),
    path('handleSignup',views.handleSignup,name="handleSignup"),
    path('handleLogin',views.handleLogin,name="handleLogin"),
    path('handleLogout',views.handleLogout,name="handleLogout"),
    path('<auth_token>', views.verify, name="verify")
]
