from django.contrib import admin
from django.urls import path, include
from core.views import HomeView,home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', home, name='homepage'),
    path('admin/', admin.site.urls),
    path('<slug:category_slug>/', home, name='category_wise_pet'),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path('pets/', include('pets.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
