from pathlib import Path
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Task,Tag,Attachment

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):model=User;fields=['username','display_name','email']

class TagForm(forms.ModelForm):
    class Meta:model=Tag;fields=['name']
    def __init__(self,*args,user,**kwargs):super().__init__(*args,**kwargs);self.user=user
    def clean_name(self):
        name=self.cleaned_data['name'].strip()
        if not name:raise forms.ValidationError('請填寫標籤名稱。')
        if Tag.objects.filter(owner=self.user,name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('你已經有相同名稱的標籤。')
        return name

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task;fields=['title','description','status','priority','due_date','tags']
        widgets={'due_date':forms.DateInput(attrs={'type':'date'})}
    def __init__(self,*args,user,**kwargs):
        super().__init__(*args,**kwargs);self.fields['tags'].queryset=Tag.objects.filter(owner=user)
    def clean_title(self):
        title=self.cleaned_data['title'].strip()
        if not title:raise forms.ValidationError('請填寫標題。')
        return title

class AttachmentForm(forms.ModelForm):
    class Meta:model=Attachment;fields=['file']
    def clean_file(self):
        upload=self.cleaned_data['file']
        if Path(upload.name).suffix.lower()!='.txt':raise forms.ValidationError('本示範只接受UTF-8文字檔。')
        if upload.size>65536:raise forms.ValidationError('檔案不可超過64 KiB。')
        content=upload.read(65537);upload.seek(0)
        try:content.decode('utf-8')
        except UnicodeDecodeError:raise forms.ValidationError('檔案必須是UTF-8文字。')
        return upload
