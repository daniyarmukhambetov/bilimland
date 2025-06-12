from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProblemListView.as_view(), name='problem-list'),
    path('<int:pk>/', views.ProblemDetailView.as_view(), name='problem-detail'),
    path('<int:pk>/submit/', views.submit_answer, name='submit-answer'),
]