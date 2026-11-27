import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    # Safe replacements for classes and forms
    content = re.sub(r'\bUsers\b', 'Candidate', content)
    content = re.sub(r'\bUsersForm\b', 'CandidateForm', content)
    content = re.sub(r'\bUserRegistrationForm\b', 'CandidateRegistrationForm', content)
    
    # Imports
    content = re.sub(r'from (\S+) import (\S*,\s*)?Candidate(\s*,\s*\S+)*', lambda m: m.group(0).replace('Candidate', 'Candidate'), content)

    # Views and URLs
    content = re.sub(r'\buser_list_view\b', 'candidate_list_view', content)
    content = re.sub(r'\buser_register\b', 'candidate_register', content)
    content = re.sub(r'\buser_login\b', 'candidate_login', content)
    content = re.sub(r'\buser_logout\b', 'candidate_logout', content)
    
    # Variables: this is tricky. We only want to replace specific known patterns
    # to avoid hitting request.user or Employee.user.
    
    # Template names
    content = re.sub(r'user_list\.html', 'candidate_list.html', content)
    content = re.sub(r'user_form\.html', 'candidate_form.html', content)
    # Add any other template renames as needed
    
    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

# We will apply this to the specified views, forms, models, and urls
files_to_process = [
    'home/users/models.py',
    'home/users/forms.py',
    'home/users/views.py',
    'home/users/urls.py',
    'Exam_dashboard/views.py',
    'results/views.py',
    'user_invite/views.py',
    'home/views.py',
    'core/urls.py',
]

for f in files_to_process:
    if os.path.exists(f):
        process_file(f)
    else:
        print(f"File not found: {f}")
