# _*_ encoding: utf-8 _*_

from django.shortcuts import render

from django.views.generic import View

from .models import CourseOrg, CityDict

from .forms import UserAskForm

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse

# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        all_cities = CityDict.objects.all()

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        category = request.GET.get('category', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # sort
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "course":
                all_orgs = all_orgs.order_by("-course_nums")

        # count
        org_nums = all_orgs.count()

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
            'all_cities': all_cities,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            "sort": sort
        }
        return render(request, 'org-list.html', context)


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg': 'error'}", content_type='application/json')