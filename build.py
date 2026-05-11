import json

with open('css_backup.txt', 'r', encoding='utf-8') as f:
    css = f.read()

with open('cse_data.json', 'r', encoding='utf-8') as f:
    cse_data = json.load(f)

# CSE data as JS string
data_js = json.dumps(cse_data, indent=2)

STATUS_COLORS = {'yes': '#10b981', 'partial': '#f59e0b', 'no': '#ef4444', 'mixed': '#6B7280'}
STATUS_LABELS = {'yes': 'Yes', 'partial': 'Partial', 'no': 'No', 'mixed': 'Mixed'}
STATUS_BG = {'yes': '#ECFDF5', 'partial': '#FFFBEB', 'no': '#FEF2F2', 'mixed': '#F3F4F6'}

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="CSE Policy & Legal Environment — 8-country snapshot">
  <meta name="author" content="Haijun Che">
  <title>CSE Policy & Legal Environment — 8 Country Snapshot</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
  <style>
{css}
    /* CSE-specific additions */
    .map-container {{ height: 400px; width: 100%; border-radius: 0 0 12px 12px; }}
    .hidden {{ display: none !important; }}
    .detail-panel {{ padding: 24px; }}
    .detail-panel h3 {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--unfpa-warm-gray); margin-bottom: 8px; }}
    .status-pill {{ display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 100px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
    .status-pill.yes {{ background: #ECFDF5; color: #10b981; }}
    .status-pill.partial {{ background: #FFFBEB; color: #f59e0b; }}
    .status-pill.no {{ background: #FEF2F2; color: #ef4444; }}
    .status-pill.mixed {{ background: #F3F4F6; color: #6B7280; }}
    .cse-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
    .cse-table th {{ background: #F8F9FA; font-weight: 600; text-align: left; padding: 14px 16px; border-bottom: 2px solid var(--border); white-space: nowrap; color: var(--unfpa-warm-gray); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; }}
    .cse-table td {{ padding: 14px 16px; border-bottom: 1px solid var(--border-light); vertical-align: top; line-height: 1.5; }}
    .cse-table tr:hover {{ background: var(--unfpa-orange-light); }}
    .cse-table td:first-child {{ font-weight: 700; color: var(--unfpa-navy); }}
    .local-name {{ font-style: italic; color: var(--unfpa-warm-gray); font-size: 0.8rem; }}
    .caveat-text {{ font-size: 0.78rem; color: var(--unfpa-warm-gray); max-width: 260px; }}
    .method-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px; }}
    .leaflet-popup-content h4 {{ font-size: 1rem; font-weight: 700; margin-bottom: 4px; }}
    .leaflet-popup-content .popup-meta {{ font-size: 0.75rem; color: var(--text-light); margin-bottom: 4px; }}
    .leaflet-popup-content .popup-status {{ display: inline-flex; align-items: center; gap: 4px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 3px 10px; border-radius: 100px; }}
    @media (max-width: 1024px) {{ .method-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <!-- Loading Screen -->
  <div id="loader">
    <div class="loader-icon"><i data-lucide="activity" style="width:48px;height:48px;color:white;"></i></div>
    <div class="loader-text">Loading Dashboard...</div>
    <div class="loader-bar"><div class="loader-bar-inner"></div></div>
  </div>

  <!-- Navbar -->
  <nav class="navbar">
    <div class="navbar-inner">
      <a href="#" class="navbar-brand" aria-label="CSE Policy Mapping">
        <div style="width:36px;height:36px;background:linear-gradient(135deg,#F36F21 0%,#E05A0C 100%);border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;">
          <i data-lucide="globe-2" style="width:20px;height:20px;"></i>
        </div>
        <span class="navbar-brand-text">CSE Policy Mapping<br><span style="color:#9CA3AF;">8-Country Snapshot</span></span>
      </a>
      <div class="navbar-links">
        <a href="#dashboard" class="navbar-link">Dashboard</a>
        <a href="#methodology" class="navbar-link">Methodology</a>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <section class="hero" id="hero">
    <div class="hero-bg-container">
      <div class="hero-bg-slide"></div><div class="hero-bg-slide"></div><div class="hero-bg-slide"></div>
      <div class="hero-bg-slide"></div><div class="hero-bg-slide"></div><div class="hero-bg-slide"></div>
    </div>
    <div class="hero-inner">
      <div class="hero-badge">
        <i data-lucide="shield-check" style="width:13px;height:13px;"></i>
        UNFPA CONSULTANCY · HOMEWORK ASSIGNMENT
      </div>
      <h1>CSE Policy & Legal<br>Environment Mapping</h1>
      <p class="hero-subtitle">Mapping the policy and legal landscape for Comprehensive Sexuality Education across 8 countries in Africa, Asia, and Latin America — curriculum integration, age of consent, and GBV legal frameworks.</p>
      <div class="hero-ctas">
        <a href="#dashboard" class="hero-cta-primary">Explore Map <i data-lucide="chevron-down" style="width:16px;height:16px;"></i></a>
        <a href="#methodology" class="hero-cta-secondary">Methodology <i data-lucide="book-open" style="width:14px;height:14px;"></i></a>
      </div>
    </div>
  </section>

  <!-- Stats Bar -->
  <div class="stats-bar fade-up">
    <div class="stat-card" id="statYes">
      <div class="stat-icon green"><i data-lucide="check-circle-2" style="width:24px;height:24px;"></i></div>
      <div class="value" id="animStat1">0</div>
      <div class="label">CSE Integrated<br>in Curricula</div>
      <div class="stat-country" id="statYesCountries"></div>
    </div>
    <div class="stat-card" id="statPartial">
      <div class="stat-icon amber"><i data-lucide="alert-circle" style="width:24px;height:24px;"></i></div>
      <div class="value" id="animStat2">0</div>
      <div class="label">Partial Integration<br>Embedded / uneven</div>
      <div class="stat-country" id="statPartialCountries"></div>
    </div>
    <div class="stat-card" id="statNo">
      <div class="stat-icon coral"><i data-lucide="x-circle" style="width:24px;height:24px;"></i></div>
      <div class="value" id="animStat3">0</div>
      <div class="label">No Integration<br>Not in curriculum</div>
      <div class="stat-country" id="statNoCountries"></div>
    </div>
    <div class="stat-card" id="statTotal">
      <div class="stat-icon" style="background:#F3F4F6;color:#6B7280;"><i data-lucide="globe" style="width:24px;height:24px;"></i></div>
      <div class="value" id="animStat4">8</div>
      <div class="label">Total Countries<br>Across 4 regions</div>
      <div class="stat-country"></div>
    </div>
  </div>

  <!-- Dashboard -->
  <section id="dashboard">
    <div style="max-width:1200px;margin:0 auto;padding:48px 40px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
        <i data-lucide="map" style="width:20px;height:20px;color:var(--unfpa-orange);"></i>
        <span style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--unfpa-orange);">Interactive Dashboard</span>
      </div>
      <h2 style="font-size:1.6rem;font-weight:800;color:var(--unfpa-navy);margin-bottom:8px;">Policy & Legal Mapping</h2>
      <p style="font-size:0.95rem;color:var(--unfpa-warm-gray);max-width:600px;">Explore CSE integration status, age of consent laws, and GBV legal frameworks across 8 focus countries. Click any marker or table row for detailed country profiles.</p>

      <div class="dashboard-grid" style="margin-top:32px;">
        <div class="card" style="padding:0;">
          <div style="display:flex;align-items:center;justify-content:space-between;padding:20px 24px 16px;border-bottom:1px solid var(--border-light);">
            <div style="display:flex;align-items:center;gap:10px;font-size:1rem;font-weight:700;color:var(--unfpa-navy);">
              <i data-lucide="map-pin" style="width:18px;height:18px;color:var(--unfpa-orange);"></i><span>World Map</span>
            </div>
            <div style="display:flex;align-items:center;gap:12px;font-size:0.75rem;color:var(--unfpa-warm-gray);">
              <span style="display:flex;align-items:center;gap:4px;"><span style="width:8px;height:8px;border-radius:50%;background:#10b981;"></span>Yes</span>
              <span style="display:flex;align-items:center;gap:4px;"><span style="width:8px;height:8px;border-radius:50%;background:#f59e0b;"></span>Partial</span>
              <span style="display:flex;align-items:center;gap:4px;"><span style="width:8px;height:8px;border-radius:50%;background:#ef4444;"></span>No</span>
            </div>
          </div>
          <div id="map" class="map-container"></div>
          <p style="padding:12px 24px;font-size:0.8rem;color:var(--text-light);text-align:center;background:#F8F9FA;border-top:1px solid var(--border-light);">Click a country marker to view full details</p>
        </div>

        <div class="card" id="detail-card">
          <div id="detail-empty" style="height:100%;min-height:400px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:var(--text-light);padding:40px;">
            <i data-lucide="mouse-pointer-click" style="width:48px;height:48px;margin-bottom:16px;opacity:0.4;"></i>
            <p style="font-size:0.9rem;">Select a country on the map<br>to view its policy profile.</p>
          </div>
          <div id="detail-content" class="hidden" style="padding:24px;max-height:520px;overflow-y:auto;"></div>
        </div>
      </div>

      <div style="margin-top:32px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
          <i data-lucide="table-2" style="width:20px;height:20px;color:var(--unfpa-orange);"></i>
          <span style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--unfpa-orange);">Comparison</span>
        </div>
        <h2 style="font-size:1.6rem;font-weight:800;color:var(--unfpa-navy);margin-bottom:8px;">Country Overview</h2>
        <p style="font-size:0.95rem;color:var(--unfpa-warm-gray);margin-bottom:24px;">Side-by-side comparison across all three mapped dimensions.</p>
        <div class="card" style="padding:0;overflow:hidden;">
          <div style="overflow-x:auto;">
            <table class="cse-table">
              <thead><tr><th>Country</th><th>Region</th><th>CSE Status</th><th>Local Framing</th><th>Age of Consent</th><th>GBV Framework</th><th>Key Caveat</th></tr></thead>
              <tbody id="table-body"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Methodology -->
  <section id="methodology" style="background:#F8F9FA;padding:60px 40px;">
    <div style="max-width:1200px;margin:0 auto;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
        <i data-lucide="book-open" style="width:20px;height:20px;color:var(--unfpa-orange);"></i>
        <span style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--unfpa-orange);">Transparency</span>
      </div>
      <h2 style="font-size:1.6rem;font-weight:800;color:var(--unfpa-navy);margin-bottom:8px;">Methodology & Limitations</h2>
      <p style="font-size:0.95rem;color:var(--unfpa-warm-gray);max-width:600px;margin-bottom:24px;">How this data was compiled and what to keep in mind when interpreting it.</p>
      <div class="method-grid">
        <div class="card" style="padding:28px;">
          <div style="width:44px;height:44px;background:var(--unfpa-orange-light);border-radius:8px;display:flex;align-items:center;justify-content:center;margin-bottom:16px;"><i data-lucide="database" style="width:22px;height:22px;color:var(--unfpa-orange);"></i></div>
          <h3 style="font-size:0.95rem;font-weight:700;color:var(--unfpa-navy);margin-bottom:10px;">Data Sources</h3>
          <p style="font-size:0.84rem;color:var(--unfpa-warm-gray);line-height:1.65;">All data from publicly available, authoritative sources: UNESCO GEM Report CSE Country Profiles (2023), PEER Education Profiles, UN Women Global Database on VAW, World Bank Women Business and the Law 2024, and official national legislation.</p>
        </div>
        <div class="card" style="padding:28px;">
          <div style="width:44px;height:44px;background:var(--unfpa-orange-light);border-radius:8px;display:flex;align-items:center;justify-content:center;margin-bottom:16px;"><i data-lucide="scale" style="width:22px;height:22px;color:var(--unfpa-orange);"></i></div>
          <h3 style="font-size:0.95rem;font-weight:700;color:var(--unfpa-navy);margin-bottom:10px;">Definitional Notes</h3>
          <ul style="font-size:0.84rem;color:var(--unfpa-warm-gray);line-height:1.65;padding-left:1.1rem;">
            <li><strong>Yes</strong> — CSE explicitly mandated with clear policy guidance.</li>
            <li><strong>Partial</strong> — Exists but not branded as CSE, or uneven.</li>
            <li><strong>No</strong> — No national-level integration.</li>
            <li><strong>Age of consent</strong> — Legal threshold; not cultural norms.</li>
          </ul>
        </div>
        <div class="card" style="padding:28px;">
          <div style="width:44px;height:44px;background:var(--unfpa-orange-light);border-radius:8px;display:flex;align-items:center;justify-content:center;margin-bottom:16px;"><i data-lucide="alert-triangle" style="width:22px;height:22px;color:var(--unfpa-orange);"></i></div>
          <h3 style="font-size:0.95rem;font-weight:700;color:var(--unfpa-navy);margin-bottom:10px;">Limitations</h3>
          <ul style="font-size:0.84rem;color:var(--unfpa-warm-gray);line-height:1.65;padding-left:1.1rem;">
            <li><strong>Law vs. practice</strong> — Legal existence does not guarantee implementation.</li>
            <li><strong>Sub-national variation</strong> — Federal systems show intra-country differences.</li>
            <li><strong>Comparability</strong> — Definitions vary across legal systems.</li>
            <li><strong>Static snapshot</strong> — Reflects May 2026 state.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer style="background:var(--unfpa-navy);color:rgba(255,255,255,0.6);padding:32px 40px;">
    <div style="max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
      <p style="font-size:0.85rem;">Built for UNFPA Data Analytics & Visualization Consultancy — Homework Assignment</p>
      <p style="font-size:0.8rem;opacity:0.7;">Haijun Che · May 2026</p>
    </div>
  </footer>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const cseData = {data_js};
    const STATUS_COLORS = {{yes: '#10b981', partial: '#f59e0b', no: '#ef4444', mixed: '#6B7280'}};
    const STATUS_LABELS = {{yes: 'Yes', partial: 'Partial', no: 'No', mixed: 'Mixed'}};
    const STATUS_BG = {{yes: '#ECFDF5', partial: '#FFFBEB', no: '#FEF2F2', mixed: '#F3F4F6'}};
    let map = null;
    let selectedIso = null;

    function init() {{
      renderStats();
      initMap();
      renderTable();
      if (cseData.length > 0) showDetail(cseData[0]);
      lucide.createIcons();
    }}

    function renderStats() {{
      const counts = {{yes: 0, partial: 0, no: 0}};
      const names = {{yes: [], partial: [], no: []}};
      cseData.forEach(c => {{
        const s = c.cse_status;
        if (counts[s] !== undefined) {{ counts[s]++; names[s].push(c.name); }}
      }});
      document.getElementById('statYesCountries').textContent = names.yes.join(', ');
      document.getElementById('statPartialCountries').textContent = names.partial.join(', ');
      document.getElementById('statNoCountries').textContent = names.no.join(', ');
    }}

    function initMap() {{
      map = L.map('map', {{center: [5, 20], zoom: 2, minZoom: 1, maxZoom: 8, scrollWheelZoom: true, attributionControl: false}});
      L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{maxZoom: 19, attribution: '© OpenStreetMap'}}).addTo(map);
      L.control.attribution({{position: 'bottomright'}}).addTo(map);
      cseData.forEach(c => {{
        const color = STATUS_COLORS[c.cse_status] || STATUS_COLORS.no;
        const marker = L.divIcon({{
          className: 'custom-marker',
          html: `<div style="width:24px;height:24px;border-radius:50%;background:${{color}};border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.25);cursor:pointer;transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.4)'" onmouseout="this.style.transform='scale(1)'"></div>`,
          iconSize: [24, 24], iconAnchor: [12, 12]
        }});
        const m = L.marker(c.coords, {{icon: marker}}).addTo(map).bindPopup(popupHTML(c));
        m.on('click', () => showDetail(c));
      }});
      const group = new L.featureGroup(cseData.map(c => L.marker(c.coords)));
      map.fitBounds(group.getBounds().pad(0.15));
    }}

    function popupHTML(c) {{
      return `<h4>${{c.name}}</h4><div class="popup-meta">${{c.region}}</div><span class="popup-status" style="background:${{STATUS_BG[c.cse_status]}};color:${{STATUS_COLORS[c.cse_status]}}">${{STATUS_LABELS[c.cse_status]}}</span>`;
    }}

    function showDetail(c) {{
      selectedIso = c.iso;
      document.getElementById('detail-empty').classList.add('hidden');
      document.getElementById('detail-content').classList.remove('hidden');
      document.getElementById('detail-content').innerHTML = `
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;padding-bottom:16px;border-bottom:2px solid var(--border-light);">
          <div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--unfpa-orange) 0%,#E05A0C 100%);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:0.85rem;">${{c.iso}}</div>
          <div><h2 style="font-size:1.25rem;font-weight:700;color:var(--unfpa-navy);line-height:1.3;">${{c.name}}</h2><div style="font-size:0.8rem;color:var(--text-light);">${{c.region}}</div></div>
        </div>
        <div class="detail-panel">
          <div style="margin-bottom:20px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;"><i data-lucide="graduation-cap" style="width:16px;height:16px;color:var(--unfpa-orange);"></i><h3>CSE in Education System</h3></div>
            <span class="status-pill ${{c.cse_status}}">${{STATUS_LABELS[c.cse_status]}}</span>
            <p style="font-style:italic;color:var(--unfpa-warm-gray);font-size:0.85rem;margin-top:6px;">"${{c.cse_name}}"</p>
            <p style="margin-top:8px;font-size:0.88rem;color:var(--unfpa-charcoal);line-height:1.65;">${{c.cse_detail}}</p>
          </div>
          <div style="margin-bottom:20px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;"><i data-lucide="shield" style="width:16px;height:16px;color:var(--unfpa-orange);"></i><h3>Age of Consent</h3></div>
            <p style="font-size:0.88rem;color:var(--unfpa-charcoal);line-height:1.65;"><strong style="font-size:1.1rem;color:var(--unfpa-navy);">${{c.consent}}</strong> — ${{c.consent_detail}}</p>
          </div>
          <div style="margin-bottom:20px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;"><i data-lucide="scale" style="width:16px;height:16px;color:var(--unfpa-orange);"></i><h3>GBV Legal Framework</h3></div>
            <span class="status-pill ${{c.gbv}}">${{STATUS_LABELS[c.gbv]}}</span>
            <p style="margin-top:8px;font-size:0.88rem;color:var(--unfpa-charcoal);line-height:1.65;">${{c.gbv_law}}</p>
            <p style="margin-top:6px;font-size:0.88rem;color:var(--unfpa-charcoal);line-height:1.65;">${{c.gbv_detail}}</p>
          </div>
          <div>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;"><i data-lucide="alert-triangle" style="width:16px;height:16px;color:var(--unfpa-orange);"></i><h3>Caveats</h3></div>
            <div style="background:linear-gradient(135deg,#FFFBEB 0%,#FEF3C7 100%);border-left:3px solid var(--status-partial);padding:14px 16px;border-radius:0 8px 8px 0;font-size:0.82rem;color:var(--unfpa-charcoal);line-height:1.55;">${{c.caveat}}</div>
          </div>
        </div>
      `;
      lucide.createIcons();
      document.getElementById('detail-card').scrollTop = 0;
      if (map) map.setView(c.coords, 4, {{animate: true, duration: 0.5}});
      document.querySelectorAll('#table-body tr').forEach(row => {{
        row.style.background = row.dataset.iso === c.iso ? 'var(--unfpa-orange-light)' : '';
      }});
    }}

    function renderTable() {{
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = cseData.map(c => `
        <tr data-iso="${{c.iso}}">
          <td>${{c.name}}</td>
          <td style="font-size:0.8rem;color:var(--text-light);">${{c.region}}</td>
          <td><span class="status-pill ${{c.cse_status}}">${{STATUS_LABELS[c.cse_status]}}</span></td>
          <td class="local-name">${{c.cse_name}}</td>
          <td>${{c.consent}}</td>
          <td><span class="status-pill ${{c.gbv}}">${{STATUS_LABELS[c.gbv]}}</span></td>
          <td class="caveat-text">${{c.caveat}}</td>
        </tr>
      `).join('');
      tbody.querySelectorAll('tr').forEach(row => {{
        row.addEventListener('click', () => {{
          const c = cseData.find(x => x.iso === row.dataset.iso);
          if (c) showDetail(c);
        }});
      }});
    }}

    // Animated stats
    function animateStat(el, target, suffix) {{
      if (!el) return;
      let current = 0;
      const inc = target / 50;
      const timer = setInterval(() => {{
        current += inc;
        if (current >= target) {{ current = target; clearInterval(timer); }}
        el.textContent = Math.round(current) + suffix;
      }}, 30);
    }}

    function initAnimatedStats() {{
      const stats = [
        {{el: 'animStat1', target: cseData.filter(c => c.cse_status === 'yes').length, suffix: ''}},
        {{el: 'animStat2', target: cseData.filter(c => c.cse_status === 'partial').length, suffix: ''}},
        {{el: 'animStat3', target: cseData.filter(c => c.cse_status === 'no').length, suffix: ''}},
        {{el: 'animStat4', target: cseData.length, suffix: ''}}
      ];
      stats.forEach((s, i) => setTimeout(() => animateStat(document.getElementById(s.el), s.target, s.suffix), i * 200));
    }}

    // Scroll animations
    function initScrollAnimations() {{
      const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{ if (entry.isIntersecting) entry.target.classList.add('visible'); }});
      }}, {{threshold: 0.1, rootMargin: '0px 0px -40px 0px'}});
      document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
    }}

    // Init
    window.addEventListener('load', () => {{
      lucide.createIcons();
      setTimeout(() => {{
        document.getElementById('loader').classList.add('hidden');
        initScrollAnimations();
        init();
        initAnimatedStats();
      }}, 1800);
    }});
  </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Built: {len(html)} chars, {len(html.split(chr(10)))} lines")