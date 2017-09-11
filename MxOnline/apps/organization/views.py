# _*_ encoding: utf-8 _*_

from django.shortcuts import render

from django.views.generic import View

from .models import CourseOrg, CityDict

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        all_cities = CityDict.objects.all()

        # pagination for orgs
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        paginator = Paginator(all_orgs, 5, request=request)
        orgs = paginator.page(page)

        context = {
            'all_orgs': orgs,
            'org_nums': org_nums,
            'all_cities': all_cities
        }
        return render(request, 'org-list.html', context)
