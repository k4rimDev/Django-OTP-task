from django.urls import path

from dashboard.api.views import FileMetadataAPIView, CommentDeleteAPIView


urlpatterns = [
    path('api/files/<int:pk>/metadata/', FileMetadataAPIView.as_view(), name='file_metadata_api'),
    path('api/comments/<int:pk>/delete/', CommentDeleteAPIView.as_view(), name='comment_delete_api'),
]
