"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

from carsales import views
from carsales.api import (
    DealerViewSet, DealerCenterViewSet,
    CarViewSet, SaleViewSet, CustomerViewSet, UserViewSet
)

router = DefaultRouter()
router.register(r'dealers', DealerViewSet)
router.register(r'dealer-centers', DealerCenterViewSet)
router.register(r'cars', CarViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'user', UserViewSet, basename="user")

urlpatterns = [
    path('', views.ShowCarsalesView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
