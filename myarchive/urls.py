from django.contrib import admin
from django.urls import path, include
from archiver import views
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='archiver/reg/login.html'), name='login'),
    path('', include('archiver.urls')),
    path('admin/', admin.site.urls),
    path('archive/', views.archive_view, name='archive-view'),
    path('accounts/', include('django.contrib.auth.urls')),

]
