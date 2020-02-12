from django.conf.urls import url
from django.urls import path
# TODO write urls here and import simapi_web
urlpatterns = [
    path('user/')
]


"""
urlpatterns = [
    url(r'^sample/$', SampleViewSet.as_view()),
    url(r'^sample/(?P<model_id>\d+)/$', require_GET(SampleViewSet.as_view())),
]
"""