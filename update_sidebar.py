import re

def update_sidebar():
    path = r"c:\Examportal Application\Examportal-applications\home\templates\includes\sidebar.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # The modules list
    modules = [
        ('Dashboard', r'<li class="nav-item">\s*{% if request.user.is_superuser %}.*?<span class="nav-link-text ms-1">{% trans \'Dashboard\' %}</span>\s*</a>\s*</li>'),
        ('Manage Role', r'<li class="nav-item">\s*<a[^>]*href="{% url \'manage_employees\' %}"[^>]*>.*?</li>'),
        ('Manage Candidate', r'<li class="nav-item">\s*<a[^>]*href="{% url \'user_list\' %}"[^>]*>.*?</li>'),
        ('Candidate Invites', r'<li class="nav-item">\s*<a[^>]*href="{% url \'user_invite_list\' %}"[^>]*>.*?</li>'),
        ('Manage Emails Templates', r'<li class="nav-item">\s*<a[^>]*href="{% url \'email_template_list\' %}"[^>]*>.*?</li>'),
        ('Manage Questions', r'<li class="nav-item">\s*<a[^>]*href="{% url \'question_list\' %}"[^>]*>.*?</li>'),
        ('Manage Tests', r'<li class="nav-item">\s*<a[^>]*href="{% url \'test_list\' %}"[^>]*>.*?</li>'),
        ('General-Test Generation', r'<li class="nav-item">\s*<a[^>]*href="{% url \'generate_test\' %}\?test_type=gt"[^>]*>.*?</li>'),
        ('Technical-Test Generation', r'<li class="nav-item">\s*<a[^>]*href="{% url \'generate_test\' %}\?test_type=tt"[^>]*>.*?</li>'),
        ('Manage Instructions', r'<li class="nav-item">\s*<a[^>]*href="{% url \'instruction_list\' %}"[^>]*>.*?</li>'),
        ('Test Results', r'<li class="nav-item">\s*<a[^>]*href="{% url \'result_list\' %}"[^>]*>.*?</li>'),
        ('Manage QR', r'<li class="nav-item">\s*<a[^>]*href="/qr/list/"[^>]*>.*?</li>'),
        ('Manage Configurations', r'<li class="nav-item">\s*<a[^>]*href="{% url \'configuration_list\' %}"[^>]*>.*?</li>'),
        ('Final Results', r'<li class="nav-item">\s*<a[^>]*href="{% url \'final_result_list\' %}"[^>]*>.*?</li>'),
        ('Change Password', r'<li class="nav-item">\s*<a[^>]*href="/admin/password_change/"[^>]*>.*?</li>'),
    ]
    
    new_block = "\n"
    for mod_name, pattern in modules:
        m = re.search(pattern, content, re.DOTALL)
        if m:
            item_html = m.group(0)
            if mod_name == 'Dashboard':
                item_html = item_html.replace('{% if request.user.is_superuser %}', '')
                item_html = item_html.replace('{% else %}', '')
                item_html = item_html.replace('{% endif %}', '')
                # Fix up Dashboard logic a bit - wait, let's keep the original inside of dashboard
                # The original had different hrefs based on superuser. Let's just keep the superuser version:
                item_html = """            <li class="nav-item">
                <a href="{% url 'admin:index' %} " class="nav-link text-white {% if 'admin' in segment %} active {% endif %} {% if request.path == '/admin/' %} active {% endif %}">
                    <div class="text-white text-center me-2 d-flex align-items-center justify-content-center">
                        <svg width="12px" height="12px" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                            <title>shop</title>
                            <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                                <g transform="translate(-1716.000000, -439.000000)" fill="#FFFFFF" fill-rule="nonzero">
                                    <g transform="translate(1716.000000, 291.000000)">
                                        <g transform="translate(0.000000, 148.000000)">
                                            <path class="color-background opacity-6" d="M46.7199583,10.7414583 L40.8449583,0.949791667 C40.4909749,0.360605034 39.8540131,0 39.1666667,0 L7.83333333,0 C7.1459869,0 6.50902508,0.360605034 6.15504167,0.949791667 L0.280041667,10.7414583 C0.0969176761,11.0460037 -1.23209662e-05,11.3946378 -1.23209662e-05,11.75 C-0.00758042603,16.0663731 3.48367543,19.5725301 7.80004167,19.5833333 L7.81570833,19.5833333 C9.75003686,19.5882688 11.6168794,18.8726691 13.0522917,17.5760417 C16.0171492,20.2556967 20.5292675,20.2556967 23.494125,17.5760417 C26.4604562,20.2616016 30.9794188,20.2616016 33.94575,17.5760417 C36.2421905,19.6477597 39.5441143,20.1708521 42.3684437,18.9103691 C45.1927731,17.649886 47.0084685,14.8428276 47.0000295,11.75 C47.0000295,11.3946378 46.9030823,11.0460037 46.7199583,10.7414583 Z"></path>
                                            <path class="color-background" d="M39.198,22.4912623 C37.3776246,22.4928106 35.5817531,22.0149171 33.951625,21.0951667 L33.92225,21.1107282 C31.1430221,22.6838032 27.9255001,22.9318916 24.9844167,21.7998837 C24.4750389,21.605469 23.9777983,21.3722567 23.4960833,21.1018359 L23.4745417,21.1129513 C20.6961809,22.6871153 17.4786145,22.9344611 14.5386667,21.7998837 C14.029926,21.6054643 13.533337,21.3722507 13.0522917,21.1018359 C11.4250962,22.0190609 9.63246555,22.4947009 7.81570833,22.4912623 C7.16510551,22.4842162 6.51607673,22.4173045 5.875,22.2911849 L5.875,44.7220845 C5.875,45.9498589 6.7517757,46.9451667 7.83333333,46.9451667 L19.5833333,46.9451667 L19.5833333,33.6066734 L27.4166667,33.6066734 L27.4166667,46.9451667 L39.1666667,46.9451667 C40.2482243,46.9451667 41.125,45.9498589 41.125,44.7220845 L41.125,22.2822926 C40.4887822,22.4116582 39.8442868,22.4815492 39.198,22.4912623 Z"></path>
                                        </g>
                                    </g>
                                </g>
                            </g>
                        </svg>
                    </div>
                    <span class="nav-link-text ms-1">{% trans 'Dashboard' %}</span>
                </a>
            </li>"""
            new_block += f"    {{% if request.user|has_module_access:'{mod_name}' %}}\n"
            new_block += f"    {item_html}\n"
            new_block += f"    {{% endif %}}\n"
        else:
            print(f"Module not found: {mod_name}")
            
    # Now replace the whole list from <ul class="navbar-nav"> to </ul>
    full_ul = re.search(r'<ul class="navbar-nav">.*?</ul>', content, re.DOTALL)
    
    if full_ul:
        new_content = content[:full_ul.start()] + '<ul class="navbar-nav">' + new_block + "        </ul>" + content[full_ul.end():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated successfully.")
    else:
        print("Full UL block not found")

if __name__ == "__main__":
    update_sidebar()
