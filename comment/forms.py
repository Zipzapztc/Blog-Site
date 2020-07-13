from django import forms
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    content_type=forms.CharField(widget=forms.HiddenInput)
    object_id=forms.CharField(widget=forms.HiddenInput)
    text=forms.CharField(label=False,widget=CKEditorWidget(config_name='comment_ckeditor'))

    def __init__(self,*args, **kwargs):
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        content_type=self.cleaned_data['content_type']
        object_id=self.cleaned_data['object_id']
        try:
            model_type=ContentType.objects.get(model=content_type).model_class()
            model_object=model_type.objects.get(id=object_id)
            self.cleaned_data['content_object']=model_object
        except exceptions.ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户未登录')

        return self.cleaned_data