from django.views.generic.edit import FormView
from django.views.generic import TemplateView
import app.forms as f
from app.parsers import get_hypem_artists


class IndexView(FormView):
    template_name = 'index.html'
    form_class = f.UsernameForm


class ResultsView(TemplateView):
    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        username = self.request.GET.get('username', '')
        context = super().get_context_data(**kwargs)
        context['username'] = username
        context['artists'] = get_hypem_artists(username)
        return context
