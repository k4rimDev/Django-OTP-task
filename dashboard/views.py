from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import File, Comment
from .forms import FileForm, CommentForm


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
        file = form.save(commit=True)
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
