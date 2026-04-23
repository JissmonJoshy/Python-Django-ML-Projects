from django import forms
from .models import LeukemiaImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = LeukemiaImage
        fields = ['image']