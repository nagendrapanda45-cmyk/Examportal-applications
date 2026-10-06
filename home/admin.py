# home/admin.py
from django.contrib.admin import AdminSite
from django.shortcuts import render
from home.users.models import Users, Question, Tests, Result,Configuration
from django.db.models import Count, Avg
import json
from django.utils.http import urlencode
from datetime import datetime, timedelta

current_year = datetime.now().year

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        if not self.has_permission(request):
            return self.login(request, extra_context)
        total_users = Users.objects.filter(deleted=False).count()
        total_questions = Question.objects.filter(deleted=False).count()
        total_tests = Tests.objects.filter(is_submitted=1).count()
        total_results = Result.objects.count()
        total_passed = Result.objects.filter(result_status='pass').count()

        if total_results > 0:
            pass_percentage = round((total_passed / total_results) * 100, 2)
        else:
            pass_percentage = 0

        
        selected_specialisation = request.GET.get('specialisation', '').strip()

        # General Test Data
        gt_attended = Tests.objects.filter(test_type='GT', is_submitted=True).count()
        gt_results = Result.objects.filter(test__test_type='GT')
        gt_qualified = gt_results.filter(result_status='pass').count()
        gt_not_qualified = gt_results.filter(result_status='fail').count()

        # Technical Test Data
        tt_attended = Tests.objects.filter(test_type='TT', is_submitted=True).count()
        tt_results = Result.objects.filter(test__test_type='TT')
        tt_qualified = tt_results.filter(result_status='pass').count()
        tt_not_qualified = tt_results.filter(result_status='fail').count()

        # Get all programming languages from config
        specialisations = Configuration.objects.filter(
        key=f'programming_languages_{current_year}', deleted=False
        ).values_list('value', flat=True).distinct()
        # Filter skills chart based on selected specialisation
        skills_qs = Result.objects.filter(result_status='pass')
        if selected_specialisation:
            skills_qs = skills_qs.filter(skill=selected_specialisation)

        skills_data = skills_qs.values('skill').annotate(count=Count('result_id')).order_by('-count')[:5]

        skills_list = list(skills_data) or [{'skill': 'No Data', 'count': 0}]

        context = {
            **self.each_context(request),
            'total_users': Users.objects.filter(deleted=False).count(),
            'total_questions': Question.objects.filter(deleted=False).count(),
            'total_tests': Tests.objects.filter(is_submitted=1).count(),
            'total_results': Result.objects.count(),
            'pass_percentage': pass_percentage,
            'gt_data': {
                'labels': json.dumps(['Attended', 'Qualified', 'Not Qualified']),
                'data': json.dumps([
                    Tests.objects.filter(test_type='GT', is_submitted=True).count(),
                    Result.objects.filter(test__test_type='GT', result_status='pass').count(),
                    Result.objects.filter(test__test_type='GT', result_status='fail').count()
                ])
            },
            'tt_data': {
                'labels': json.dumps(['Attended', 'Qualified', 'Not Qualified']),
                'data': json.dumps([
                    Tests.objects.filter(test_type='TT', is_submitted=True).count(),
                    Result.objects.filter(test__test_type='TT', result_status='pass').count(),
                    Result.objects.filter(test__test_type='TT', result_status='fail').count()
                ])
            },
            'skills_chart': {
                'labels': json.dumps([item['skill'] or 'Unspecified' for item in skills_list]),
                'data': json.dumps([item['count'] for item in skills_list])
            },
            'specialisations': specialisations,
            'selected_specialisation': selected_specialisation,
        }


        if extra_context:
            context.update(extra_context)
        return render(request, 'admin/index.html', context)

custom_admin = CustomAdminSite(name='custom_admin')