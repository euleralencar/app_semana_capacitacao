const searchInput = document.querySelector('#ranking-search');
const rankingBody = document.querySelector('#ranking-body');
const rankingStatus = document.querySelector('#ranking-status');

// Cache para evitar re-renders desnecessários
let lastRankingData = null;

// Verificar se está dentro do horário de funcionamento do evento (9h às 20h)
function isEventHours() {
  const now = new Date();
  const hour = now.getHours();
  return hour >= 9 && hour < 20;
}

async function loadRanking() {
  const matricula = searchInput.value.trim();
  try {
    const response = await fetch(`/api/ranking?matricula=${encodeURIComponent(matricula)}`, { 
      cache: 'default'  // Permite cache do navegador
    });
    const payload = await response.json();
    
    if (!response.ok) {
      throw new Error(payload.error || 'Não foi possível carregar o ranking.');
    }

    // Comparar com cache: se dados são iguais, não re-renderizar
    const currentData = JSON.stringify(payload.ranking);
    if (currentData === lastRankingData) {
      rankingStatus.textContent = `Usando cache (Atualizado às ${new Date().toLocaleTimeString('pt-BR')})`;  
      return;
    }

    lastRankingData = currentData;
    
    rankingBody.replaceChildren();
    if (!payload.ranking.length) {
      const row = document.createElement('tr');
      row.innerHTML = '<td class="px-5 py-5 text-slate-500" colspan="3">Nenhum participante encontrado.</td>';
      rankingBody.append(row);
    } else {
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
    }
    rankingStatus.textContent = `Atualizado às ${new Date().toLocaleTimeString('pt-BR')}.`;
  } catch (error) {
    rankingStatus.textContent = `Erro: ${error.message}`;
    console.error(`Error loading ranking: ${error.message}`);
  }
}

async function refreshRanking() {
  try { 
    await loadRanking(); 
  }
  catch (error) { 
    rankingStatus.textContent = `Erro: ${error.message}`; 
    console.error('Ranking refresh error:', error);
  }
}

// Busca com debounce para evitar requisições excessivas enquanto digita
let searchTimer;
searchInput.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(refreshRanking, 250);
});

// Carregamento inicial
refreshRanking();

// Auto-atualização a cada 30 minutos, apenas durante horário do evento (9h às 20h)
// Fora desse horário, o usuário pode fazer refresh manual para atualizar
setInterval(() => {
  if (isEventHours()) {
    refreshRanking();
  }
}, 1800000); // 30 minutos em milissegundos
