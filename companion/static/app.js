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

  let html = `<div class="modal-header"><h2>${escHtml(primary.name)}</h2><div class="type-badges">${typeBadges([primary.type_1, primary.type_2])}</div></div>`;
  html += `<div class="modal-body">`;

  if (primary.sprites?.icon) {
    html += `<span class="poke-icon" style="background-image:url('${primary.sprites.icon}')"></span>`;
  }

  html += `<div class="modal-info">
    <p><strong>Category:</strong> ${escHtml(primary.category)}</p>
    <p><strong>Type:</strong> ${escHtml(primary.type_1)}${primary.type_2 ? ` / ${escHtml(primary.type_2)}` : ''}</p>
    <p><strong>Location:</strong> ${escHtml(primary.location)}</p>
    <p><strong>TCG Set:</strong> ${escHtml(primary.tcg_set)}</p>
  </div>`;

  if (primary.stats) {
    html += `<div class="stats-section"><h3>Stats</h3><div class="stats-grid">
      ${['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'].map((stat, i) => {
        const values = [primary.stats.hp, primary.stats.attack, primary.stats.defense, primary.stats.spAtk, primary.stats.spDef, primary.stats.speed];
        return `<div class="stat-box"><strong>${stat}</strong><div class="stat-bar" style="width:${(values[i]/255)*100}%"></div>${values[i]}</div>`;
      }).join('')}
    </div></div>`;
  }

  if (primary.abilities) {
    html += `<div class="abilities-section"><h3>Abilities</h3><div class="abilities-list">
      ${primary.abilities.map((a, i) => `<span class="ability-item${i === 2 ? ' ability-hidden' : ''}">${a || '—'}</span>`).join('')}
    </div></div>`;
  }

  if (primary.movesets?.levelup?.length) {
    html += `<div class="movesets-section"><h3>Level-up Moves</h3><table class="moves-table"><tr><th>Lvl</th><th>Move</th><th>Type</th><th>Power</th><th>Acc</th></tr>`;
    primary.movesets.levelup.slice(0, 10).forEach(m => {
      html += `<tr><td>${m.level}</td><td>${escHtml(m.name)}</td><td><span class="type-badge type-${escHtml(m.type)}">${escHtml(m.type)}</span></td><td>${m.power || '—'}</td><td>${m.accuracy || '—'}</td></tr>`;
    });
    html += `</table></div>`;
  }

  if (allCards.length) {
    html += `<div class="tcg-cards-section"><h3>TCG Cards</h3>`;
    allCards.forEach((card, idx) => {
      html += `<div class="tcg-card-small" style="cursor:pointer" onclick="openCardLightbox('${card.img_url}', ${JSON.stringify(cardUrls)}, ${idx})"><img src="${card.img_url}" alt="" loading="lazy"><p>${escHtml(card.set)} #${escHtml(card.number)}</p></div>`;
    });
    html += `</div>`;
  }

  html += `</div>`;
  modalContent.innerHTML = html;
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
