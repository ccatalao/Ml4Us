from django.views.generic import TemplateView

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        context["title"] = "Learning Applications"
        return context


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context["title"] = "About"
        return context


