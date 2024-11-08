from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from todo.models import Tasks
from todo.forms import TaskForm
# Create your views here.
#authentication
#User login
def loginUser(request):
    page = True
    context = {'page':page}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,"Username does not exist.")
            return redirect('login')
        else:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f"welcome {request.user}")
                return redirect('home')
            else:
                messages.error(request,"User OR Password entered wrong..")
                return redirect('login')
    return render(request,'todo/login_register.html',context)

#User logout
def logoutUser(request):
    logout(request)
    return redirect('home')

#User register
def registerUser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exclude():
            messages.error(request,"Username already taken!")
            return redirect('register')
        else:
            if password != confirm_password:
                messages.error(request,"password does not matching!")
                return redirect('register')
            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = username
            )
            user.set_password(password)
            user.save()
            login(request,user)
            return redirect('home')


    return render(request,'todo/login_register.html')

#data rendering
# @login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        tasks = None
    else:
        user = request.user
        tasks = Tasks.objects.filter(user=user)
    return render(request,'todo/home.html',{'tasks':tasks})

#Adding Task
@login_required
def add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request,"Task added successfully..")
            return redirect('add')
    else:
        form = TaskForm()
    return render(request,'todo/add.html',{'form':form})
    
#update task
@login_required(login_url='login')
def updateTask(request,pk):
    obj = get_object_or_404(Tasks,id=pk)
    messages.warning(request,"If you update you task now, existing task will get deleted")
    if request.method == "POST":
        form = TaskForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"Task Successfully updated...")
            return redirect('home')
    else:
        form = TaskForm(instance=obj)
    return render(request,'todo/update.html',{'form':form,'id':obj.id})
#delete task
@login_required(login_url='login')
def deleteTask(request,pk):
    obj = get_object_or_404(Tasks,id = pk)
    messages.warning(request,"If you delete task now, the task will get deleted permanently.. ")
    if request.method == "POST":
        obj.delete()
        messages.success(request,"the task has been delete successfully...")
        return redirect('home')
    return render(request,'todo/delete.html',{'form':obj,'id':obj.id})

#Task details
@login_required(login_url='login')
def details(request):
    user = request.user
    tasks = Tasks.objects.filter(user=user)
    context = {'tasks':tasks}
    return render(request,'todo/details.html',context)