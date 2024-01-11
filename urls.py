from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "App"

urlpatterns = [
    path("", views.loginpage),
    path("index", views.indexpage),
    path("delete/<int:id>/", views.delete,name="delete"),
    path("update/<int:id>/", views.update,name="update"),
    path('ajax', views.ajax, name='ajax'),
    path('status_change/', views.status_change, name='status_change'),
   
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
