'use strict';

const state = {
  activeTab: 'pokedex',
  activeView: 'gallery',
  searchQuery: '',
  pokedexData: [],
  tcgData: [],
  pokedexFiltered: [],
  tcgFiltered: [],
  activeTcgSet: 'All Sets',
  tcgSets: [],
};

const $ = id => document.getElementById(id);
const pokedexGrid = $('pokedex-grid');
const tcgGrid = $('tcg-grid');
const setTabsEl = $('set-tabs');
const searchInput = $('search');
const searchCount = $('search-count');
const modalOverlay = $('modal-overlay');
const modalContent = $('modal-content');
const modalClose = $('modal-close');
const cardLightbox = $('card-lightbox-overlay');
const cardLightboxImg = $('card-lightbox-img');
const cardLightboxClose = $('card-lightbox-close');
const cardLightboxPrev = $('card-lightbox-prev');
const cardLightboxNext = $('card-lightbox-next');

let lightboxCards = [];
let currentCardIndex = -1;

document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  setupViewToggle();
  setupSearch();
  setupModal();
  setupCardLightbox();

  Promise.all([
    fetch('/api/pokedex').then(r => r.json()),
    fetch('/api/tcg').then(r => r.json()),
  ]).then(([pokedex, tcg]) => {
    state.pokedexData = pokedex;
    state.tcgData = tcg;
    state.tcgSets = ['All Sets', ...new Set(tcg.map(c => c.set))];
    filterAll('');
    buildSetTabs();
    render();
  });
});

function setupCardLightbox() {
  cardLightboxClose.addEventListener('click', closeCardLightbox);
  cardLightboxPrev.addEventListener('click', () => navigateLightbox(-1));
  cardLightboxNext.addEventListener('click', () => navigateLightbox(1));

  cardLightbox.addEventListener('click', e => {
    if (e.target === cardLightbox) closeCardLightbox();
  });

  document.addEventListener('keydown', e => {
    if (cardLightbox.classList.contains('hidden')) return;
    if (e.key === 'Escape') closeCardLightbox();
    if (e.key === 'ArrowLeft') navigateLightbox(-1);
    if (e.key === 'ArrowRight') navigateLightbox(1);
  });
}

function openCardLightbox(imgUrl, cardsArray = null, cardIndex = null) {
  cardLightboxImg.src = imgUrl;

  if (cardsArray && cardsArray.length > 1) {
    lightboxCards = cardsArray;
    currentCardIndex = cardIndex !== null ? cardIndex : cardsArray.indexOf(imgUrl);
    cardLightboxPrev.style.display = 'block';
    cardLightboxNext.style.display = 'block';
  } else {
    lightboxCards = [];
    currentCardIndex = -1;
    cardLightboxPrev.style.display = 'none';
    cardLightboxNext.style.display = 'none';
  }

  cardLightbox.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function navigateLightbox(direction) {
  if (lightboxCards.length === 0) return;
  currentCardIndex += direction;
  if (currentCardIndex < 0) currentCardIndex = lightboxCards.length - 1;
  if (currentCardIndex >= lightboxCards.length) currentCardIndex = 0;
  cardLightboxImg.src = lightboxCards[currentCardIndex];
}

function closeCardLightbox() {
  cardLightbox.classList.add('hidden');
  document.body.style.overflow = '';
  lightboxCards = [];
  currentCardIndex = -1;
}

function setupTabs() {
  document.querySelectorAll('.tab').forEach(btn => {
    btn.addEventListener('click', () => {
      state.activeTab = btn.dataset.tab;
      document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b === btn));
      document.querySelectorAll('.view').forEach(v => v.classList.toggle('active', v.id === `view-${state.activeTab}`));
      render();
    });
  });
}

function setupViewToggle() {
  const toggleBtns = document.querySelectorAll('.toggle-btn');
  toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      state.activeView = btn.dataset.view;
      toggleBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render();
    });
  });
}

function setupSearch() {
  searchInput.addEventListener('input', e => {
    state.searchQuery = e.target.value;
    filterAll(state.searchQuery);
    render();
  });
}

