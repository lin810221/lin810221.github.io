import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse

class User(AbstractUser):
    display_name=models.CharField('顯示名稱',max_length=60,blank=True)

class Tag(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['owner','name'],name='unique_owner_tag')]
        ordering=['name','pk']
    def __str__(self):return self.name

class TaskQuerySet(models.QuerySet):
    def for_user(self,user):return self.filter(owner=user)

class Task(models.Model):
    class Status(models.TextChoices):
        TODO='todo','待開始'
        DOING='doing','進行中'
        DONE='done','已完成'
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='study_tasks')
    title=models.CharField('標題',max_length=120)
    description=models.TextField('說明',blank=True)
    status=models.CharField('狀態',max_length=8,choices=Status.choices,default=Status.TODO)
    priority=models.PositiveSmallIntegerField('優先度',default=2,validators=[MinValueValidator(1),MaxValueValidator(3)])
    due_date=models.DateField('預計日期',null=True,blank=True)
    tags=models.ManyToManyField(Tag,blank=True,related_name='tasks')
    revision=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TaskQuerySet.as_manager()
    class Meta:
        ordering=['-created_at','-pk']
        indexes=[models.Index(fields=['owner','status'],name='task_owner_status_idx')]
        constraints=[models.CheckConstraint(condition=Q(priority__gte=1,priority__lte=3),name='valid_task_priority'),
            models.CheckConstraint(condition=Q(status__in=['todo','doing','done']),name='valid_task_status')]
        permissions=[('export_task','Can export own study tasks')]
    def get_absolute_url(self):return reverse('desk:detail',kwargs={'pk':self.pk})
    def __str__(self):return self.title

def private_upload(instance,filename):return f'attachments/{uuid.uuid4().hex}.txt'

class Attachment(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name='attachments')
    file=models.FileField(upload_to=private_upload)
    uploaded_at=models.DateTimeField(auto_now_add=True)

class CompletionEvent(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name='completion_events')
    key=models.CharField(max_length=64)
    revision=models.PositiveIntegerField()
    class Meta:
        constraints=[models.UniqueConstraint(fields=['task','key'],name='unique_task_command')]
