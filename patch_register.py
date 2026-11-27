import re

with open('home/users/templates/users/register.html', 'r') as f:
    content = f.read()

# Replace mobile section
mobile_search = '''                                <label class=\"form-label\">Mobile <span class=\"required\">*</span></label>
                                {{ form.mobile }}'''
mobile_replace = '''                                <label class=\"form-label\">Mobile <span class=\"required\">*</span></label>
                                <div class=\"input-group\">
                                    {{ form.mobile_country_code }}
                                    {{ form.mobile }}
                                </div>'''

content = content.replace(mobile_search, mobile_replace)

alt_mobile_search = '''                                <label class=\"form-label\">Alternative Mobile</label>
                                {{ form.alternative_mobile }}'''
alt_mobile_replace = '''                                <label class=\"form-label\">Alternative Mobile</label>
                                <div class=\"input-group\">
                                    {{ form.alt_mobile_country_code }}
                                    {{ form.alternative_mobile }}
                                </div>'''

content = content.replace(alt_mobile_search, alt_mobile_replace)

with open('home/users/templates/users/register.html', 'w') as f:
    f.write(content)
