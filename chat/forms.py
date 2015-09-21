
from django import forms
from .models import Message

class PostForm(forms.ModelForm):
    class Meta:
        model = Message
        # exclude = ['author', 'updated', 'created', ]
        fields = ['message_text']
        #message_text = forms.TextInput(widget=forms.TextInput(attrs={'size': '70'}))
        #message_text = forms.CharField(widget=forms.Textarea)
        widgets = {
            'message_text': forms.TextInput(
                attrs={'id': 'message_text', 'required': True, 'placeholder': 'new message...',}
            ),
        }