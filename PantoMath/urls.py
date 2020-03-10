"""PantoMath URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from panto_math_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('register_user/', views.registerUser),
    path('test/', views.test),
    path('forgot_password/', views.forgotPassword),
    path('forgot/', views.send_email),
    path('reset/', views.reset),
    path('create_user/', views.createUser),
    path('dashboard/', views.userDashboard),
    path('login/', views.userLogin),
    path('testAuthPassword/', views.testAuthPassword),
    path('show_keyword/', views.showKeyword),
    path('show_text/', views.showText),
    path('fetch_keyword/', views.fetchKeyword),
    path('fetch_text_sentiments/', views.fetchTextSentiments),
    path('verify_email/<str:verification_string_through_email>', views.verifyEmail),
    path('show_compare/', views.showCompare),
]
