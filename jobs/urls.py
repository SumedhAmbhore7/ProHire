from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
    path('list/', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('application/<int:application_id>/status/<str:new_status>/', views.update_application_status, name='update_application_status'),
]
