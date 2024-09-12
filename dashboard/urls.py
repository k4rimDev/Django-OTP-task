from django.urls import path

from dashboard.views import (
    FileListView, 
    FileUploadView, 
    FileDetailView, 
    FileDeleteView, 
    FileAccessByLinkView, 
    CommentDeleteView,
    FileEditView,
    HashtagFilesView,
    FileDownloadView
)


urlpatterns = [
    path('', FileListView.as_view(), name='file_list'),
    path('files/upload/', FileUploadView.as_view(), name='file_upload'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file_detail'),
    path('files/<int:pk>/delete/', FileDeleteView.as_view(), name='file_delete'),
    path('file/<str:unique_link>/', FileAccessByLinkView.as_view(), name='file_access_by_link'),
    path('file/<int:pk>/edit/', FileEditView.as_view(), name='file_edit'),
    path('file/<int:pk>/download/', FileDownloadView.as_view(), name='file_download'),

    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),


    path('hashtag/<int:pk>/', HashtagFilesView.as_view(), name='hashtag_files')
]
