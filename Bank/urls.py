from django.contrib import admin
from django.urls import path, include

# Список всіх шляхів проекту
urlpatterns = [
    # Адмінстраторська частина Django проєкту
    path('admin/', admin.site.urls),
    
    # Шлях до головного застосунку проєкту
    path('', include('paydesk.urls'))
]
