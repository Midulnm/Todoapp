from django.shortcuts import render,HttpResponse,redirect
from . forms import RegisterForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm

from django.shortcuts import get_object_or_404
# Create your views here.

@login_required
def home(request):

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        
        # Create task and link to the logged-in user
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority
        )
        return redirect('home')

    # Security fix: Filter by request.user so users don't see each other's tasks
    tasks = Task.objects.filter(user=request.user).order_by('-create_at')
    return render(request, "index.html", {"tasks": tasks})

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = RegisterForm()

    return render(request,"register.html",{'form':form})

def login_view(request):
    if request.method =="POST":
        username =request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            return render(request,"login.html",{"error": "Invalid username or password"})

    return render(request,"login.html")
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def delete_task(request,id):
    task = get_object_or_404(Task, id=id, user = request.user)
    task.delete()

    return redirect('home')
@login_required
def complete_task(request, id):
    # Fetch the task, ensuring it belongs to the logged-in user
    task = get_object_or_404(Task, id=id, user=request.user)
    
    # Toggle the boolean value (True becomes False, False becomes True)
    task.complete = not task.complete 
    task.save()
    
    return redirect('home')

