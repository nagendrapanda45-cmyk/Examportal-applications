import sys

with open('home/users/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find the language_selection function
pattern = r"def language_selection\(request\):.*?return redirect\('instructions_view', test_type='TT'\)"
replacement = """def language_selection(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    if request.method == 'POST':
        lang_id = request.POST.get('programming_language')
        if lang_id:
            request.session['selected_language'] = lang_id
            return redirect('instructions_view', test_type='TT')
        else:
            messages.error(request, 'Please select a language.')

    programming_languages = [
        {'language_id': 'Python', 'display_name': 'Python', 'description': 'Solve Data Structures and Algorithms in Python', 'icon_class': 'fab fa-python'},
        {'language_id': 'Java', 'display_name': 'Java', 'description': 'Solve Data Structures and Algorithms in Java', 'icon_class': 'fab fa-java'},
        {'language_id': 'C++', 'display_name': 'C++', 'description': 'Solve Data Structures and Algorithms in C++', 'icon_class': 'fab fa-cuttlefish'}
    ]
    return render(request, 'users/language_selection.html', {'programming_languages': programming_languages})"""

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('home/users/views.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Restored language_selection view!")
