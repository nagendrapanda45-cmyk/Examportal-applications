with open('core/middleware/restrict_public.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """ALLOWED_PATHS = [
    '/candidates/register', '/candidates/register/',
    '/candidates/registration-success', '/candidates/registration-success/',
    '/candidates/submit-registration-feedback', '/candidates/submit-registration-feedback/',
    '/submit-registration-feedback', '/submit-registration-feedback/',
    '/candidates/check-registration', '/candidates/check-registration/',
    '/candidates/login', '/candidates/login/',
    '/metrics'
]"""

replacement = """ALLOWED_PATHS = [
    '/', '',
    '/dashboard', '/dashboard/',
    '/login', '/login/',
    '/mindmap', '/mindmap/',
    '/candidates/register', '/candidates/register/',
    '/candidates/registration-success', '/candidates/registration-success/',
    '/candidates/submit-registration-feedback', '/candidates/submit-registration-feedback/',
    '/submit-registration-feedback', '/submit-registration-feedback/',
    '/candidates/check-registration', '/candidates/check-registration/',
    '/candidates/login', '/candidates/login/',
    '/candidates/dashboard', '/candidates/dashboard/',
    '/results', '/results/',
    '/qr/list', '/qr/list/',
    '/metrics'
]"""

text = text.replace(target, replacement, 1)

target2 = "or any(path.startswith(p) for p in ['/static/', '/media/', '/candidates/', '/exam_dashboard/', '/submit-registration-feedback'])"
replacement2 = "or any(path.startswith(p) for p in ['/static/', '/media/', '/candidates/', '/exam_dashboard/', '/submit-registration-feedback', '/mindmap/', '/dashboard/', '/admin/', '/results/', '/qr/', '/tests/', '/role_based_access/', '/invite/', '/email_scheduler/', '/configurations/'])"

text = text.replace(target2, replacement2, 1)

with open('core/middleware/restrict_public.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS")
