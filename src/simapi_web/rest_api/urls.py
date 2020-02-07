from django.conf.urls import url
from django.urls import path
from .views import UserViewSet, UserInitViewSet, UserInputViewSet, UserOutputViewSet

urlpatterns = [
    path('user/', UserViewSet.as_view({'get': 'list'}), name='api-user-list'),
    path('user/<int:pk>/', UserViewSet.as_view({'get': 'detail'}), name='api-user-detail'),
    path('user/<int:pk>/input/', UserInputViewSet.as_view({'get': 'detail'}), name='api-user-input'),
    path('user/<int:pk>/output/', UserOutputViewSet.as_view({'get': 'detail'}), name='api-user-output'),
    path('user/<int:pk>/init_model/', UserInitViewSet.as_view({'get': 'detail'}), name='api-user-init'),
]


"""
urlpatterns = [
    url(r'^sample/$', SampleViewSet.as_view()),
    url(r'^sample/(?P<model_id>\d+)/$', require_GET(SampleViewSet.as_view())),
]
"""