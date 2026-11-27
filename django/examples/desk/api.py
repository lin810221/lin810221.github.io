from rest_framework import serializers,viewsets,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task,Tag
from .services import complete_task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task;fields=['id','owner','title','description','status','priority','due_date','tags','revision']
        read_only_fields=['id','owner','revision']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        user=self.context['request'].user
        self.fields['tags'].child_relation.queryset=Tag.objects.filter(owner=user) if user.is_authenticated else Tag.objects.none()

class IsOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):return obj.owner_id==request.user.pk

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class=TaskSerializer;permission_classes=[permissions.IsAuthenticated,IsOwner]
    def get_queryset(self):
        qs=Task.objects.for_user(self.request.user).select_related('owner').prefetch_related('tags')
        status=self.request.query_params.get('status')
        if status:
            if status not in Task.Status.values:raise serializers.ValidationError({'status':'Unknown choice'})
            qs=qs.filter(status=status)
        return qs
    def perform_create(self,serializer):serializer.save(owner=self.request.user)
    @action(detail=True,methods=['post'])
    def complete(self,request,pk=None):
        self.get_object()
        try:task,created=complete_task(user=request.user,pk=pk,key=request.data.get('key',''))
        except ValueError as exc:raise serializers.ValidationError({'key':str(exc)})
        return Response({'id':task.pk,'status':task.status,'revision':task.revision,'created':created})
