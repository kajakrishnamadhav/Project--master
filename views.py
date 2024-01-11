from django.shortcuts import render, redirect, get_object_or_404
from App.models import Report
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import openpyxl
from django.db.models import Q
from .forms import ReportForm
from datetime import date
from django.contrib import messages
import os
from django.http import JsonResponse

# Create your views here.


def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect("/index")
        else:
            return HttpResponse("<h1>No user Found </h1>")

    return render(request, "loginpage.html")


@login_required
def indexpage(request):
    #files = Report.objects.all().order_by("-updated_by").filter(updated_by=request.user)
    if request.user.groups.filter(name='Part Inspector').exists() or request.user.is_superuser:
        files=Report.objects.all().order_by("-created_at")
    else:
        files=Report.objects.all().order_by("-created_at").filter(created_by=request.user)
    part_inspector = request.user.groups.filter(name='Part Inspector').exists() or request.user.is_superuser
    print(part_inspector,'part_inspector part_inspector')
    if request.method == "POST":
        if request.POST.get("upload"):
            files1 = request.FILES["file"]       
            file_nme=request.POST.get('file_name')     
            current_user = request.user
            doc = Report.objects.create(file=files1,file_name=file_nme, created_by=current_user.username)
            doc.save()
            return HttpResponseRedirect("/index")
        if request.POST.get("logout"):
            logout(request)
            return HttpResponseRedirect("/")
        
    return render(request,'indexpage.html',{"files": files,'part_inspector':part_inspector})



@login_required
def update(request, id):
    rep = Report.objects.get(id=id)
    if request.method == "POST" :
        form = ReportForm(request.POST, request.FILES,request.user, instance = rep)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_approved = 1
            instance.updated_by = request.user.username
            instance.save()
            print(instance.is_approved)
            messages.success(request, 'File Updated successfullly !')
            return redirect("/index")
        message = 'Something we are wrong!'
        return render(request, 'edit.html',{'message':message,'fm':form})
    else:
        rep = Report.objects.get(id=id)
        form = ReportForm(instance = rep)
        content = {'fm':form,'id':id}
        return render(request, 'edit.html',content)

@login_required
def delete(request, id):
    file=Report.objects.get(id=id)
    file.delete()
      
    return redirect("/index")


def ajax(request):
    if request.is_ajax():
        month = request.POST.get('month', None) # getting data from first_name input 
        print("ajax successfullly called")
        rep=Report.objects.filter(updated__month=month)
    return render(request,'empty.html')


def status_change(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        new_status = request.POST.get('new_status')
        remarks = request.POST.get('new_status')
        # Perform your logic to update the status
        
        report_obj = Report.objects.get(pk=record_id)
        print(report_obj.is_approved,'report_obj.is_approved')
        report_obj.is_approved = 1 if new_status == '1' else 0
        report_obj.remarks = remarks
        report_obj.updated_by = request.user.username
        print(report_obj.is_approved,'report_obj.is_approved')
        report_obj.save()

        # Respond with a success message
        return JsonResponse({'message': 'Status changed successfully.'})

    # Handle invalid requests (GET, etc.)
    return JsonResponse({'message': 'Invalid request method.'}, status=400)