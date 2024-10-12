from django.urls import path
from .views import archive_form, archive_success, clear_archives, export_archives_csv, view_archives, reg, about_us
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('archive/', archive_form, name='archive_form'),
    path('success/', archive_success, name='archive_success'),
    path('view_archive/', view_archives, name='view_archives'),
    path('clear_archives/', clear_archives, name='clear_archives'),
    path('export_archives/', export_archives_csv, name='export_archives_csv'),
    path('reg/', reg, name='reg'),
    path('login/', auth_views.LoginView.as_view(
        template_name='archiver/reg/login.html'), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', about_us, name='about'),
]
