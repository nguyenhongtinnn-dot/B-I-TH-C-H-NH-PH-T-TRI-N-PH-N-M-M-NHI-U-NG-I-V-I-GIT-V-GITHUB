"""
URL configuration for Home project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('blog/', include('blog.urls')),
    
    # Bổ sung các đường dẫn mới từ Chương 9
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="page/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path("login/", views.Login, name="login"),
    # Sửa từ views.logout thành views.logout_view
path("logout/", views.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)