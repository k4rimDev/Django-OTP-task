from django.urls import path

from dashboard.views import (
    FileListView, 
    FileUploadView, 
    FileDetailView, 
    FileDeleteView, 
    FileAccessByLinkView
)


urlpatterns = [
    path('files/', FileListView.as_view(), name='file_list'),
    path('files/upload/', FileUploadView.as_view(), name='file_upload'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file_detail'),
    path('files/<int:pk>/delete/', FileDeleteView.as_view(), name='file_delete'),
    path('file/<str:unique_link>/', FileAccessByLinkView.as_view(), name='file_access_by_link'),
]
