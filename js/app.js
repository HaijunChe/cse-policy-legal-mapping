(function () {
  'use strict';

  const STATUS_COLORS = {
    yes:     '#10b981',
    partial: '#f59e0b',
    no:      '#ef4444',
    mixed:   '#6B7280'
  };

  const STATUS_BG = {
    yes:     '#ECFDF5',
    partial: '#FFFBEB',
    no:      '#FEF2F2',
    mixed:   '#F3F4F6'
  };

  const STATUS_LABELS = {
    yes:     'Yes',
    partial: 'Partial',
    no:      'No',
    mixed:   'Mixed'
  };

  const ICONS = {
    yes:     'check-circle-2',
    partial: 'alert-circle',
    no:      'x-circle',
    mixed:   'help-circle'
  };

  let countries = [];
  let map = null;
  let selectedIso = null;

  async function init() {
    try {
      const response = await fetch('data/countries.json');
      const data = await response.json();
      countries = data.countries;
      renderPage(countries);
      lucide.createIcons();
    } catch (err) {
      console.error('Failed to load data:', err);
    }
  }

  function renderPage(data) {
    renderSummaryCards(data);
    initMap(data);
    renderTable(data);
    if (data.length > 0) showCountryDetail(data[0]);
  }

  function renderSummaryCards(data) {
    const counts = { yes: 0, partial: 0, no: 0 };
    const cseCountries = { yes: [], partial: [], no: [] };

    data.forEach(c => {
      const s = c.cse.status;
      if (counts[s] !== undefined) {
        counts[s]++;
        cseCountries[s].push(c.name);
      }
    });

    const statuses = [
      { key: 'yes',     label: 'CSE Integrated',      sub: 'Explicitly mandated' },
      { key: 'partial', label: 'Partial Integration', sub: 'Embedded / uneven' },
      { key: 'no',      label: 'No Integration',      sub: 'Not in curriculum' }
    ];

    const container = document.getElementById('summary-cards');
    container.innerHTML = statuses.map(s => `
      <div class="summary-card ${s.key === 'yes' ? 'active' : ''}" data-status="${s.key}"
           onclick="window.filterByStatus('${s.key}')"
           onmouseenter="window.showCountries('${s.key}')"
           onmouseleave="window.hideCountries()">
        <div class="summary-card-header">
          <span class="summary-card-title">${s.label}</span>
          <div class="summary-card-icon ${s.key}">
            <i data-lucide="${ICONS[s.key]}"></i>
          </div>
        </div>
        <div class="summary-card-count">${counts[s.key]}</div>
        <div class="summary-card-label">${s.sub}</div>
        <div class="summary-card-countries">${cseCountries[s.key].join(', ')}</div>
      </div>
    `).join('') + `
      <div class="summary-card" style="cursor:default">
        <div class="summary-card-header">
          <span class="summary-card-title">Total Countries</span>
          <div class="summary-card-icon" style="background:#F3F4F6;color:#6B7280">
            <i data-lucide="globe"></i>
          </div>
        </div>
        <div class="summary-card-count">${data.length}</div>
        <div class="summary-card-label">Across 4 regions, 3 continents</div>
        <div class="summary-card-countries">&nbsp;</div>
      </div>
    `;
  }

  window.showCountries = function(status) {
    document.querySelectorAll('.summary-card').forEach(card => {
      if (card.dataset.status === status) {
        card.querySelector('.summary-card-countries').style.opacity = '1';
      }
    });
  };

  window.hideCountries = function() {
    document.querySelectorAll('.summary-card-countries').forEach(el => {
      if (!el.closest('.summary-card').classList.contains('active')) {
        el.style.opacity = '';
      }
    });
  };

  window.filterByStatus = function(status) {
    document.querySelectorAll('.summary-card').forEach(card => {
      card.classList.toggle('active', card.dataset.status === status);
    });
  };

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

    L.control.attribution({ position: 'bottomright' }).addTo(map);

    data.forEach(country => {
      const color = STATUS_COLORS[country.cse.status] || STATUS_COLORS.no;
      const marker = L.divIcon({
        className: 'custom-marker',
        html: `<div style="
          width:24px; height:24px;
          border-radius:50%;
          background:${color};
          border:3px solid white;
          box-shadow:0 2px 8px rgba(0,0,0,0.25);
          cursor:pointer;
          transition:transform 0.2s;
        " onmouseover="this.style.transform='scale(1.4)'" onmouseout="this.style.transform='scale(1)'"
        ></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });

      const m = L.marker(country.coordinates, { icon: marker })
        .addTo(map)
        .bindPopup(popupHTML(country));

      m.on('click', () => showCountryDetail(country));
    });

    const group = new L.featureGroup(data.map(c => L.marker(c.coordinates)));
    map.fitBounds(group.getBounds().pad(0.15));
  }

  function popupHTML(c) {
    const status = c.cse.status;
    const color = STATUS_COLORS[status];
    const bg = STATUS_BG[status];
    return `
      <h4>${c.name}</h4>
      <div class="popup-meta">${c.region}</div>
      <span class="popup-status" style="background:${bg};color:${color}">
        ${STATUS_LABELS[status]}
      </span>
    `;
  }

  function showCountryDetail(c) {
    selectedIso = c.iso;

    const emptyEl = document.getElementById('detail-empty');
    const contentEl = document.getElementById('detail-content');

    emptyEl.classList.add('hidden');
    contentEl.classList.remove('hidden');

    const cseStatus = c.cse.status;
    const gbvStatus = c.gbv_law.status;

    contentEl.innerHTML = `
      <div class="detail-country-header">
        <div class="detail-flag">${c.iso}</div>
        <div>
          <h2>${c.name}</h2>
          <div class="detail-region">${c.region}</div>
        </div>
      </div>

      <div class="detail-section">
        <div class="detail-section-header">
          <i data-lucide="graduation-cap"></i>
          <h3>CSE in Education System</h3>
        </div>
        <span class="status-badge ${cseStatus}">
          <i data-lucide="${ICONS[cseStatus]}" style="width:12px;height:12px"></i>
          ${STATUS_LABELS[cseStatus]}
        </span>
        <p class="local-name">"${c.cse.local_name}"</p>
        <p style="margin-top:8px">${c.cse.details}</p>
        ${sourcesList(c.cse.sources)}
      </div>

      <div class="detail-section">
        <div class="detail-section-header">
          <i data-lucide="shield"></i>
          <h3>Age of Consent</h3>
        </div>
        <p><strong style="font-size:1.1rem;color:var(--unfpa-navy)">${c.age_of_consent.value}</strong> — ${c.age_of_consent.details}</p>
        ${sourcesList(c.age_of_consent.sources)}
      </div>

      <div class="detail-section">
        <div class="detail-section-header">
          <i data-lucide="scale"></i>
          <h3>GBV Legal Framework</h3>
        </div>
        <span class="status-badge ${gbvStatus}">
          <i data-lucide="${ICONS[gbvStatus]}" style="width:12px;height:12px"></i>
          ${STATUS_LABELS[gbvStatus]}
        </span>
        <p style="margin-top:8px">${c.gbv_law.law_name}</p>
        <p style="margin-top:6px">${c.gbv_law.details}</p>
        ${sourcesList(c.gbv_law.sources)}
      </div>

      ${c.caveats ? `
        <div class="detail-section">
          <div class="detail-section-header">
            <i data-lucide="alert-triangle"></i>
            <h3>Caveats</h3>
          </div>
          <div class="caveat-box">${c.caveats}</div>
        </div>
      ` : ''}
    `;

    const panel = document.getElementById('detail-card');
    if (panel) panel.scrollTop = 0;

    if (map) {
      map.setView(c.coordinates, 4, { animate: true, duration: 0.5 });
    }

    lucide.createIcons();

    document.querySelectorAll('#table-body tr').forEach(row => {
      row.style.background = row.dataset.iso === c.iso ? 'var(--unfpa-orange-light)' : '';
    });
  }

  function sourcesList(sources) {
    if (!sources || sources.length === 0) return '';
    const items = sources.map(s =>
      `<li><a href="${s.url}" target="_blank" rel="noopener">${s.name}</a></li>`
    ).join('');
    return `<ul class="sources-list">${items}</ul>`;
  }

  function renderTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = data.map(c => `
      <tr data-iso="${c.iso}">
        <td>${c.name}</td>
        <td class="td-region">${c.region}</td>
        <td>${badgeCell(c.cse.status)}</td>
        <td class="td-local">${escapeHtml(c.cse.local_name)}</td>
        <td>${c.age_of_consent.value}</td>
        <td>${badgeCell(c.gbv_law.status)}</td>
        <td class="td-caveat">${escapeHtml(c.caveats || '')}</td>
      </tr>
    `).join('');

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
    const icon = ICONS[status] || 'help-circle';
    return `<span class="status-badge ${status}"><i data-lucide="${icon}" style="width:12px;height:12px"></i>${label}</span>`;
  }

  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  document.addEventListener('DOMContentLoaded', init);
})();
