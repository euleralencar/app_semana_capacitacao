const searchInput = document.querySelector('#ranking-search');
const rankingBody = document.querySelector('#ranking-body');
const rankingStatus = document.querySelector('#ranking-status');

async function loadRanking() {
  const matricula = searchInput.value.trim();
  const response = await fetch(`/api/ranking?matricula=${encodeURIComponent(matricula)}`, { cache: 'no-store' });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || 'Não foi possível carregar o ranking.');

  rankingBody.replaceChildren();
  if (!payload.ranking.length) {
    const row = document.createElement('tr');
    row.innerHTML = '<td class="px-5 py-5 text-slate-500" colspan="3">Nenhum participante encontrado.</td>';
    rankingBody.append(row);
  }
  payload.ranking.forEach(({ posicao, matricula: itemMatricula, pontos }) => {
    const row = document.createElement('tr');
    row.className = 'border-t border-slate-100';
    [posicao, itemMatricula, pontos].forEach((value, index) => {
      const cell = document.createElement('td');
      cell.className = `px-5 py-4${index === 2 ? ' text-right font-semibold' : ''}`;
      cell.textContent = value;
      row.append(cell);
    });
    rankingBody.append(row);
  });
  rankingStatus.textContent = `Atualizado às ${new Date().toLocaleTimeString('pt-BR')}.`;
}

async function refreshRanking() {
  try { await loadRanking(); }
  catch (error) { rankingStatus.textContent = error.message; }
}

let searchTimer;
searchInput.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(refreshRanking, 250);
});

refreshRanking();
setInterval(refreshRanking, 5000);

