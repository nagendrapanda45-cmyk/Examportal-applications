with open('TalentAssess_360_MindMap_Visual.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the quick URL banner with prominent Public URL banner
old_banner = """  <!-- Pinned Quick URL Banner -->
  <div class="no-print bg-gradient-to-r from-emerald-950/60 via-slate-900 to-pink-950/60 border-b border-emerald-800/40 px-6 py-2.5 flex flex-wrap items-center justify-between text-xs gap-3">
    <div class="flex items-center gap-2">
      <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
      <span class="text-slate-300 font-semibold">Live Server Running on Port 8080:</span>
      <span class="text-emerald-400 font-mono font-bold bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800/60">http://127.0.0.1:8080/</span>
    </div>
    <div class="flex items-center gap-2">
      <a href="http://127.0.0.1:8080/dashboard/" target="_blank" class="px-2.5 py-1 bg-pink-600/30 hover:bg-pink-600 text-pink-300 hover:text-white rounded border border-pink-500/40 font-semibold transition flex items-center gap-1">
        📊 Admin Dashboard ➜
      </a>
      <a href="http://127.0.0.1:8080/candidates/register/" target="_blank" class="px-2.5 py-1 bg-emerald-600/30 hover:bg-emerald-600 text-emerald-300 hover:text-white rounded border border-emerald-500/40 font-semibold transition flex items-center gap-1">
        📝 Candidate Register ➜
      </a>
    </div>
  </div>"""

new_banner = """  <!-- Pinned Quick Public & Local URL Banner -->
  <div class="no-print bg-gradient-to-r from-emerald-950/80 via-slate-900 to-pink-950/80 border-b border-emerald-500/50 px-6 py-3 flex flex-wrap items-center justify-between text-xs gap-3 shadow-lg">
    <div class="flex flex-wrap items-center gap-3">
      <div class="flex items-center gap-1.5 bg-emerald-900/40 border border-emerald-500/50 px-3 py-1 rounded-lg">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-slate-300 font-semibold">Public Internet URL:</span>
        <a href="https://popper-unrobed-cameo.ngrok-free.dev/mindmap/" target="_blank" class="text-emerald-300 font-mono font-bold hover:underline select-all">
          https://popper-unrobed-cameo.ngrok-free.dev/mindmap/
        </a>
      </div>
      <div class="flex items-center gap-1.5 bg-slate-900 border border-slate-700 px-3 py-1 rounded-lg">
        <span class="text-slate-400">Local:</span>
        <span class="text-slate-300 font-mono">http://127.0.0.1:8080/</span>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <a href="https://popper-unrobed-cameo.ngrok-free.dev/dashboard/" target="_blank" class="px-3 py-1 bg-pink-600 hover:bg-pink-500 text-white rounded-lg font-bold transition flex items-center gap-1 shadow">
        📊 Public Admin Dashboard ➜
      </a>
      <a href="https://popper-unrobed-cameo.ngrok-free.dev/candidates/register/" target="_blank" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-bold transition flex items-center gap-1 shadow">
        📝 Public Candidate Register ➜
      </a>
    </div>
  </div>"""

text = text.replace(old_banner, new_banner, 1)

destinations = [
    r"C:\Users\User\Downloads\TalentAssess_360_MindMap_Visual.html",
    r"c:\Examportal Application\Examportal-applications\TalentAssess_360_MindMap_Visual.html",
    r"C:\Users\User\.gemini\antigravity\brain\fe8240e4-d948-4a3f-bd80-cd638df2f4e2\TalentAssess_360_MindMap_Visual.html"
]

for d in destinations:
    with open(d, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated public URL banner in {d}")
