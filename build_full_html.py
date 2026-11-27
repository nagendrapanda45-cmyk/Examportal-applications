import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Intelligenz IT TalentAssess 360™ - Mind Map, Architecture, URLs & Interactive Wireframe</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    body {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }
    .hover-card {
      transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s ease;
    }
    .hover-card:hover {
      transform: translateY(-4px);
    }
    .wireframe-screen {
      transition: opacity 0.3s ease, transform 0.3s ease;
    }
    .copy-tooltip {
      transition: opacity 0.2s ease;
    }
    @media print {
      .no-print { display: none !important; }
      body { background: white !important; color: black !important; }
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-pink-500 selection:text-white">

  <!-- Executive Top Bar -->
  <header class="no-print bg-slate-900/95 backdrop-blur border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-50 shadow-md">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-600 via-rose-500 to-indigo-600 flex items-center justify-center font-extrabold text-white text-lg shadow-lg shadow-pink-500/20">
        IT
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-lg font-bold tracking-tight text-white">Intelligenz IT | TalentAssess 360™</h1>
          <span class="px-2 py-0.5 text-xs font-semibold bg-pink-500/10 text-pink-400 border border-pink-500/20 rounded-full">Executive Suite</span>
        </div>
        <p class="text-xs text-slate-400">AI-Powered Assessment & Digital Recruitment Platform • Transforming Possibilities</p>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <nav class="flex items-center gap-1 bg-slate-950/80 p-1.5 rounded-xl border border-slate-800 text-xs">
      <button onclick="switchTab('urls')" id="btn-tab-urls" class="px-3.5 py-2 rounded-lg font-bold transition bg-emerald-600 text-white shadow flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
        🔗 Live System URLs
      </button>
      <button onclick="switchTab('mindmap')" id="btn-tab-mindmap" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-300 hover:text-white hover:bg-slate-800">
        🌟 8-Pillar Mind Map
      </button>
      <button onclick="switchTab('architecture')" id="btn-tab-architecture" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-300 hover:text-white hover:bg-slate-800">
        🏗️ System Architecture
      </button>
      <button onclick="switchTab('benefits')" id="btn-tab-benefits" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-300 hover:text-white hover:bg-slate-800">
        💡 Benefits & Features
      </button>
      <button onclick="switchTab('wireframe')" id="btn-tab-wireframe" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-1.5">
        📱 MarvelApp Wireframes
      </button>
      <button onclick="switchTab('dordod')" id="btn-tab-dordod" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-300 hover:text-white hover:bg-slate-800">
        📋 DoR & DoD
      </button>
    </nav>

    <!-- Executive Asset Links -->
    <div class="flex items-center gap-2">
      <a href="file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_Executive_Dossier.docx" class="flex items-center gap-1.5 px-3 py-1.5 bg-blue-900/40 hover:bg-blue-900/60 text-blue-300 border border-blue-700/50 rounded-lg text-xs font-semibold transition" title="Open Executive Dossier in Microsoft Word">
        <span class="w-4 h-4 rounded bg-blue-600 flex items-center justify-center font-bold text-white text-[9px]">W</span>
        Word Dossier
      </a>
      <a href="file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_CEO.pptx" class="flex items-center gap-1.5 px-3 py-1.5 bg-orange-900/40 hover:bg-orange-900/60 text-orange-300 border border-orange-700/50 rounded-lg text-xs font-semibold transition" title="Open Presentation Deck in Microsoft PowerPoint">
        <span class="w-4 h-4 rounded bg-orange-600 flex items-center justify-center font-bold text-white text-[9px]">P</span>
        CEO Slide Deck
      </a>
      <button onclick="window.print()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700 transition">
        🖨️ Print
      </button>
    </div>
  </header>

  <!-- Pinned Quick URL Banner -->
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
  </div>

  <!-- TAB: LIVE SYSTEM URLS DIRECTORY (PROMINENT VIEW) -->
  <section id="tab-urls" class="flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <span>Live Platform URLs & Endpoints Directory</span>
          <span class="text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-full border border-emerald-500/30">All 100% Operational (HTTP 200 OK)</span>
        </h2>
        <p class="text-xs text-slate-400">Directly click, copy, or launch any portal endpoint. Both Admin side and User/Candidate side routes are live.</p>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <span class="px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-slate-300">
          Target Host: <strong class="text-pink-400 font-mono">127.0.0.1:8080</strong>
        </span>
      </div>
    </div>

    <!-- Two-Column Cards: Admin Side vs Candidate Side -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      
      <!-- Card A: Admin & Internal Management URLs -->
      <div class="bg-slate-900 border border-pink-500/30 rounded-2xl p-6 shadow-xl">
        <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-lg bg-pink-600/20 text-pink-400 flex items-center justify-center font-bold text-sm">🛡️</span>
            <div>
              <h3 class="font-extrabold text-sm text-pink-400 uppercase tracking-wider">Admin & Internal Operations URLs</h3>
              <p class="text-[11px] text-slate-400">Governance, Evaluation, QR Drives & Role Management</p>
            </div>
          </div>
          <span class="px-2 py-0.5 bg-pink-500/10 text-pink-400 text-[10px] font-bold rounded border border-pink-500/20">ADMIN SIDE</span>
        </div>

        <div class="space-y-3 text-xs">
          
          <!-- URL 1: Admin Dashboard -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-pink-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>📊 Admin Dashboard</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/dashboard/" target="_blank" class="px-3 py-1 bg-pink-600 hover:bg-pink-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-pink-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/dashboard/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/dashboard/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 2: Manage Candidates -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-pink-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>👥 Manage Candidates & PDF Dossiers</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/list/" target="_blank" class="px-3 py-1 bg-pink-600 hover:bg-pink-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-pink-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/candidates/list/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/list/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 3: Test Results -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-pink-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>📈 Instant Test Results & Scoring Hub</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/results/" target="_blank" class="px-3 py-1 bg-pink-600 hover:bg-pink-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-pink-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/results/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/results/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 4: Campus Drive QR Codes -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-pink-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>📱 Campus Placement QR Generator</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/qr/list/" target="_blank" class="px-3 py-1 bg-pink-600 hover:bg-pink-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-pink-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/qr/list/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/qr/list/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 5: Manage Roles & RBAC -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-pink-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>🔐 Manage Roles (15-Module RBAC Permissions)</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/role_based_access/manage_roles/" target="_blank" class="px-3 py-1 bg-pink-600 hover:bg-pink-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-pink-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/role_based_access/manage_roles/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/role_based_access/manage_roles/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

        </div>
      </div>

      <!-- Card B: Candidate & User Facing URLs -->
      <div class="bg-slate-900 border border-emerald-500/30 rounded-2xl p-6 shadow-xl">
        <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-lg bg-emerald-600/20 text-emerald-400 flex items-center justify-center font-bold text-sm">👤</span>
            <div>
              <h3 class="font-extrabold text-sm text-emerald-400 uppercase tracking-wider">Candidate & Public Facing URLs</h3>
              <p class="text-[11px] text-slate-400">Discovery, Onboarding, AI Camera Test & Exam Execution</p>
            </div>
          </div>
          <span class="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 text-[10px] font-bold rounded border border-emerald-500/20">CANDIDATE SIDE</span>
        </div>

        <div class="space-y-3 text-xs">
          
          <!-- URL 1: Candidate Registration -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-emerald-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>📝 Candidate Registration Portal (Global Codes & PAN)</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/register/" target="_blank" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-emerald-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/candidates/register/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/register/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 2: Candidate Login -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-emerald-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>🔑 Candidate Login Portal</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/login/" target="_blank" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-emerald-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/candidates/login/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/login/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 3: Instructions & Camera Check -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-emerald-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>📋 Instructions & Webcam AI Proctor Handshake</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/instructions/GT/" target="_blank" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-emerald-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/candidates/instructions/GT/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/instructions/GT/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 4: Candidate Dashboard -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-emerald-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>💻 Candidate Personal Dashboard</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/dashboard/" target="_blank" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-emerald-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/candidates/dashboard/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/dashboard/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 5: Registration Success & 5-Star Feedback -->
          <div class="p-3 bg-slate-950 border border-slate-800 rounded-xl hover:border-emerald-500/50 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-white flex items-center gap-1.5">
                <span>⭐ Registration Success & 5-Star Feedback</span>
                <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-semibold">Live</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/registration-success/" target="_blank" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-slate-900 px-2.5 py-1.5 rounded-lg border border-slate-800">
              <code class="text-emerald-300 font-mono text-[11px] select-all">http://127.0.0.1:8080/candidates/registration-success/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/registration-success/')" class="text-slate-400 hover:text-white text-[11px] font-semibold">Copy</button>
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- Presentation Files Direct Access -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-sm font-extrabold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
        <span>📁 Local Presentation & Report Files (Downloads Folder)</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="p-4 bg-slate-950 border border-blue-600/30 rounded-xl flex items-center justify-between">
          <div>
            <strong class="text-blue-300 text-sm block">Microsoft Word Executive Dossier</strong>
            <code class="text-slate-400 text-[10px] block mt-0.5 select-all">file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_Executive_Dossier.docx</code>
          </div>
          <a href="file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_Executive_Dossier.docx" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg transition">
            Open File
          </a>
        </div>
        <div class="p-4 bg-slate-950 border border-orange-600/30 rounded-xl flex items-center justify-between">
          <div>
            <strong class="text-orange-300 text-sm block">Microsoft PowerPoint CEO Slide Deck</strong>
            <code class="text-slate-400 text-[10px] block mt-0.5 select-all">file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_CEO.pptx</code>
          </div>
          <a href="file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_CEO.pptx" class="px-3 py-1.5 bg-orange-600 hover:bg-orange-500 text-white font-bold rounded-lg transition">
            Open File
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- TAB 2: 8-PILLAR BUSINESS MIND MAP -->
  <section id="tab-mindmap" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <span>Exam Portal – Business Mind Map</span>
          <span class="text-xs font-medium text-pink-400 bg-pink-500/10 px-2 py-0.5 rounded border border-pink-500/20">AI-Powered Platform</span>
        </h2>
        <p class="text-xs text-slate-400">Complete strategic alignment: Why, Who, What, How, Key Features, Where, When, and Business Benefits.</p>
      </div>
      <div class="text-xs text-slate-400 flex items-center gap-2 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
        <span>Vision:</span>
        <strong class="text-pink-400">Transforming Human Capital Acquisition with AI & Automation</strong>
      </div>
    </div>

    <!-- 8 Pillars Grid Layout -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      
      <!-- 1. WHY? (Pink/Rose) -->
      <div class="hover-card bg-slate-900/80 border border-rose-500/40 rounded-2xl p-5 shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-rose-500 to-pink-500"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center font-bold text-sm">🎯</div>
          <h3 class="font-extrabold text-sm text-rose-400 uppercase tracking-wide">1. WHY? Business Need & Value</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-2">
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> Reduce manual recruitment effort</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> Faster and consistent hiring cycles</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> Standardized candidate assessments</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> Lower recruitment cost-per-hire</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> Better quality candidate shortlisting</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> Data-driven leadership decisions</li>
        </ul>
      </div>

      <!-- 2. WHO? (Purple) -->
      <div class="hover-card bg-slate-900/80 border border-purple-500/40 rounded-2xl p-5 shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 to-indigo-500"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold text-sm">👥</div>
          <h3 class="font-extrabold text-sm text-purple-400 uppercase tracking-wide">2. WHO? Users / Stakeholders</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-2">
          <li class="flex items-center gap-2"><span class="text-purple-400 font-bold">👤</span> Candidates (Students & Professionals)</li>
          <li class="flex items-center gap-2"><span class="text-purple-400 font-bold">👤</span> Recruiters & Talent Acquisition Teams</li>
          <li class="flex items-center gap-2"><span class="text-purple-400 font-bold">👤</span> Technical Hiring Managers & Leads</li>
          <li class="flex items-center gap-2"><span class="text-purple-400 font-bold">👤</span> System Administrators (RBAC Governance)</li>
          <li class="flex items-center gap-2"><span class="text-purple-400 font-bold">👤</span> Executive Leadership & C-Suite</li>
        </ul>
      </div>

      <!-- 3. WHAT? (Sky Blue) -->
      <div class="hover-card bg-slate-900/80 border border-sky-500/40 rounded-2xl p-5 shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-sky-500 to-blue-500"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center font-bold text-sm">⚙️</div>
          <h3 class="font-extrabold text-sm text-sky-400 uppercase tracking-wide">3. WHAT? Core Capabilities</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-2">
          <li class="flex items-center gap-2"><span class="text-sky-400 font-bold">⚙</span> Job requisitions & approval gates</li>
          <li class="flex items-center gap-2"><span class="text-sky-400 font-bold">⚙</span> Candidate registration & profiles</li>
          <li class="flex items-center gap-2"><span class="text-sky-400 font-bold">⚙</span> Document upload & PAN verification</li>
          <li class="flex items-center gap-2"><span class="text-sky-400 font-bold">⚙</span> 2-Tier assessments (General + Technical)</li>
          <li class="flex items-center gap-2"><span class="text-sky-400 font-bold">⚙</span> AI-enabled proctoring & anti-cheat</li>
          <li class="flex items-center gap-2"><span class="text-sky-400 font-bold">⚙</span> Candidate tracking & evaluations</li>
          <li class="flex items-center gap-2"><span class="text-sky-400 font-bold">⚙</span> Offer management & onboarding</li>
        </ul>
      </div>

      <!-- 4. HOW? (Orange) -->
      <div class="hover-card bg-slate-900/80 border border-orange-500/40 rounded-2xl p-5 shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-orange-500 to-amber-500"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 rounded-lg bg-orange-500/20 text-orange-400 flex items-center justify-center font-bold text-sm">🛠️</div>
          <h3 class="font-extrabold text-sm text-orange-400 uppercase tracking-wide">4. HOW? Technology & Process</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-2">
          <li class="flex items-center gap-2"><span class="text-orange-400 font-bold">⚡</span> Web-based responsive portal (Bootstrap)</li>
          <li class="flex items-center gap-2"><span class="text-orange-400 font-bold">⚡</span> Structured multi-step test workflows</li>
          <li class="flex items-center gap-2"><span class="text-orange-400 font-bold">⚡</span> Real-time AI vision (Camera, Tab, Screen)</li>
          <li class="flex items-center gap-2"><span class="text-orange-400 font-bold">⚡</span> Secure authentication & RBAC access</li>
          <li class="flex items-center gap-2"><span class="text-orange-400 font-bold">⚡</span> Indexed MySQL database architecture</li>
          <li class="flex items-center gap-2"><span class="text-orange-400 font-bold">⚡</span> Cloud or on-premise container deployment</li>
          <li class="flex items-center gap-2"><span class="text-orange-400 font-bold">⚡</span> Integration with Odoo ERP (HR/Payroll)</li>
        </ul>
      </div>

      <!-- 5. KEY FEATURES (Teal) -->
      <div class="hover-card bg-slate-900/80 border border-teal-500/40 rounded-2xl p-5 shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-teal-500 to-emerald-500"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 rounded-lg bg-teal-500/20 text-teal-400 flex items-center justify-center font-bold text-sm">⭐</div>
          <h3 class="font-extrabold text-sm text-teal-400 uppercase tracking-wide">5. KEY FEATURES What We Offer</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-2">
          <li class="flex items-center gap-2"><span class="text-teal-400 font-bold">★</span> Online proctored assessments</li>
          <li class="flex items-center gap-2"><span class="text-teal-400 font-bold">★</span> Intelligent candidate ranking engine</li>
          <li class="flex items-center gap-2"><span class="text-teal-400 font-bold">★</span> Bilingual portal (Arabic & English ready)</li>
          <li class="flex items-center gap-2"><span class="text-teal-400 font-bold">★</span> Complete Applicant Tracking System (ATS)</li>
          <li class="flex items-center gap-2"><span class="text-teal-400 font-bold">★</span> Dynamic question randomization & timers</li>
          <li class="flex items-center gap-2"><span class="text-teal-400 font-bold">★</span> Granular 15-module permission governance</li>
          <li class="flex items-center gap-2"><span class="text-teal-400 font-bold">★</span> Direct integration with Odoo ERP</li>
        </ul>
      </div>

      <!-- 6. WHERE? (Amber/Yellow) -->
      <div class="hover-card bg-slate-900/80 border border-amber-500/40 rounded-2xl p-5 shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 to-yellow-500"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm">📍</div>
          <h3 class="font-extrabold text-sm text-amber-400 uppercase tracking-wide">6. WHERE? Deployment & Channels</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-2">
          <li class="flex items-center gap-2"><span class="text-amber-400 font-bold">📍</span> Company official careers portal</li>
          <li class="flex items-center gap-2"><span class="text-amber-400 font-bold">📍</span> LinkedIn & Naukri inbound applicant pipelines</li>
          <li class="flex items-center gap-2"><span class="text-amber-400 font-bold">📍</span> Dynamic QR campaigns (Campus / Walk-ins)</li>
          <li class="flex items-center gap-2"><span class="text-amber-400 font-bold">📍</span> Corporate website & intranet integration</li>
          <li class="flex items-center gap-2"><span class="text-amber-400 font-bold">📍</span> Cloud (AWS / Azure) or Secure On-Premise</li>
          <li class="flex items-center gap-2"><span class="text-amber-400 font-bold">📍</span> Deployed across GCC, Middle East & India</li>
        </ul>
      </div>

      <!-- 7. WHEN? (Indigo) -->
      <div class="hover-card bg-slate-900/80 border border-indigo-500/40 rounded-2xl p-5 shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-500"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-sm">📅</div>
          <h3 class="font-extrabold text-sm text-indigo-400 uppercase tracking-wide">7. WHEN? Use Cases / Scenarios</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-2">
          <li class="flex items-center gap-2"><span class="text-indigo-400 font-bold">📅</span> Mass campus recruitment placement drives</li>
          <li class="flex items-center gap-2"><span class="text-indigo-400 font-bold">📅</span> Bulk hiring (50,000+ applicants at scale)</li>
          <li class="flex items-center gap-2"><span class="text-indigo-400 font-bold">📅</span> Lateral engineering & domain hiring</li>
          <li class="flex items-center gap-2"><span class="text-indigo-400 font-bold">📅</span> Graduate & fresher trainee recruitment</li>
          <li class="flex items-center gap-2"><span class="text-indigo-400 font-bold">📅</span> Ongoing talent & periodic skill assessments</li>
        </ul>
      </div>

      <!-- 8. BENEFITS (Green) -->
      <div class="hover-card bg-slate-900/80 border border-emerald-500/40 rounded-2xl p-5 shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-500 to-teal-500"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-sm">📈</div>
          <h3 class="font-extrabold text-sm text-emerald-400 uppercase tracking-wide">8. BENEFITS Business Outcomes</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-2">
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> 50,000+ candidates handled without latency</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> 100% test integrity (Zero proxy test-takers)</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> 85% reduction in engineering interview hours</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> 70% decrease in overall recruitment cost</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> Premium candidate UX & 5-star brand trust</li>
          <li class="flex items-center gap-2"><span class="text-emerald-400 font-bold">✔</span> Seamless ERP/HR data synchronization</li>
        </ul>
      </div>

    </div>

    <!-- Central Branding Footer -->
    <div class="mt-8 text-center p-6 bg-slate-900/60 border border-slate-800 rounded-2xl flex flex-col items-center justify-center">
      <div class="w-12 h-12 rounded-full bg-pink-600/20 border border-pink-500/40 flex items-center justify-center text-xl mb-2">🎓</div>
      <h3 class="text-lg font-bold text-white">Intelligenz IT | TalentAssess 360™</h3>
      <p class="text-xs text-pink-400 font-semibold uppercase tracking-wider mt-0.5">Hire Smarter • Assess Fairer • Build Stronger Teams</p>
      <p class="text-xs text-slate-400 max-w-xl mt-2">
        An enterprise assessment and talent acquisition cloud engineered with Edge AI proctoring, 15-module administration, and frictionless candidate experiences.
      </p>
    </div>
  </section>

  <!-- TAB 3: TECHNICAL ARCHITECTURE -->
  <section id="tab-architecture" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6">
      <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
        <span>End-to-End Workflow & Technical Architecture</span>
        <span class="text-xs font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Discovery to Onboarding</span>
      </h2>
      <p class="text-xs text-slate-400">Three-tier architectural overview: Candidate Journey, System Topology, and 14 Admin Command Modules.</p>
    </div>

    <!-- SECTION A: Candidate Journey (8 Stages) -->
    <div class="mb-8 bg-slate-900/90 border border-pink-500/30 rounded-2xl p-6 shadow-xl">
      <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
        <h3 class="text-sm font-extrabold text-pink-400 uppercase tracking-wider flex items-center gap-2">
          <span>A. Candidate Journey (External Users)</span>
        </h3>
        <span class="text-[11px] font-semibold text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full">Simple • Secure • Seamless</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full bg-pink-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">1</span>
          <h4 class="font-bold text-xs text-white">Find Opportunity</h4>
          <p class="text-[10px] text-slate-400 mt-1">LinkedIn, Naukri, Careers page, Campus QR code</p>
        </div>
        <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full bg-pink-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">2</span>
          <h4 class="font-bold text-xs text-white">Registration</h4>
          <p class="text-[10px] text-slate-400 mt-1">PAN authentication, global dial codes, doc upload</p>
        </div>
        <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full bg-pink-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">3</span>
          <h4 class="font-bold text-xs text-white">Success & Email</h4>
          <p class="text-[10px] text-slate-400 mt-1">Confirmation screen & automated status email</p>
        </div>
        <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full bg-pink-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">4</span>
          <h4 class="font-bold text-xs text-white">Login</h4>
          <p class="text-[10px] text-slate-400 mt-1">Secure login via Reg ID & credentials</p>
        </div>
        <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full bg-pink-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">5</span>
          <h4 class="font-bold text-xs text-white">Profile Review</h4>
          <p class="text-[10px] text-slate-400 mt-1">Check profile details & qualification fields</p>
        </div>
        <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full bg-pink-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">6</span>
          <h4 class="font-bold text-xs text-white">Instructions & Camera</h4>
          <p class="text-[10px] text-slate-400 mt-1">Accept rules & run live webcam check</p>
        </div>
        <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full bg-pink-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">7</span>
          <h4 class="font-bold text-xs text-white">Take Test</h4>
          <p class="text-[10px] text-slate-400 mt-1">Round 1 General Aptitude -> Round 2 Technical</p>
        </div>
        <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full bg-pink-600 text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">8</span>
          <h4 class="font-bold text-xs text-white">Completion</h4>
          <p class="text-[10px] text-slate-400 mt-1">5-star rating, auto-scoring & result email</p>
        </div>
      </div>
    </div>

    <!-- SECTION B: System Architecture (High-Level) -->
    <div class="mb-8 bg-slate-900/90 border border-sky-500/30 rounded-2xl p-6 shadow-xl">
      <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
        <h3 class="text-sm font-extrabold text-sky-400 uppercase tracking-wider flex items-center gap-2">
          <span>B. High-Level System Topology & Integrations</span>
        </h3>
        <span class="text-[11px] font-semibold text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full">Django 5 • MySQL • Edge AI • Odoo ERP</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <!-- Left: Client Devices & Security Services -->
        <div class="space-y-4">
          <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-4">
            <h4 class="text-xs font-bold text-sky-400 uppercase mb-2 flex items-center gap-1.5">💻 Candidate Devices (Browser)</h4>
            <ul class="text-xs text-slate-300 space-y-1.5">
              <li>• Desktop / Laptop (Chrome, Edge, Firefox)</li>
              <li>• Mobile / Tablet (Responsive Web UI)</li>
              <li>• Webcam: Live Camera Check & Stream</li>
              <li>• Geolocation & IP Network Verification</li>
            </ul>
          </div>

          <div class="bg-slate-950/80 border border-orange-500/30 rounded-xl p-4">
            <h4 class="text-xs font-bold text-orange-400 uppercase mb-2 flex items-center gap-1.5">🛡️ Security & Proctoring Shield</h4>
            <ul class="text-xs text-slate-300 space-y-1.5">
              <li>• Coco-SSD Face Tracking (Browser Edge AI)</li>
              <li>• Multi-Person Detection & Cubicle Noise Filter</li>
              <li>• Tab-Switching & ChatGPT Lockout</li>
              <li>• Dual-Monitor & Display Extension Defense</li>
              <li>• DevTools (F12) & Clipboard (Copy/Paste) Lock</li>
            </ul>
          </div>
        </div>

        <!-- Center: Django Web Application Core -->
        <div class="bg-slate-950/80 border border-pink-500/30 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <h4 class="text-xs font-bold text-pink-400 uppercase mb-3 flex items-center gap-1.5">🐍 Web Application Layer (Django / Python)</h4>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="p-2 bg-slate-900 border border-slate-800 rounded-lg">
                <strong class="text-white block">Auth & Users</strong>
                <span class="text-[10px] text-slate-400">Profile & Credentials</span>
              </div>
              <div class="p-2 bg-slate-900 border border-slate-800 rounded-lg">
                <strong class="text-white block">Exam Dashboard</strong>
                <span class="text-[10px] text-slate-400">Test Execution</span>
              </div>
              <div class="p-2 bg-slate-900 border border-slate-800 rounded-lg">
                <strong class="text-white block">Question Bank</strong>
                <span class="text-[10px] text-slate-400">Randomized MCQs</span>
              </div>
              <div class="p-2 bg-slate-900 border border-slate-800 rounded-lg">
                <strong class="text-white block">Role Access</strong>
                <span class="text-[10px] text-slate-400">15-Module RBAC</span>
              </div>
              <div class="p-2 bg-slate-900 border border-slate-800 rounded-lg">
                <strong class="text-white block">Email Scheduler</strong>
                <span class="text-[10px] text-slate-400">Automated Alerts</span>
              </div>
              <div class="p-2 bg-slate-900 border border-slate-800 rounded-lg">
                <strong class="text-white block">QR Generator</strong>
                <span class="text-[10px] text-slate-400">Campus Drives</span>
              </div>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-slate-800">
            <h5 class="text-[11px] font-bold text-emerald-400 uppercase mb-1">🗄️ Database & Storage Layer</h5>
            <p class="text-xs text-slate-300">
              Enterprise MySQL with indexation (<code class="text-pink-400">db_index=True</code>) and server-side pagination (<code class="text-pink-400">Paginator 50</code>) supporting 50,000+ candidates with sub-second queries.
            </p>
          </div>
        </div>

        <!-- Right: External Integrations & DevOps -->
        <div class="space-y-4">
          <div class="bg-slate-950/80 border border-purple-500/30 rounded-xl p-4">
            <h4 class="text-xs font-bold text-purple-400 uppercase mb-2 flex items-center gap-1.5">🔗 External Integrations</h4>
            <ul class="text-xs text-slate-300 space-y-1.5">
              <li>• <strong>Email Service:</strong> SMTP / SendGrid Automation</li>
              <li>• <strong>Job Sources:</strong> LinkedIn & Naukri Portals</li>
              <li>• <strong>Odoo ERP:</strong> HR, Payroll & Onboarding Sync</li>
              <li>• <strong>Corporate Careers:</strong> Embeddable Iframe / API</li>
            </ul>
          </div>

          <div class="bg-slate-950/80 border border-indigo-500/30 rounded-xl p-4">
            <h4 class="text-xs font-bold text-indigo-400 uppercase mb-2 flex items-center gap-1.5">🚀 Infrastructure & DevOps</h4>
            <ul class="text-xs text-slate-300 space-y-1.5">
              <li>• Cloud Deployment (AWS / Azure) or On-Premise</li>
              <li>• Containerized Docker Infrastructure</li>
              <li>• Nginx High-Concurrency Reverse Proxy</li>
              <li>• Prometheus & Grafana Performance Metrics</li>
            </ul>
          </div>
        </div>

      </div>
    </div>

    <!-- SECTION C: Admin / HR Workflow (14 Modules) -->
    <div class="bg-slate-900/90 border border-emerald-500/30 rounded-2xl p-6 shadow-xl">
      <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
        <h3 class="text-sm font-extrabold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
          <span>C. Admin / HR Workflow (14 Management Modules)</span>
        </h3>
        <span class="text-[11px] font-semibold text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full">End-to-End Governance</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-7 gap-3 text-xs">
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-pink-400 font-bold block mb-1">01. Dashboard</span>
          <p class="text-[10px] text-slate-400">Live test funnel & department metrics</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-pink-400 font-bold block mb-1">02. Candidates</span>
          <p class="text-[10px] text-slate-400">Profiles, search & 1-click PDF dossiers</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-pink-400 font-bold block mb-1">03. Manage Tests</span>
          <p class="text-[10px] text-slate-400">Test blueprints, durations & cutoffs</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-pink-400 font-bold block mb-1">04. Question Bank</span>
          <p class="text-[10px] text-slate-400">Tagged MCQs & programming challenges</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-pink-400 font-bold block mb-1">05. Invites</span>
          <p class="text-[10px] text-slate-400">Batch invitations & tokenized test links</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-pink-400 font-bold block mb-1">06. Monitor AI</span>
          <p class="text-[10px] text-slate-400">Live proctoring & violation audits</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-pink-400 font-bold block mb-1">07. Results</span>
          <p class="text-[10px] text-slate-400">Instant auto-scoring & merit ranks</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-sky-400 font-bold block mb-1">08. Instructions</span>
          <p class="text-[10px] text-slate-400">Pre-exam compliance guidelines</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-sky-400 font-bold block mb-1">09. Manage QR</span>
          <p class="text-[10px] text-slate-400">Rapid campus drive QR generation</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-sky-400 font-bold block mb-1">10. Email Builder</span>
          <p class="text-[10px] text-slate-400">Custom branded HTML communications</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-sky-400 font-bold block mb-1">11. Role RBAC</span>
          <p class="text-[10px] text-slate-400">15 toggleable permissions per user</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-sky-400 rounded-xl">
          <span class="text-sky-400 font-bold block mb-1">12. Configuration</span>
          <p class="text-[10px] text-slate-400">System parameters & passing marks</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-slate-800 rounded-xl">
          <span class="text-sky-400 font-bold block mb-1">13. Analytics</span>
          <p class="text-[10px] text-slate-400">Hiring throughput & cohort insights</p>
        </div>
        <div class="p-3 bg-slate-950/80 border border-emerald-500/50 rounded-xl">
          <span class="text-emerald-400 font-bold block mb-1">14. Odoo Onboard</span>
          <p class="text-[10px] text-slate-400">Offer generation & contract sync</p>
        </div>
      </div>
    </div>
  </section>

  <!-- TAB 4: BENEFITS, ADVANTAGES & FEATURES EXPLANATION -->
  <section id="tab-benefits" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6">
      <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
        <span>Strategic Value: Benefits, Advantages & Features</span>
        <span class="text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Executive Deep-Dive</span>
      </h2>
      <p class="text-xs text-slate-400">Clear breakdown of tangible business outcomes, competitive advantages over 3rd-party SaaS, and technical features.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- Card 1: BENEFITS (Business Outcomes) -->
      <div class="bg-slate-900 border border-emerald-500/40 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-emerald-500 to-teal-400"></div>
        <div class="flex items-center gap-2.5 mb-4">
          <span class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-sm">📈</span>
          <h3 class="text-base font-extrabold text-emerald-400 uppercase tracking-wider">Benefits (What You Gain)</h3>
        </div>
        <p class="text-xs text-slate-400 mb-4 leading-relaxed">
          Measurable commercial, operational, and financial returns achieved by transitioning to TalentAssess 360.
        </p>
        <ul class="text-xs text-slate-300 space-y-3">
          <li class="flex items-start gap-2">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>85% Reduction in Engineering Screening Hours:</strong> Reclaims 300+ billable senior developer hours monthly by automating Rounds 1 & 2.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>70% Drop in Cost-Per-Hire:</strong> Eliminates recurring test vendor fees, third-party proctoring markups, and recruiter coordination waste.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Zero-Latency Assessment Delivery:</strong> 50,000+ candidates can register and test in parallel with sub-second page loads.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Instant Campus Placement Throughput:</strong> Test thousands of college students in under 3 hours with automatic results ready for same-day interviews.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Elevated Candidate Trust & UX:</strong> Clean, responsive UI with interactive 5-star feedback and automated branded emails.</div>
          </li>
        </ul>
      </div>

      <!-- Card 2: ADVANTAGES (Why It Beats Competitors) -->
      <div class="bg-slate-900 border border-sky-500/40 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-sky-500 to-blue-500"></div>
        <div class="flex items-center gap-2.5 mb-4">
          <span class="w-8 h-8 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center font-bold text-sm">🏆</span>
          <h3 class="text-base font-extrabold text-sky-400 uppercase tracking-wider">Advantages (Competitive Edge)</h3>
        </div>
        <p class="text-xs text-slate-400 mb-4 leading-relaxed">
          Why our proprietary platform decisively outperforms external SaaS vendors like HackerRank, Mercer Mettl, or Codility.
        </p>
        <ul class="text-xs text-slate-300 space-y-3">
          <li class="flex items-start gap-2">
            <span class="text-sky-400 font-bold mt-0.5">★</span>
            <div><strong>Zero Cloud GPU Streaming Cost:</strong> Coco-SSD vision AI runs directly inside the candidate's browser, eliminating massive AWS/GCP GPU streaming bills.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-sky-400 font-bold mt-0.5">★</span>
            <div><strong>100% In-House Intellectual Property:</strong> No annual license fees ($15,000–$25,000 saved per year); all candidate data and question banks remain strictly confidential.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-sky-400 font-bold mt-0.5">★</span>
            <div><strong>Cubicle Noise Filter:</strong> Distinguishes actual proxy test-takers from background office colleagues walking across open cubicles.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-sky-400 font-bold mt-0.5">★</span>
            <div><strong>Bilingual Middle East & GCC Readiness:</strong> Built-in dual-language support (Arabic & English) with direct Odoo ERP integration.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-sky-400 font-bold mt-0.5">★</span>
            <div><strong>Zero N+1 Query Architecture:</strong> Indexed relational schema ensuring smooth execution across millions of assessment queries.</div>
          </li>
        </ul>
      </div>

      <!-- Card 3: FEATURES (Platform Capabilities) -->
      <div class="bg-slate-900 border border-pink-500/40 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-pink-500 to-rose-400"></div>
        <div class="flex items-center gap-2.5 mb-4">
          <span class="w-8 h-8 rounded-lg bg-pink-500/20 text-pink-400 flex items-center justify-center font-bold text-sm">⚡</span>
          <h3 class="text-base font-extrabold text-pink-400 uppercase tracking-wider">Features (What's Built-In)</h3>
        </div>
        <p class="text-xs text-slate-400 mb-4 leading-relaxed">
          Comprehensive inventory of functional and technical capabilities powering the candidate and recruiter portals.
        </p>
        <ul class="text-xs text-slate-300 space-y-3">
          <li class="flex items-start gap-2">
            <span class="text-pink-400 font-bold mt-0.5">⚙</span>
            <div><strong>2-Tier Automated Testing:</strong> Round 1 General Cognitive (Aptitude/Logic) + Round 2 Technical Coding/MCQs.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-pink-400 font-bold mt-0.5">⚙</span>
            <div><strong>Multi-Vector Anti-Cheat Shield:</strong> Webcam tracking, tab-switching lockout, dual-monitor lockout, and clipboard/F12 lock.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-pink-400 font-bold mt-0.5">⚙</span>
            <div><strong>Global Onboarding:</strong> 240+ international dial codes, 10-digit alphanumeric PAN verification, and adaptive % vs CGPA logic.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-pink-400 font-bold mt-0.5">⚙</span>
            <div><strong>14-Module Admin Command Hub:</strong> Granular RBAC, test compilers, question bank taxonomy, and live candidate tracking.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-pink-400 font-bold mt-0.5">⚙</span>
            <div><strong>1-Click Candidate Dossiers:</strong> Verified candidate PDF portfolios with test scores, photos, feedback, and hiring recommendations.</div>
          </li>
        </ul>
      </div>

    </div>
  </section>

  <!-- TAB 5: MARVELAPP-STYLE INTERACTIVE CLICKABLE WIREFRAME PROTOTYPE -->
  <section id="tab-wireframe" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
          <span>MarvelApp-Style Interactive Clickable Prototype</span>
          <span class="text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">All Buttons Active</span>
        </h2>
        <p class="text-xs text-slate-400">Click anywhere inside the device frame to interact with the screens, test validations, and launch live endpoints.</p>
      </div>

      <!-- Mode Switcher: Candidate vs Admin -->
      <div class="flex items-center gap-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800 text-xs">
        <button onclick="setWireframePerspective('candidate')" id="btn-wf-cand" class="px-3 py-1.5 rounded-lg font-bold transition bg-pink-600 text-white">
          Candidate Side (External)
        </button>
        <button onclick="setWireframePerspective('admin')" id="btn-wf-admin" class="px-3 py-1.5 rounded-lg font-bold transition text-slate-400 hover:text-white">
          Admin Side (Internal)
        </button>
      </div>
    </div>

    <!-- Interactive MarvelApp Device Wrapper -->
    <div class="bg-slate-900 border-2 border-slate-800 rounded-3xl p-4 sm:p-8 shadow-2xl relative">
      
      <!-- Device Top Bar / Browser Shell -->
      <div class="bg-slate-950 border border-slate-800 rounded-2xl p-3 mb-6 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-rose-500"></span>
          <span class="w-3 h-3 rounded-full bg-amber-500"></span>
          <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
          <span id="wf-url-bar" class="ml-3 px-3 py-1 bg-slate-900 rounded-md text-[11px] text-slate-400 font-mono border border-slate-800">
            http://127.0.0.1:8080/candidates/register/
          </span>
        </div>
        <div class="flex items-center gap-2">
          <a id="wf-live-btn" href="http://127.0.0.1:8080/candidates/register/" target="_blank" class="px-2.5 py-1 bg-pink-600/30 hover:bg-pink-600 text-pink-300 hover:text-white border border-pink-500/50 rounded text-[11px] font-semibold transition">
            🔗 Launch in Live Server
          </a>
        </div>
      </div>

      <!-- Candidate Side Screens -->
      <div id="perspective-candidate" class="wireframe-screen">
        
        <!-- Step Navigation Bar -->
        <div class="flex flex-wrap items-center gap-2 mb-6 border-b border-slate-800 pb-3 text-xs">
          <button onclick="showCandidateScreen('register')" id="btn-scr-register" class="px-3 py-1.5 rounded-lg font-semibold bg-pink-600 text-white">1. Registration Form</button>
          <button onclick="showCandidateScreen('camera')" id="btn-scr-camera" class="px-3 py-1.5 rounded-lg font-semibold text-slate-400 hover:text-white hover:bg-slate-800">2. Webcam AI Check</button>
          <button onclick="showCandidateScreen('test')" id="btn-scr-test" class="px-3 py-1.5 rounded-lg font-semibold text-slate-400 hover:text-white hover:bg-slate-800">3. Live Test Screen</button>
          <button onclick="showCandidateScreen('feedback')" id="btn-scr-feedback" class="px-3 py-1.5 rounded-lg font-semibold text-slate-400 hover:text-white hover:bg-slate-800">4. 5-Star Feedback</button>
        </div>

        <!-- Candidate Screen 1: Registration Form -->
        <div id="scr-candidate-register" class="bg-slate-950 border border-slate-800 rounded-2xl p-6">
          <div class="max-w-2xl mx-auto">
            <h3 class="text-base font-extrabold text-white mb-1">Candidate Registration Form</h3>
            <p class="text-xs text-slate-400 mb-6">Complete your profile to unlock proctored assessment credentials.</p>

            <form onsubmit="event.preventDefault(); simulateRegistration();" class="space-y-4 text-xs">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-slate-300 font-semibold mb-1">First Name *</label>
                  <input type="text" id="demo-fn" value="Nagendra" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white">
                </div>
                <div>
                  <label class="block text-slate-300 font-semibold mb-1">Last Name *</label>
                  <input type="text" id="demo-ln" value="Panda" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white">
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-slate-300 font-semibold mb-1">PAN Number (10-Digit Alphanumeric) *</label>
                  <input type="text" id="demo-pan" value="ABCDE1234F" maxlength="10" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-pink-400 font-mono font-bold uppercase">
                </div>
                <div>
                  <label class="block text-slate-300 font-semibold mb-1">Country Dial Code *</label>
                  <select class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white">
                    <option>+91 (India)</option>
                    <option>+1 (USA/Canada)</option>
                    <option>+971 (UAE)</option>
                    <option>+44 (UK)</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-slate-300 font-semibold mb-1">Mobile Number *</label>
                  <input type="tel" value="9876543210" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white">
                </div>
                <div>
                  <label class="block text-slate-300 font-semibold mb-1">Highest Qualification *</label>
                  <select id="demo-qual" onchange="toggleScoreType(this.value)" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white">
                    <option value="UG">UG (Under Graduate) - Requires %</option>
                    <option value="PG">PG (Post Graduate) - Requires CGPA</option>
                    <option value="PhD">PhD - Requires CGPA</option>
                  </select>
                </div>
              </div>

              <div id="box-percentage">
                <label class="block text-slate-300 font-semibold mb-1">Undergraduate Percentage (%) *</label>
                <input type="number" value="82.5" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white">
              </div>

              <div id="box-cgpa" class="hidden">
                <label class="block text-slate-300 font-semibold mb-1">Postgraduate CGPA (Scale of 10.0) *</label>
                <input type="number" step="0.1" value="8.9" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-white">
              </div>

              <button type="submit" class="w-full py-3 bg-pink-600 hover:bg-pink-500 font-bold text-white rounded-xl shadow-lg transition mt-4">
                🚀 Submit Registration & Verify Credentials
              </button>
            </form>
          </div>
        </div>

        <!-- Candidate Screen 2: Webcam AI Check -->
        <div id="scr-candidate-camera" class="hidden bg-slate-950 border border-slate-800 rounded-2xl p-6">
          <div class="max-w-xl mx-auto text-center">
            <h3 class="text-base font-extrabold text-white mb-1">Pre-Exam Webcam & Hardware Handshake</h3>
            <p class="text-xs text-slate-400 mb-4">Edge AI proctoring active. Verify that only one candidate is in the camera frame.</p>

            <!-- Video Simulation Box -->
            <div class="relative bg-slate-900 border-2 border-emerald-500 rounded-2xl h-64 flex flex-col items-center justify-center overflow-hidden mb-4 shadow-inner">
              <div class="w-24 h-24 rounded-full bg-slate-800 border-2 border-emerald-400 flex items-center justify-center text-4xl mb-2 animate-pulse">
                👤
              </div>
              <span class="px-3 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 rounded-full text-xs font-semibold flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                Face Verified • Single Candidate Confirmed (100% Quality)
              </span>
              <div class="absolute top-3 left-3 text-[10px] text-slate-400 font-mono bg-slate-950/80 px-2 py-0.5 rounded">
                Coco-SSD Vision Engine v2.1
              </div>
              <div class="absolute bottom-3 right-3 text-[10px] text-emerald-400 font-semibold bg-slate-950/80 px-2 py-0.5 rounded">
                Cubicle Noise Filter: ACTIVE
              </div>
            </div>

            <div class="flex items-center justify-center gap-3">
              <button onclick="showCandidateScreen('test')" class="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 font-bold text-white rounded-xl text-xs shadow-lg transition">
                Proceed to Round 1: General Test ➜
              </button>
            </div>
          </div>
        </div>

        <!-- Candidate Screen 3: Live Test Screen -->
        <div id="scr-candidate-test" class="hidden bg-slate-950 border border-slate-800 rounded-2xl p-6">
          <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
            <div>
              <span class="text-xs font-bold text-pink-400 uppercase">Round 1: General Cognitive & Technical Test</span>
              <h3 class="text-sm font-extrabold text-white">Question 4 of 25 (Time Remaining: <span id="timer" class="text-emerald-400 font-mono font-bold">18:42</span>)</h3>
            </div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-semibold rounded border border-emerald-500/20">
                Camera Live: 🟢 1 Person
              </span>
            </div>
          </div>

          <div class="bg-slate-900 p-4 rounded-xl border border-slate-800 mb-4">
            <p class="text-xs text-white font-medium mb-3">
              In a distributed system, which HTTP status code represents that the server successfully received and processed the request without any client or server error?
            </p>
            <div class="space-y-2 text-xs">
              <label class="flex items-center gap-2 p-2.5 bg-slate-950 border border-slate-800 rounded-lg cursor-pointer hover:border-pink-500">
                <input type="radio" name="q4" class="text-pink-600">
                <span class="text-slate-300">A) 404 Not Found</span>
              </label>
              <label class="flex items-center gap-2 p-2.5 bg-slate-950 border border-pink-500 rounded-lg cursor-pointer bg-pink-500/10">
                <input type="radio" name="q4" checked class="text-pink-600">
                <span class="text-white font-semibold">B) 200 OK</span>
              </label>
              <label class="flex items-center gap-2 p-2.5 bg-slate-950 border border-slate-800 rounded-lg cursor-pointer hover:border-pink-500">
                <input type="radio" name="q4" class="text-pink-600">
                <span class="text-slate-300">C) 500 Internal Server Error</span>
              </label>
              <label class="flex items-center gap-2 p-2.5 bg-slate-950 border border-slate-800 rounded-lg cursor-pointer hover:border-pink-500">
                <input type="radio" name="q4" class="text-pink-600">
                <span class="text-slate-300">D) 403 Forbidden</span>
              </label>
            </div>
          </div>

          <div class="flex justify-between items-center text-xs">
            <button class="px-4 py-2 bg-slate-800 text-slate-300 rounded-lg font-semibold">Previous Question</button>
            <button onclick="showCandidateScreen('feedback')" class="px-6 py-2 bg-pink-600 hover:bg-pink-500 text-white rounded-lg font-bold shadow transition">
              Submit Exam & Complete Evaluation ➜
            </button>
          </div>
        </div>

        <!-- Candidate Screen 4: 5-Star Feedback -->
        <div id="scr-candidate-feedback" class="hidden bg-slate-950 border border-slate-800 rounded-2xl p-6 text-center max-w-lg mx-auto">
          <div class="w-14 h-14 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center text-2xl mx-auto mb-3">
            🎉
          </div>
          <h3 class="text-base font-extrabold text-white">Assessment Submitted Successfully!</h3>
          <p class="text-xs text-slate-400 mt-1 mb-4">Your responses have been securely computed and forwarded to the HR review panel.</p>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 text-xs mb-4">
            <span class="text-slate-300 font-semibold block mb-2">How was your testing experience today?</span>
            <div class="flex justify-center gap-2 text-2xl text-amber-400 cursor-pointer mb-3">
              <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
            </div>
            <textarea placeholder="Write your feedback comments here..." class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-white text-xs"></textarea>
            <button onclick="alert('Thank you! Your feedback has been recorded into your candidate dossier.');" class="w-full mt-2 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg transition">
              Submit Candidate Feedback
            </button>
          </div>

          <a href="http://127.0.0.1:8080/candidates/login/" target="_blank" class="text-xs text-pink-400 hover:underline">
            Go to Candidate Login
          </a>
        </div>

      </div>

      <!-- Admin Side Screens -->
      <div id="perspective-admin" class="hidden wireframe-screen">
        
        <!-- Admin Sub-Navigation -->
        <div class="flex flex-wrap items-center gap-2 mb-6 border-b border-slate-800 pb-3 text-xs">
          <button onclick="showAdminScreen('dash')" id="btn-adm-dash" class="px-3 py-1.5 rounded-lg font-semibold bg-pink-600 text-white">1. Admin Dashboard</button>
          <button onclick="showAdminScreen('cand')" id="btn-adm-cand" class="px-3 py-1.5 rounded-lg font-semibold text-slate-400 hover:text-white hover:bg-slate-800">2. Candidate List & PDF</button>
          <button onclick="showAdminScreen('res')" id="btn-adm-res" class="px-3 py-1.5 rounded-lg font-semibold text-slate-400 hover:text-white hover:bg-slate-800">3. Test Results Hub</button>
          <button onclick="showAdminScreen('qr')" id="btn-adm-qr" class="px-3 py-1.5 rounded-lg font-semibold text-slate-400 hover:text-white hover:bg-slate-800">4. QR Code Generator</button>
        </div>

        <!-- Admin Screen 1: Dashboard -->
        <div id="scr-admin-dash" class="bg-slate-950 border border-slate-800 rounded-2xl p-6">
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span class="text-xs text-slate-400 uppercase font-semibold">Total Candidates</span>
              <h4 class="text-2xl font-extrabold text-white mt-1">1,482</h4>
              <span class="text-[10px] text-emerald-400">+12% this week</span>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span class="text-xs text-slate-400 uppercase font-semibold">Tests Completed</span>
              <h4 class="text-2xl font-extrabold text-sky-400 mt-1">948</h4>
              <span class="text-[10px] text-slate-400">Rounds 1 & 2</span>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span class="text-xs text-slate-400 uppercase font-semibold">Pass Rate</span>
              <h4 class="text-2xl font-extrabold text-emerald-400 mt-1">21.4%</h4>
              <span class="text-[10px] text-slate-400">Strict cutoffs applied</span>
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span class="text-xs text-slate-400 uppercase font-semibold">Anti-Cheat Flags</span>
              <h4 class="text-2xl font-extrabold text-rose-400 mt-1">0</h4>
              <span class="text-[10px] text-emerald-400">100% Integrity</span>
            </div>
          </div>

          <div class="flex justify-between items-center text-xs">
            <span class="text-slate-400">Live system status: All 14 modules operational.</span>
            <a href="http://127.0.0.1:8080/dashboard/" target="_blank" class="px-4 py-2 bg-pink-600 hover:bg-pink-500 text-white font-bold rounded-lg transition">
              Open Full Live Dashboard (Port 8080) ➜
            </a>
          </div>
        </div>

        <!-- Admin Screen 2: Candidate List -->
        <div id="scr-admin-cand" class="hidden bg-slate-950 border border-slate-800 rounded-2xl p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-extrabold text-white">Manage Candidates (50,000+ Indexed Records)</h3>
            <a href="http://127.0.0.1:8080/candidates/list/" target="_blank" class="text-xs text-pink-400 hover:underline">Launch Live /candidates/list/</a>
          </div>

          <table class="w-full text-xs text-left">
            <thead class="bg-slate-900 text-slate-400 border-b border-slate-800">
              <tr>
                <th class="p-2.5">Reg ID</th>
                <th class="p-2.5">Candidate Name</th>
                <th class="p-2.5">PAN Number</th>
                <th class="p-2.5">Status</th>
                <th class="p-2.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800 text-slate-300">
              <tr>
                <td class="p-2.5 font-mono text-pink-400 font-bold">REG-2026-INTITIN000005</td>
                <td class="p-2.5 font-semibold text-white">Nagendra Panda</td>
                <td class="p-2.5 font-mono">ABCDE1234F</td>
                <td class="p-2.5"><span class="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded-full text-[10px] font-semibold">Test Completed</span></td>
                <td class="p-2.5 text-right">
                  <a href="http://127.0.0.1:8080/candidates/pdf/5/" target="_blank" class="px-2.5 py-1 bg-blue-600/30 text-blue-300 rounded hover:bg-blue-600 hover:text-white transition">
                    📄 Export PDF Dossier
                  </a>
                </td>
              </tr>
              <tr>
                <td class="p-2.5 font-mono text-pink-400 font-bold">REG-2026-INTITIN000004</td>
                <td class="p-2.5 font-semibold text-white">Rahul Verma</td>
                <td class="p-2.5 font-mono">BCDEF2345G</td>
                <td class="p-2.5"><span class="px-2 py-0.5 bg-sky-500/20 text-sky-400 rounded-full text-[10px] font-semibold">Registered</span></td>
                <td class="p-2.5 text-right">
                  <span class="text-slate-500 text-[11px]">Pending Exam</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Admin Screen 3: Test Results -->
        <div id="scr-admin-res" class="hidden bg-slate-950 border border-slate-800 rounded-2xl p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-extrabold text-white">Real-Time Test Results & Auto-Scoring Hub</h3>
            <a href="http://127.0.0.1:8080/results/" target="_blank" class="text-xs text-pink-400 hover:underline">Launch Live /results/</a>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 text-xs space-y-3">
            <div class="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-800">
              <div>
                <strong class="text-white block">Nagendra Panda (General Test)</strong>
                <span class="text-slate-400 text-[11px]">Score: 16/20 (80.0%) • Status: <span class="text-emerald-400 font-bold">PASSED</span></span>
              </div>
              <a href="http://127.0.0.1:8080/results/" target="_blank" class="px-3 py-1 bg-emerald-600 text-white rounded font-semibold text-[11px]">
                Review Submission
              </a>
            </div>
          </div>
        </div>

        <!-- Admin Screen 4: QR Code Generator -->
        <div id="scr-admin-qr" class="hidden bg-slate-950 border border-slate-800 rounded-2xl p-6 text-center max-w-md mx-auto">
          <h3 class="text-sm font-extrabold text-white mb-1">Campus Placement QR Generator</h3>
          <p class="text-xs text-slate-400 mb-4">Project this QR code on auditorium screens for instant candidate onboarding.</p>

          <div class="bg-white p-4 rounded-xl inline-block shadow-lg mb-4">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=http://127.0.0.1:8080/candidates/register/" alt="QR" class="w-36 h-36">
          </div>

          <div class="flex justify-center gap-2 text-xs">
            <a href="http://127.0.0.1:8080/qr/list/" target="_blank" class="px-4 py-2 bg-pink-600 hover:bg-pink-500 text-white font-bold rounded-lg transition">
              Manage All QR Campaigns (Port 8080)
            </a>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- TAB 6: DoR, DoD & REAL-WORLD USE CASES -->
  <section id="tab-dordod" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6">
      <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
        <span>Engineering Governance & Enterprise Methodology</span>
        <span class="text-xs font-semibold text-pink-400 bg-pink-500/10 px-2 py-0.5 rounded border border-pink-500/20">DoR & DoD Standards</span>
      </h2>
      <p class="text-xs text-slate-400">Strict criteria ensuring zero assessment defects during high-concurrency placement drives.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      
      <!-- DoR Table -->
      <div class="bg-slate-900 border border-pink-500/30 rounded-2xl p-6 shadow-xl">
        <div class="flex items-center gap-2 mb-4 pb-3 border-b border-slate-800">
          <span class="w-7 h-7 rounded-lg bg-pink-600/20 text-pink-400 flex items-center justify-center font-bold text-sm">🎯</span>
          <h3 class="font-extrabold text-sm text-pink-400 uppercase tracking-wide">Definition of Ready (DoR) - Pre-Exam Gate</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-3">
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Candidate Identity Verified:</strong> Alphanumeric PAN + matching global country code validated against database.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Hardware Handshake:</strong> Webcam resolution, microphone permission, and bandwidth speed confirmed.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Anti-Cheat Agreement:</strong> Candidate accepts SweetAlert2 strict compliance rules (no tabs, sit silently).</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Exam Compilation:</strong> Questions randomized from Question Bank with configured cutoffs and timers.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Edge AI Proctor Active:</strong> Coco-SSD computer vision initialized inside candidate's browser (Single face check).</div>
          </li>
        </ul>
      </div>

      <!-- DoD Table -->
      <div class="bg-slate-900 border border-emerald-500/30 rounded-2xl p-6 shadow-xl">
        <div class="flex items-center gap-2 mb-4 pb-3 border-b border-slate-800">
          <span class="w-7 h-7 rounded-lg bg-emerald-600/20 text-emerald-400 flex items-center justify-center font-bold text-sm">🏁</span>
          <h3 class="font-extrabold text-sm text-emerald-400 uppercase tracking-wide">Definition of Done (DoD) - Evaluation Gate</h3>
        </div>
        <ul class="text-xs text-slate-300 space-y-3">
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Responses Committed:</strong> All candidate answers written securely to MySQL with zero unhandled exceptions.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Auto-Evaluation:</strong> Raw marks, section-by-section breakdown, and pass/fail flags calculated instantly.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Proctoring Audit Passed:</strong> Zero unhandled multi-person or tab-switching violations in violation log.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>Result Registered:</strong> Candidate result record appears immediately at the top of Admin Results view.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-400 font-bold mt-0.5">✔</span>
            <div><strong>PDF Dossier Generated:</strong> 1-click candidate dossier generated containing scores, 5-star rating, and feedback.</div>
          </li>
        </ul>
      </div>

    </div>

    <!-- Real-World Enterprise Use Cases -->
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-sm font-extrabold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
        <span>📌 Real-World Enterprise Use Cases</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="p-4 bg-slate-950 border border-slate-800 rounded-xl">
          <h4 class="font-bold text-pink-400 text-sm mb-1">Campus Drives (5,000+ Students)</h4>
          <p class="text-slate-300">
            QR codes displayed on auditorium screens enable instant self-registration and simultaneous aptitude testing. Results compiled in 5 minutes for same-day technical interviews.
          </p>
        </div>
        <div class="p-4 bg-slate-950 border border-slate-800 rounded-xl">
          <h4 class="font-bold text-sky-400 text-sm mb-1">Lateral Tech Hiring (AI & Cloud)</h4>
          <p class="text-slate-300">
            Proprietary Edge AI proctor blocks ChatGPT in background tabs, dual monitors, and proxy assistants, ensuring 100% genuine engineering talent.
          </p>
        </div>
        <div class="p-4 bg-slate-950 border border-slate-800 rounded-xl">
          <h4 class="font-bold text-emerald-400 text-sm mb-1">Global / GCC & Odoo ERP</h4>
          <p class="text-slate-300">
            Bilingual portal support (Arabic & English) with direct Odoo ERP integration for automated contracts, HR onboarding, and payroll synchronization.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Interactive JavaScript Controller -->
  <script>
    function switchTab(tabId) {
      ['urls', 'mindmap', 'architecture', 'benefits', 'wireframe', 'dordod'].forEach(t => {
        document.getElementById('tab-' + t).classList.add('hidden');
        const btn = document.getElementById('btn-tab-' + t);
        btn.classList.remove('bg-pink-600', 'bg-emerald-600', 'text-white', 'shadow');
        btn.classList.add('text-slate-300');
      });
      document.getElementById('tab-' + tabId).classList.remove('hidden');
      const activeBtn = document.getElementById('btn-tab-' + tabId);
      if (tabId === 'urls') {
        activeBtn.classList.add('bg-emerald-600', 'text-white', 'shadow');
      } else {
        activeBtn.classList.add('bg-pink-600', 'text-white', 'shadow');
      }
      activeBtn.classList.remove('text-slate-300');
    }

    function setWireframePerspective(persp) {
      if (persp === 'candidate') {
        document.getElementById('perspective-candidate').classList.remove('hidden');
        document.getElementById('perspective-admin').classList.add('hidden');
        document.getElementById('btn-wf-cand').classList.add('bg-pink-600', 'text-white');
        document.getElementById('btn-wf-cand').classList.remove('text-slate-400');
        document.getElementById('btn-wf-admin').classList.remove('bg-pink-600', 'text-white');
        document.getElementById('btn-wf-admin').classList.add('text-slate-400');
        document.getElementById('wf-url-bar').textContent = 'http://127.0.0.1:8080/candidates/register/';
        document.getElementById('wf-live-btn').href = 'http://127.0.0.1:8080/candidates/register/';
      } else {
        document.getElementById('perspective-admin').classList.remove('hidden');
        document.getElementById('perspective-candidate').classList.add('hidden');
        document.getElementById('btn-wf-admin').classList.add('bg-pink-600', 'text-white');
        document.getElementById('btn-wf-admin').classList.remove('text-slate-400');
        document.getElementById('btn-wf-cand').classList.remove('bg-pink-600', 'text-white');
        document.getElementById('btn-wf-cand').classList.add('text-slate-400');
        document.getElementById('wf-url-bar').textContent = 'http://127.0.0.1:8080/dashboard/';
        document.getElementById('wf-live-btn').href = 'http://127.0.0.1:8080/dashboard/';
      }
    }

    function showCandidateScreen(scr) {
      ['register', 'camera', 'test', 'feedback'].forEach(s => {
        document.getElementById('scr-candidate-' + s).classList.add('hidden');
        const b = document.getElementById('btn-scr-' + s);
        b.classList.remove('bg-pink-600', 'text-white');
        b.classList.add('text-slate-400');
      });
      document.getElementById('scr-candidate-' + scr).classList.remove('hidden');
      const active = document.getElementById('btn-scr-' + scr);
      active.classList.add('bg-pink-600', 'text-white');
      active.classList.remove('text-slate-400');

      const urls = {
        'register': 'http://127.0.0.1:8080/candidates/register/',
        'camera': 'http://127.0.0.1:8080/candidates/instructions/GT/',
        'test': 'http://127.0.0.1:8080/exam_dashboard/test_page/GT/',
        'feedback': 'http://127.0.0.1:8080/candidates/registration-success/'
      };
      document.getElementById('wf-url-bar').textContent = urls[scr];
      document.getElementById('wf-live-btn').href = urls[scr];
    }

    function showAdminScreen(scr) {
      ['dash', 'cand', 'res', 'qr'].forEach(s => {
        document.getElementById('scr-admin-' + s).classList.add('hidden');
        const b = document.getElementById('btn-adm-' + s);
        b.classList.remove('bg-pink-600', 'text-white');
        b.classList.add('text-slate-400');
      });
      document.getElementById('scr-admin-' + scr).classList.remove('hidden');
      const active = document.getElementById('btn-adm-' + scr);
      active.classList.add('bg-pink-600', 'text-white');
      active.classList.remove('text-slate-400');

      const urls = {
        'dash': 'http://127.0.0.1:8080/dashboard/',
        'cand': 'http://127.0.0.1:8080/candidates/list/',
        'res': 'http://127.0.0.1:8080/results/',
        'qr': 'http://127.0.0.1:8080/qr/list/'
      };
      document.getElementById('wf-url-bar').textContent = urls[scr];
      document.getElementById('wf-live-btn').href = urls[scr];
    }

    function toggleScoreType(val) {
      if (val === 'PG' || val === 'PhD') {
        document.getElementById('box-percentage').classList.add('hidden');
        document.getElementById('box-cgpa').classList.remove('hidden');
      } else {
        document.getElementById('box-percentage').classList.remove('hidden');
        document.getElementById('box-cgpa').classList.add('hidden');
      }
    }

    function simulateRegistration() {
      alert('Simulation: PAN ABCDE1234F verified successfully! Advancing to Hardware & Camera Check...');
      showCandidateScreen('camera');
    }

    function copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard: ' + text);
      }).catch(err => {
        prompt('Copy this URL:', text);
      });
    }
  </script>
</body>
</html>
"""

# Destination paths
destinations = [
    r"C:\Users\User\Downloads\TalentAssess_360_MindMap_Visual.html",
    r"c:\Examportal Application\Examportal-applications\TalentAssess_360_MindMap_Visual.html",
    r"C:\Users\User\.gemini\antigravity\brain\fe8240e4-d948-4a3f-bd80-cd638df2f4e2\TalentAssess_360_MindMap_Visual.html"
]

for d in destinations:
    try:
        with open(d, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Successfully written to: {d}")
    except Exception as e:
        print(f"Error writing to {d}: {e}")
