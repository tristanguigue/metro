from django.views.generic import TemplateView
from django.utils import translation
from django.shortcuts import redirect


def set_language_from_url(request, user_language):
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return redirect('home-view')


class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
    template_name = 'index.html'


class RelevanceView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(RelevanceView, self).get_context_data(**kwargs)
        return context
    template_name = 'relevance.html'


class ExplanationView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ExplanationView, self).get_context_data(**kwargs)
        return context
    template_name = 'explanation.html'


class MethodologyView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(MethodologyView, self).get_context_data(**kwargs)
        return context
    template_name = 'methodology.html'
