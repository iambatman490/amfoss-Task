// State Management
let allCoins = [];
let watchlist = JSON.parse(localStorage.getItem('apex_crypto_watchlist')) || [];
let activeCoin = null;
let currentDays = 7;
let chartInstance = null;
let currentTab = 'all';

// DOM Elements
const tableBody = document.getElementById('cryptoTableBody');
const searchInput = document.getElementById('searchInput');
const themeToggle = document.getElementById('themeToggle');
const loader = document.getElementById('loader');
const watchlistCount = document.getElementById('watchlistCount');
const tabAll = document.getElementById('tabAll');
const tabWatchlist = document.getElementById('tabWatchlist');
const timeButtons = document.querySelectorAll('.time-btn');

// Theme Management
const savedTheme = localStorage.getItem('apex_theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);

themeToggle.addEventListener('click', () => {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', nextTheme);
  localStorage.setItem('apex_theme', nextTheme);
  if (chartInstance) renderChartTheme();
});

// Fetch Top Market Coins
async function fetchCoins() {
  try {
    loader.style.display = 'block';
    const res = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1&sparkline=false');
    if (!res.ok) throw new Error('API Rate limit or error');
    allCoins = await res.json();
    loader.style.display = 'none';

    if (allCoins.length > 0 && !activeCoin) {
      setActiveCoin(allCoins[0]);
    }
    renderTable();
    updateWatchlistCount();
  } catch (error) {
    loader.innerText = 'Error fetching market data. CoinGecko free API rate limit reached, retrying in a moment...';
  }
}

// Render Table
function renderTable() {
  const query = searchInput.value.toLowerCase().trim();
  tableBody.innerHTML = '';

  let filtered = allCoins.filter(c => 
    c.name.toLowerCase().includes(query) || c.symbol.toLowerCase().includes(query)
  );

  if (currentTab === 'watchlist') {
    filtered = filtered.filter(c => watchlist.includes(c.id));
  }

  if (filtered.length === 0) {
    tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 20px; color: var(--text-secondary);">No cryptocurrencies found.</td></tr>`;
    return;
  }

  filtered.forEach(coin => {
    const isStarred = watchlist.includes(coin.id);
    const isPos = coin.price_change_percentage_24h >= 0;
    const tr = document.createElement('tr');

    tr.innerHTML = `
      <td>
        <button class="star-btn ${isStarred ? 'starred' : ''}" onclick="toggleWatchlist(event, '${coin.id}')">
          ${isStarred ? '★' : '☆'}
        </button>
      </td>
      <td>${coin.market_cap_rank || '-'}</td>
      <td>
        <div class="coin-cell">
          <img src="${coin.image}" alt="${coin.name}" loading="lazy">
          <span>${coin.name}</span>
          <span class="coin-symbol">${coin.symbol}</span>
        </div>
      </td>
      <td>$${coin.current_price.toLocaleString()}</td>
      <td class="${isPos ? 'positive' : 'negative'}">
        ${isPos ? '+' : ''}${coin.price_change_percentage_24h ? coin.price_change_percentage_24h.toFixed(2) : 0}%
      </td>
      <td>$${coin.market_cap.toLocaleString()}</td>
      <td>
        <button class="btn-chart" onclick="selectCoin('${coin.id}')">View Chart</button>
      </td>
    `;
    tr.addEventListener('click', (e) => {
      if (!e.target.closest('.star-btn')) selectCoin(coin.id);
    });
    tableBody.appendChild(tr);
  });
}

// Watchlist Logic
window.toggleWatchlist = function(event, coinId) {
  event.stopPropagation();
  if (watchlist.includes(coinId)) {
    watchlist = watchlist.filter(id => id !== coinId);
  } else {
    watchlist.push(coinId);
  }
  localStorage.setItem('apex_crypto_watchlist', JSON.stringify(watchlist));
  updateWatchlistCount();
  renderTable();
};

function updateWatchlistCount() {
  watchlistCount.innerText = watchlist.length;
}

// Set Active Coin & Fetch Chart Data
window.selectCoin = function(coinId) {
  const coin = allCoins.find(c => c.id === coinId);
  if (coin) {
    setActiveCoin(coin);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

function setActiveCoin(coin) {
  activeCoin = coin;
  document.getElementById('activeCoinName').innerText = `${coin.name} (${coin.symbol.toUpperCase()})`;
  document.getElementById('activeCoinIcon').src = coin.image;
  document.getElementById('activeCoinPrice').innerText = `$${coin.current_price.toLocaleString()}`;
  
  const changeEl = document.getElementById('activeCoinChange');
  const isPos = coin.price_change_percentage_24h >= 0;
  changeEl.className = `change-tag ${isPos ? 'positive' : 'negative'}`;
  changeEl.innerText = `${isPos ? '+' : ''}${coin.price_change_percentage_24h ? coin.price_change_percentage_24h.toFixed(2) : 0}%`;

  fetchChartData(coin.id, currentDays);
}

// Fetch Historical Chart Data
async function fetchChartData(coinId, days) {
  try {
    const res = await fetch(`https://api.coingecko.com/api/v3/coins/${coinId}/market_chart?vs_currency=usd&days=${days}`);
    const data = await res.json();
    const prices = data.prices;

    const labels = prices.map(p => {
      const date = new Date(p[0]);
      return days === 1 ? date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    });
    const values = prices.map(p => p[1]);

    renderChart(labels, values);
  } catch (err) {
    console.error('Failed to load chart data', err);
  }
}

// Render Chart.js
function renderChart(labels, values) {
  const ctx = document.getElementById('coinChart').getContext('2d');
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const accentColor = isDark ? '#38bdf8' : '#0284c7';
  const gridColor = isDark ? '#334155' : '#e2e8f0';
  const textColor = isDark ? '#94a3b8' : '#64748b';

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Price (USD)',
        data: values,
        borderColor: accentColor,
        backgroundColor: isDark ? 'rgba(56, 189, 248, 0.1)' : 'rgba(2, 132, 199, 0.1)',
        fill: true,
        tension: 0.25,
        pointRadius: 0,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false, mode: 'index' },
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: gridColor }, ticks: { color: textColor, maxTicksLimit: 8 } },
        y: { grid: { color: gridColor }, ticks: { color: textColor, callback: val => '$' + val.toLocaleString() } }
      }
    }
  });
}

function renderChartTheme() {
  if (activeCoin) fetchChartData(activeCoin.id, currentDays);
}

// Event Listeners
searchInput.addEventListener('input', renderTable);

tabAll.addEventListener('click', () => {
  currentTab = 'all';
  tabAll.classList.add('active');
  tabWatchlist.classList.remove('active');
  renderTable();
});

tabWatchlist.addEventListener('click', () => {
  currentTab = 'watchlist';
  tabWatchlist.classList.add('active');
  tabAll.classList.remove('active');
  renderTable();
});

timeButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    timeButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentDays = parseInt(btn.dataset.days);
    if (activeCoin) fetchChartData(activeCoin.id, currentDays);
  });
});

// Initialize
fetchCoins();