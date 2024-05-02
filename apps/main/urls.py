from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="users-home"),
    path("dashboard/", views.dashboard, name="main-dashboard"),

    # The child paths
    path("child/add/", views.register_child, name="manage_child"),
    path("child/list/", views.child_list, name="child_list"),
    path("child/list/details/<int:pk>", views.child_details, name="child_details"),
    path("child/update/<int:pk>", views.update_child, name="update_child"),
    path("child/delete/<int:pk>", views.delete_child, name="delete_child"),

    # For the related models
    path("child/profile-picture/", views.update_picture, name="update_picture"),
    path('child/progress/', views.child_progress, name='child_progress'),
    path('child/progress/report/', views.child_progress_report, name='child_progress_report'),
    path("child/progress/delete/<int:pk>", views.delete_progress, name="delete_progress"),
    path("child/correspondence/", views.child_correspondence, name="child_correspondence"),
    path('child/correspondence/report/', views.child_correspondence_report, name='child_correspondence_report'),
    path("child/correspondence/delete/<int:pk>", views.delete_correspondence, name="delete_correspondence"),
    path("child/incident/", views.child_incident, name="child_incident"),
    path('child/incident/report/', views.child_incident_report, name='child_incident_report'),
    path("child/incident/delete/<int:pk>", views.delete_incident, name="delete_incident"),


    # Excel import paths
    path("child/import/", views.import_data, name="import"),
    path("excel/list/", views.import_details, name="imported_data"),
    path("del/excel-data/<int:pk>", views.delete_excel_data, name="delete_excel"),
    path("delete_confirmation/", views.delete_confirmation, name="delete_confirmation"),
]
