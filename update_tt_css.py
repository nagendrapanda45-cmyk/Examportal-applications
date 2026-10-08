import os
path = 'Exam_dashboard/templates/technical_test_page.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old_css = """    .alert-error {
        background-color: #ffebee;
        color: #c62828;
        border: 1px solid #ef9a9a;
    }"""
new_css = """    .alert-error {
        background-color: #e91e63;
        color: #ffffff;
        border: 1px solid #c2185b;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4);
    }"""
c = c.replace(old_css, new_css)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("technical_test_page.html updated")
