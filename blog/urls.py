from django.urls import path

from .views import ListContentAPIView, SubmitScoreAPIView

urlpatterns = [

    path('list', ListContentAPIView.as_view(), name='blog-list'),
    path('submit_score', SubmitScoreAPIView.as_view(), name='submit-score'),

]
