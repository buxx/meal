from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
import debug_toolbar

from meal.views import EditCurrentUserView
from meal.views import MenuDetailView
from meal.views import CancelReservationView
from meal.views import MenuListView
from meal.views import ContactView
from meal.views import cancel_to_reservations
from meal.views import return_to_reservations
from meal.views import PreparePaymentView
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
    url(r'^accounts/group/create/$', CreateGroupView.as_view(), name='create_group'),
    url(r'^accounts/reservations/$', ReservationsView.as_view(), name='reservations'),
    url(r'^accounts/reservations/return/$', return_to_reservations, name='return_to_reservations'),
    url(r'^accounts/reservations/cancel/$', cancel_to_reservations, name='cancel_to_reservations'),
    url(r'^account/reservation/cancel/(?P<pk>\d+)/$', CancelReservationView.as_view(), name='cancel_reservation'),
    url(r'^accounts/pay/$', PreparePaymentView.as_view(), name='pay'),
    url(r'^account/contact/$', ContactView.as_view(), name='contact'),
    url(r'^account/menu/list/$', MenuListView.as_view(), name='menu_list'),
    url(r'^account/menu/(?P<pk>\d+)/$', MenuDetailView.as_view(), name='menu_detail'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
