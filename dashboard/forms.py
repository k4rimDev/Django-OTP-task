from django import forms
from .models import File, Hashtag, Comment

class FileForm(forms.ModelForm):
    new_hashtags = forms.CharField(
        required=False,
        help_text="Separate new hashtags with commas.",
        widget=forms.TextInput(attrs={'placeholder': 'Add new hashtags'}),
    )

    class Meta:
        model = File
        fields = ['file', 'description', 'hashtags', 'public', 'expiration_date'] 
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the `user` argument
        super().__init__(*args, **kwargs)

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')

        allowed_file_types = ['image/png', 'application/msword', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']
        
        if uploaded_file.content_type not in allowed_file_types:
            raise forms.ValidationError("Unsupported file type. Please upload .png, .doc, or .pptx files.")

        return uploaded_file

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set the owner from the passed user
        if self.user:
            instance.owner = self.user

        if commit:
            instance.save()

        # Process new hashtags
        new_hashtags = self.cleaned_data.get('new_hashtags', '')
        if new_hashtags:
            hashtag_names = [tag.strip() for tag in new_hashtags.split(',') if tag.strip()]
            for tag_name in hashtag_names:
                hashtag, created = Hashtag.objects.get_or_create(name=tag_name)
                instance.hashtags.add(hashtag)

        self.save_m2m()

        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
