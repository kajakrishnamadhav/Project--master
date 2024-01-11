from django.contrib import admin
from App.models import Report,create_user

admin.site.register(create_user)

class ReportAdmin(admin.ModelAdmin):
    list_display=('id','file','file_name','created_by','updated_at','updated_by')

admin.site.register(Report,ReportAdmin)