function filterAll(query) {
  const q = query.toLowerCase().trim();
  if (!q) {
    state.pokedexFiltered = state.pokedexData;
    state.tcgFiltered = state.tcgData;
  } else {
    state.pokedexFiltered = state.pokedexData.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.type_1.toLowerCase().includes(q) ||
      (p.type_2 && p.type_2.toLowerCase().includes(q)) ||
      p.location.toLowerCase().includes(q) ||
      p.category.toLowerCase().includes(q)
    );
    state.tcgFiltered = state.tcgData.filter(c =>
      c.name.toLowerCase().includes(q) ||
      c.set.toLowerCase().includes(q) ||
      c.rarity.toLowerCase().includes(q)
    );
  }
  updateSearchCount();
}

function updateSearchCount() {
  const dex = state.pokedexFiltered.length;
  const tcg = filterTcgBySet(state.tcgFiltered, state.activeTcgSet).length;
  if (!state.searchQuery) {
    searchCount.textContent = '';
    return;
  }
  searchCount.textContent = state.activeTab === 'pokedex' ? `${dex} pokémon · ${tcg} cards` : `${tcg} cards · ${dex} pokémon`;
}

function render() {
  if (state.activeTab === 'pokedex') {
    state.activeView === 'gallery' ? renderPokedex() : renderPokedexTable();
  } else {
    state.activeView === 'gallery' ? renderTcg() : renderTcgTable();
  }
  updateSearchCount();
}

function renderPokedex() {
  if (!state.pokedexFiltered.length) {
    pokedexGrid.innerHTML = '<p class="empty-state">No Pokémon found.</p>';
    return;
  }
  const seen = new Map();
  state.pokedexFiltered.forEach(p => {
    if (!seen.has(p.name)) seen.set(p.name, p);
  });
  pokedexGrid.innerHTML = [...seen.values()].map(p => `
    <div class="poke-card" data-name="${escHtml(p.name)}" role="button" tabindex="0">
      ${p.needs_review ? '<span class="review-badge">Review</span>' : ''}
      <span class="poke-icon" style="background-image:url('${p.sprites.icon}')"></span>
      <span class="poke-name">${escHtml(p.name)}</span>
      <div class="type-badges">${typeBadges([p.type_1, p.type_2])}</div>
      <div class="poke-location">${escHtml(p.location)}</div>
    </div>`).join('');
  pokedexGrid.querySelectorAll('.poke-card').forEach(card => {
    card.addEventListener('click', () => openModal(card.dataset.name));
  });
}

function renderPokedexTable() {
  if (!state.pokedexFiltered.length) {
    pokedexGrid.innerHTML = '<p class="empty-state">No Pokémon found.</p>';
    return;
  }
  const seen = new Map();
  state.pokedexFiltered.forEach(p => {
    if (!seen.has(p.name)) seen.set(p.name, p);
  });
  const rows = [...seen.values()].map(p => `
    <tr class="pokedex-row" data-name="${escHtml(p.name)}">
      <td class="col-name">${escHtml(p.name)}</td>
      <td class="col-type">${typeBadges([p.type_1, p.type_2])}</td>
      <td class="col-location">${escHtml(p.location)}</td>
      <td class="col-tcg-set">${escHtml(p.tcg_set)}</td>
    </tr>`).join('');
  pokedexGrid.innerHTML = `
    <table class="pokedex-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th>Location</th>
          <th>TCG Set</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>`;
  pokedexGrid.querySelectorAll('.pokedex-row').forEach(row => {
    row.addEventListener('click', () => openModal(row.dataset.name));
  });
}

function buildSetTabs() {
  setTabsEl.innerHTML = state.tcgSets.map(s =>
    `<button class="set-tab${s === state.activeTcgSet ? ' active' : ''}" data-set="${escHtml(s)}">${escHtml(s)}</button>`
  ).join('');
  setTabsEl.querySelectorAll('.set-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      state.activeTcgSet = btn.dataset.set;
      setTabsEl.querySelectorAll('.set-tab').forEach(b => b.classList.toggle('active', b === btn));
      render();
      updateSearchCount();
    });
  });
}

function filterTcgBySet(cards, set) {
  return set === 'All Sets' ? cards : cards.filter(c => c.set === set);
}

