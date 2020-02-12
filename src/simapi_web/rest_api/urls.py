from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('user/')
]


"""
urlpatterns = [
    url(r'^sample/$', SampleViewSet.as_view()),
    url(r'^sample/(?P<model_id>\d+)/$', require_GET(SampleViewSet.as_view())),
]
"""