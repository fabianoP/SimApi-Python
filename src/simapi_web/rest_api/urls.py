from django.urls import path
import rest_api.views

urlpatterns = [
    path('user/', rest_api.views.ListUserView.as_view(), name='api-user-list'),
    path('user/<int:pk>', rest_api.views.DetailsUserView.as_view(), name='api-user-details'),
    path('model/', rest_api.views.ListInitModelView.as_view(), name='api-model-list'),
    path('model/<int:pk>', rest_api.views.DetailsInitModelView.as_view(), name='api-model-details'),
    path('timestep/', rest_api.views.ListTimestepView.as_view(), name='api-timestep-list'),
    path('timestep/<int:pk>', rest_api.views.DetailsTimestepView.as_view(), name='api-timestep-details'),
    path('input/', rest_api.views.ListInputView.as_view(), name='api-input-list'),
    path('input/<int:pk>', rest_api.views.DetailsInputView.as_view(), name='api-input-details'),
    path('output/', rest_api.views.ListOutputView.as_view(), name='api-output-list'),
    path('output/<int:pk>', rest_api.views.DetailsOutputView.as_view(), name='api-output-details'),
]
