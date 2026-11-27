from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Task,Tag

@admin.register(User)
class StudyUserAdmin(UserAdmin):
    fieldsets=UserAdmin.fieldsets+(('學習資料',{'fields':['display_name']}),)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=['title','owner','status','priority','updated_at']
    list_filter=['status','priority'];search_fields=['title','owner__username'];list_select_related=['owner']
    readonly_fields=['revision','created_at','updated_at'];filter_horizontal=['tags']
    def get_queryset(self,request):
        qs=super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(owner=request.user)
    def get_readonly_fields(self,request,obj=None):
        return self.readonly_fields if request.user.is_superuser else [*self.readonly_fields,'owner']
    def save_model(self,request,obj,form,change):
        if not request.user.is_superuser:obj.owner=request.user
        super().save_model(request,obj,form,change)
    def formfield_for_manytomany(self,db_field,request,**kwargs):
        if db_field.name=='tags' and not request.user.is_superuser:kwargs['queryset']=Tag.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field,request,**kwargs)
# Tag editing deliberately remains in the ORM examples; no unscoped admin shortcut.
