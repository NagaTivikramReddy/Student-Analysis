from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.GetCreateStudents.as_view()),
    path('student/add-mark/', views.GetAddMarks.as_view()),
    path('students/results/', views.GetFinalReport),
]
