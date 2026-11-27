import os

with open('TalentAssess_360_MindMap_Visual.html', 'r', encoding='utf-8') as f:
    html = f.read()

dynamic_script = """
    // Dynamic Host Adaptation for Public URL & Localhost
    window.addEventListener('DOMContentLoaded', () => {
      const isHttp = window.location.protocol.startsWith('http');
      const activeOrigin = isHttp ? window.location.origin : 'http://127.0.0.1:8080';

      // Update all links pointing to 127.0.0.1:8080
      document.querySelectorAll('a').forEach(a => {
        if (a.href && a.href.includes('127.0.0.1:8080')) {
          a.href = a.href.replace('http://127.0.0.1:8080', activeOrigin);
        }
      });

      // Update code blocks showing 127.0.0.1:8080
      document.querySelectorAll('code').forEach(c => {
        if (c.textContent.includes('127.0.0.1:8080')) {
          c.textContent = c.textContent.replaceAll('http://127.0.0.1:8080', activeOrigin);
        }
      });

      // Update banner text
      const bannerSpan = document.querySelector('span.text-emerald-400.font-mono.font-bold');
      if (bannerSpan) {
        bannerSpan.textContent = activeOrigin + '/';
      }
      const hostSpan = document.querySelector('strong.text-pink-400.font-mono');
      if (hostSpan && isHttp) {
        hostSpan.textContent = window.location.host;
      }
    });
"""

target = "</script>"
idx = html.rfind(target)
if idx != -1:
    html = html[:idx] + dynamic_script + html[idx:]
    destinations = [
        r"C:\Users\User\Downloads\TalentAssess_360_MindMap_Visual.html",
        r"c:\Examportal Application\Examportal-applications\TalentAssess_360_MindMap_Visual.html",
        r"C:\Users\User\.gemini\antigravity\brain\fe8240e4-d948-4a3f-bd80-cd638df2f4e2\TalentAssess_360_MindMap_Visual.html"
    ]
    for d in destinations:
        with open(d, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated dynamic origin in: {d}")
else:
    print("Could not find </script>")
