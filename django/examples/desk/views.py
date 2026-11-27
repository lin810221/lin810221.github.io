from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.exceptions import BadRequest
from django.db import transaction,IntegrityError
from django.http import FileResponse,HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from .forms import SignupForm,TaskForm,AttachmentForm,TagForm
from .models import Task,Attachment,Tag
from .services import complete_task,owner_summary

def health(request):return JsonResponse({'status':'ok','application':'studyhub'})

class SignupView(CreateView):
    form_class=SignupForm;template_name='registration/signup.html';success_url=reverse_lazy('login')

class OwnerQuerysetMixin(LoginRequiredMixin):
    model=Task
    def get_queryset(self):return Task.objects.for_user(self.request.user)

class TaskList(OwnerQuerysetMixin,ListView):
    template_name='desk/task_list.html';context_object_name='tasks';paginate_by=5
    def get_queryset(self):
        qs=super().get_queryset().select_related('owner').prefetch_related('tags')
        status=self.request.GET.get('status','');q=self.request.GET.get('q','').strip()[:120]
        if status and status not in Task.Status.values:raise BadRequest('Unknown status')
        if status:qs=qs.filter(status=status)
        if q:qs=qs.filter(title__icontains=q)
        return qs
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs);context['summary']=owner_summary(self.request.user)
        context['filters']=self.request.GET.copy();context['filters'].pop('page',None)
        return context

class TaskDetail(OwnerQuerysetMixin,DetailView):
    template_name='desk/task_detail.html';context_object_name='task'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs);context['upload_form']=AttachmentForm();return context

class TaskFormMixin(LoginRequiredMixin):
    model=Task;form_class=TaskForm;template_name='desk/task_form.html'
    def get_form_kwargs(self):return {**super().get_form_kwargs(),'user':self.request.user}
    def form_valid(self,form):
        form.instance.owner=self.request.user
        messages.success(self.request,'任務已儲存。')
        return super().form_valid(form)

class TaskCreate(TaskFormMixin,CreateView):pass
class TaskUpdate(OwnerQuerysetMixin,TaskFormMixin,UpdateView):pass
class TaskDelete(OwnerQuerysetMixin,DeleteView):
    template_name='desk/task_confirm_delete.html';success_url=reverse_lazy('desk:list')

class TagOwnerMixin(LoginRequiredMixin):
    model=Tag
    def get_queryset(self):return Tag.objects.filter(owner=self.request.user)

class TagSaveMixin(LoginRequiredMixin):
    form_class=TagForm
    def get_form_kwargs(self):return {**super().get_form_kwargs(),'user':self.request.user}
    def form_valid(self,form):
        try:
            with transaction.atomic():
                form.instance.owner=self.request.user;form.save()
        except IntegrityError:
            form.add_error('name','相同名稱已存在，請重新確認。');return self.form_invalid(form)
        return redirect('desk:tags')

class TagList(TagSaveMixin,FormView):
    template_name='desk/tag_list.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs);context['tags']=Tag.objects.filter(owner=self.request.user);return context

class TagUpdate(TagOwnerMixin,TagSaveMixin,UpdateView):template_name='desk/tag_form.html'
class TagDelete(TagOwnerMixin,DeleteView):
    template_name='desk/tag_confirm_delete.html';success_url=reverse_lazy('desk:tags')

@login_required
@require_POST
def complete(request,pk):
    get_object_or_404(Task.objects.for_user(request.user),pk=pk)
    try:complete_task(user=request.user,pk=pk,key=request.POST.get('key',''))
    except ValueError:return HttpResponse('缺少有效的命令識別碼。',status=400)
    return redirect('desk:detail',pk=pk)

@login_required
@require_POST
def upload(request,pk):
    task=get_object_or_404(Task.objects.for_user(request.user),pk=pk)
    form=AttachmentForm(request.POST,request.FILES)
    if form.is_valid():
        item=form.save(commit=False);item.task=task;item.save();return redirect(task)
    return render(request,'desk/upload_error.html',{'form':form,'task':task},status=400)

@login_required
def download(request,pk):
    item=get_object_or_404(Attachment.objects.select_related('task').filter(task__owner=request.user),pk=pk)
    return FileResponse(item.file.open('rb'),as_attachment=True,filename=f'note-{item.pk}.txt',content_type='text/plain; charset=utf-8')

class ExportView(OwnerQuerysetMixin,PermissionRequiredMixin,ListView):
    permission_required='desk.export_task';raise_exception=True
    def render_to_response(self,context,**kwargs):
        return JsonResponse({'tasks':list(self.get_queryset().values('id','title','status'))})

async def async_health(request):
    # Pure async view, intentionally no blocking ORM or network I/O.
    return JsonResponse({'status':'ok','mode':'async'})
