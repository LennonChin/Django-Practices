# _*_ encoding: utf-8 _*_

from django.shortcuts import render

from django.views.generic import View

from .models import CourseOrg, CityDict

# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        all_cities = CityDict.objects.all()
        context = {
            'all_orgs': all_orgs,
            'org_nums': org_nums,
            'all_cities': all_cities
        }
        return render(request, 'org-list.html', context)
