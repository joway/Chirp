from django.conf.urls import include, url
from django.contrib import admin

from config.router import router

urlpatterns = [
    # Examples:
    # url(r'^$', 'config.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r"^", include(router.urls)),
]
