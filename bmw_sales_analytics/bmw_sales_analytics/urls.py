from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', include('prediction.urls')),
    path('', include('visualization.urls')),
    path('basemode/', include('admin_data.urls')),
]
