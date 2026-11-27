import os, re

base_dir = r'c:\Examportal Application\Examportal-applications'

# 1. Update Role_based_Access/views.py
rba_views = os.path.join(base_dir, 'Role_based_Access', 'views.py')
with open(rba_views, 'r', encoding='utf-8') as f:
    rba_content = f.read()

# Add Paginator import if missing
if 'from django.core.paginator import Paginator' not in rba_content:
    rba_content = rba_content.replace('from django.shortcuts', 'from django.core.paginator import Paginator\nfrom django.shortcuts')

# Replace manage_employees
manage_employees_new = '''@login_required
@module_access_required('Manage Role')
def manage_employees(request):
    search_query = request.GET.get('search_query', '')
    employees = Employee.objects.select_related('user').all()
    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    paginator = Paginator(employees, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Role_based_Access/manage_employees.html', {
        'employees': page_obj,
        'page_obj': page_obj,
        'search_query': search_query
    })
'''
rba_content = re.sub(r'@login_required\s*@module_access_required\(\'Manage Role\'\)\s*def manage_employees.*?return render.*?\}\)', manage_employees_new, rba_content, flags=re.DOTALL)

with open(rba_views, 'w', encoding='utf-8') as f:
    f.write(rba_content)

print('Updated Role_based_Access/views.py')

# 2. Update Role_based_Access/templates/Role_based_Access/manage_employees.html
rba_html = os.path.join(base_dir, 'Role_based_Access', 'templates', 'Role_based_Access', 'manage_employees.html')
with open(rba_html, 'r', encoding='utf-8') as f:
    rba_html_content = f.read()

pagination_html = '''
{% if page_obj.has_other_pages %}
<nav aria-label="Page navigation">
  <ul class="pagination justify-content-center mt-4">
    {% if page_obj.has_previous %}
      <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if search_query %}&search_query={{ search_query }}{% endif %}">Previous</a></li>
    {% endif %}
    <li class="page-item disabled"><span class="page-link">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span></li>
    {% if page_obj.has_next %}
      <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}{% if search_query %}&search_query={{ search_query }}{% endif %}">Next</a></li>
    {% endif %}
  </ul>
</nav>
{% endif %}
'''

if 'pagination' not in rba_html_content.lower():
    rba_html_content = re.sub(r'(</div>\s*{%\s*endblock\s*%})', r'  ' + pagination_html.replace('\n', '\n  ') + r'\n\1', rba_html_content)
    with open(rba_html, 'w', encoding='utf-8') as f:
        f.write(rba_html_content)

# 3. Update templates/home/candidate_list.html
user_html = os.path.join(base_dir, 'templates', 'home', 'candidate_list.html')
if os.path.exists(user_html):
    with open(user_html, 'r', encoding='utf-8') as f:
        u_content = f.read()
    u_content = u_content.replace('{% for user in users %}', '{% for user in page_obj %}')
    if 'pagination' not in u_content.lower():
        u_content = re.sub(r'(</div>\s*{%\s*endblock\s*%})', r'  ' + pagination_html.replace('\n', '\n  ') + r'\n\1', u_content)
        with open(user_html, 'w', encoding='utf-8') as f:
            f.write(u_content)

print('Updated templates')
