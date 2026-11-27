from django.db import transaction
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Task,Attachment
from .services import invalidate_after_commit

@receiver(post_save,sender=Task)
@receiver(post_delete,sender=Task)
def task_changed(sender,instance,**kwargs):invalidate_after_commit(instance.owner_id)

@receiver(post_delete,sender=Attachment)
def attachment_deleted(sender,instance,**kwargs):
    storage=instance.file.storage;name=instance.file.name
    if name:transaction.on_commit(lambda:storage.delete(name))
