from django.urls import path

from core.views.resource import add_resource_view, success_view
from core.views.home import HomeView
from core.views.user_management import login_view, logout_view, signup_view

urlpatterns = [
    path('add-resource/',
         add_resource_view,
         name='core-add-resource'),
    path('add-resource/success/',
         success_view,
         name='core-success'),
    path('add-resource/error/',
         success_view,
         name='core-error'),
    path('',
        HomeView.as_view(),
         name='home'),
    path('login/',
        login_view,
         name='login'),
    path('logout/',
        logout_view,
         name='logout'),
    path('signup/',
         signup_view,
         name='signup'),
]
