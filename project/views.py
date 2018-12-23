from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from project.models import Project, Label, Doc
from django.utils import timezone
from project.forms import ProjectForm, LabelForm, DocForm

from django.views.generic import (View, TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class ProjectExampleView(LoginRequiredMixin, DetailView):    
    template_name = 'project/project_detail.html'
    model = Project


class ProjectDetailView(DetailView):
    model = Project

def docs_list(request, pk):
    
    context = {}

    obj = get_object_or_404(Label, pk=pk)
    qs = Doc.objects.filter(label=pk)

    context['title'] = obj.text
    context['label_pk'] = pk

    paginator = Paginator(qs, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    context['docs_list'] = paginator.get_page(page)
    return render(request, 'project/doc_list.html', context)
'''
class DocListView(ListView):
    model = Doc
    paginate_by = 10
    
    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk')
        return self.model.objects.filter(label=pk)
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Label, pk=pk)
        queryset = self.model.objects.filter(label=pk)
        context = {}
        context['title'] = obj.text
        context['label_pk'] = pk
        context['doc_list'] = queryset
        return context
'''

class ProjectListView(View):
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            project_list = Project.objects.order_by('created')
            return render(request, "project/project_list.html", {"title": 'Projects', "project_list": project_list})

        user = request.user
        qs = Project.objects.filter(author=user).order_by('created')
        return render(request, "project/project_list.html", {"title": 'My projects', 'project_list': qs})



class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'project/project_form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        return super(ProjectCreateView, self).form_valid(form)

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create Project'
        return context


class ProjectUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'project/project_detail.html'

    form_class = ProjectForm

    model = Project


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'project/project_draft_list.html'

    model = Project

    def get_queryset(self):
        return Project.objects.filter(published_date__isnull=True).order_by('created')


class ProjectDeleteView(LoginRequiredMixin,DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def project_publish(request, pk):
    post = get_object_or_404(Project, pk=pk)
    post.publish()
    return redirect('project_detail', pk=pk)

@login_required
def add_label_to_project(request, pk):
    post = get_object_or_404(Project, pk=pk)

    if request.method == "POST":

        form = LabelForm(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            label.project = post
            label.save()
            return redirect('project_detail', pk=post.pk)
    else:
        form = LabelForm()
    return render(request, 'project/label_form.html', {'form': form, 'title': "New"})


@login_required
def label_approve(request, pk):
    label = get_object_or_404(Label, pk=pk)
    label.approve()
    return redirect('project_detail', pk=label.project.pk)


@login_required
def label_edit(request, pk):
    obj = get_object_or_404(Label, pk=pk)
    form = LabelForm(request.POST or None, instance = obj)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('project_detail', pk=obj.project.pk)

    return render(request, 'project/label_form.html', {'form': form, 'title': "Edit"})



@login_required
def label_remove(request, pk):
    obj = get_object_or_404(Label, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('project_detail', pk=obj.project.pk)
    context = {
        "object": obj,
    }
    template = "project/label_confirm_delete.html"
    return render(request, template, context)


@login_required
def add_doc_to_label(request, pk):
    post = get_object_or_404(Label, pk=pk)
    context = {}
    
    if request.method == "POST":
        form = DocForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.label = post
            doc.save()
            return redirect('label_docs_list', pk=pk)
    else:
        form = DocForm()

    return render(request, 'project/doc_form.html', {'form': form, 'title': "New"})


@login_required
def doc_edit(request, pk):
    obj = get_object_or_404(Doc, pk=pk)
    form = DocForm(request.POST or None, instance = obj)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('label_docs_list', pk=obj.label.pk)

    return render(request, 'project/doc_form.html', {'form': form, 'title': "Edit"})

@login_required
def doc_remove(request, pk):
    obj = get_object_or_404(Doc, pk=pk)
    obj.delete()
    context = {
        "object": obj,
    }
    return redirect('label_docs_list', pk=obj.label.pk)

@login_required
def import_data(request, pk):

    template_name = 'project/populate.html'

    label = get_object_or_404(Label, pk=pk)
    
    try:
        label_data = pd.read_excel("data/" + label.text + ".xlsx")  

        for i in range(len(label_data)):           
            d = Doc(label = label, text = label_data['texto'][i])
            d.save()
        return render(request, template_name, {"title": 'Success in importing text for '+label.text, "project_id": label.project.id})
    except:
        pass


    return render(request, template_name, {"title": 'Import data failed: Could not find a file named '+label.text + ' in the media folder.', "project_id": label.project.id})


