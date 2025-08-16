from django.shortcuts import render
from django.views import View


class PageNotFoundView(View):
    status = 404
    template_name = '404.html'

    def get(self, request, exception=None):
        return render(request=request, template_name=self.template_name, status=self.status)
