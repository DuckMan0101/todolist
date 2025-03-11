from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm

# View to list tasks
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Only show tasks for the logged-in user
        return Task.objects.filter(user=self.request.user)

# View to add a new task
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        # Associate the task with the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

# View to mark a task as completed
class TaskCompleteView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = []  # No fields to update, just mark as completed
    template_name = 'tasks/task_confirm_complete.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        # Mark the task as completed
        form.instance.completed = True
        return super().form_valid(form)

# View to delete a task
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        # Ensure only the logged-in user can delete their tasks
        return Task.objects.filter(user=self.request.user)



