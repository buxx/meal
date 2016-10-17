from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
import debug_toolbar

from meal.views import EditCurrentUserView
from meal.views import ReservationsView
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
    url(r'^accounts/reservations/', ReservationsView.as_view(), name='reservations'),
]
