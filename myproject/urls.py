from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

def redirect_to_task(request):
    return redirect('task/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_task),
    path('task/', include('core.urls')),
]