function renderTcg() {
  const cards = filterTcgBySet(state.tcgFiltered, state.activeTcgSet);
  if (!cards.length) {
    tcgGrid.innerHTML = '<p class="empty-state">No cards found.</p>';
    return;
  }
  const cardUrls = cards.map(c => c.img_url);
  tcgGrid.innerHTML = cards.map((c, idx) => `
    <div class="tcg-card" role="button" tabindex="0">
      <div class="tcg-card-img-wrap">
        <img src="${c.img_url}" alt="${escHtml(c.name)}" loading="lazy" decoding="async">
      </div>
      <div class="tcg-card-details">
        <span class="tcg-card-name">${escHtml(c.name)}</span>
        <div class="tcg-card-meta">
          <span>${escHtml(c.rarity)}</span>
          <span class="tcg-card-number">#${escHtml(c.number)}</span>
        </div>
      </div>
    </div>`).join('');
  tcgGrid.querySelectorAll('.tcg-card').forEach((card, idx) => {
    card.addEventListener('click', () => openCardLightbox(cardUrls[idx], cardUrls, idx));
  });
}

function renderTcgTable() {
  const cards = filterTcgBySet(state.tcgFiltered, state.activeTcgSet);
  if (!cards.length) {
    tcgGrid.innerHTML = '<p class="empty-state">No cards found.</p>';
    return;
  }
  const cardUrls = cards.map(c => c.img_url);
  const rows = cards.map((c, idx) => `
    <tr class="tcg-table-row" data-card-url="${escHtml(c.img_url)}" data-index="${idx}">
      <td>${escHtml(c.name)}</td>
      <td>${escHtml(c.set)}</td>
      <td>${escHtml(c.rarity)}</td>
      <td>#${escHtml(c.number)}</td>
    </tr>`).join('');
  tcgGrid.innerHTML = `
    <table class="tcg-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Set</th>
          <th>Rarity</th>
          <th>Number</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>`;
  tcgGrid.querySelectorAll('.tcg-table-row').forEach(row => {
    const idx = parseInt(row.dataset.index);
    row.addEventListener('click', () => openCardLightbox(cardUrls[idx], cardUrls, idx));
  });
}

function setupModal() {
  modalClose.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', e => { if (e.target === modalOverlay) closeModal(); });
  document.addEventListener('keydown', e => {
    if (!modalOverlay.classList.contains('hidden') && e.key === 'Escape') closeModal();
  });
}

function formatEvoMethod(method, param) {
  if (!method) return '';
  if (method === 'level' && param > 0) return `Lv ${param}`;
  if (method === 'level') return '';
  return method.charAt(0).toUpperCase() + method.slice(1);
}

function buildEvolutionChain(primary) {
  const findEntry = name => state.pokedexData.find(p => p.name === name);
  const findNextForm = name => state.pokedexData.find(p => p.evolves_from === name);

  // Walk back to root using CSV evolves_from
  let root = primary;
  const visited = new Set();
  while (root.evolves_from && !visited.has(root.name)) {
    visited.add(root.name);
    const prev = findEntry(root.evolves_from);
    if (!prev) break;
    root = prev;
  }

  // Walk forward from root to build the full linear chain
  const chain = [];
  let current = root;
  const seen = new Set();
  while (current && !seen.has(current.name)) {
    seen.add(current.name);
    chain.push(current);
    current = findNextForm(current.name) || null;
  }

  if (chain.length <= 1) return '';

  let html = `<div class="evo-chain">`;
  chain.forEach((entry, i) => {
    if (i > 0) {
      const prev = chain[i - 1];
      const label = formatEvoMethod(prev.evolution?.method, prev.evolution?.param);
      html += `<div class="evo-arrow-wrap">
        ${label ? `<span class="evo-method">${escHtml(label)}</span>` : ''}
        <span class="evo-arrow">→</span>
      </div>`;
    }
    const iconUrl = entry.sprites?.icon || '';
    html += `<button class="evo-btn${entry.name === primary.name ? ' evo-active' : ''}" onclick="openModal('${escHtml(entry.name)}')">
      ${iconUrl ? `<span class="evo-icon" style="background-image:url('${iconUrl}')"></span>` : ''}
      <span class="evo-name">${escHtml(entry.name)}</span>
    </button>`;
  });
  html += `</div>`;
  return html;
}

