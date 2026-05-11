(function () {
  'use strict';

  // ── Config ──────────────────────────────────────────────────────────
  const STATUS_COLORS = {
    yes:    { fill: '#0B7A3A', stroke: '#095c2d' },
    partial:{ fill: '#D68C00', stroke: '#a86a00' },
    no:     { fill: '#D92D20', stroke: '#a61f16' },
    mixed:  { fill: '#6C757D', stroke: '#545b62' }
  };

  const STATUS_LABELS = {
    yes:     'Yes',
    partial: 'Partial',
    no:      'No',
    mixed:   'Mixed'
  };

  // ── State ───────────────────────────────────────────────────────────
  let countries = [];
  let map = null;

  // ── Init ────────────────────────────────────────────────────────────
  async function init() {
    try {
      const response = await fetch('data/countries.json');
      const data = await response.json();
      countries = data.countries;
      renderPage(countries);
    } catch (err) {
      console.error('Failed to load country data:', err);
      document.querySelector('.main-view').innerHTML =
        '<p style="padding:2rem;color:#D92D20;">Unable to load data. Please ensure <code>data/countries.json</code> is available.</p>';
    }
  }

  // ── Render full page ────────────────────────────────────────────────
  function renderPage(data) {
    initMap(data);
    renderTable(data);
    // Select first country by default
    if (data.length > 0) showCountryDetail(data[0]);
  }

  // ── Map ─────────────────────────────────────────────────────────────
  function initMap(data) {
    map = L.map('map', {
      center: [5, 20],
      zoom: 2,
      minZoom: 1,
      maxZoom: 8,
      scrollWheelZoom: true,
      attributionControl: false
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }).addTo(map);

    // Custom attribution (bottom-right, unobtrusive)
    L.control.attribution({ position: 'bottomright' }).addTo(map);

    data.forEach(country => {
      const color = STATUS_COLORS[country.cse.status] || STATUS_COLORS.no;
      const marker = L.divIcon({
        className: 'custom-marker',
        html: `<div style="
          width:22px; height:22px;
          border-radius:50%;
          background:${color.fill};
          border:2px solid ${color.stroke};
          box-shadow:0 1px 4px rgba(0,0,0,0.3);
          cursor:pointer;
          transition:transform 0.15s;
        " onmouseover="this.style.transform='scale(1.3)'" onmouseout="this.style.transform='scale(1)'">
        </div>`,
        iconSize: [22, 22],
        iconAnchor: [11, 11]
      });

      const m = L.marker(country.coordinates, { icon: marker })
        .addTo(map)
        .bindPopup(popupHTML(country));

      m.on('click', () => showCountryDetail(country));
    });

    // Fit bounds to all markers with padding
    const group = new L.featureGroup(data.map(c => L.marker(c.coordinates)));
    map.fitBounds(group.getBounds().pad(0.15));
  }

  function popupHTML(c) {
    const status = c.cse.status;
    const color = STATUS_COLORS[status]?.fill || '#999';
    return `
      <h4>${c.name}</h4>
      <div style="color:#666;font-size:0.8rem;margin-bottom:0.3rem;">${c.region}</div>
      <div class="popup-status" style="color:${color}">
        ${STATUS_LABELS[status]} — ${c.cse.local_name.substring(0, 45)}${c.cse.local_name.length > 45 ? '...' : ''}
      </div>
    `;
  }

  // ── Detail Panel ────────────────────────────────────────────────────
  function showCountryDetail(c) {
    const emptyEl = document.getElementById('detail-empty');
    const contentEl = document.getElementById('detail-content');

    emptyEl.classList.add('hidden');
    contentEl.classList.remove('hidden');

    const cseStatus = c.cse.status;
    const gbvStatus = c.gbv_law.status;

    contentEl.innerHTML = `
      <div class="detail-country-header">
        <div>
          <h2>${c.name}</h2>
          <span class="region">${c.region}</span>
        </div>
      </div>

      <div class="detail-section">
        <h3>CSE in Education System</h3>
        <span class="status-badge ${cseStatus}">${STATUS_LABELS[cseStatus]}</span>
        <p class="local-name">"${c.cse.local_name}"</p>
        <p style="margin-top:0.5rem;">${c.cse.details}</p>
        ${sourcesList(c.cse.sources)}
      </div>

      <div class="detail-section">
        <h3>Age of Consent</h3>
        <p><strong>${c.age_of_consent.value}</strong> — ${c.age_of_consent.details}</p>
        ${sourcesList(c.age_of_consent.sources)}
      </div>

      <div class="detail-section">
        <h3>GBV Legal Framework</h3>
        <span class="status-badge ${gbvStatus}">${STATUS_LABELS[gbvStatus]}</span>
        <p style="margin-top:0.5rem;">${c.gbv_law.law_name}</p>
        <p style="margin-top:0.4rem;">${c.gbv_law.details}</p>
        ${sourcesList(c.gbv_law.sources)}
      </div>

      ${c.caveats ? `
        <div class="detail-section">
          <h3>Caveats</h3>
          <div class="caveat-box">${c.caveats}</div>
        </div>
      ` : ''}
    `;

    // Scroll detail panel to top
    const panel = document.getElementById('detail-panel');
    if (panel) panel.scrollTop = 0;

    // Pan map to country
    if (map) {
      map.setView(c.coordinates, 4, { animate: true, duration: 0.5 });
    }
  }

  function sourcesList(sources) {
    if (!sources || sources.length === 0) return '';
    const items = sources.map(s =>
      `<li><a href="${s.url}" target="_blank" rel="noopener">${s.name}</a></li>`
    ).join('');
    return `<ul class="sources-list">${items}</ul>`;
  }

  // ── Comparison Table ────────────────────────────────────────────────
  function renderTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = data.map(c => `
      <tr data-iso="${c.iso}" style="cursor:pointer">
        <td>${c.name}</td>
        <td>${c.region}</td>
        <td>${badgeCell(c.cse.status)}</td>
        <td>${escapeHtml(c.cse.local_name)}</td>
        <td>${c.age_of_consent.value}</td>
        <td>${badgeCell(c.gbv_law.status)}</td>
        <td class="td-caveat">${escapeHtml(c.caveats || '')}</td>
      </tr>
    `).join('');

    // Click to select
    tbody.querySelectorAll('tr').forEach(row => {
      row.addEventListener('click', () => {
        const iso = row.dataset.iso;
        const country = countries.find(c => c.iso === iso);
        if (country) showCountryDetail(country);
      });
    });
  }

  function badgeCell(status) {
    const label = STATUS_LABELS[status] || status;
    return `<span class="status-badge ${status}">${label}</span>`;
  }

  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // ── Start ───────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', init);
})();
