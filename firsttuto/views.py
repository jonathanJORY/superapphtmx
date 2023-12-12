from django.shortcuts import render
from django.views.generic import TemplateView,FormView,ListView
from django.contrib import messages
from django.contrib.auth.views import LoginView
from firsttuto.forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from firsttuto.models import Task

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class Login(LoginView):
    template_name = 'registration/login.html'

    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self,form):
        messages.error(self.request,'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        form.save() #save the user
        return super().form_valid(form)

def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists.</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available.</div>")

class TaskList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    template_name = 'task/tasks.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()
    
@login_required
def add_task(request):
    desc = request.POST.get('taskdescription')
    task = Task.objects.get_or_create(description=desc)[0]
    request.user.tasks.add(task)
    tasks = request.user.tasks.all()
    messages.success(request,"New Task: %s" % (desc))
    return render(request,'task/task-list.html',{'tasks':tasks})

@login_required
@require_http_methods(['DELETE'])
def delete_task(request,pk):
    request.user.tasks.remove(pk)
    tasks = request.user.tasks.all()
    return render(request,'task/task-list.html',{'tasks':tasks})

@login_required
def search_task(request):
    search_text = request.POST.get('search')
    usertasks = request.user.tasks.all()
    results = Task.objects.filter(description__icontains=search_text).exclude(
        description__in=usertasks.values_list('description',flat=True))[:10]
    context={"results":results}
    return render(request,'task/search-results.html',context)

def clear(request):
    return HttpResponse("")