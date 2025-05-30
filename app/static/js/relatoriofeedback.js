document.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('graficoEstrelas').getContext('2d');
  const graficoSection = document.querySelector('.grafico-section');

  // Remover estilos de layout via JS, deixar apenas lógica de criação da legenda
  const legendDiv = document.createElement('div');
  legendDiv.id = 'estrelas-legenda';
  graficoSection.appendChild(legendDiv);

  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['5 estrelas', '4 estrelas', '3 estrelas', '2 estrelas', '1 estrela'],
      datasets: [{
        label: '% de Avaliações',
        data: [0, 0, 0, 0, 0],
        backgroundColor: ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545'],
        borderRadius: 10,
        barThickness: 38,
        categoryPercentage: 0.7,
        barPercentage: 0.9
      }]
    },
    options: {
      indexAxis: 'y',
      layout: { padding: { top: 0, bottom: 0 } },
      animation: {
        duration: 1200,
        easing: 'easeOutQuart'
      },
      scales: {
        x: {
          min: 0,
          max: 100,
          ticks: {
            callback: value => value + '%',
            font: { size: 18 }
          },
          grid: { display: false }
        },
        y: {
          ticks: { font: { size: 20, weight: 'bold' } },
          grid: { display: false }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });

  let totais = [0, 0, 0, 0, 0];

  function atualizarLegenda() {
    legendDiv.innerHTML = '';
    const labels = ['5', '4', '3', '2', '1'];
    for (let i = 0; i < 5; i++) {
      const cor = chart.data.datasets[0].backgroundColor[i];
      const span = document.createElement('span');
      span.style.display = 'flex';
      span.style.alignItems = 'center';
      span.style.gap = '10px';
      span.innerHTML = `
        <span style="display:inline-block;width:22px;height:22px;background:${cor};border-radius:6px;"></span>
        <span style='font-size:1.18rem;font-weight:600;min-width:22px;text-align:center;'>${labels[i]}</span>
        <span style='color:#001f5b;font-size:1.18rem;font-weight:600;min-width:32px;text-align:left; margin-left:2px;'>${totais[i]}</span>
      `;
      legendDiv.appendChild(span);
    }
  }

  const select = document.getElementById('unidade-select');
  select.addEventListener('change', () => {
    const unidadeId = select.value;
    fetch(`/api/feedback_porcentagem/${unidadeId}`)
      .then(res => res.json())
      .then(data => {
        chart.data.datasets[0].data = [
          data['5 estrelas'] || 0,
          data['4 estrelas'] || 0,
          data['3 estrelas'] || 0,
          data['2 estrelas'] || 0,
          data['1 estrela'] || 0
        ];
        totais = [
          data['total_5'] || 0,
          data['total_4'] || 0,
          data['total_3'] || 0,
          data['total_2'] || 0,
          data['total_1'] || 0
        ];
        chart.update();
        atualizarLegenda();
      })
      .catch(error => {
        console.error('Erro ao carregar dados:', error);
        chart.data.datasets[0].data = [0, 0, 0, 0, 0];
        totais = [0, 0, 0, 0, 0];
        chart.update();
        atualizarLegenda();
      });
  });

  // Gatilho inicial
  select.dispatchEvent(new Event('change'));
});
