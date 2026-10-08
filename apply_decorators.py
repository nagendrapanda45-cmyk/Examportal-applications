import os
import re

# We will apply the decorator to the functions by finding `def <view_name>(` and inserting the decorator right before it.
# We also need to add the import statement at the top of the file.

replacements = {
    r"home\views.py": [
        ('index', "Dashboard"),
        ('test_list', "Manage Tests"),
        ('instruction_list', "Manage Instructions"),
        ('result_list', "Test Results"),
        ('generate_test', "General-Test Generation', 'Technical-Test Generation"),
        ('final_result_list', "Final Results"),
    ],
    r"Role_based_Access\views.py": [
        ('manage_employees', "Manage Role"),
        ('add_employee', "Manage Role"),
        ('edit_employee', "Manage Role"),
        ('delete_employee', "Manage Role"),
    ],
    r"home\users\views.py": [
        ('user_list_view', "Manage Candidate"),
    ],
    r"user_invite\views.py": [
        ('user_invite_list_view', "Candidate Invites"),
        ('email_template_list', "Manage Emails Templates"),
    ],
    r"questions\views.py": [
        ('question_list', "Manage Questions"),
    ],
    r"qr_generator\views.py": [
        ('qr_list', "Manage QR"),
        ('qr_detail', "Manage QR"),
        ('regenerate_qr', "Manage QR"),
        ('qr_create', "Manage QR"),
        ('qr_delete', "Manage QR"),
    ]
}

base_dir = r"c:\Examportal Application\Examportal-applications"

for file_path, views in replacements.items():
    full_path = os.path.join(base_dir, file_path)
    if not os.path.exists(full_path):
        continue
        
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "from Role_based_Access.decorators import module_access_required" not in content:
        # insert after the first import or at top
        content = "from Role_based_Access.decorators import module_access_required\n" + content

    for view, module in views:
        # We look for def view_name(
        # We need to insert @module_access_required('...') right before it, 
        # but after @login_required if it exists
        
        pattern = re.compile(rf'(@login_required\n\s*)?def {view}\(')
        
        def replacer(match):
            prefix = match.group(1) or ""
            return f"{prefix}@module_access_required('{module}')\ndef {view}("
            
        content = pattern.sub(replacer, content)

    # For ConfigurationListView in home/views.py
    if file_path == r"home\views.py":
        if "from django.utils.decorators import method_decorator" not in content:
            content = "from django.utils.decorators import method_decorator\n" + content
            
        cbv_pattern = re.compile(r'class ConfigurationListView\(')
        def cbv_replacer(match):
            # Check if it already has @method_decorator
            return f"@method_decorator(module_access_required('Manage Configurations'), name='dispatch')\nclass ConfigurationListView("
        if "@method_decorator(module_access_required('Manage Configurations')" not in content:
            content = cbv_pattern.sub(cbv_replacer, content)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Decorators applied!")
