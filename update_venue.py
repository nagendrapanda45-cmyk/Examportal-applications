import sys

with open('home/users/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
lines[623:630] = [
    '    <p><strong>Venue:</strong><br>',
    '    Intelligenz IT Info Solutions Pvt Ltd<br>',
    '    2nd Floor, Solitaire Building, Image Incubation,<br>',
    '    HITEC City Road, Serilingampally, Madhapur,<br>',
    '    Hyderabad, Telangana — 500081, India<br>',
    '    <a href="https://www.google.com/maps/search/?api=1&query=Intelligenz+IT+Hyderabad+500081&utm_source=chatgpt.com">Google Map</a></p>'
]

with open('home/users/views.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
