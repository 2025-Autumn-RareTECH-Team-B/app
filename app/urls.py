"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ↓ namespace 付きで include（goals/urls.py に app_name="goals" があるのでOK）
    path('goals/', include(('app.goals.urls', 'goals'), namespace='goals')),
    # ↓ これも namespace を付ける（steps/urls.py に app_name="steps" 必須）
    path('steps/', include(('app.steps.urls', 'steps'), namespace='steps')),
    path('', include('app.accounts.urls')),
]

