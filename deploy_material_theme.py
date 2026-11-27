import os

html_content = """<!DOCTYPE html>
<html lang="en" class="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Intelligenz IT TalentAssess 360™ - Material Mind Map, Architecture & Interactive Suite</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    body {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }
    .material-card {
      background: #ffffff;
      border: 1px solid rgba(226, 232, 240, 0.8);
      border-radius: 1rem;
      box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.05), 0 7px 10px -5px rgba(0, 0, 0, 0.04);
      transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s ease;
    }
    .material-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
    }
    .floating-icon {
      border-radius: 0.75rem;
      box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.14), 0 7px 10px -5px rgba(0, 0, 0, 0.2);
    }
    .floating-pink {
      background: linear-gradient(195deg, #ec407a 0%, #d81b60 100%);
      box-shadow: 0 4px 20px 0 rgba(233, 30, 99, 0.35), 0 7px 10px -5px rgba(233, 30, 99, 0.4);
    }
    .floating-dark {
      background: linear-gradient(195deg, #42424a 0%, #191919 100%);
      box-shadow: 0 4px 20px 0 rgba(25, 25, 25, 0.35), 0 7px 10px -5px rgba(25, 25, 25, 0.4);
    }
    .floating-green {
      background: linear-gradient(195deg, #66bb6a 0%, #43a047 100%);
      box-shadow: 0 4px 20px 0 rgba(76, 175, 80, 0.35), 0 7px 10px -5px rgba(76, 175, 80, 0.4);
    }
    .floating-blue {
      background: linear-gradient(195deg, #49a3f1 0%, #1a73e8 100%);
      box-shadow: 0 4px 20px 0 rgba(33, 150, 243, 0.35), 0 7px 10px -5px rgba(33, 150, 243, 0.4);
    }
    .floating-orange {
      background: linear-gradient(195deg, #ffa726 0%, #fb8c00 100%);
      box-shadow: 0 4px 20px 0 rgba(255, 152, 0, 0.35), 0 7px 10px -5px rgba(255, 152, 0, 0.4);
    }
    .floating-purple {
      background: linear-gradient(195deg, #ab47bc 0%, #8e24aa 100%);
      box-shadow: 0 4px 20px 0 rgba(156, 39, 176, 0.35), 0 7px 10px -5px rgba(156, 39, 176, 0.4);
    }
    .floating-teal {
      background: linear-gradient(195deg, #26a69a 0%, #00897b 100%);
      box-shadow: 0 4px 20px 0 rgba(0, 150, 136, 0.35), 0 7px 10px -5px rgba(0, 150, 136, 0.4);
    }
    .wireframe-screen {
      transition: opacity 0.3s ease, transform 0.3s ease;
    }
    @media print {
      .no-print { display: none !important; }
      body { background: white !important; color: black !important; }
    }
  </style>
</head>
<body class="bg-[#f0f2f5] text-[#344767] min-h-screen flex flex-col antialiased selection:bg-pink-500 selection:text-white">

  <!-- Material Top Header -->
  <header class="no-print bg-white/90 backdrop-blur border-b border-slate-200/80 px-6 py-3.5 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-50 shadow-sm">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl floating-pink flex items-center justify-center font-extrabold text-white text-lg">
        IT
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-lg font-bold tracking-tight text-slate-800">Intelligenz IT | TalentAssess 360™</h1>
          <span class="px-2 py-0.5 text-xs font-semibold bg-pink-50 text-pink-600 border border-pink-200 rounded-full">Material Suite</span>
        </div>
        <p class="text-xs text-slate-500">AI-Powered Assessment & Digital Recruitment Platform • Transforming Possibilities</p>
      </div>
    </div>

    <!-- Navigation Tabs (Material Style) -->
    <nav class="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
      <button onclick="switchTab('urls')" id="btn-tab-urls" class="px-3.5 py-2 rounded-lg font-bold transition floating-green text-white shadow flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
        🔗 Live System URLs
      </button>
      <button onclick="switchTab('mindmap')" id="btn-tab-mindmap" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-600 hover:text-slate-900 hover:bg-white">
        🌟 8-Pillar Mind Map
      </button>
      <button onclick="switchTab('architecture')" id="btn-tab-architecture" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-600 hover:text-slate-900 hover:bg-white">
        🏗️ System Architecture
      </button>
      <button onclick="switchTab('benefits')" id="btn-tab-benefits" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-600 hover:text-slate-900 hover:bg-white">
        💡 Benefits & Features
      </button>
      <button onclick="switchTab('wireframe')" id="btn-tab-wireframe" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-600 hover:text-slate-900 hover:bg-white flex items-center gap-1.5">
        📱 MarvelApp Wireframes
      </button>
      <button onclick="switchTab('dordod')" id="btn-tab-dordod" class="px-3.5 py-2 rounded-lg font-bold transition text-slate-600 hover:text-slate-900 hover:bg-white">
        📋 DoR & DoD
      </button>
    </nav>

    <!-- Executive Asset Links & Print -->
    <div class="flex items-center gap-2">
      <a href="file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_Executive_Dossier.docx" class="flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded-lg text-xs font-semibold transition" title="Open Executive Dossier in Microsoft Word">
        <span class="w-4 h-4 rounded bg-blue-600 flex items-center justify-center font-bold text-white text-[9px]">W</span>
        Word Dossier
      </a>
      <a href="file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_CEO.pptx" class="flex items-center gap-1.5 px-3 py-1.5 bg-orange-50 hover:bg-orange-100 text-orange-700 border border-orange-200 rounded-lg text-xs font-semibold transition" title="Open Presentation Deck in Microsoft PowerPoint">
        <span class="w-4 h-4 rounded bg-orange-600 flex items-center justify-center font-bold text-white text-[9px]">P</span>
        CEO Slide Deck
      </a>
      <button onclick="window.print()" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg border border-slate-300 transition">
        🖨️ Print
      </button>
    </div>
  </header>

  <!-- Pinned Quick Public & Local URL Banner -->
  <div class="no-print bg-white border-b border-slate-200/80 px-6 py-2.5 flex flex-wrap items-center justify-between text-xs gap-3 shadow-sm">
    <div class="flex flex-wrap items-center gap-3">
      <div class="flex items-center gap-1.5 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-lg">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
        <span class="text-slate-700 font-semibold">Public Internet URL:</span>
        <a href="https://popper-unrobed-cameo.ngrok-free.dev/mindmap/" target="_blank" class="text-emerald-700 font-mono font-bold hover:underline select-all">
          https://popper-unrobed-cameo.ngrok-free.dev/mindmap/
        </a>
      </div>
      <div class="flex items-center gap-1.5 bg-slate-100 border border-slate-200 px-3 py-1 rounded-lg">
        <span class="text-slate-500">Local Host:</span>
        <span class="text-slate-800 font-mono font-semibold">http://127.0.0.1:8080/</span>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <a href="https://popper-unrobed-cameo.ngrok-free.dev/dashboard/" target="_blank" class="px-3 py-1 floating-pink text-white rounded-lg font-bold transition flex items-center gap-1">
        📊 Public Admin Dashboard ➜
      </a>
      <a href="https://popper-unrobed-cameo.ngrok-free.dev/candidates/register/" target="_blank" class="px-3 py-1 floating-green text-white rounded-lg font-bold transition flex items-center gap-1">
        📝 Public Candidate Register ➜
      </a>
    </div>
  </div>

  <!-- TAB 1: LIVE SYSTEM URLS DIRECTORY (PROMINENT MATERIAL VIEW) -->
  <section id="tab-urls" class="flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-extrabold text-slate-800 flex items-center gap-2">
          <span>Live Platform URLs & Endpoints Directory</span>
          <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full border border-emerald-200">100% Operational (HTTP 200 OK)</span>
        </h2>
        <p class="text-xs text-slate-500">Click, copy, or launch any portal endpoint. Both Admin side and Candidate side routes are live on the internet.</p>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <span class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-slate-600 shadow-sm">
          Active Port: <strong class="text-pink-600 font-mono">8080 (Django 5)</strong>
        </span>
      </div>
    </div>

    <!-- Two-Column Cards: Admin Side vs Candidate Side -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      
      <!-- Card A: Admin & Internal Management URLs -->
      <div class="material-card p-6">
        <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 floating-pink text-white flex items-center justify-center font-bold text-sm">🛡️</div>
            <div>
              <h3 class="font-extrabold text-sm text-pink-600 uppercase tracking-wider">Admin & Internal Operations URLs</h3>
              <p class="text-[11px] text-slate-500">Governance, Evaluation, QR Drives & Role Management</p>
            </div>
          </div>
          <span class="px-2 py-0.5 bg-pink-50 text-pink-600 text-[10px] font-bold rounded border border-pink-200">ADMIN SIDE</span>
        </div>

        <div class="space-y-3 text-xs">
          
          <!-- URL 1: Admin Dashboard -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-pink-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>📊 Admin Dashboard</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/dashboard/" target="_blank" class="px-3 py-1 floating-pink text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-pink-600 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/dashboard/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/dashboard/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 2: Manage Candidates -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-pink-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>👥 Manage Candidates & PDF Dossiers</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/list/" target="_blank" class="px-3 py-1 floating-pink text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-pink-600 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/candidates/list/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/list/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 3: Test Results -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-pink-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>📈 Instant Test Results & Scoring Hub</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/results/" target="_blank" class="px-3 py-1 floating-pink text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-pink-600 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/results/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/results/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 4: Campus Drive QR Codes -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-pink-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>📱 Campus Placement QR Generator</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/qr/list/" target="_blank" class="px-3 py-1 floating-pink text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-pink-600 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/qr/list/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/qr/list/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 5: Manage Roles & RBAC -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-pink-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>🔐 Manage Roles (15-Module RBAC Permissions)</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/role_based_access/manage_roles/" target="_blank" class="px-3 py-1 floating-pink text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-pink-600 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/role_based_access/manage_roles/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/role_based_access/manage_roles/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

        </div>
      </div>

      <!-- Card B: Candidate & User Facing URLs -->
      <div class="material-card p-6">
        <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 floating-green text-white flex items-center justify-center font-bold text-sm">👤</div>
            <div>
              <h3 class="font-extrabold text-sm text-emerald-600 uppercase tracking-wider">Candidate & Public Facing URLs</h3>
              <p class="text-[11px] text-slate-500">Discovery, Onboarding, AI Camera Test & Exam Execution</p>
            </div>
          </div>
          <span class="px-2 py-0.5 bg-emerald-50 text-emerald-700 text-[10px] font-bold rounded border border-emerald-200">CANDIDATE SIDE</span>
        </div>

        <div class="space-y-3 text-xs">
          
          <!-- URL 1: Candidate Registration -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-emerald-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>📝 Candidate Registration Portal (Global Codes & PAN)</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/register/" target="_blank" class="px-3 py-1 floating-green text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-emerald-700 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/candidates/register/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/register/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 2: Candidate Login -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-emerald-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>🔑 Candidate Login Portal</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/login/" target="_blank" class="px-3 py-1 floating-green text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-emerald-700 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/candidates/login/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/login/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 3: Instructions & Camera Check -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-emerald-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>📋 Instructions & Webcam AI Proctor Handshake</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/instructions/GT/" target="_blank" class="px-3 py-1 floating-green text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-emerald-700 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/candidates/instructions/GT/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/instructions/GT/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 4: Candidate Dashboard -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-emerald-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>💻 Candidate Personal Dashboard</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/dashboard/" target="_blank" class="px-3 py-1 floating-green text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-emerald-700 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/candidates/dashboard/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/dashboard/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

          <!-- URL 5: Registration Success & 5-Star Feedback -->
          <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl hover:border-emerald-400 transition">
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-bold text-slate-800 flex items-center gap-1.5">
                <span>⭐ Registration Success & 5-Star Feedback</span>
                <span class="text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.2 rounded font-semibold">Active</span>
              </span>
              <a href="http://127.0.0.1:8080/candidates/registration-success/" target="_blank" class="px-3 py-1 floating-green text-white rounded font-semibold text-[11px] transition">
                Open ➜
              </a>
            </div>
            <div class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200">
              <code class="text-emerald-700 font-mono text-[11px] font-semibold select-all">http://127.0.0.1:8080/candidates/registration-success/</code>
              <button onclick="copyToClipboard('http://127.0.0.1:8080/candidates/registration-success/')" class="text-slate-500 hover:text-slate-800 text-[11px] font-semibold">Copy</button>
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- Presentation Files Direct Access -->
    <div class="material-card p-6">
      <h3 class="text-sm font-extrabold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-2">
        <span>📁 Local Presentation & Report Files (Downloads Folder)</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="p-4 bg-slate-50 border border-blue-200 rounded-xl flex items-center justify-between">
          <div>
            <strong class="text-blue-700 text-sm block">Microsoft Word Executive Dossier</strong>
            <code class="text-slate-500 text-[10px] block mt-0.5 select-all">file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_Executive_Dossier.docx</code>
          </div>
          <a href="file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_Executive_Dossier.docx" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg transition shadow">
            Open File
          </a>
        </div>
        <div class="p-4 bg-slate-50 border border-orange-200 rounded-xl flex items-center justify-between">
          <div>
            <strong class="text-orange-700 text-sm block">Microsoft PowerPoint CEO Slide Deck</strong>
            <code class="text-slate-500 text-[10px] block mt-0.5 select-all">file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_CEO.pptx</code>
          </div>
          <a href="file:///C:/Users/User/Downloads/Intelligenz_TalentAssess_360_CEO.pptx" class="px-3 py-1.5 bg-orange-600 hover:bg-orange-500 text-white font-bold rounded-lg transition shadow">
            Open File
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- TAB 2: 8-PILLAR BUSINESS MIND MAP (MATERIAL WHITE THEME) -->
  <section id="tab-mindmap" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-extrabold text-slate-800 flex items-center gap-2">
          <span>Exam Portal – Business Mind Map</span>
          <span class="text-xs font-semibold text-pink-600 bg-pink-50 px-2 py-0.5 rounded border border-pink-200">AI-Powered Platform</span>
        </h2>
        <p class="text-xs text-slate-500">Complete strategic alignment: Why, Who, What, How, Key Features, Where, When, and Business Benefits.</p>
      </div>
      <div class="text-xs text-slate-600 flex items-center gap-2 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-sm">
        <span>Vision:</span>
        <strong class="text-pink-600">Transforming Human Capital Acquisition with AI & Automation</strong>
      </div>
    </div>

    <!-- 8 Pillars Grid Layout -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      
      <!-- 1. WHY? (Pink) -->
      <div class="material-card p-5 relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-pink"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 floating-pink text-white flex items-center justify-center font-bold text-sm">🎯</div>
          <h3 class="font-extrabold text-sm text-pink-600 uppercase tracking-wide">1. WHY? Business Need</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-2">
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> Reduce manual recruitment effort</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> Faster and consistent hiring cycles</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> Standardized candidate assessments</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> Lower recruitment cost-per-hire</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> Better quality candidate shortlisting</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> Data-driven leadership decisions</li>
        </ul>
      </div>

      <!-- 2. WHO? (Purple) -->
      <div class="material-card p-5 relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-purple"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 floating-purple text-white flex items-center justify-center font-bold text-sm">👥</div>
          <h3 class="font-extrabold text-sm text-purple-700 uppercase tracking-wide">2. WHO? Stakeholders</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-2">
          <li class="flex items-center gap-2"><span class="text-purple-600 font-bold">👤</span> Candidates (Students & Pros)</li>
          <li class="flex items-center gap-2"><span class="text-purple-600 font-bold">👤</span> Recruiters & HR Talent Teams</li>
          <li class="flex items-center gap-2"><span class="text-purple-600 font-bold">👤</span> Technical Hiring Managers</li>
          <li class="flex items-center gap-2"><span class="text-purple-600 font-bold">👤</span> System Administrators (RBAC)</li>
          <li class="flex items-center gap-2"><span class="text-purple-600 font-bold">👤</span> Executive Leadership & C-Suite</li>
        </ul>
      </div>

      <!-- 3. WHAT? (Blue) -->
      <div class="material-card p-5 relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-blue"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 floating-blue text-white flex items-center justify-center font-bold text-sm">⚙️</div>
          <h3 class="font-extrabold text-sm text-blue-700 uppercase tracking-wide">3. WHAT? Capabilities</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-2">
          <li class="flex items-center gap-2"><span class="text-blue-500 font-bold">⚙</span> Job requisitions & approval gates</li>
          <li class="flex items-center gap-2"><span class="text-blue-500 font-bold">⚙</span> Candidate registration & profiles</li>
          <li class="flex items-center gap-2"><span class="text-blue-500 font-bold">⚙</span> Document upload & PAN check</li>
          <li class="flex items-center gap-2"><span class="text-blue-500 font-bold">⚙</span> 2-Tier tests (General + Technical)</li>
          <li class="flex items-center gap-2"><span class="text-blue-500 font-bold">⚙</span> AI-enabled proctoring & anti-cheat</li>
          <li class="flex items-center gap-2"><span class="text-blue-500 font-bold">⚙</span> Candidate tracking & evaluations</li>
          <li class="flex items-center gap-2"><span class="text-blue-500 font-bold">⚙</span> Offer management & onboarding</li>
        </ul>
      </div>

      <!-- 4. HOW? (Orange) -->
      <div class="material-card p-5 relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-orange"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 floating-orange text-white flex items-center justify-center font-bold text-sm">🛠️</div>
          <h3 class="font-extrabold text-sm text-orange-600 uppercase tracking-wide">4. HOW? Process</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-2">
          <li class="flex items-center gap-2"><span class="text-orange-500 font-bold">⚡</span> Responsive web portal (Bootstrap)</li>
          <li class="flex items-center gap-2"><span class="text-orange-500 font-bold">⚡</span> Structured multi-step workflows</li>
          <li class="flex items-center gap-2"><span class="text-orange-500 font-bold">⚡</span> Real-time AI vision (Camera/Tab/Screen)</li>
          <li class="flex items-center gap-2"><span class="text-orange-500 font-bold">⚡</span> Secure authentication & RBAC access</li>
          <li class="flex items-center gap-2"><span class="text-orange-500 font-bold">⚡</span> Indexed MySQL database core</li>
          <li class="flex items-center gap-2"><span class="text-orange-500 font-bold">⚡</span> Cloud or on-premise containerization</li>
          <li class="flex items-center gap-2"><span class="text-orange-500 font-bold">⚡</span> Integration with Odoo ERP (HR/Payroll)</li>
        </ul>
      </div>

      <!-- 5. KEY FEATURES (Teal) -->
      <div class="material-card p-5 relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-teal"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 floating-teal text-white flex items-center justify-center font-bold text-sm">⭐</div>
          <h3 class="font-extrabold text-sm text-teal-700 uppercase tracking-wide">5. KEY FEATURES</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-2">
          <li class="flex items-center gap-2"><span class="text-teal-600 font-bold">★</span> Online proctored assessments</li>
          <li class="flex items-center gap-2"><span class="text-teal-600 font-bold">★</span> Intelligent candidate ranking engine</li>
          <li class="flex items-center gap-2"><span class="text-teal-600 font-bold">★</span> Bilingual portal (Arabic & English)</li>
          <li class="flex items-center gap-2"><span class="text-teal-600 font-bold">★</span> Applicant Tracking System (ATS)</li>
          <li class="flex items-center gap-2"><span class="text-teal-600 font-bold">★</span> Dynamic question randomization & timers</li>
          <li class="flex items-center gap-2"><span class="text-teal-600 font-bold">★</span> Granular 15-module permission RBAC</li>
          <li class="flex items-center gap-2"><span class="text-teal-600 font-bold">★</span> Direct integration with Odoo ERP</li>
        </ul>
      </div>

      <!-- 6. WHERE? (Dark Slate) -->
      <div class="material-card p-5 relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-dark"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 floating-dark text-white flex items-center justify-center font-bold text-sm">📍</div>
          <h3 class="font-extrabold text-sm text-slate-800 uppercase tracking-wide">6. WHERE? Channels</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-2">
          <li class="flex items-center gap-2"><span class="text-slate-800 font-bold">📍</span> Company official careers portal</li>
          <li class="flex items-center gap-2"><span class="text-slate-800 font-bold">📍</span> LinkedIn & Naukri applicant pipelines</li>
          <li class="flex items-center gap-2"><span class="text-slate-800 font-bold">📍</span> Dynamic QR campaigns (Campus drives)</li>
          <li class="flex items-center gap-2"><span class="text-slate-800 font-bold">📍</span> Corporate website & intranet integration</li>
          <li class="flex items-center gap-2"><span class="text-slate-800 font-bold">📍</span> Cloud (AWS / Azure) or Secure On-Premise</li>
          <li class="flex items-center gap-2"><span class="text-slate-800 font-bold">📍</span> Deployed across GCC, Middle East & India</li>
        </ul>
      </div>

      <!-- 7. WHEN? (Blue/Indigo) -->
      <div class="material-card p-5 relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-blue"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 floating-blue text-white flex items-center justify-center font-bold text-sm">📅</div>
          <h3 class="font-extrabold text-sm text-blue-700 uppercase tracking-wide">7. WHEN? Scenarios</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-2">
          <li class="flex items-center gap-2"><span class="text-blue-600 font-bold">📅</span> Mass campus placement drives</li>
          <li class="flex items-center gap-2"><span class="text-blue-600 font-bold">📅</span> Bulk hiring (50,000+ applicants at scale)</li>
          <li class="flex items-center gap-2"><span class="text-blue-600 font-bold">📅</span> Lateral engineering & domain hiring</li>
          <li class="flex items-center gap-2"><span class="text-blue-600 font-bold">📅</span> Graduate & fresher trainee recruitment</li>
          <li class="flex items-center gap-2"><span class="text-blue-600 font-bold">📅</span> Ongoing talent & periodic skill assessments</li>
        </ul>
      </div>

      <!-- 8. BENEFITS (Green) -->
      <div class="material-card p-5 relative overflow-hidden group">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-green"></div>
        <div class="flex items-center gap-2.5 mb-3">
          <div class="w-8 h-8 floating-green text-white flex items-center justify-center font-bold text-sm">📈</div>
          <h3 class="font-extrabold text-sm text-emerald-700 uppercase tracking-wide">8. BENEFITS Outcomes</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-2">
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> 50,000+ candidates handled without lag</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> 100% test integrity (Zero proxy cheaters)</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> 85% reduction in engineering hours</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> 70% decrease in overall cost-per-hire</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> Premium candidate UX & 5-star brand trust</li>
          <li class="flex items-center gap-2"><span class="text-emerald-500 font-bold">✔</span> Seamless ERP/HR data synchronization</li>
        </ul>
      </div>

    </div>

    <!-- Central Branding Footer -->
    <div class="mt-8 text-center p-6 material-card flex flex-col items-center justify-center">
      <div class="w-12 h-12 rounded-full floating-pink flex items-center justify-center text-xl text-white mb-2">🎓</div>
      <h3 class="text-lg font-bold text-slate-800">Intelligenz IT | TalentAssess 360™</h3>
      <p class="text-xs text-pink-600 font-semibold uppercase tracking-wider mt-0.5">Hire Smarter • Assess Fairer • Build Stronger Teams</p>
      <p class="text-xs text-slate-500 max-w-xl mt-2">
        An enterprise assessment and talent acquisition cloud engineered with Edge AI proctoring, 15-module administration, and frictionless candidate experiences.
      </p>
    </div>
  </section>

  <!-- TAB 3: TECHNICAL ARCHITECTURE -->
  <section id="tab-architecture" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6">
      <h2 class="text-xl font-extrabold text-slate-800 flex items-center gap-2">
        <span>End-to-End Workflow & Technical Architecture</span>
        <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-200">Discovery to Onboarding</span>
      </h2>
      <p class="text-xs text-slate-500">Three-tier architectural overview: Candidate Journey, System Topology, and 14 Admin Command Modules.</p>
    </div>

    <!-- SECTION A: Candidate Journey (8 Stages) -->
    <div class="mb-8 material-card p-6">
      <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
        <h3 class="text-sm font-extrabold text-pink-600 uppercase tracking-wider flex items-center gap-2">
          <span>A. Candidate Journey (External Users)</span>
        </h3>
        <span class="text-[11px] font-semibold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-full">Simple • Secure • Seamless</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full floating-pink text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">1</span>
          <h4 class="font-bold text-xs text-slate-800">Find Opportunity</h4>
          <p class="text-[10px] text-slate-500 mt-1">LinkedIn, Naukri, Careers page, QR code</p>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full floating-pink text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">2</span>
          <h4 class="font-bold text-xs text-slate-800">Registration</h4>
          <p class="text-[10px] text-slate-500 mt-1">PAN authentication, global dial codes, doc upload</p>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full floating-pink text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">3</span>
          <h4 class="font-bold text-xs text-slate-800">Success & Email</h4>
          <p class="text-[10px] text-slate-500 mt-1">Confirmation screen & automated status email</p>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full floating-pink text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">4</span>
          <h4 class="font-bold text-xs text-slate-800">Login</h4>
          <p class="text-[10px] text-slate-500 mt-1">Secure login via Reg ID & credentials</p>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full floating-pink text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">5</span>
          <h4 class="font-bold text-xs text-slate-800">Profile Review</h4>
          <p class="text-[10px] text-slate-500 mt-1">Check profile details & qualification fields</p>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full floating-pink text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">6</span>
          <h4 class="font-bold text-xs text-slate-800">Instructions & Camera</h4>
          <p class="text-[10px] text-slate-500 mt-1">Accept rules & run live webcam check</p>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full floating-pink text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">7</span>
          <h4 class="font-bold text-xs text-slate-800">Take Test</h4>
          <p class="text-[10px] text-slate-500 mt-1">Round 1 General Aptitude -> Round 2 Technical</p>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
          <span class="w-6 h-6 rounded-full floating-pink text-white font-bold text-xs flex items-center justify-center mx-auto mb-2">8</span>
          <h4 class="font-bold text-xs text-slate-800">Completion</h4>
          <p class="text-[10px] text-slate-500 mt-1">5-star rating, auto-scoring & result email</p>
        </div>
      </div>
    </div>

    <!-- SECTION B: System Architecture (High-Level) -->
    <div class="mb-8 material-card p-6">
      <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
        <h3 class="text-sm font-extrabold text-blue-600 uppercase tracking-wider flex items-center gap-2">
          <span>B. High-Level System Topology & Integrations</span>
        </h3>
        <span class="text-[11px] font-semibold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-full">Django 5 • MySQL • Edge AI • Odoo ERP</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <!-- Left: Client Devices & Security Services -->
        <div class="space-y-4">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
            <h4 class="text-xs font-bold text-blue-600 uppercase mb-2 flex items-center gap-1.5">💻 Candidate Devices (Browser)</h4>
            <ul class="text-xs text-slate-600 space-y-1.5">
              <li>• Desktop / Laptop (Chrome, Edge, Firefox)</li>
              <li>• Mobile / Tablet (Responsive Web UI)</li>
              <li>• Webcam: Live Camera Check & Stream</li>
              <li>• Geolocation & IP Network Verification</li>
            </ul>
          </div>

          <div class="bg-slate-50 border border-orange-200 rounded-xl p-4">
            <h4 class="text-xs font-bold text-orange-600 uppercase mb-2 flex items-center gap-1.5">🛡️ Security & Proctoring Shield</h4>
            <ul class="text-xs text-slate-600 space-y-1.5">
              <li>• Coco-SSD Face Tracking (Browser Edge AI)</li>
              <li>• Multi-Person Detection & Cubicle Noise Filter</li>
              <li>• Tab-Switching & ChatGPT Lockout</li>
              <li>• Dual-Monitor & Display Extension Defense</li>
              <li>• DevTools (F12) & Clipboard (Copy/Paste) Lock</li>
            </ul>
          </div>
        </div>

        <!-- Center: Django Web Application Core -->
        <div class="bg-slate-50 border border-pink-200 rounded-xl p-4 flex flex-col justify-between">
          <div>
            <h4 class="text-xs font-bold text-pink-600 uppercase mb-3 flex items-center gap-1.5">🐍 Web Application Layer (Django / Python)</h4>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="p-2 bg-white border border-slate-200 rounded-lg shadow-sm">
                <strong class="text-slate-800 block">Auth & Users</strong>
                <span class="text-[10px] text-slate-500">Profile & Credentials</span>
              </div>
              <div class="p-2 bg-white border border-slate-200 rounded-lg shadow-sm">
                <strong class="text-slate-800 block">Exam Dashboard</strong>
                <span class="text-[10px] text-slate-500">Test Execution</span>
              </div>
              <div class="p-2 bg-white border border-slate-200 rounded-lg shadow-sm">
                <strong class="text-slate-800 block">Question Bank</strong>
                <span class="text-[10px] text-slate-500">Randomized MCQs</span>
              </div>
              <div class="p-2 bg-white border border-slate-200 rounded-lg shadow-sm">
                <strong class="text-slate-800 block">Role Access</strong>
                <span class="text-[10px] text-slate-500">15-Module RBAC</span>
              </div>
              <div class="p-2 bg-white border border-slate-200 rounded-lg shadow-sm">
                <strong class="text-slate-800 block">Email Scheduler</strong>
                <span class="text-[10px] text-slate-500">Automated Alerts</span>
              </div>
              <div class="p-2 bg-white border border-slate-200 rounded-lg shadow-sm">
                <strong class="text-slate-800 block">QR Generator</strong>
                <span class="text-[10px] text-slate-500">Campus Drives</span>
              </div>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-slate-200">
            <h5 class="text-[11px] font-bold text-emerald-700 uppercase mb-1">🗄️ Database & Storage Layer</h5>
            <p class="text-xs text-slate-600">
              Enterprise MySQL with indexation (<code class="text-pink-600 font-semibold">db_index=True</code>) and server-side pagination (<code class="text-pink-600 font-semibold">Paginator 50</code>) supporting 50,000+ candidates with sub-second queries.
            </p>
          </div>
        </div>

        <!-- Right: External Integrations & DevOps -->
        <div class="space-y-4">
          <div class="bg-slate-50 border border-purple-200 rounded-xl p-4">
            <h4 class="text-xs font-bold text-purple-700 uppercase mb-2 flex items-center gap-1.5">🔗 External Integrations</h4>
            <ul class="text-xs text-slate-600 space-y-1.5">
              <li>• <strong>Email Service:</strong> SMTP / SendGrid Automation</li>
              <li>• <strong>Job Sources:</strong> LinkedIn & Naukri Portals</li>
              <li>• <strong>Odoo ERP:</strong> HR, Payroll & Onboarding Sync</li>
              <li>• <strong>Corporate Careers:</strong> Embeddable Iframe / API</li>
            </ul>
          </div>

          <div class="bg-slate-50 border border-indigo-200 rounded-xl p-4">
            <h4 class="text-xs font-bold text-indigo-700 uppercase mb-2 flex items-center gap-1.5">🚀 Infrastructure & DevOps</h4>
            <ul class="text-xs text-slate-600 space-y-1.5">
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
    <div class="material-card p-6">
      <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
        <h3 class="text-sm font-extrabold text-emerald-700 uppercase tracking-wider flex items-center gap-2">
          <span>C. Admin / HR Workflow (14 Management Modules)</span>
        </h3>
        <span class="text-[11px] font-semibold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-full">End-to-End Governance</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-7 gap-3 text-xs">
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-pink-600 font-bold block mb-1">01. Dashboard</span>
          <p class="text-[10px] text-slate-500">Live test funnel & department metrics</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-pink-600 font-bold block mb-1">02. Candidates</span>
          <p class="text-[10px] text-slate-500">Profiles, search & 1-click PDF dossiers</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-pink-600 font-bold block mb-1">03. Manage Tests</span>
          <p class="text-[10px] text-slate-500">Test blueprints, durations & cutoffs</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-pink-600 font-bold block mb-1">04. Question Bank</span>
          <p class="text-[10px] text-slate-500">Tagged MCQs & programming challenges</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-pink-600 font-bold block mb-1">05. Invites</span>
          <p class="text-[10px] text-slate-500">Batch invitations & tokenized test links</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-pink-600 font-bold block mb-1">06. Monitor AI</span>
          <p class="text-[10px] text-slate-500">Live proctoring & violation audits</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-pink-600 font-bold block mb-1">07. Results</span>
          <p class="text-[10px] text-slate-500">Instant auto-scoring & merit ranks</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-blue-600 font-bold block mb-1">08. Instructions</span>
          <p class="text-[10px] text-slate-500">Pre-exam compliance guidelines</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-blue-600 font-bold block mb-1">09. Manage QR</span>
          <p class="text-[10px] text-slate-500">Rapid campus drive QR generation</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-blue-600 font-bold block mb-1">10. Email Builder</span>
          <p class="text-[10px] text-slate-500">Custom branded HTML communications</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-blue-600 font-bold block mb-1">11. Role RBAC</span>
          <p class="text-[10px] text-slate-500">15 toggleable permissions per user</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-blue-600 font-bold block mb-1">12. Configuration</span>
          <p class="text-[10px] text-slate-500">System parameters & passing marks</p>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl">
          <span class="text-blue-600 font-bold block mb-1">13. Analytics</span>
          <p class="text-[10px] text-slate-500">Hiring throughput & cohort insights</p>
        </div>
        <div class="p-3 bg-slate-50 border border-emerald-300 rounded-xl">
          <span class="text-emerald-700 font-bold block mb-1">14. Odoo Onboard</span>
          <p class="text-[10px] text-slate-500">Offer generation & contract sync</p>
        </div>
      </div>
    </div>
  </section>

  <!-- TAB 4: BENEFITS, ADVANTAGES & FEATURES EXPLANATION -->
  <section id="tab-benefits" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6">
      <h2 class="text-xl font-extrabold text-slate-800 flex items-center gap-2">
        <span>Strategic Value: Benefits, Advantages & Features</span>
        <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-200">Executive Deep-Dive</span>
      </h2>
      <p class="text-xs text-slate-500">Clear breakdown of tangible business outcomes, competitive advantages over 3rd-party SaaS, and technical features.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- Card 1: BENEFITS (Business Outcomes) -->
      <div class="material-card p-6 relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-green"></div>
        <div class="flex items-center gap-2.5 mb-4">
          <span class="w-8 h-8 floating-green text-white flex items-center justify-center font-bold text-sm">📈</span>
          <h3 class="text-base font-extrabold text-emerald-700 uppercase tracking-wider">Benefits (What You Gain)</h3>
        </div>
        <p class="text-xs text-slate-500 mb-4 leading-relaxed">
          Measurable commercial, operational, and financial returns achieved by transitioning to TalentAssess 360.
        </p>
        <ul class="text-xs text-slate-600 space-y-3">
          <li class="flex items-start gap-2">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>85% Reduction in Engineering Hours:</strong> Reclaims 300+ billable senior developer hours monthly by automating Rounds 1 & 2.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>70% Drop in Cost-Per-Hire:</strong> Eliminates recurring test vendor fees, third-party proctoring markups, and recruiter coordination waste.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Zero-Latency Assessment Delivery:</strong> 50,000+ candidates can register and test in parallel with sub-second page loads.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Instant Campus Placement Throughput:</strong> Test thousands of college students in under 3 hours with automatic results ready for same-day interviews.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Elevated Candidate Trust & UX:</strong> Clean, responsive UI with interactive 5-star feedback and automated branded emails.</div>
          </li>
        </ul>
      </div>

      <!-- Card 2: ADVANTAGES (Why It Beats Competitors) -->
      <div class="material-card p-6 relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-blue"></div>
        <div class="flex items-center gap-2.5 mb-4">
          <span class="w-8 h-8 floating-blue text-white flex items-center justify-center font-bold text-sm">🏆</span>
          <h3 class="text-base font-extrabold text-blue-700 uppercase tracking-wider">Advantages (Competitive Edge)</h3>
        </div>
        <p class="text-xs text-slate-500 mb-4 leading-relaxed">
          Why our proprietary platform decisively outperforms external SaaS vendors like HackerRank, Mercer Mettl, or Codility.
        </p>
        <ul class="text-xs text-slate-600 space-y-3">
          <li class="flex items-start gap-2">
            <span class="text-blue-500 font-bold mt-0.5">★</span>
            <div><strong>Zero Cloud GPU Streaming Cost:</strong> Coco-SSD vision AI runs directly inside the candidate's browser, eliminating massive AWS/GCP GPU streaming bills.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-blue-500 font-bold mt-0.5">★</span>
            <div><strong>100% In-House Intellectual Property:</strong> No annual license fees ($15,000–$25,000 saved per year); all candidate data and question banks remain strictly confidential.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-blue-500 font-bold mt-0.5">★</span>
            <div><strong>Cubicle Noise Filter:</strong> Distinguishes actual proxy test-takers from background office colleagues walking across open cubicles.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-blue-500 font-bold mt-0.5">★</span>
            <div><strong>Bilingual Middle East & GCC Readiness:</strong> Built-in dual-language support (Arabic & English) with direct Odoo ERP integration.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-blue-500 font-bold mt-0.5">★</span>
            <div><strong>Zero N+1 Query Architecture:</strong> Indexed relational schema ensuring smooth execution across millions of assessment queries.</div>
          </li>
        </ul>
      </div>

      <!-- Card 3: FEATURES (Platform Capabilities) -->
      <div class="material-card p-6 relative overflow-hidden">
        <div class="absolute top-0 left-0 right-0 h-1.5 floating-pink"></div>
        <div class="flex items-center gap-2.5 mb-4">
          <span class="w-8 h-8 floating-pink text-white flex items-center justify-center font-bold text-sm">⚡</span>
          <h3 class="text-base font-extrabold text-pink-600 uppercase tracking-wider">Features (What's Built-In)</h3>
        </div>
        <p class="text-xs text-slate-500 mb-4 leading-relaxed">
          Comprehensive inventory of functional and technical capabilities powering the candidate and recruiter portals.
        </p>
        <ul class="text-xs text-slate-600 space-y-3">
          <li class="flex items-start gap-2">
            <span class="text-pink-500 font-bold mt-0.5">⚙</span>
            <div><strong>2-Tier Automated Testing:</strong> Round 1 General Cognitive (Aptitude/Logic) + Round 2 Technical Coding/MCQs.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-pink-500 font-bold mt-0.5">⚙</span>
            <div><strong>Multi-Vector Anti-Cheat Shield:</strong> Webcam tracking, tab-switching lockout, dual-monitor lockout, and clipboard/F12 lock.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-pink-500 font-bold mt-0.5">⚙</span>
            <div><strong>Global Onboarding:</strong> 240+ international dial codes, 10-digit alphanumeric PAN verification, and adaptive % vs CGPA logic.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-pink-500 font-bold mt-0.5">⚙</span>
            <div><strong>14-Module Admin Command Hub:</strong> Granular RBAC, test compilers, question bank taxonomy, and live candidate tracking.</div>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-pink-500 font-bold mt-0.5">⚙</span>
            <div><strong>1-Click Candidate Dossiers:</strong> Verified candidate PDF portfolios with test scores, photos, feedback, and hiring recommendations.</div>
          </li>
        </ul>
      </div>

    </div>
  </section>

  <!-- TAB 5: MARVELAPP-STYLE INTERACTIVE CLICKABLE WIREFRAME PROTOTYPE (MATERIAL THEME) -->
  <section id="tab-wireframe" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-extrabold text-slate-800 flex items-center gap-2">
          <span>MarvelApp-Style Interactive Clickable Prototype</span>
          <span class="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-200">All Buttons Active</span>
        </h2>
        <p class="text-xs text-slate-500">Click anywhere inside the device frame to interact with the screens, test validations, and launch live endpoints.</p>
      </div>

      <!-- Mode Switcher: Candidate vs Admin -->
      <div class="flex items-center gap-2 bg-white p-1 rounded-xl border border-slate-200 shadow-sm text-xs">
        <button onclick="setWireframePerspective('candidate')" id="btn-wf-cand" class="px-3.5 py-1.5 rounded-lg font-bold transition text-slate-600 hover:text-slate-900">
          Candidate Side (External)
        </button>
        <button onclick="setWireframePerspective('admin')" id="btn-wf-admin" class="px-3.5 py-1.5 rounded-lg font-bold transition floating-pink text-white">
          Admin Side (Internal)
        </button>
      </div>
    </div>

    <!-- Interactive MarvelApp Device Wrapper (Material Clean Surface) -->
    <div class="material-card p-4 sm:p-8 relative">
      
      <!-- Device Top Bar / Browser Shell -->
      <div class="bg-slate-100 border border-slate-200 rounded-2xl p-3 mb-6 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-rose-500"></span>
          <span class="w-3 h-3 rounded-full bg-amber-500"></span>
          <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
          <span id="wf-url-bar" class="ml-3 px-3 py-1 bg-white rounded-md text-[11px] text-slate-700 font-mono font-semibold border border-slate-200 shadow-sm">
            http://127.0.0.1:8080/dashboard/
          </span>
        </div>
        <div class="flex items-center gap-2">
          <a id="wf-live-btn" href="http://127.0.0.1:8080/dashboard/" target="_blank" class="px-3 py-1 floating-pink text-white rounded text-[11px] font-semibold transition">
            🔗 Launch in Live Server
          </a>
        </div>
      </div>

      <!-- Admin Side Screens (Default) -->
      <div id="perspective-admin" class="wireframe-screen">
        
        <!-- Admin Sub-Navigation -->
        <div class="flex flex-wrap items-center gap-2 mb-6 border-b border-slate-200 pb-3 text-xs">
          <button onclick="showAdminScreen('dash')" id="btn-adm-dash" class="px-3 py-1.5 rounded-lg font-semibold floating-pink text-white">1. Admin Dashboard</button>
          <button onclick="showAdminScreen('cand')" id="btn-adm-cand" class="px-3 py-1.5 rounded-lg font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100">2. Candidate List & PDF</button>
          <button onclick="showAdminScreen('res')" id="btn-adm-res" class="px-3 py-1.5 rounded-lg font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100">3. Test Results Hub</button>
          <button onclick="showAdminScreen('qr')" id="btn-adm-qr" class="px-3 py-1.5 rounded-lg font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100">4. QR Code Generator</button>
        </div>

        <!-- Admin Screen 1: Dashboard (Matching User Image 2 with Floating Colored Badges) -->
        <div id="scr-admin-dash" class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          
          <!-- Top 4 Floating Stat Cards (Replicating Screenshot Exactly) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 pt-2">
            
            <!-- Stat 1: Total Users (Pink Floating Badge) -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-4 shadow-md relative pt-6">
              <div class="w-12 h-12 floating-pink text-white flex items-center justify-center text-xl absolute -top-4 left-4">
                👥
              </div>
              <div class="text-right">
                <span class="text-xs text-slate-500 font-semibold uppercase">Total Users</span>
                <h4 class="text-2xl font-extrabold text-slate-800 mt-0.5">5</h4>
              </div>
            </div>

            <!-- Stat 2: Total Questions (Dark Slate Floating Badge) -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-4 shadow-md relative pt-6">
              <div class="w-12 h-12 floating-dark text-white flex items-center justify-center text-xl absolute -top-4 left-4">
                💬
              </div>
              <div class="text-right">
                <span class="text-xs text-slate-500 font-semibold uppercase">Total Questions</span>
                <h4 class="text-2xl font-extrabold text-slate-800 mt-0.5">104</h4>
              </div>
            </div>

            <!-- Stat 3: Total Tests (Green Floating Badge) -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-4 shadow-md relative pt-6">
              <div class="w-12 h-12 floating-green text-white flex items-center justify-center text-xl absolute -top-4 left-4">
                📋
              </div>
              <div class="text-right">
                <span class="text-xs text-slate-500 font-semibold uppercase">Total Tests</span>
                <h4 class="text-2xl font-extrabold text-slate-800 mt-0.5">4</h4>
              </div>
            </div>

            <!-- Stat 4: Pass Percentage (Blue Floating Badge) -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-4 shadow-md relative pt-6">
              <div class="w-12 h-12 floating-blue text-white flex items-center justify-center text-xl absolute -top-4 left-4">
                📊
              </div>
              <div class="text-right">
                <span class="text-xs text-slate-500 font-semibold uppercase">Pass Percentage</span>
                <h4 class="text-2xl font-extrabold text-slate-800 mt-0.5">0.0%</h4>
              </div>
            </div>

          </div>

          <!-- 3 Colored Graph Cards (Matching User Image 2 Below the Stats) -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            
            <!-- Graph 1: General Test (Pink Header) -->
            <div class="bg-white border border-slate-200 rounded-2xl shadow-md overflow-hidden">
              <div class="floating-pink h-36 m-3 rounded-xl p-3 flex flex-col justify-between text-white">
                <div class="flex justify-between items-center text-[11px] opacity-80">
                  <span>General Test Analytics</span>
                  <span>Live</span>
                </div>
                <div class="flex items-end justify-around h-20 px-4">
                  <div class="w-2 bg-white rounded-t h-14"></div>
                  <div class="w-2 bg-white/40 rounded-t h-2"></div>
                  <div class="w-2 bg-white rounded-t h-14"></div>
                </div>
                <div class="flex justify-around text-[9px] opacity-90 font-semibold">
                  <span>Attended</span>
                  <span>Qualified</span>
                  <span>Not Qualified</span>
                </div>
              </div>
              <div class="p-4 pt-1">
                <h5 class="text-xs font-bold text-slate-800">General Test: Attended vs Qualified</h5>
                <p class="text-[10px] text-slate-500 mt-0.5">Cognitive aptitude & verbal benchmark</p>
              </div>
            </div>

            <!-- Graph 2: Technical Test (Orange Header) -->
            <div class="bg-white border border-slate-200 rounded-2xl shadow-md overflow-hidden">
              <div class="floating-orange h-36 m-3 rounded-xl p-3 flex flex-col justify-between text-white">
                <div class="flex justify-between items-center text-[11px] opacity-80">
                  <span>Technical Test Analytics</span>
                  <span>Live</span>
                </div>
                <div class="flex items-center justify-center h-20 text-xs opacity-75">
                  No Data Yet
                </div>
                <div class="flex justify-around text-[9px] opacity-90 font-semibold">
                  <span>Attended</span>
                  <span>Qualified</span>
                  <span>Not Qualified</span>
                </div>
              </div>
              <div class="p-4 pt-1">
                <h5 class="text-xs font-bold text-slate-800">Technical Test: Attended vs Qualified</h5>
                <p class="text-[10px] text-slate-500 mt-0.5">Domain coding & technical concepts</p>
              </div>
            </div>

            <!-- Graph 3: Skills of Candidates (Green Header) -->
            <div class="bg-white border border-slate-200 rounded-2xl shadow-md overflow-hidden">
              <div class="floating-green h-36 m-3 rounded-xl p-3 flex flex-col justify-between text-white">
                <div class="flex justify-between items-center text-[11px]">
                  <span>Skill Distribution</span>
                  <span class="bg-white/20 px-2 py-0.5 rounded text-[10px]">All ▼</span>
                </div>
                <div class="flex items-center justify-center h-20 text-xs opacity-75">
                  No Data Yet
                </div>
                <div class="text-[9px] opacity-80 text-center">Skill Matrix</div>
              </div>
              <div class="p-4 pt-1">
                <h5 class="text-xs font-bold text-slate-800">Skills of Qualified Candidates</h5>
                <p class="text-[10px] text-slate-500 mt-0.5">AI, Python, Cloud, QA breakdown</p>
              </div>
            </div>

          </div>

          <div class="flex justify-between items-center text-xs pt-2 border-t border-slate-100">
            <span class="text-slate-500">© Intelligenz IT • All 14 modules operational.</span>
            <a href="http://127.0.0.1:8080/dashboard/" target="_blank" class="px-4 py-2 floating-pink text-white font-bold rounded-lg transition shadow">
              Open Full Live Dashboard (Port 8080) ➜
            </a>
          </div>
        </div>

        <!-- Admin Screen 2: Candidate List -->
        <div id="scr-admin-cand" class="hidden bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-extrabold text-slate-800">Manage Candidates (50,000+ Indexed Records)</h3>
            <a href="http://127.0.0.1:8080/candidates/list/" target="_blank" class="text-xs text-pink-600 hover:underline font-semibold">Launch Live /candidates/list/</a>
          </div>

          <table class="w-full text-xs text-left">
            <thead class="bg-slate-50 text-slate-600 border-b border-slate-200">
              <tr>
                <th class="p-2.5">Reg ID</th>
                <th class="p-2.5">Candidate Name</th>
                <th class="p-2.5">PAN Number</th>
                <th class="p-2.5">Status</th>
                <th class="p-2.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-slate-700">
              <tr>
                <td class="p-2.5 font-mono text-pink-600 font-bold">REG-2026-INTITIN000005</td>
                <td class="p-2.5 font-semibold text-slate-800">Nagendra Panda</td>
                <td class="p-2.5 font-mono">ABCDE1234F</td>
                <td class="p-2.5"><span class="px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded-full text-[10px] font-semibold">Test Completed</span></td>
                <td class="p-2.5 text-right">
                  <a href="http://127.0.0.1:8080/candidates/pdf/5/" target="_blank" class="px-2.5 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded hover:bg-blue-600 hover:text-white transition font-semibold">
                    📄 Export PDF Dossier
                  </a>
                </td>
              </tr>
              <tr>
                <td class="p-2.5 font-mono text-pink-600 font-bold">REG-2026-INTITIN000004</td>
                <td class="p-2.5 font-semibold text-slate-800">Rahul Verma</td>
                <td class="p-2.5 font-mono">BCDEF2345G</td>
                <td class="p-2.5"><span class="px-2 py-0.5 bg-sky-100 text-sky-700 rounded-full text-[10px] font-semibold">Registered</span></td>
                <td class="p-2.5 text-right">
                  <span class="text-slate-400 text-[11px]">Pending Exam</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Admin Screen 3: Test Results -->
        <div id="scr-admin-res" class="hidden bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-sm font-extrabold text-slate-800">Real-Time Test Results & Auto-Scoring Hub</h3>
            <a href="http://127.0.0.1:8080/results/" target="_blank" class="text-xs text-pink-600 hover:underline font-semibold">Launch Live /results/</a>
          </div>

          <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs space-y-3">
            <div class="flex items-center justify-between p-3 bg-white rounded-lg border border-slate-200 shadow-sm">
              <div>
                <strong class="text-slate-800 block">Nagendra Panda (General Test)</strong>
                <span class="text-slate-500 text-[11px]">Score: 16/20 (80.0%) • Status: <span class="text-emerald-600 font-bold">PASSED</span></span>
              </div>
              <a href="http://127.0.0.1:8080/results/" target="_blank" class="px-3 py-1 floating-green text-white rounded font-semibold text-[11px]">
                Review Submission
              </a>
            </div>
          </div>
        </div>

        <!-- Admin Screen 4: QR Code Generator -->
        <div id="scr-admin-qr" class="hidden bg-white border border-slate-200 rounded-2xl p-6 text-center max-w-md mx-auto shadow-sm">
          <h3 class="text-sm font-extrabold text-slate-800 mb-1">Campus Placement QR Generator</h3>
          <p class="text-xs text-slate-500 mb-4">Project this QR code on auditorium screens for instant candidate onboarding.</p>

          <div class="bg-white p-4 rounded-xl inline-block shadow-md border border-slate-200 mb-4">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=http://127.0.0.1:8080/candidates/register/" alt="QR" class="w-36 h-36">
          </div>

          <div class="flex justify-center gap-2 text-xs">
            <a href="http://127.0.0.1:8080/qr/list/" target="_blank" class="px-4 py-2 floating-pink text-white font-bold rounded-lg transition shadow">
              Manage All QR Campaigns (Port 8080)
            </a>
          </div>
        </div>

      </div>

      <!-- Candidate Side Screens -->
      <div id="perspective-candidate" class="hidden wireframe-screen">
        
        <!-- Step Navigation Bar -->
        <div class="flex flex-wrap items-center gap-2 mb-6 border-b border-slate-200 pb-3 text-xs">
          <button onclick="showCandidateScreen('register')" id="btn-scr-register" class="px-3 py-1.5 rounded-lg font-semibold floating-pink text-white">1. Registration Form</button>
          <button onclick="showCandidateScreen('camera')" id="btn-scr-camera" class="px-3 py-1.5 rounded-lg font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100">2. Webcam AI Check</button>
          <button onclick="showCandidateScreen('test')" id="btn-scr-test" class="px-3 py-1.5 rounded-lg font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100">3. Live Test Screen</button>
          <button onclick="showCandidateScreen('feedback')" id="btn-scr-feedback" class="px-3 py-1.5 rounded-lg font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100">4. 5-Star Feedback</button>
        </div>

        <!-- Candidate Screen 1: Registration Form -->
        <div id="scr-candidate-register" class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div class="max-w-2xl mx-auto">
            <h3 class="text-base font-extrabold text-slate-800 mb-1">Candidate Registration Form</h3>
            <p class="text-xs text-slate-500 mb-6">Complete your profile to unlock proctored assessment credentials.</p>

            <form onsubmit="event.preventDefault(); simulateRegistration();" class="space-y-4 text-xs">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-slate-700 font-semibold mb-1">First Name *</label>
                  <input type="text" id="demo-fn" value="Nagendra" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-800">
                </div>
                <div>
                  <label class="block text-slate-700 font-semibold mb-1">Last Name *</label>
                  <input type="text" id="demo-ln" value="Panda" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-800">
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-slate-700 font-semibold mb-1">PAN Number (10-Digit Alphanumeric) *</label>
                  <input type="text" id="demo-pan" value="ABCDE1234F" maxlength="10" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-pink-600 font-mono font-bold uppercase">
                </div>
                <div>
                  <label class="block text-slate-700 font-semibold mb-1">Country Dial Code *</label>
                  <select class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-800">
                    <option>+91 (India)</option>
                    <option>+1 (USA/Canada)</option>
                    <option>+971 (UAE)</option>
                    <option>+44 (UK)</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-slate-700 font-semibold mb-1">Mobile Number *</label>
                  <input type="tel" value="9876543210" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-800">
                </div>
                <div>
                  <label class="block text-slate-700 font-semibold mb-1">Highest Qualification *</label>
                  <select id="demo-qual" onchange="toggleScoreType(this.value)" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-800">
                    <option value="UG">UG (Under Graduate) - Requires %</option>
                    <option value="PG">PG (Post Graduate) - Requires CGPA</option>
                    <option value="PhD">PhD - Requires CGPA</option>
                  </select>
                </div>
              </div>

              <div id="box-percentage">
                <label class="block text-slate-700 font-semibold mb-1">Undergraduate Percentage (%) *</label>
                <input type="number" value="82.5" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-800">
              </div>

              <div id="box-cgpa" class="hidden">
                <label class="block text-slate-700 font-semibold mb-1">Postgraduate CGPA (Scale of 10.0) *</label>
                <input type="number" step="0.1" value="8.9" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-800">
              </div>

              <button type="submit" class="w-full py-3 floating-pink font-bold text-white rounded-xl shadow-lg transition mt-4">
                🚀 Submit Registration & Verify Credentials
              </button>
            </form>
          </div>
        </div>

        <!-- Candidate Screen 2: Webcam AI Check -->
        <div id="scr-candidate-camera" class="hidden bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div class="max-w-xl mx-auto text-center">
            <h3 class="text-base font-extrabold text-slate-800 mb-1">Pre-Exam Webcam & Hardware Handshake</h3>
            <p class="text-xs text-slate-500 mb-4">Edge AI proctoring active. Verify that only one candidate is in the camera frame.</p>

            <!-- Video Simulation Box -->
            <div class="relative bg-slate-900 border-2 border-emerald-500 rounded-2xl h-64 flex flex-col items-center justify-center overflow-hidden mb-4 shadow-inner">
              <div class="w-24 h-24 rounded-full bg-slate-800 border-2 border-emerald-400 flex items-center justify-center text-4xl mb-2 animate-pulse text-white">
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
              <button onclick="showCandidateScreen('test')" class="px-6 py-2.5 floating-green font-bold text-white rounded-xl text-xs shadow-lg transition">
                Proceed to Round 1: General Test ➜
              </button>
            </div>
          </div>
        </div>

        <!-- Candidate Screen 3: Live Test Screen -->
        <div id="scr-candidate-test" class="hidden bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-200">
            <div>
              <span class="text-xs font-bold text-pink-600 uppercase">Round 1: General Cognitive & Technical Test</span>
              <h3 class="text-sm font-extrabold text-slate-800">Question 4 of 25 (Time Remaining: <span id="timer" class="text-emerald-600 font-mono font-bold">18:42</span>)</h3>
            </div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-1 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded border border-emerald-200">
                Camera Live: 🟢 1 Person
              </span>
            </div>
          </div>

          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 mb-4">
            <p class="text-xs text-slate-800 font-semibold mb-3">
              In a distributed system, which HTTP status code represents that the server successfully received and processed the request without any client or server error?
            </p>
            <div class="space-y-2 text-xs">
              <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg cursor-pointer hover:border-pink-500 shadow-sm">
                <input type="radio" name="q4" class="text-pink-600">
                <span class="text-slate-700">A) 404 Not Found</span>
              </label>
              <label class="flex items-center gap-2 p-2.5 bg-pink-50 border border-pink-400 rounded-lg cursor-pointer shadow-sm">
                <input type="radio" name="q4" checked class="text-pink-600">
                <span class="text-pink-700 font-bold">B) 200 OK</span>
              </label>
              <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg cursor-pointer hover:border-pink-500 shadow-sm">
                <input type="radio" name="q4" class="text-pink-600">
                <span class="text-slate-700">C) 500 Internal Server Error</span>
              </label>
              <label class="flex items-center gap-2 p-2.5 bg-white border border-slate-200 rounded-lg cursor-pointer hover:border-pink-500 shadow-sm">
                <input type="radio" name="q4" class="text-pink-600">
                <span class="text-slate-700">D) 403 Forbidden</span>
              </label>
            </div>
          </div>

          <div class="flex justify-between items-center text-xs">
            <button class="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg font-semibold hover:bg-slate-300">Previous Question</button>
            <button onclick="showCandidateScreen('feedback')" class="px-6 py-2 floating-pink text-white rounded-lg font-bold shadow transition">
              Submit Exam & Complete Evaluation ➜
            </button>
          </div>
        </div>

        <!-- Candidate Screen 4: 5-Star Feedback -->
        <div id="scr-candidate-feedback" class="hidden bg-white border border-slate-200 rounded-2xl p-6 text-center max-w-lg mx-auto shadow-sm">
          <div class="w-14 h-14 rounded-full bg-emerald-100 text-emerald-600 border border-emerald-200 flex items-center justify-center text-2xl mx-auto mb-3">
            🎉
          </div>
          <h3 class="text-base font-extrabold text-slate-800">Assessment Submitted Successfully!</h3>
          <p class="text-xs text-slate-500 mt-1 mb-4">Your responses have been securely computed and forwarded to the HR review panel.</p>

          <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs mb-4">
            <span class="text-slate-700 font-semibold block mb-2">How was your testing experience today?</span>
            <div class="flex justify-center gap-2 text-2xl text-amber-400 cursor-pointer mb-3">
              <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
            </div>
            <textarea placeholder="Write your feedback comments here..." class="w-full bg-white border border-slate-300 rounded-lg p-2 text-slate-800 text-xs shadow-inner"></textarea>
            <button onclick="alert('Thank you! Your feedback has been recorded into your candidate dossier.');" class="w-full mt-2 py-2 floating-green text-white font-bold rounded-lg transition shadow">
              Submit Candidate Feedback
            </button>
          </div>

          <a href="http://127.0.0.1:8080/candidates/login/" target="_blank" class="text-xs text-pink-600 hover:underline font-semibold">
            Go to Candidate Login
          </a>
        </div>

      </div>

    </div>
  </section>

  <!-- TAB 6: DoR, DoD & REAL-WORLD USE CASES -->
  <section id="tab-dordod" class="hidden flex-1 p-4 sm:p-8 max-w-7xl mx-auto w-full">
    <div class="mb-6">
      <h2 class="text-xl font-extrabold text-slate-800 flex items-center gap-2">
        <span>Engineering Governance & Enterprise Methodology</span>
        <span class="text-xs font-semibold text-pink-600 bg-pink-50 px-2 py-0.5 rounded border border-pink-200">DoR & DoD Standards</span>
      </h2>
      <p class="text-xs text-slate-500">Strict criteria ensuring zero assessment defects during high-concurrency placement drives.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      
      <!-- DoR Table -->
      <div class="material-card p-6">
        <div class="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
          <span class="w-7 h-7 floating-pink text-white flex items-center justify-center font-bold text-sm">🎯</span>
          <h3 class="font-extrabold text-sm text-pink-600 uppercase tracking-wide">Definition of Ready (DoR) - Pre-Exam Gate</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-3">
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Candidate Identity Verified:</strong> Alphanumeric PAN + matching global country code validated against database.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Hardware Handshake:</strong> Webcam resolution, microphone permission, and bandwidth speed confirmed.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Anti-Cheat Agreement:</strong> Candidate accepts SweetAlert2 strict compliance rules (no tabs, sit silently).</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Exam Compilation:</strong> Questions randomized from Question Bank with configured cutoffs and timers.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Edge AI Proctor Active:</strong> Coco-SSD computer vision initialized inside candidate's browser (Single face check).</div>
          </li>
        </ul>
      </div>

      <!-- DoD Table -->
      <div class="material-card p-6">
        <div class="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
          <span class="w-7 h-7 floating-green text-white flex items-center justify-center font-bold text-sm">🏁</span>
          <h3 class="font-extrabold text-sm text-emerald-700 uppercase tracking-wide">Definition of Done (DoD) - Evaluation Gate</h3>
        </div>
        <ul class="text-xs text-slate-600 space-y-3">
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Responses Committed:</strong> All candidate answers written securely to MySQL with zero unhandled exceptions.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Auto-Evaluation:</strong> Raw marks, section-by-section breakdown, and pass/fail flags calculated instantly.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Proctoring Audit Passed:</strong> Zero unhandled multi-person or tab-switching violations in violation log.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>Result Registered:</strong> Candidate result record appears immediately at the top of Admin Results view.</div>
          </li>
          <li class="flex items-start gap-2.5">
            <span class="text-emerald-500 font-bold mt-0.5">✔</span>
            <div><strong>PDF Dossier Generated:</strong> 1-click candidate dossier generated containing scores, 5-star rating, and feedback.</div>
          </li>
        </ul>
      </div>

    </div>

    <!-- Real-World Enterprise Use Cases -->
    <div class="material-card p-6">
      <h3 class="text-sm font-extrabold text-slate-800 uppercase tracking-wider mb-4 flex items-center gap-2">
        <span>📌 Real-World Enterprise Use Cases</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <h4 class="font-bold text-pink-600 text-sm mb-1">Campus Drives (5,000+ Students)</h4>
          <p class="text-slate-600">
            QR codes displayed on auditorium screens enable instant self-registration and simultaneous aptitude testing. Results compiled in 5 minutes for same-day technical interviews.
          </p>
        </div>
        <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <h4 class="font-bold text-blue-600 text-sm mb-1">Lateral Tech Hiring (AI & Cloud)</h4>
          <p class="text-slate-600">
            Proprietary Edge AI proctor blocks ChatGPT in background tabs, dual monitors, and proxy assistants, ensuring 100% genuine engineering talent.
          </p>
        </div>
        <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl">
          <h4 class="font-bold text-emerald-700 text-sm mb-1">Global / GCC & Odoo ERP</h4>
          <p class="text-slate-600">
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
        btn.classList.remove('floating-pink', 'floating-green', 'text-white', 'shadow');
        btn.classList.add('text-slate-600');
      });
      document.getElementById('tab-' + tabId).classList.remove('hidden');
      const activeBtn = document.getElementById('btn-tab-' + tabId);
      if (tabId === 'urls') {
        activeBtn.classList.add('floating-green', 'text-white', 'shadow');
      } else {
        activeBtn.classList.add('floating-pink', 'text-white', 'shadow');
      }
      activeBtn.classList.remove('text-slate-600');
    }

    function setWireframePerspective(persp) {
      if (persp === 'candidate') {
        document.getElementById('perspective-candidate').classList.remove('hidden');
        document.getElementById('perspective-admin').classList.add('hidden');
        document.getElementById('btn-wf-cand').classList.add('floating-pink', 'text-white');
        document.getElementById('btn-wf-cand').classList.remove('text-slate-600');
        document.getElementById('btn-wf-admin').classList.remove('floating-pink', 'text-white');
        document.getElementById('btn-wf-admin').classList.add('text-slate-600');
        document.getElementById('wf-url-bar').textContent = 'http://127.0.0.1:8080/candidates/register/';
        document.getElementById('wf-live-btn').href = 'http://127.0.0.1:8080/candidates/register/';
      } else {
        document.getElementById('perspective-admin').classList.remove('hidden');
        document.getElementById('perspective-candidate').classList.add('hidden');
        document.getElementById('btn-wf-admin').classList.add('floating-pink', 'text-white');
        document.getElementById('btn-wf-admin').classList.remove('text-slate-600');
        document.getElementById('btn-wf-cand').classList.remove('floating-pink', 'text-white');
        document.getElementById('btn-wf-cand').classList.add('text-slate-600');
        document.getElementById('wf-url-bar').textContent = 'http://127.0.0.1:8080/dashboard/';
        document.getElementById('wf-live-btn').href = 'http://127.0.0.1:8080/dashboard/';
      }
    }

    function showCandidateScreen(scr) {
      ['register', 'camera', 'test', 'feedback'].forEach(s => {
        document.getElementById('scr-candidate-' + s).classList.add('hidden');
        const b = document.getElementById('btn-scr-' + s);
        b.classList.remove('floating-pink', 'text-white');
        b.classList.add('text-slate-600');
      });
      document.getElementById('scr-candidate-' + scr).classList.remove('hidden');
      const active = document.getElementById('btn-scr-' + scr);
      active.classList.add('floating-pink', 'text-white');
      active.classList.remove('text-slate-600');

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
        b.classList.remove('floating-pink', 'text-white');
        b.classList.add('text-slate-600');
      });
      document.getElementById('scr-admin-' + scr).classList.remove('hidden');
      const active = document.getElementById('btn-adm-' + scr);
      active.classList.add('floating-pink', 'text-white');
      active.classList.remove('text-slate-600');

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

    // Dynamic Host Adaptation for Public URL & Localhost
    window.addEventListener('DOMContentLoaded', () => {
      const isHttp = window.location.protocol.startsWith('http');
      const activeOrigin = isHttp ? window.location.origin : 'http://127.0.0.1:8080';

      document.querySelectorAll('a').forEach(a => {
        if (a.href && a.href.includes('127.0.0.1:8080')) {
          a.href = a.href.replace('http://127.0.0.1:8080', activeOrigin);
        }
      });

      document.querySelectorAll('code').forEach(c => {
        if (c.textContent.includes('127.0.0.1:8080')) {
          c.textContent = c.textContent.replaceAll('http://127.0.0.1:8080', activeOrigin);
        }
      });
    });
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
        print(f"Successfully deployed Material Dashboard theme to: {d}")
    except Exception as e:
        print(f"Error writing to {d}: {e}")
