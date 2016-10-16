"""meal_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
import debug_toolbar

from meal.views import EditCurrentUserView
from meal.views import CreateDays
from meal.views import LoginView
from meal.views import CreateGroupView
from meal.views import index_view
from meal.views import HomeView

urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^admin/meal/day/create_multiple/$', CreateDays.as_view(), name='admin.create_days'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', EditCurrentUserView.as_view(), name='edit_current_user'),
    url(r'^accounts/home/$', HomeView.as_view(), name='home'),
    url(r'^accounts/group/create/', CreateGroupView.as_view(), name='create_group'),
]
