import os
path = 'Exam_dashboard/templates/test_page.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    'alert(" ANTI-CHEAT WARNING: You have opened a new tab, another browser, or an AI tool. This is strictly prohibited. Your action has been recorded!");',
    "Swal.fire({icon: 'warning', title: 'ANTI-CHEAT WARNING', text: 'You have opened a new tab, another browser, or an AI tool. This is strictly prohibited. Your action has been recorded!', confirmButtonColor: '#e91e63'});"
)
c = c.replace(
    'alert(" ANTI-CHEAT WARNING: You switched to another application or opened a file. Please return to the exam window immediately!");',
    "Swal.fire({icon: 'warning', title: 'ANTI-CHEAT WARNING', text: 'You switched to another application or opened a file. Please return to the exam window immediately!', confirmButtonColor: '#e91e63'});"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("test_page.html updated")
