from django.views.generic import TemplateView
from django.shortcuts import render


class SignUpInfoView(TemplateView):
    http_method_names = ['get']
    template_name = 'sign_up_info/sign_up_info.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
