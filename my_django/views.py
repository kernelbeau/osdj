from django.views.generic.base import TemplateView
from django.http import HttpResponse

class Index(TemplateView):
    template_name = "index.html"
