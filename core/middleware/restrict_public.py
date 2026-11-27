# # middleware/restrict_public.py
from django.http import HttpResponseForbidden

ALLOWED_PATHS = [
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
]

INTERNAL_IP_RANGES = [
    '127.0.0.1', '::1', 'localhost',
    '192.168.', '172.', '10.',
    '13.232.128', '0.0.0.0', '49.249.160.198', '183.82.6.191', '13.232.128.222'
]

class RestrictPublicAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if (
            path in ALLOWED_PATHS
            or any(path.startswith(p) for p in ['/static/', '/media/', '/candidates/', '/exam_dashboard/', '/submit-registration-feedback', '/mindmap/', '/dashboard/', '/admin/', '/results/', '/qr/', '/tests/', '/role_based_access/', '/invite/', '/email_scheduler/', '/configurations/'])
        ):
            return self.get_response(request)

        ip = request.META.get('REMOTE_ADDR', '')
        if not any(ip.startswith(r) for r in INTERNAL_IP_RANGES):
            return HttpResponseForbidden("Access Denied")
        return self.get_response(request)

# ------------------------------------------------------------------------

# from django.http import HttpResponseForbidden
# import ipaddress

# ALLOWED_PATHS = ['/users/register','/users/registration-success','/static/custom/css/cdn-jsdelivr-bootstrap.min.css','/static/custom/css/cdnjs-cloudflare-font-awesome.min.css','/static/custom/css/user-register.css']
# INTERNAL_NETWORKS = [
#     ipaddress.ip_network('192.168.1.0/24'),
#     ipaddress.ip_network('172.168.1.0/24'),
# ]

# class RestrictPublicAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         ip_str = request.META.get('REMOTE_ADDR', '')
#         try:
#             ip = ipaddress.ip_address(ip_str)
#         except ValueError:
#             # If invalid IP, block access
#             return HttpResponseForbidden("Access Denied")

#         if request.path not in ALLOWED_PATHS and not any(ip in net for net in INTERNAL_NETWORKS):
#             return HttpResponseForbidden("Access Denied")

#         return self.get_response(request)

# ------------------------------------------------------------------------

# middleware/restrict_public.py
# from django.http import HttpResponseForbidden

# # Public URLs allowed from outside (no internal IP required)
# ALLOWED_PATHS = [
#     '/users/register',
#     '/users/registration-success',
#     '/static/custom/css/cdn-jsdelivr-bootstrap.min.css',
#     '/static/custom/css/cdnjs-cloudflare-font-awesome.min.css',
#     '/static/custom/css/user-register.css',
#     # Add any other publicly allowed URLs here
# ]

# # Internal IP prefixes allowed full access (adjust to your network)
# INTERNAL_IP_RANGES = [
#     '192.168.1.0/24',   # e.g., 192.168.1.0/24
#     '172.168.1.0/24',   # e.g., 172.168.1.0/24
#     # Add more if needed
# ]

# class RestrictPublicAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Get client IP considering proxy headers
#         ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
#         if ',' in ip:
#             # X-Forwarded-For can be a list of IPs, take first
#             ip = ip.split(',')[0].strip()

#         # DEBUG: log IP and requested path - remove or disable in production
#         print(f"[RestrictPublicAccessMiddleware] Client IP: {ip} Path: {request.path}")

#         # Allow if path is public
#         if request.path in ALLOWED_PATHS:
#             return self.get_response(request)

#         # Allow if IP is in internal ranges
#         if any(ip.startswith(prefix) for prefix in INTERNAL_IP_RANGES):
#             return self.get_response(request)

#         # Deny access otherwise
#         return HttpResponseForbidden("Access Denied")