function openModal(name) {
  const entries = state.pokedexData.filter(p => p.name === name);
  if (!entries.length) return;

  const primary = entries[0];
  const allCards = entries.filter(e => e.card_img_url).map(e => ({
    img_url: e.card_img_url,
    set: e.tcg_set,
    number: e.card_number
  }));
  const cardUrls = allCards.map(c => c.img_url);

  const categoryLabel = primary.categoryName ? `${primary.categoryName} Pokémon` : (primary.category || '');

  // Header
  let html = `
    <div class="modal-header">
      <div class="modal-header-left">
        <span class="modal-name">${escHtml(primary.name)}</span>
        <div class="modal-types">${typeBadges([primary.type_1, primary.type_2])}</div>
      </div>
      <div class="modal-header-right">
        <span class="modal-category">${escHtml(categoryLabel)}</span>
      </div>
    </div>`;

  // Tabs
  html += `
    <div class="modal-tabs">
      <button class="modal-tab-btn active" data-tab="overview">Overview</button>
      <button class="modal-tab-btn" data-tab="moveset">Moveset</button>
      <button class="modal-tab-btn" data-tab="location">Location</button>
      <button class="modal-tab-btn" data-tab="tcg">TCG</button>
    </div>`;

  // ── Overview Tab ──────────────────────────────────────────────────────────
  html += `<div class="modal-tab-panel active" data-tab-panel="overview">`;

  html += buildEvolutionChain(primary);

  // Sprites
  html += `
    <div class="sprite-panel">
      <div class="sprite-group">
        <div class="sprite-group-label">Normal</div>
        <div class="sprite-group-row">
          <div class="sprite-block">
            <div class="sprite-cell">
              <span class="sprite-main-anim" style="background-image:url('${primary.sprites.main}')"></span>
            </div>
            <span class="sprite-label">Main</span>
          </div>
          <div class="sprite-block">
            <div class="sprite-cell">
              <span class="sprite-static" style="background-image:url('${primary.sprites.front}')"></span>
            </div>
            <span class="sprite-label">Front</span>
          </div>
          <div class="sprite-block">
            <div class="sprite-cell">
              <img class="sprite-back-img" src="${primary.sprites.back}" loading="lazy">
            </div>
            <span class="sprite-label">Back</span>
          </div>
          <div class="sprite-block">
            <div class="sprite-cell">
              <span class="sprite-icon-sm" style="background-image:url('${primary.sprites.icon}')"></span>
            </div>
            <span class="sprite-label">Icon</span>
          </div>
        </div>
      </div>
      <div class="sprite-divider"></div>
      <div class="sprite-group">
        <div class="sprite-group-label shiny-label">Shiny</div>
        <div class="sprite-group-row">
          <div class="sprite-block">
            <div class="sprite-cell shiny-cell">
              <span class="sprite-main-anim" style="background-image:url('${primary.sprites.shiny_front}')"></span>
            </div>
            <span class="sprite-label">Main</span>
          </div>
          <div class="sprite-block">
            <div class="sprite-cell shiny-cell">
              <span class="sprite-static" style="background-image:url('${primary.sprites.shiny_front}')"></span>
            </div>
            <span class="sprite-label">Front</span>
          </div>
          <div class="sprite-block">
            <div class="sprite-cell shiny-cell">
              <img class="sprite-back-img" src="${primary.sprites.shiny_back}" loading="lazy">
            </div>
            <span class="sprite-label">Back</span>
          </div>
        </div>
      </div>
    </div>`;

  // Stats
  if (primary.stats) {
    const statDefs = [
      { key: 'HP',      label: 'HP',      color: '#ff5959' },
      { key: 'Attack',  label: 'Attack',  color: '#f08030' },
      { key: 'Defense', label: 'Defense', color: '#f8d030' },
      { key: 'SpAtk',   label: 'Sp. Atk', color: '#6890f0' },
      { key: 'SpDef',   label: 'Sp. Def', color: '#78c850' },
      { key: 'Speed',   label: 'Speed',   color: '#f85888' },
    ];
    html += `<div class="stats-section"><h3>Base Stats</h3><div class="stats-grid">`;
    statDefs.forEach(s => {
      const val = primary.stats[s.key] || 0;
      const pct = ((val / 255) * 100).toFixed(1);
      html += `
        <div class="stat-row">
          <span class="stat-name">${s.label}</span>
          <div class="stat-bar-container">
            <div class="stat-bar" style="width:${pct}%; background:${s.color};"></div>
          </div>
          <span class="stat-value">${val}</span>
        </div>`;
    });
    html += `</div></div>`;
  }

  // Abilities
  if (primary.abilities) {
    const labels = ['Ability 1', 'Ability 2', 'Hidden'];
    html += `<div class="abilities-section"><h3>Abilities</h3><div class="abilities-grid">`;
    [0, 1, 2].forEach(i => {
      const val = primary.abilities[i] || '—';
      html += `
        <div class="ability-slot${i === 2 ? ' ability-hidden' : ''}">
          <span class="ability-slot-label">${labels[i]}</span>
          <span class="ability-slot-value">${escHtml(val)}</span>
        </div>`;
    });
    html += `</div></div>`;
  }

  html += `</div>`; // end overview

  // ── Moveset Tab ───────────────────────────────────────────────────────────
  html += `<div class="modal-tab-panel" data-tab-panel="moveset">`;
  if (primary.movesets?.levelup?.length) {
    html += `<div class="movesets-section"><h3>Level-up Moves</h3>
      <table class="moveset-table">
        <thead><tr>
          <th class="move-level">Lvl</th>
          <th class="move-name">Move</th>
          <th class="move-type">Type</th>
          <th class="move-power">Pwr</th>
          <th class="move-accuracy">Acc</th>
        </tr></thead>
        <tbody>`;
    primary.movesets.levelup.forEach(m => {
      html += `<tr>
        <td class="move-level">${m.level}</td>
        <td class="move-name">${escHtml(m.name)}</td>
        <td class="move-type"><span class="type-badge type-${escHtml(m.type)}">${escHtml(m.type)}</span></td>
        <td class="move-power">${m.power || '—'}</td>
        <td class="move-accuracy">${m.accuracy || '—'}</td>
      </tr>`;
    });
    html += `</tbody></table></div>`;
  } else {
    html += `<p class="empty-state">No moveset data.</p>`;
  }
  html += `</div>`; // end moveset

  // ── Location Tab ──────────────────────────────────────────────────────────
  html += `<div class="modal-tab-panel" data-tab-panel="location">
    <div class="location-info">
      <div class="info-row">
        <span class="info-label">Location</span>
        <span class="info-value">${escHtml(primary.location)}</span>
      </div>
      <div class="info-row">
        <span class="info-label">TCG Set</span>
        <span class="info-value">${escHtml(primary.tcg_set)}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Pokédex #</span>
        <span class="info-value">${primary.dex_number}</span>
      </div>
      ${primary.evolves_from ? `<div class="info-row">
        <span class="info-label">Evolves From</span>
        <span class="info-value">${escHtml(primary.evolves_from)}</span>
      </div>` : ''}
    </div>
  </div>`; // end location

  // ── TCG Tab ───────────────────────────────────────────────────────────────
  html += `<div class="modal-tab-panel" data-tab-panel="tcg">`;
  if (allCards.length) {
    html += `<div class="modal-cards-section"><h3>Cards</h3><div class="modal-card-list">`;
    allCards.forEach((card, idx) => {
      html += `<div class="modal-tcg-card" onclick="openCardLightbox('${card.img_url}', ${JSON.stringify(cardUrls)}, ${idx})">
        <img src="${card.img_url}" alt="${escHtml(card.set)}" loading="lazy">
        <div class="modal-tcg-card-label">${escHtml(card.set)} #${escHtml(card.number)}</div>
      </div>`;
    });
    html += `</div></div>`;
  } else {
    html += `<p class="empty-state">No TCG cards for this Pokémon.</p>`;
  }
  html += `</div>`; // end tcg

  modalContent.innerHTML = html;

  // Wire up tab switching
  modalContent.querySelectorAll('.modal-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      modalContent.querySelectorAll('.modal-tab-btn').forEach(b => b.classList.remove('active'));
      modalContent.querySelectorAll('.modal-tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      modalContent.querySelector(`[data-tab-panel="${btn.dataset.tab}"]`).classList.add('active');
    });
  });

  modalOverlay.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  modalOverlay.classList.add('hidden');
  document.body.style.overflow = '';
}

function escHtml(str) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return String(str).replace(/[&<>"']/g, c => map[c]);
}

function typeBadges(types) {
  return types.filter(Boolean).map(t => `<span class="type-badge type-${escHtml(t)}">${escHtml(t)}</span>`).join('');
}
