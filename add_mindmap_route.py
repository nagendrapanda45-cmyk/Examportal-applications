with open('home/views.py', 'r', encoding='utf-8') as f:
    v_text = f.read()

target_v = """def index(request):
    return dashboard_view(request)"""

replacement_v = """def index(request):
    return dashboard_view(request)

def mindmap_view(request):
    html_path = os.path.join(settings.BASE_DIR, 'TalentAssess_360_MindMap_Visual.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    downloads_path = r'C:\\Users\\User\\Downloads\\TalentAssess_360_MindMap_Visual.html'
    if os.path.exists(downloads_path):
        with open(downloads_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    return HttpResponse("Mind Map Visual not found.", status=404)"""

if target_v in v_text:
    v_text = v_text.replace(target_v, replacement_v, 1)
    with open('home/views.py', 'w', encoding='utf-8') as f:
        f.write(v_text)
    print("home/views.py updated with mindmap_view")
else:
    print("target_v not found in home/views.py")

with open('home/urls.py', 'r', encoding='utf-8') as f:
    u_text = f.read()

target_u = """    path('login/', views.login_router, name='login'),"""
replacement_u = """    path('login/', views.login_router, name='login'),
    path('mindmap/', views.mindmap_view, name='mindmap_view'),"""

if target_u in u_text:
    u_text = u_text.replace(target_u, replacement_u, 1)
    with open('home/urls.py', 'w', encoding='utf-8') as f:
        f.write(u_text)
    print("home/urls.py updated with mindmap/ path")
else:
    print("target_u not found in home/urls.py")
