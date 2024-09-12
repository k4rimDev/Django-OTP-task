from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.views import View
from django.views.generic import (
    ListView, 
    CreateView, 
    DetailView, 
    DeleteView, 
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from dashboard.models import File, Comment, Hashtag
from dashboard.forms import FileForm, CommentForm


class FileListView(ListView):
    model = File
    template_name = 'dashboard/file_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        return File.objects.filter(public=True)

class FileAccessByLinkView(DetailView):
    model = File
    template_name = 'dashboard/file_detail.html'
    context_object_name = 'file'

    def get_object(self, queryset=None):
        return get_object_or_404(File, unique_link=self.kwargs['unique_link'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.increment_views()
        return super().get(request, *args, **kwargs)

class FileUploadView(LoginRequiredMixin, CreateView):
    model = File
    form_class = FileForm
    template_name = 'dashboard/file_upload.html'
    success_url = reverse_lazy('file_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        file = form.save()
        file.generate_unique_link()         
        file.save()
        form.save_m2m()
        return super().form_valid(form)


class FileDetailView(DetailView):
    model = File
    template_name = 'dashboard/file_detail.html'
    context_object_name = 'file'

    def get_context_data(self, **kwargs):
        # Increment file views and add comments to context
        self.object.increment_views()
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        context['views'] = self.object.get_views()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.user = request.user
            comment.file = self.object
            comment.save()
            return redirect('file_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)


class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    template_name = 'dashboard/file_confirm_delete.html'
    success_url = reverse_lazy('file_list') 

    def dispatch(self, request, *args, **kwargs):
        file = self.get_object()
        if file.owner != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('file_list')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user) | qs.filter(file__owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        file_id = self.object.file.id
        success_url = reverse_lazy('file_detail', kwargs={'pk': file_id})
        self.object.delete()
        return redirect(success_url)


class FileEditView(LoginRequiredMixin, UpdateView):
    model = File
    form_class = FileForm
    template_name = 'dashboard/file_edit.html'
    success_url = reverse_lazy('file_list')

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)
    

class FileDownloadView(View):
    def get(self, request, pk, *args, **kwargs):
        file_instance = get_object_or_404(File, pk=pk)
        response = HttpResponse(file_instance.file.open(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
        return response


class HashtagFilesView(ListView):
    model = File
    template_name = 'dashboard/hashtag_files.html'
    context_object_name = 'files'
    
    def get_queryset(self):
        self.hashtag = get_object_or_404(Hashtag, pk=self.kwargs['pk'])
        return File.objects.filter(hashtags=self.hashtag)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hashtag'] = self.hashtag
        return context
