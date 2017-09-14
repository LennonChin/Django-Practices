from django.shortcuts import render

from django.views.generic import View

from .models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # sort
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # pagination for all_courses
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        paginator = Paginator(all_courses, 3, request=request)
        courses = paginator.page(page)

        context = {
            'courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        }
        return render(request, 'course-list.html', context)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        context = {
            'course': course
        }
        return render(request, 'course-detail.html', context)
