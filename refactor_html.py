import os
import re

print("Starting html refactoring...")
for root, dirs, files in os.walk('templates'):
    for name in files:
        if name.endswith('.html'):
            filepath = os.path.join(root, name)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original = content
                
                content = content.replace("'user_register'", "'candidate_register'")
                content = content.replace('"user_register"', '"candidate_register"')
                content = content.replace("'user_login'", "'candidate_login'")
                content = content.replace('"user_login"', '"candidate_login"')
                content = content.replace("'user_logout'", "'candidate_logout'")
                content = content.replace('"user_logout"', '"candidate_logout"')
                content = content.replace("'user_list_view'", "'candidate_list_view'")
                content = content.replace('"user_list_view"', '"candidate_list_view"')
                content = content.replace("'user_list'", "'candidate_list'")
                content = content.replace('"user_list"', '"candidate_list"')
                
                if original != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Updated {filepath}')
            except Exception as e:
                print(f"Failed on {filepath}: {e}")
print("Done.")
