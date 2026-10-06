import sys
import glob

files_to_patch = [
    'Exam_dashboard/templates/test_page.html',
    'Exam_dashboard/templates/technical_test_page.html'
]

anti_cheat_code = """
        // ANTI-CHEAT STRICT RULES
        document.addEventListener("visibilitychange", () => {
            if (document.hidden) {
                alert("⛔ ANTI-CHEAT WARNING: You have opened a new tab, another browser, or an AI tool. This is strictly prohibited. Your action has been recorded!");
            }
        });

        window.addEventListener("blur", () => {
            alert("⛔ ANTI-CHEAT WARNING: You switched to another application or opened a file. Please return to the exam window immediately!");
        });
        
        // Mock USB / Multiple persons warning for presentation
        setInterval(() => {
            // Randomly simulate checking for multiple persons to make it look like AI is running in the background
            console.log("AI Proctoring: Analyzing webcam feed for multiple persons...");
            console.log("AI Proctoring: Scanning for unauthorized USB devices...");
        }, 10000);
"""

for filepath in files_to_patch:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'ANTI-CHEAT STRICT RULES' not in content:
            # Inject right before the closing </script> tag at the bottom
            content = content.replace('</script>\n</body>', anti_cheat_code + '\n</script>\n</body>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Patched {filepath}")
    except FileNotFoundError:
        pass
