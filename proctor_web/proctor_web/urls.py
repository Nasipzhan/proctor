"""proctor_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from proctorweb.views import LoginView, RegisterView
from django.contrib import admin
from django.urls import path
from proctorweb import views
urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('instr', views.instr, name='instr'),
    path('logout', views.logout_view, name='instr'),
    path('faq', views.faq, name='faq'),
    path('login', LoginView.as_view(), name='login'),
    path('search', views.search, name='search'),
    path('camera',views.camera, name='camera'),
    path('test/<int:id>', views.test, name='test'),
    path('admin/', admin.site.urls),
    path('register', RegisterView.as_view(),name='register')
]
