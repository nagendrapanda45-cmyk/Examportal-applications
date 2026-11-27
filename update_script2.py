import os

fpath = r'c:\Examportal Application\Examportal-applications\Role_based_Access\templates\Role_based_Access\manage_employees.html'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

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

if 'pagination' not in content.lower():
    content = content.replace('</table>', '</table>\n' + pagination_html)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
print('Updated manage_employees.html')
